import os
from pathlib import Path
from dotenv import load_dotenv
import importlib.util


def resolve_path(path: str) -> str:
    """
    Resolves a relative or absolute file path, and ensures the parent directories exist.

    - Supports Windows and Unix-style paths.
    - Does NOT expand '~' (home directory).
    - Creates parent directories if they don't exist.

    Args:
        path (str): The path to resolve (e.g. 'reports/output.json').

    Returns:
        str: The absolute, usable path.
    """
    # Normalize and get absolute path
    abs_path = os.path.abspath(path)

    # Ensure the parent directory exists
    dir_path = os.path.dirname(abs_path)
    os.makedirs(dir_path, exist_ok=True)

    return abs_path


def get_queries_dir():
    # 1. Try to load from .env
    env_path = os.getenv("QUERIES_DIR")

    if env_path:
        QUERIES_DIR = Path(env_path)
    else:
        # 2. Fallback: locate actual `repo_radar.queries` module
        spec = importlib.util.find_spec("repo_radar.queries")
        if not spec or not spec.submodule_search_locations:
            raise RuntimeError("Could not locate repo_radar.queries module.")

        QUERIES_DIR = Path(spec.submodule_search_locations[0])
    return QUERIES_DIR
