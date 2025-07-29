# scripts/run_llm_audit.py

import os
import json
import openai
from repo_radar.audit_runner import run_queries
from repo_radar.github_client import get_repo
from repo_radar.schema import get_tool_schemas

openai.api_key = os.getenv("OPENAI_API_KEY")
repo = get_repo()

def call_llm_with_mcp(prompt, config):
    tools = get_tool_schemas()

    response = openai.ChatCompletion.create(
        model="gpt-4o",  # or gpt-4o-mini (o3)
        messages=[{"role": "user", "content": prompt}],
        tools=tools,
        tool_choice="auto",
    )

    tool_call = response.choices[0].message.tool_calls[0]
    fn_name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)

    print(f"🤖 LLM picked: {fn_name} with args:\n{json.dumps(args, indent=2)}")

    result = run_queries(args, repo)[fn_name]
    return result


if __name__ == "__main__":
    # Example config + prompt
    config = {
        "teams": {
            "backend": ["alice", "bob"]
        },
        "start_date": "2025-07-21",
        "end_date": "2025-07-28"
    }

    prompt = "Which PRs were merged into non-main branches last week by the backend team?"

    output = call_llm_with_mcp(prompt, config)
    print("📊 Audit result from LLM:")
    print(json.dumps(output, indent=2))
