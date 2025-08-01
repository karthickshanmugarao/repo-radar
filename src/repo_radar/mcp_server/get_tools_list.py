import requests
import json

SERVER_URL = "http://localhost:8000/mcp"  # Replace with your FastMCP server URL

# MCP protocol for listing tools
request_payload = {"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}

try:
    response = requests.post(SERVER_URL, json=request_payload)
    response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)

    # FastMCP uses the MCP protocol.
    # The list of tools will be in the 'result' field of the JSON response.
    tools_data = response.json()
    print("Response JSON:", tools_data)

    if "result" in tools_data and isinstance(tools_data["result"], list):
        print("Available tools:")
        for tool in tools_data["result"]:
            print(f"- Name: {tool.get('name')}, Description: {tool.get('description')}")
    else:
        print("Unexpected response format for tools/list.")

except requests.exceptions.ConnectionError as e:
    print(
        f"Error: Could not connect to the FastMCP server at {SERVER_URL}. Is it running?"
    )
    print(f"Details: {e}")
except requests.exceptions.RequestException as e:
    print(f"Error during request to FastMCP server: {e}")
    print(f"Response content: {response.text if 'response' in locals() else 'N/A'}")
