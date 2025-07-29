from github import Github
from github.Repository import Repository
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any
from repo_radar.utils.team_utils import get_team_for_user

def get_stale_or_long_lived_prs(gh: Github, repo: Repository, config: Dict[str, Any]) -> List[Dict[str, Any]]:
    owner, repo_name = repo.full_name.split("/")
    pr_age_threshold = config.get("get_stale_or_long_lived_prs", {}).get("pr_age_threshold", 7)
    start_date = config["start_date"]
    end_date = config["end_date"]
    start_dt = datetime.fromisoformat(start_date)
    end_dt = datetime.fromisoformat(end_date)

    results = []

    # 🟡 Closed PRs in the given window
    closed_query = f"repo:{owner}/{repo_name} is:pr is:closed closed:{start_date}..{end_date}"
    closed_issues = gh.search_issues(query=closed_query)

    for issue in closed_issues:
        pr = repo.get_pull(issue.number)
        if pr.created_at and pr.closed_at:
            age_days = (pr.closed_at - pr.created_at).days
            if age_days > pr_age_threshold:
                results.append({
                    "number": pr.number,
                    "title": pr.title,
                    "user": pr.user.login,
                    "created_at": pr.created_at.isoformat(),
                    "closed_at": pr.closed_at.isoformat(),
                    "open_duration_days": age_days,
                    "state": "closed",
                    "team": get_team_for_user(pr.user.login, config.get("teams", {}))
                })

    # 🟢 Open PRs older than threshold
    open_query = f"repo:{owner}/{repo_name} is:pr is:open created:<{(datetime.utcnow() - timedelta(days=pr_age_threshold)).date()}"
    open_issues = gh.search_issues(query=open_query)

    for issue in open_issues:
        pr = repo.get_pull(issue.number)
        age_days = (datetime.now(timezone.utc) - pr.created_at).days
        if age_days > pr_age_threshold:
            results.append({
                "number": pr.number,
                "title": pr.title,
                "user": pr.user.login,
                "created_at": pr.created_at.isoformat(),
                "closed_at": None,
                "open_duration_days": age_days,
                "state": "open",
                "team": get_team_for_user(pr.user.login, config.get("teams", {}))
            })

    return results
