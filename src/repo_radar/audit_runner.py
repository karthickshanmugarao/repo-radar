from importlib import import_module

def run_queries(config: dict, repo):
    from os import listdir
    from os.path import dirname, isfile, join

    results = {}
    enabled = config.get("enabled_checks", [])

    queries_dir = dirname(__file__) + "/queries"
    py_files = [f for f in listdir(queries_dir) if f.endswith(".py") and f != "__init__.py"]

    for file in py_files:
        module_name = f"reporadar.queries.{file[:-3]}"
        module = import_module(module_name)
        for name in dir(module):
            if name.startswith("get_"):
                if not enabled or name in enabled:
                    fn = getattr(module, name)
                    results[name] = fn(repo, config)
    return results
