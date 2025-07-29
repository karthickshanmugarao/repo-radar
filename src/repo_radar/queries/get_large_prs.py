# repo_radar/queries/get_large_closed_prs.py

from datetime import datetime
from github import Github
from github.Repository import Repository
from typing import Dict, Any, List
from tqdm import tqdm

from repo_radar.utils.team_utils import get_team_for_user

def get_large_prs(
    gh: Github,
    repo: Repository,
    config: Dict[str, Any]
) -> List[Dict[str, Any]]:
    owner, repo_name = repo.full_name.split("/")
    start_date = config["start_date"]
    end_date = config["end_date"]

    check_config = config.get("get_large_prs", {})
    pr_threshold = check_config.get("pr_threshold", 20)
    merged_only = check_config.get("merged_only", True)
    teams = config.get("teams", {})

    results = []

    # 1️⃣ Search Closed PRs
    closed_query = (
        f"repo:{owner}/{repo_name} is:pr is:closed closed:{start_date}..{end_date}"
    )
    closed_issues = gh.search_issues(query=closed_query)

    for issue in tqdm(closed_issues, total=closed_issues.totalCount, desc="🔍 Checking Closed PRs with large number of files"):
        try:
            pr = repo.get_pull(issue.number)
            if merged_only and not pr.merged:
                continue
            if pr.changed_files > pr_threshold:
                results.append({
                    "number": pr.number,
                    "title": pr.title,
                    "user": pr.user.login,
                    "state": pr.state,
                    "merged": pr.merged,
                    "changed_files": pr.changed_files,
                    "created_at": pr.created_at.isoformat(),
                    "closed_at": pr.closed_at.isoformat() if pr.closed_at else None,
                    "html_url": pr.html_url,
                    "team": get_team_for_user(pr.user.login, teams)
                })
        except Exception as e:
            print(f"⚠️ Failed to process closed PR #{issue.number}: {e}")

    # 2️⃣ Search Open PRs
    open_query = f"repo:{owner}/{repo_name} is:pr is:open"
    open_issues = gh.search_issues(query=open_query)

    for i, issue in enumerate(tqdm(open_issues, total=open_issues.totalCount, desc="🔍 Checking Open PRs with large number of files")):
        try:
            pr = repo.get_pull(issue.number)
            if pr.changed_files > pr_threshold:
                results.append({
                    "number": pr.number,
                    "title": pr.title,
                    "user": pr.user.login,
                    "state": pr.state,
                    "merged": False,
                    "changed_files": pr.changed_files,
                    "created_at": pr.created_at.isoformat(),
                    "closed_at": None,
                    "html_url": pr.html_url,
                    "team": get_team_for_user(pr.user.login, teams)
                })
            if i > 20:
                print("Too many open PRs, stopping analysis after 100 PRs")
                break
        except Exception as e:
            print(f"⚠️ Failed to process open PR #{issue.number}: {e}")

    return results