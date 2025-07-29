import os
from github import Github
from github.Repository import Repository
from dotenv import load_dotenv
from urllib.parse import urlparse
from typing import Tuple

def get_repo(config: dict = None) -> Repository:
    load_dotenv()
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise EnvironmentError("❌ GITHUB_TOKEN not found in environment variables.")

    if not config or "repository" not in config:
        raise ValueError("❌ Missing 'repository' key in config file.")

    gh = Github(token)
    return gh.get_repo(config["repository"])

def get_github_and_repo(config: dict) -> Tuple[Github, Repository]:
    load_dotenv()
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("Missing GITHUB_TOKEN in environment")

    repo_url = config.get("repository")
    if not repo_url:
        raise ValueError("repository must be provided in the config")

    parsed = urlparse(repo_url)
    host = parsed.netloc
    path = parsed.path.strip("/")

    if "github.com" in host:
        gh = Github(token)
    else:
        # Enterprise GitHub
        base_url = config.get("base_url")
        if not base_url: # if base url is not explicitly mentioned in config
            base_url = f"https://{host}/api/v3"
        gh = Github(base_url=base_url, login_or_token=token)

    repo = gh.get_repo(path)
    return gh, repo


