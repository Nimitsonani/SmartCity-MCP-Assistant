from fastmcp import Client
from MCP.Server import mcp
from Cache.cache_handler import cache
from MCP.Nearby_Category import CATEGORY_MAP
from App.Conversations import chat
import requests
import json
import time
from dotenv import load_dotenv
import os

load_dotenv('.env')
mistral_api_key = os.getenv('MISTRAL_API_KEY')

client = Client(mcp)

#call mistral api
def call_mistral(content):
    ans = None
    payload = {
        'model': 'mistral-large-latest',
        "messages": content
    }
    headers = {
        'Authorization': f'Bearer {mistral_api_key}',
        'Content-Type': 'application/json'
    }
    try:
        ans = requests.post(url='https://api.mistral.ai/v1/chat/completions', json=payload, headers=headers)
        ans = ans.json()
        ans = ans['choices'][0]['message']['content']
    except Exception as e:
        print(e)
    return ans


#make list of tool name and description.
my_list=[]
def make_tool_list(tools):
    for i in tools:
        name = i.name
        description = i.description.replace('\n', '')
        my_list.append({name: description})


#this call decided whether needs to call MCP tool.
def primary_call():
    data = [{"role": "system",
             "content": f"you are a city assistant bot citizens may ask you questions related to the city.analyze the user query and check if it requires calling MCP tools.{my_list}here are name of all MCP tools with their Description and what parameters they take.all parameters are provided with default values except for category parameter in nearby place.if user query requires any changes in parameters then you can give changed parameters otherwise give None.after analyzing user query always response in this exact format.{{'tool_name':'enter MCP tool that needs to be called here.','parameters':'write No changes if parameters dont need to be changed'}}below is the example of response for nearby_place tool and inside category only give data from provided words inside list in nearby_place description and if no word exist inside nearby_place description related to user query just respond i cant find that.{{'tool_name':'nearby_place','parameters':{{'category':'hospital'}}}}. if you can answer user query without calling any MCP tool then just give normal reply. if you can't answer the user query with or without using tools don't make up answers just say i can't help you with that. if the query requires to call tool then always respond in json format. never give response in markdown."}]
    for i in chat.chat:
        data.append({"role": i['role'],
                     "content":i['content']})
    return call_mistral(data)


#this call gives output of MCP tool with user query
def secondary_call(tool_response):
    data = [{"role": "system",
              "content": f"you are a city assistant bot citizens may ask you questions related to the city.{tool_response}analyze this data got from the api call and answer the user query by using that data. never give response in markdown."}]
    for i in chat.chat:
        data.append({"role": i['role'],
                     "content":i['content']})
    return call_mistral(data)


#check whether data is latest in cache or not
def check_cache(tool_name,parameters):
    current = time.time()

    #fetch data from cache or create cache in json file.
    cache.cache[f'{tool_name}_{parameters}'] = cache.cache.get(f'{tool_name}_{parameters}',{})

    #fetch time from cache if cache exist
    current_cache_time = cache.cache[f"{tool_name}_{parameters}"].get('time',None)

    TIME_MAP={
        "current_weather": 1800,
        "hourly_weather":14400,
        "daily_weather": 86400,
        "current_air": 1800,
        "hourly_air": 14400,
        "daily_air": 86400,
        "news": 1800,
        "nearby_place": 259200
    }
    if current_cache_time is not None:
        time_to_check = TIME_MAP[f'{tool_name}']
        if current - float(current_cache_time) < time_to_check:
            return cache.cache[f"{tool_name}_{parameters}"]['data']
    return False



async def main():
    async with client:
        await client.ping()
        tools = await client.list_tools()

        #create a list of MCP tool name and description to give to LLM
        make_tool_list(tools)

        #make primary call
        primary_response = primary_call()
        print(primary_response)

        #if needs to call MCP tool
        if '```json' in primary_response or '{' in primary_response:
            primary_response = primary_response.replace('json', '')
            primary_response = primary_response.replace('```', '')
            primary_response = primary_response.replace(': None', '"No changes"')
            primary_response = primary_response.replace(':None', '"No changes"')
            primary_response = primary_response.replace("'",'"')

            #convert str to dict
            primary_response = json.loads(primary_response)

            #check cache for if data is latest in cache
            tool_name_str = primary_response['tool_name']
            parameters_str = str(primary_response['parameters'])
            tool_response = check_cache(tool_name_str,parameters_str)

            #if need to call MCP tool else use data from cache
            if not tool_response:
                if primary_response['parameters'] == "No changes":
                    primary_response['parameters'] = None

                #handles category map for nearby place tool
                if primary_response['tool_name'] == 'nearby_place':
                    primary_response['parameters']['category'] = CATEGORY_MAP[primary_response['parameters']['category']]
                tool_response = await client.call_tool(primary_response['tool_name'], primary_response['parameters'])
                cache.add(f"{primary_response['tool_name']}_{parameters_str}", tool_response.data)

            #secondary call
            secondary_response = secondary_call(tool_response)
            return secondary_response.replace('**','')
        return primary_response.replace('**','')


