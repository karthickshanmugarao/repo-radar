# repo_radar/mcp_server.py

import importlib.util
import inspect
from pathlib import Path
from fastmcp import FastMCP
from typing import Callable, Tuple, Type
from pydantic import BaseModel

mcp = FastMCP("RepoRadarMCP")


def load_tools_for_mcp():
    QUERIES_DIR = Path(r"E:\py_workspace\repo-radar\src\repo_radar\queries")

    for file in QUERIES_DIR.glob("*.py"):
        mod_name = f"repo_radar.queries.{file.stem}"
        spec = importlib.util.spec_from_file_location(mod_name, file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if hasattr(module, file.stem) and hasattr(module, "Config"):
            func = getattr(module, file.stem)
            doc = inspect.getdoc(func)

            config_model: Type[BaseModel] = getattr(module, "Config")
            config_doc = inspect.getdoc(config_model) or ""
            full_description = doc or ""
            if config_doc:
                full_description += f"\n\nConfig Schema:\n{config_doc}"

            mcp.tool(name=file.stem, description=full_description)(func)
