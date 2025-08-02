from openai import OpenAI
import json
from dotenv import load_dotenv
import asyncio
from fastmcp import Client
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client_openai = OpenAI(
    api_key=OPENAI_API_KEY
)  # Automatically uses OPENAI_API_KEY env variable


async def ask_gpt4o_for_tool(user_query="find stale PRs from repo "):
    client = Client("http://127.0.0.1:8000/mcp/")
    tools = []
    async with client:
        # Fetch and print all available tools
        tools = await client.list_tools()
    tool_list = "\n".join(
        f"- {tool.name}: {tool.description or 'No description'}" for tool in tools
    )

    prompt = f"""
You are an AI assistant. Here are the tools you can call:

{tool_list}

The user said: "{user_query}"

Based on this, respond in JSON with two fields:
- tool: the name of the tool to call
- inputs: the JSON object of inputs to pass to that tool

Example:
{{"tool": "greet", "inputs": {{"name": "Bob"}}}}
"""

    response = client_openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    print(prompt)

    content = response.choices[0].message.content
    print(content)

    plan = json.loads(content)  # safely parse GPT's JSON output
    tool_name = plan["tool"]
    inputs = plan["inputs"]

    # Call the FastMCP tool
    async with client:
        result = await client.call_tool(tool_name, inputs)
        print(result)
        print(result.data)
    return result


if __name__ == "__main__":
    asyncio.run(ask_gpt4o_for_tool())
