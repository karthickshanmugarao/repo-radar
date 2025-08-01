# client.py
import asyncio
from fastmcp import Client


async def main():
    client = Client("http://127.0.0.1:8000/mcp/")
    async with client:
        # Fetch and print all available tools
        tools = await client.list_tools()
        print("Available tools on server:")
        for tool in tools:
            print(f"  - {tool.name}: {tool.description or 'No description'}")

        # Call one of the tools (e.g., 'greet') if it exists
        if any(tool.name == "greet" for tool in tools):
            result = await client.call_tool("greet", {"name": "Alice"})
            print("Server responded:", result)
        else:
            print("Tool 'greet' not found on server.")


if __name__ == "__main__":
    asyncio.run(main())
