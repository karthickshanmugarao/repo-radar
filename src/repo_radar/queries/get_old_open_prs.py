from typing import Dict, Any, List
from github.Repository import Repository
from datetime import datetime, timedelta
from repo_radar.utils.team_utils import get_team_for_user

def get_old_open_prs(repo: Repository, config: Dict[str, Any]) -> List[Dict[str, Any]]:
    start_date = datetime.strptime(config["start_date"], "%Y-%m-%d")
    end_date = datetime.strptime(config["end_date"], "%Y-%m-%d")
    query_config = config.get("get_old_open_prs", {})
    old_pr_days = query_config.get("old_pr_days", 7)
    threshold_date = datetime.utcnow() - timedelta(days=old_pr_days)
    teams = config.get("teams", {})

    results = []

    open_prs = repo.get_pulls(state="open", sort="created", direction="asc")

    for pr in open_prs:
        if pr.created_at < threshold_date:
            author = pr.user.login
            team = get_team_for_user(author, teams)
            results.append({
                "pr": pr.number,
                "title": pr.title,
                "author": author,
                "created_at": pr.created_at.strftime("%Y-%m-%d"),
                "team": team,
                "url": pr.html_url
            })

    return results


