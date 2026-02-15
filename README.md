# SmartCity-MCP-Assistant

SmartCity-MCP-Assistant is a city information assistant built using the Model Context Protocol (MCP).

Instead of hardcoding API calls inside the chat logic, the system separates reasoning (LLM) from tool execution (MCP tools).  
The LLM decides when external data is needed, and MCP handles structured API calls.

---

## What This Project Is

This project connects a Large Language Model with real-world public APIs such as:

- Weather
- Air quality
- News
- Nearby places

The assistant does not simply respond with static text.  
It analyzes the query, determines whether live data is required, and invokes tools dynamically.

It also implements caching to avoid unnecessary API calls.

---

## How It Works

The system is divided into three layers.

### 1. Context Providers (External APIs)

These are the real-world data sources:

- Open-Meteo → Weather + Air Quality  
- NewsData.io → News  
- Geoapify → Nearby Places  

Each provider returns structured JSON data.

---

### 2. MCP Server (Tool Layer)

The MCP server:

- Registers tools using FastMCP
- Wraps external API calls
- Applies default parameters (city, latitude, longitude)
- Returns structured outputs to the client

Each tool represents a specific capability (e.g., get weather, fetch news, find hospitals).

---

### 3. MCP Client + LLM (Reasoning Layer)

The client:

- Sends the user query to the LLM
- Determines whether a tool call is required
- Calls the appropriate MCP tool if needed
- Feeds tool output back to the LLM
- Generates the final response

The LLM is used for reasoning and formatting — not for retrieving raw data.

---

## Tool Invocation Flow

1. User submits a query.
2. The LLM analyzes the intent.
3. If real-time data is required:
   - The system checks cache.
   - If cache is expired, the MCP tool is invoked.
4. Tool output is returned.
5. The LLM generates a contextual, natural-language response.

This keeps data retrieval structured and reasoning separate.

---

## Caching Strategy

To reduce API usage, the system caches tool responses for specific durations:

- Current weather → 30 minutes  
- Hourly weather → 4 hours  
- Daily weather → 24 hours  
- Air quality → 30 minutes / 4 hours / 24 hours  
- News → 30 minutes  
- Nearby places → 3 days  

Cache is stored in `cache.json`.

---

## Example Use Cases

### Weather Advice

User:  
"Is it a good time to go out?"

The system fetches current weather and air quality, then generates advice.

![Weather Screenshot](https://github.com/user-attachments/assets/76317c6b-c8b7-4efa-8c74-3523784eea9b)

---

### News Retrieval

User:  
"What’s the latest news?"

The system fetches recent headlines and formats them.

![News Screenshot](https://github.com/user-attachments/assets/5113c622-8902-437d-8bd6-47406f3abb07)

---

### Nearby Hospital Search

User:  
"Find nearby hospitals."

The system queries Geoapify and returns location-based results.

![Nearby Hospital Screenshot](https://github.com/user-attachments/assets/912963d0-f7a8-4943-ba67-8c5f2e16421f)

---

## Tech Stack

- Python
- FastAPI
- FastMCP (Model Context Protocol)
- Mistral API
- Open-Meteo API
- NewsData.io API
- Geoapify Places API
- Jinja2
- HTML / CSS

---

## Project Structure

SmartCity-MCP-Assistant  
│  
├── App/  
│   ├── Routes.py  
│   ├── Conversations.py  
│  
├── MCP/  
│   ├── Server.py  
│   ├── Client.py  
│   ├── Nearby_Category.py  
│  
├── Cache/  
│   ├── cache_handler.py  
│   ├── cache.json  
│  
├── templates/  
│   └── index.html  
│  
├── initial_prompt.txt  
├── secondary_prompt.txt  
├── main.py  
├── requirements.txt  

---

## Environment Configuration

Create a `.env` file in the root directory:

```
MISTRAL_API_KEY=your_mistral_api_key
NEWS_API_KEY=your_news_api_key
GEOPIFY_API_KEY=your_geoapify_api_key
LATITUDE=your_latitude
LONGITUDE=your_longitude
CITY=your_default_city
LANGUAGES=preferred_language
```

All sensitive keys are loaded through environment variables.

---

## Running Locally

1. Install dependencies:

```
pip install -r requirements.txt
```

2. Configure your `.env` file.

3. Run:

```
python main.py
```

The FastAPI server will start locally and the assistant interface will be available in the browser.
