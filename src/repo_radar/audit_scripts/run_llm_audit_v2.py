import json
import inspect
import importlib.util
from pathlib import Path
from typing import Any
import os
import openai
from pydantic import BaseModel
from dotenv import load_dotenv

from repo_radar.audit_runner import run_dynamic_query
from repo_radar.github_client import get_github_and_repo
from repo_radar.mcp_server.tool_loader import mcp
import requests


QUERIES_DIR = Path(__file__).parent / "queries"


def get_tool_schemas() -> list[dict[str, Any]]:
    """
    Load tool schemas from the queries directory for OpenAI tool-calling.
    Each tool must define:
    - A function with same name as the file
    - A `Config` class (subclass of Pydantic BaseModel)
    """
    tool_schemas = []

    for file in QUERIES_DIR.glob("*.py"):
        mod_name = f"repo_radar.queries.{file.stem}"
        spec = importlib.util.spec_from_file_location(mod_name, file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if hasattr(module, file.stem) and hasattr(module, "Config"):
            func = getattr(module, file.stem)
            config_model: type[BaseModel] = getattr(module, "Config")
            doc = inspect.getdoc(func) or "No description provided."

            tool_schemas.append(
                {
                    "type": "function",
                    "function": {
                        "name": file.stem,
                        "description": doc,
                        "parameters": config_model.model_json_schema(),
                    },
                }
            )

    return tool_schemas


MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8000/mcp")


def call_llm_with_mcp(prompt: str, config: dict) -> dict:
    # 1. Fetch OpenAI-compatible tool schemas from MCP server
    schema_resp = requests.get(f"{MCP_SERVER_URL}/openai/schema")
    if schema_resp.status_code != 200:
        raise RuntimeError(f"Failed to get tool schema: {schema_resp.text}")

    tools = schema_resp.json()

    # 2. Call OpenAI with those tool schemas
    response = openai.chat.completions.create(
        model="gpt-4o",  # or gpt-3.5-turbo
        messages=[{"role": "user", "content": prompt}],
        tools=tools,
        tool_choice="auto",
    )

    tool_call = response.choices[0].message.tool_calls[0]
    fn_name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)

    print(f"🤖 LLM picked: {fn_name} with args:\n{json.dumps(args, indent=2)}")

    merged_config = {**config, **args}

    # 3. POST tool call to the MCP server (remote execution)
    result_resp = requests.post(
        f"{MCP_SERVER_URL}/openai/tool_call",
        json={
            "tool_call": {"name": fn_name, "arguments": args},
            "extra_context": {"config": merged_config},
        },
    )

    if result_resp.status_code != 200:
        raise RuntimeError(f"MCP tool call failed: {result_resp.text}")

    return {fn_name: result_resp.json()}


def load_cli_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="Path to config JSON file", default=r"")
    parser.add_argument(
        "--enabled_checks_config",
        help="Path to the enabled checks config JSON file",
        default=r"",
    )
    parser.add_argument(
        "--prompt",
        help="Natural language prompt for audit",
        default="find stale PRs from last week",
    )
    args = parser.parse_args()

    config_path: str = args.config
    enabled_checks_config: str = args.enabled_checks_config
    prompt: str = args.prompt

    load_dotenv()

    repo_radar_config_dir = os.getenv("REPO_RADAR_CONFIG_DIR")

    config_path = (
        config_path
        if config_path
        else os.path.join(repo_radar_config_dir, "config.json")
    )
    enabled_checks_config = (
        enabled_checks_config
        if enabled_checks_config
        else os.path.join(repo_radar_config_dir, "enabled_checks_config.json")
    )

    return config_path, enabled_checks_config, prompt


if __name__ == "__main__":
    import argparse

    config_path, enabled_checks_config_path, prompt = load_cli_arguments()

    with open(config_path) as f:
        base_config = json.load(f)

    result = call_llm_with_mcp(prompt, base_config)
    print("\n✅ Final Result:\n", json.dumps(result, indent=2))
