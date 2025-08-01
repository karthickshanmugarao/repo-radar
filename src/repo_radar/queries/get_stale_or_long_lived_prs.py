"""
Identify stale (open too long) and long-lived (closed but took long) pull requests.

Finds:
- Open PRs that have been open for more than `age_threshold_days`.
- Closed PRs that were open longer than `age_threshold_days` and closed within a date range.
"""

from datetime import datetime, timezone
from typing import List, Dict, Any

from github import Github, Repository
from pydantic import BaseModel, Field, Extra
from tqdm import tqdm

from repo_radar.utils.team_utils import get_team_for_user


class Config(BaseModel, extra=Extra.allow):
    """Configuration for stale or long-lived PRs.

    Parameters
    ----------
    start_date : str
        Start date for filtering closed PRs (YYYY-MM-DD).
    end_date : str
        End date for filtering closed PRs (YYYY-MM-DD).
    age_threshold_days : int
        Threshold (in days) to consider a PR stale or long-lived.
    """

    start_date: str
    end_date: str
    age_threshold_days: int = 7


def get_stale_or_long_lived_prs(
    gh: Github,
    repo: Repository.Repository,
    config: Config,
) -> List[Dict[str, Any]]:
    owner, repo_name = repo.full_name.split("/")

    start_date = config.start_date
    end_date = config.end_date
    age_threshold = config.age_threshold_days

    results = []

    query_closed = (
        f"repo:{owner}/{repo_name} is:pr is:closed closed:{start_date}..{end_date}"
    )
    closed_issues = gh.search_issues(query=query_closed)

    for issue in tqdm(
        closed_issues, total=closed_issues.totalCount, desc="Checking Closed PRs"
    ):
        pr = repo.get_pull(issue.number)
        if not pr.created_at or not pr.closed_at:
            continue

        pr_age_days = (pr.closed_at - pr.created_at).days
        if pr_age_days > age_threshold:
            results.append(
                {
                    "number": pr.number,
                    "title": pr.title,
                    "user": pr.user.login,
                    "created_at": pr.created_at.isoformat(),
                    "closed_at": pr.closed_at.isoformat(),
                    "age_days": pr_age_days,
                    "state": "closed",
                    "type": "long_lived",
                    "team": get_team_for_user(
                        pr.user.login, getattr(config, "teams", {})
                    ),
                }
            )

    open_query = f"repo:{repo.full_name} is:pr is:open"
    open_issues = gh.search_issues(open_query)

    for i, pr in enumerate(
        tqdm(open_issues, total=open_issues.totalCount, desc="Checking Open PRs")
    ):
        pr_age_days = (datetime.now(timezone.utc) - pr.created_at).days
        if pr_age_days > age_threshold:
            results.append(
                {
                    "number": pr.number,
                    "title": pr.title,
                    "user": pr.user.login,
                    "created_at": pr.created_at.isoformat(),
                    "closed_at": None,
                    "age_days": pr_age_days,
                    "state": "open",
                    "type": "stale",
                    "team": get_team_for_user(
                        pr.user.login, getattr(config, "teams", {})
                    ),
                }
            )

        if i >= getattr(config, "max_open_prs_to_analyse", 200):
            print(f"Too many open PRs, stopping analysis after {i+1} PRs")
            break

    return results
