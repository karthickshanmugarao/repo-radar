import asyncio
from fastmcp import Client


client = Client("mcp_server.py")


async def call_tool(name: str):
    async with client:
        result = await client.call_tool(
            "get_large_prs",
            {
                "get_large_prs": {
                    "pr_file_threshold": 20,
                    "merged_only": True,
                    "include_open": True,
                }
            },
        )
        print(result)


asyncio.run(call_tool("get_large_prs"))
