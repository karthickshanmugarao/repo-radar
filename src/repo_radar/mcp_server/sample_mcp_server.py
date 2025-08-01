# server.py
from fastmcp import FastMCP

mcp = FastMCP(name="SimpleFastMCPServer")


@mcp.tool
def greet(name: str) -> str:
    """Return a simple greeting."""
    return f"Hello, {name}!"


if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8000)
