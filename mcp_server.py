from mcp.server.fastmcp import FastMCP                                        #It imports FastMCP (the toolkit for building an MCP server) and datetime (so it can work with dates and times).
from datetime import datetime
import requests


mcp = FastMCP("My First MCP Server")                                          #this builds the actual server and gives it a name. Like hanging up a sign that says "Kitchen open."


@mcp.tool()                                                                   #@mcp.tool() — this is a decorator. It's basically a sticky note that says "hey, the function right below me is a tool anyone can call." Without it, the function below would just be a private helper.
def get_current_time():                                                       
    """Get current time"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@mcp.tool()
def get_stock_price(symbol: str) -> str:
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        data = response.json()
        price = data["chart"]["result"][0]["meta"]["regularMarketPrice"]
        return f"{symbol.upper()} stock price is ${price}"

    except Exception as e:
        return f"Unable to fetch stock price for {symbol}"
    
@mcp.tool()
def calculator(expression: str):
    return str(eval(expression))

@mcp.tool()
def get_weather(city: str):
    return f"{city} is 70°F"


if __name__ == "__main__":                                                   #if __name__ == "__main__": block is the "start me up" part. 
    mcp.run()                                                                #mcp.run() starts the server and keeps it waiting for someone to connect.