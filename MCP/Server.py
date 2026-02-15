import requests
from fastmcp import FastMCP
from dotenv import load_dotenv
import os

load_dotenv('.env')
latitude_env = float(os.getenv('LATITUDE'))
longitude_env = float(os.getenv('LONGITUDE'))
geopify_api_key = os.getenv('GEOPIFY_API_KEY')
news_api_key = os.getenv('NEWS_API_KEY')
city = os.getenv('CITY')
languages = os.getenv('LANGUAGES')

#MCP Server
mcp = FastMCP('my-server')


#fun for API call
def call(url,parameters = None):
    ans = None
    try:
        ans = requests.get(url=url,params=parameters)
        ans = ans.json()
    except Exception as e:
        print(e)
    return ans



@mcp.tool()
def current_weather(latitude: float = latitude_env,
                    longitude: float = longitude_env,
                    timezone: str = 'auto'):
    """
    Fetches current weather conditions using Open-Meteo API.

    Parameters:
    - latitude (float): Geographic latitude of the location.
    - longitude (float): Geographic longitude of the location.
    - timezone (str): Timezone for the response (default: 'auto').

    Returns:
    - temperature_2m (°C)
    - relative_humidity_2m (%)
    - apparent_temperature (°C)
    - is_day (0 = night, 1 = day)
    - rain (mm)
    - cloud_cover (%)
    - wind_speed_10m (km/h)
    - wind_gusts_10m (km/h)
    - weather_code (Open-Meteo WMO weather interpretation code)
    """
    url = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,relative_humidity_2m,apparent_temperature,is_day,rain,weather_code,cloud_cover,wind_speed_10m,wind_gusts_10m&timezone={timezone}&forecast_days=1'
    return call(url=url)


@mcp.tool()
def hourly_weather(latitude: float = latitude_env,
                    longitude: float = longitude_env,
                    timezone: str = 'auto'):
    """
    Fetches hourly weather forecast for the next 24 hours using Open-Meteo API.

    Parameters:
    - latitude (float): Geographic latitude.
    - longitude (float): Geographic longitude.
    - timezone (str): Timezone for the response.

    Returns:
    Hourly data including:
    - temperature_2m (°C)
    - relative_humidity_2m (%)
    - dew_point_2m (°C)
    - apparent_temperature (°C)
    - rain (mm)
    - snowfall (cm)
    - precipitation (mm)
    - precipitation_probability (%)
    - cloud_cover (%)
    - wind_speed_10m (km/h)
    - wind_direction_10m (degrees)
    - wind_gusts_10m (km/h)
    - visibility (meters)
    - uv_index
    - is_day (0 or 1)
    - weather_code (Open-Meteo WMO code)
    """
    url=f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,relative_humidity_2m,dew_point_2m,apparent_temperature,rain,snowfall,precipitation_probability,precipitation,cloud_cover,wind_speed_10m,wind_direction_10m,wind_gusts_10m,visibility,weather_code,uv_index,is_day&timezone={timezone}&forecast_days=1'
    return call(url=url)


@mcp.tool()
def daily_weather(latitude: float = latitude_env,
                  longitude: float = longitude_env,
                  timezone: str = 'auto',
                  day:int = 7):
    """
    Fetches daily weather forecast for multiple days using Open-Meteo API.

    Parameters:
    - latitude (float): Geographic latitude.
    - longitude (float): Geographic longitude.
    - timezone (str): Timezone for the response.
    - day (int): Number of forecast days (default: 7, max: 16).

    Returns:
    Daily forecast data including:
    - temperature_2m_max (°C)
    - temperature_2m_min (°C)
    - uv_index_max
    - precipitation_sum (mm)
    - precipitation_probability_max (%)
    - weather_code (Open-Meteo WMO code)
    """
    url=f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=weather_code,temperature_2m_max,temperature_2m_min,uv_index_max,precipitation_sum,precipitation_probability_max&timezone={timezone}&forecast_days={day}'
    return call(url=url)

