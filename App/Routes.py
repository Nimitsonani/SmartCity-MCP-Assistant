import asyncio
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from MCP.Client import main
from App.Conversations import chat

app = FastAPI()
templates = Jinja2Templates(directory='templates')

@app.get('/')
def home(request: Request):
    return templates.TemplateResponse(name= 'index.html', request= request, context={'chat':chat.chat})

@app.post('/')
def post_home(query: str = Form(...)):
    chat.add("user",query)
    try:
        chat.add("assistant",f"{asyncio.run(main())}")
    except Exception as e:
        print(e)
        chat.add("assistant",f"Something went wrong. Please try again later.")
    return RedirectResponse("/", status_code=303)