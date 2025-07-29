import os
from github import Github
from github.Repository import Repository
import json

def get_repo(config: dict = None) -> Repository:
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise EnvironmentError("❌ GITHUB_TOKEN not found in environment variables.")

    if not config or "repository" not in config:
        raise ValueError("❌ Missing 'repository' key in config file.")

    gh = Github(token)
    return gh.get_repo(config["repository"])

