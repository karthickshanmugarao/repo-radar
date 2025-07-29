import os
from github import Github
from github.Repository import Repository
from dotenv import load_dotenv

def get_repo(config: dict = None) -> Repository:
    load_dotenv()
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise EnvironmentError("❌ GITHUB_TOKEN not found in environment variables.")

    if not config or "repository" not in config:
        raise ValueError("❌ Missing 'repository' key in config file.")

    gh = Github(token)
    return gh.get_repo(config["repository"])

def get_github_and_repo(config: dict = None) -> tuple[Github, Repository]:
    load_dotenv()
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise EnvironmentError("❌ GITHUB_TOKEN not found in environment variables.")

    if not config or "repository" not in config:
        raise ValueError("❌ Missing 'repository' key in config file.")
    
    gh = Github(token)
    repo = gh.get_repo(config["repository"])
    return gh, repo