@mcp.tool()
def current_air(latitude: float = latitude_env,
                longitude: float = longitude_env,
                timezone: str = 'auto'):
    """
    Fetches current atmospheric weather data (not air quality).

    Parameters:
    - latitude (float): Geographic latitude.
    - longitude (float): Geographic longitude.
    - timezone (str): Timezone for the response.

    Returns:
    Current weather-related metrics including:
    - temperature
    - humidity
    - wind speed and gusts
    - cloud cover
    - rain
    - weather_code (Open-Meteo WMO code)
    """
    url=f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,apparent_temperature,is_day,relative_humidity_2m,weather_code,rain,wind_speed_10m,wind_gusts_10m,cloud_cover&timezone={timezone}&forecast_days=1'
    return call(url=url)


@mcp.tool()
def hourly_air(latitude: float = latitude_env,
                longitude: float = longitude_env,
                timezone: str = 'auto'):
    """
    Fetches hourly air quality data using Open-Meteo Air Quality API.

    Parameters:
    - latitude (float): Geographic latitude.
    - longitude (float): Geographic longitude.
    - timezone (str): Timezone for the response.

    Returns:
    Hourly air pollution metrics including:
    - pm10 (µg/m³)
    - pm2_5 (µg/m³)
    - nitrogen_dioxide (NO₂ µg/m³)
    - ozone (O₃ µg/m³)
    - carbon_monoxide (CO µg/m³)
    """
    url=f'https://air-quality-api.open-meteo.com/v1/air-quality?latitude={latitude}&longitude={longitude}&hourly=pm10,pm2_5,nitrogen_dioxide,ozone,carbon_monoxide&timezone={timezone}&forecast_days=1'
    return call(url=url)


@mcp.tool()
def daily_air(latitude: float = latitude_env,
              longitude: float = longitude_env,
              timezone: str = 'auto',
              day:int = 7):
    """
    Fetches daily weather forecast data (not air quality).

    Parameters:
    - latitude (float): Geographic latitude.
    - longitude (float): Geographic longitude.
    - timezone (str): Timezone for the response.
    - day (int): Number of forecast days.(default: 7, max: 16)

    Returns:
    Daily weather metrics including:
    - temperature_2m_max/min
    - sunrise, sunset
    - precipitation_sum
    - precipitation_probability_max
    - wind_speed_10m_max
    - weather_code (Open-Meteo WMO code)
    """
    url=f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=weather_code,temperature_2m_max,temperature_2m_min,sunrise,sunset,precipitation_sum,precipitation_probability_max,wind_speed_10m_max&timezone={timezone}&forecast_days={day}'
    return call(url=url)


@mcp.tool()
def news(search = city,
         country = 'in',
         languages = languages,):
    """
    Fetches latest news articles using the NewsData.io API.

    Parameters:
    - search (str): Keyword to search in article titles (default: city name).
    - country (str): Country code for filtering news (default: 'in' for India).
    - languages (str): Comma-separated language codes for filtering news
    (default: 'en,hi,gu' for English, Hindi, Gujarati).

    Returns:
    - A list of recent news articles matching the provided filters,
    including details such as title, description, source, and publication date.
    """
    url=f'https://newsdata.io/api/1/latest?apikey={news_api_key}&qInTitle={search}&country={country}&language={languages}'
    return call(url=url)


@mcp.tool()
def nearby_place(category,
                 latitude: float = latitude_env,
                 longitude: float = longitude_env,
                 radius_in_meters: float = 2000,
                 limit: int = 20):
    """
    Fetches nearby places using Geoapify Places API.

    Parameters:
    - latitude (float): Geographic latitude.
    - longitude (float): Geographic longitude.
    - radius_in_meters (float): Search radius.
    - limit (int): Maximum number of places to return.
    - category (str): Must be one of the following words only:

    [supermarket, grocery, mall, pharmacy, medical_store,
    electronics, clothing, shoes, jewelry,
    restaurant, cafe, coffee, fast_food, bakery, bar,
    hospital, clinic, dentist,
    school, college, university, library,bank, atm,
    hotel, hostel, guest_house,
    bus_stop, railway_station, metro_station, airport,
    park, playground, gym, stadium, swimming_pool,
    police, fire_station, post_office]

    Return only one category word from the list above.

    Returns:
    List of nearby places within the specified radius
    matching the selected category.
    """

    url = 'https://api.geoapify.com/v2/places'
    parameters = {"apiKey":geopify_api_key,
                  "categories":category,
                  "filter":f"circle:{longitude},{latitude},{radius_in_meters}",
                  "limit":limit}

    return call(url=url,parameters=parameters)
