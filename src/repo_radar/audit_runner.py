import importlib
import inspect
import os
from pathlib import Path
from typing import Callable, Tuple, Type
from pydantic import BaseModel
import json
from repo_radar.github_client import get_github_and_repo

QUERIES_PATH = Path(__file__).parent / "queries"


def load_query_function_and_config(query_name: str) -> Tuple[Callable, Type[BaseModel]]:
    module_path = f"repo_radar.queries.{query_name}"
    module = importlib.import_module(module_path)

    # Get function
    func = getattr(module, query_name)

    # Get associated Config class
    for name, obj in inspect.getmembers(module):
        if (
            name.lower() == "config"
            and inspect.isclass(obj)
            and issubclass(obj, BaseModel)
        ):
            return func, obj

    raise ValueError(f"No Config class found in {query_name}")


def run_dynamic_query(query_name: str, raw_config: dict):
    func, ConfigClass = load_query_function_and_config(query_name)
    config_obj = ConfigClass(**raw_config)

    gh, repo = get_github_and_repo(raw_config)
    # repo = get_repo(gh, raw_config)

    result = func(gh, repo, config_obj)
    return result
