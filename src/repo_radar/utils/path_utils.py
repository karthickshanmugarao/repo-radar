import os

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
