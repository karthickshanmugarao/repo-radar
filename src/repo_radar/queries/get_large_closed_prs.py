# reporadar/queries/pr_large_closed.py

from typing import Any, Dict, List
from github.Repository import Repository
from datetime import datetime
from repo_radar.utils.team_utils import get_team_for_user

def get_large_closed_prs(repo: Repository, config: Dict[str, Any]) -> List[Dict[str, Any]]:
    start_date = datetime.strptime(config["start_date"], "%Y-%m-%d")
    end_date = datetime.strptime(config["end_date"], "%Y-%m-%d")
    query_config = config.get("get_large_closed_prs", {})
    file_threshold = query_config.get("pr_threshold", 20)
    teams = config.get("teams", {})

    results = []

    closed_prs = repo.get_pulls(state="closed", sort="updated", direction="desc")

    for pr in closed_prs:
        if pr.merged_at is None:
            continue
        if not (start_date <= pr.merged_at <= end_date):
            continue
        if pr.changed_files > file_threshold:
            author = pr.user.login
            team = get_team_for_user(author, teams)
            results.append({
                "pr": pr.number,
                "title": pr.title,
                "author": author,
                "merged_at": pr.merged_at.strftime("%Y-%m-%d"),
                "changed_files": pr.changed_files,
                "team": team,
                "url": pr.html_url
            })

    return results
