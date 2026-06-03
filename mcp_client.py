from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client
import anyio


async def main():                                         #async def main(): — the whole program lives inside this. The word async matters: it means this code can "wait" for slow things (like a server responding) without freezing everything else. await later in the file means "pause here until this finishes, then continue."
    server_params = StdioServerParameters(                #server_params describes how to launch the server — basically "run python mcp_server.py." So the client actually starts up the kitchen itself.
        command="python",                                 
        args=["mcp_server.py"]
    )

    async with stdio_client(server_params) as (read, write):     #Opens a connection to the server (the read, write are the two channels for sending and receiving messages).
        async with ClientSession(read, write) as session:        #You wrap those two channels into a session. The session is smart — it knows how to turn your simple Python commands into proper messages the server understands, send them, and read the replies. You talk to session in plain Python; it handles the messy details.

            await session.initialize()                           #(initialize): First message sent: "Hi, are you there? What version are you, and what can you do?" The server answers. This is just the two programs introducing themselves. The await means your code waits here until the server replies before moving on.
            tools = await session.list_tools()                   #(list_tools): You ask the server: "What functions do you have?" The server sends back a list — names, descriptions, and what info each one needs. 
            
            print("Available Tools:")                            
            print(tools)        

            result = await session.call_tool(                    # (call_tool): You tell the server: "Run the one called get_current_time." The {} means "I'm not giving it any extra info" (because that function doesn't need any).
                "get_current_time",
                {}
            )
            result = await session.call_tool(
                "get_stock_price",
                {
                    "symbol": "AAPL"
                    }
            )

            result = await session.call_tool(
                "calculator",
                {"expression": "500 * 2"}
            )
            
            result=await session.call_tool(
                "get_weather",
                {"city": "Indianapolis"}
            )

            print("\nTool Result:")
            print(result)


anyio.run(main)                                               #(anyio.run(main)): This is the actual "go" button. Everything above is just defined but asleep. This line wakes it up and runs it from start to finish.


