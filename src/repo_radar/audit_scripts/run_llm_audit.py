import os
import json
import openai
from repo_radar.audit_runner import run_queries
from repo_radar.github_client import get_repo
from repo_radar.schema import get_tool_schemas
import argparse

# Load OpenAI key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")

def call_llm_with_mcp(prompt: str, config: dict) -> dict:
    tools = get_tool_schemas()

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",  # or "gpt-4o-mini" for o3
        messages=[
            {"role": "user", "content": prompt}
        ],
        tools=tools,
        tool_choice="auto"
    )

    tool_call = response.choices[0].message.tool_calls[0]
    fn_name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)

    print(f"🤖 LLM picked: `{fn_name}` with args:\n{json.dumps(args, indent=2)}")

    # Merge args with the config (teams, dates, etc.)
    merged_config = {**config, **args}

    repo = get_repo(merged_config)
    result = run_queries(merged_config, repo)[fn_name]
    return result


if __name__ == "__main__":
    # Example minimal config
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="Path to config JSON file",
                        default=r"E:\py_workspace\repo-radar\src\repo_radar\examples\config.example.json")
    args = parser.parse_args()

    with open(args.config) as f:
        config = json.load(f)

    prompt = "Which PRs were too old in the repo during the last week and owned by any team?"

    output = call_llm_with_mcp(prompt, config)
    print("📊 Audit result from LLM:")
    print(json.dumps(output, indent=2))
