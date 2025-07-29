import os
from github import Github

def get_repo():
    token = os.getenv("GITHUB_TOKEN")
    repo_name = os.getenv("REPO_NAME")
    
    if not token or not repo_name:
        raise EnvironmentError("GITHUB_TOKEN and REPO_NAME must be set.")

    gh = Github(token)
    return gh.get_repo(repo_name)
