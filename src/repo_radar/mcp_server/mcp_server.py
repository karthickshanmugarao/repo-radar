from fastmcp import FastMCP
from fastapi import FastAPI
from fastapi import APIRouter
import uvicorn

import repo_radar.mcp_server.tool_loader  # this registers all tools

from repo_radar.mcp_server.tool_loader import mcp, load_tools_for_mcp

load_tools_for_mcp()

if __name__ == "__main__":
    # uvicorn.run(mcp, host="0.0.0.0", port=8000)
    mcp.run(transport="http", port=8000)
