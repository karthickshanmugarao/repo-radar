from fastapi import FastAPI, Request
from repo_radar.audit_runner import run_queries
from repo_radar.github_client import get_repo

app = FastAPI(title="RepoRadar MCP Server")

@app.post("/mcp_query")
async def mcp_query(request: Request):
    body = await request.json()
    config = body.get("config")

    if not config or "repository" not in config:
        return {"error": "Missing 'repository' in config"}

    repo = get_repo(config)
    results = run_queries(config, repo)

    return results
