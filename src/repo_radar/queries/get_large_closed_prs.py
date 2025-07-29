# repo_radar/queries/get_large_closed_prs.py

from datetime import datetime
from github import Github
from github.Repository import Repository
from typing import Dict, Any, List

from repo_radar.utils.team_utils import get_team_for_user

def get_large_closed_prs(gh: Github, repo: Repository, config: Dict[str, Any]) -> List[Dict[str, Any]]:
    owner, repo_name = repo.full_name.split("/")
    start_date = config["start_date"]
    end_date = config["end_date"]
    file_threshold = config.get("get_large_closed_prs", {}).get("pr_file_threshold", 20)
    merged_only = config.get("get_large_closed_prs", {}).get("merged_only", True)

    results = []

    # Search for PRs closed in the date range
    query = f"repo:{owner}/{repo_name} is:pr is:closed closed:{start_date}..{end_date}"
    issues = gh.search_issues(query=query)

    for issue in issues:
        pr = repo.get_pull(issue.number)

        if merged_only and not pr.merged:
            continue

        if pr.changed_files > file_threshold:
            results.append({
                "number": pr.number,
                "title": pr.title,
                "user": pr.user.login,
                "created_at": pr.created_at.isoformat(),
                "closed_at": pr.closed_at.isoformat() if pr.closed_at else None,
                "merged": pr.merged,
                "changed_files": pr.changed_files,
                "team": get_team_for_user(pr.user.login, config.get("teams", {}))
            })

    return results
