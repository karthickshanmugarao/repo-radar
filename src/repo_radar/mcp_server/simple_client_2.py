import os
import requests
from openai import OpenAI
from typing import Dict, List, Any
from dotenv import load_dotenv

load_dotenv()

# Create OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MCP_SERVER_URL = "http://localhost:8000"


def get_mcp_tools() -> List[Dict[str, Any]]:
    """Fetch available tools from the local MCP server"""
    url = f"{MCP_SERVER_URL}/tools"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def call_tool_via_mcp(tool_call: Dict[str, Any]) -> Dict:
    """Send a tool call to MCP and get the response"""
    tool_name = tool_call["function"]["name"]
    arguments = tool_call["function"]["arguments"]
    response = requests.post(f"{MCP_SERVER_URL}/call/{tool_name}", json=arguments)
    response.raise_for_status()
    return response.json()


def chat_with_openai(prompt: str, tools: List[Dict[str, Any]]) -> Dict:
    """Send a message to OpenAI with tools"""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        tools=tools,
        tool_choice="auto",
    )
    return response


def main():
    prompt = "Find stale PRs"

    # 1. Get tools from MCP
    print("[*] Fetching MCP tools...")
    tools = get_mcp_tools()
    print(f"[+] Retrieved {len(tools)} tools.")

    # 2. Send prompt to OpenAI with tools
    print("[*] Sending message to OpenAI with tools...")
    response = chat_with_openai(prompt, tools)

    # 3. Handle tool call if present
    choice = response.choices[0]
    if choice.message.tool_calls:
        for tool_call in choice.message.tool_calls:
            print(f"[+] Tool call requested: {tool_call.function.name}")
            result = call_tool_via_mcp(tool_call.model_dump())
            print("[*] Tool call result:")
            print(result)
    else:
        print("[+] No tool call. Assistant response:")
        print(choice.message.content)


if __name__ == "__main__":
    main()
