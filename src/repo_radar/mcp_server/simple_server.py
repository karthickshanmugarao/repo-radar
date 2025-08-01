from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# OPENAI_API_KEY =

# Your server URL (replace with your actual URL)
url = "http://127.0.0.1:8000/mcp/"

client = OpenAI()

resp = client.responses.create(
    model="gpt-4o",
    tools=[
        {
            "type": "mcp",
            "server_label": "RepoRadarMCP",
            "server_url": f"{url}/mcp/",
            "require_approval": "never",
        },
    ],
    input="find stale PRs",
)

print(resp.output_text)
