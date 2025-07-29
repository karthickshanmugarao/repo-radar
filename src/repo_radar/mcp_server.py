from fastapi import FastAPI, Request
from .audit_runner import run_queries
from .github_client import get_repo

app = FastAPI()
repo = get_repo()

@app.post("/mcp_query")
async def mcp_query(request: Request):
    body = await request.json()
    config = body.get("config")
    results = run_queries(config, repo)
    return results
