# repo_radar/mcp_server.py

import importlib.util
import inspect
from pathlib import Path
from fastmcp import FastMCP
from typing import Callable, Tuple, Type
from pydantic import BaseModel
from typing import Dict

import argparse
import json
from repo_radar.github_client import get_repo, get_github_and_repo
from repo_radar.audit_runner import run_dynamic_query
from repo_radar.utils.path_utils import get_queries_dir
from typing import Dict, List, Any
from dotenv import load_dotenv
import os


def load_cli_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="Path to config JSON file", default=r"")
    parser.add_argument(
        "--enabled_checks_config",
        help="Path to the enabled checks config JSON file",
        default=r"",
    )
    args = parser.parse_args()

    config_path: str = args.config
    enabled_checks_config: str = args.enabled_checks_config

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

    return config_path, enabled_checks_config


mcp = FastMCP("RepoRadarMCP")


def get_config_from_files():
    config_path, enabled_checks_config_path = load_cli_arguments()

    with open(config_path) as f:
        raw_config = json.load(f)

    with open(enabled_checks_config_path) as f:
        # Currently this is not used
        enabled_checks_config = json.load(f)

    return raw_config, enabled_checks_config


def insert_default_config_from_file(func, config_class):
    def wrapper(config: dict):
        # Load defaults
        configs_from_file, _ = get_config_from_files()

        # Merge: LLM overrides defaults
        merged_config = {**configs_from_file, **config}

        # Convert to model
        parsed_config = config_class(**merged_config)

        # 🔧 Auto-create internal dependencies
        gh, repo = get_github_and_repo(configs_from_file)

        # Call tool with just config, and inject gh/repo internally
        return func(gh, repo, parsed_config)

    return wrapper


def load_tools_for_mcp():

    QUERIES_DIR = get_queries_dir()

    for file in QUERIES_DIR.glob("*.py"):
        mod_name = f"repo_radar.queries.{file.stem}"
        spec = importlib.util.spec_from_file_location(mod_name, file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if hasattr(module, file.stem) and hasattr(module, "Config"):
            func = getattr(module, file.stem)
            doc = inspect.getdoc(func)

            config_class: Type[BaseModel] = getattr(module, "Config")
            config_doc = inspect.getdoc(config_class) or ""
            full_description = doc or ""
            if config_doc:
                full_description += f"\n\nConfig Schema:\n{config_doc}"

            wrapped_func = insert_default_config_from_file(func, config_class)
            mcp.tool(name=file.stem, description=full_description)(wrapped_func)
