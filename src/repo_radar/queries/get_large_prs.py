# repo_radar/queries/get_large_prs.py

from typing import List, Dict, Any
from github import Github, Repository
from pydantic import BaseModel, Extra, ConfigDict
from tqdm import tqdm
from repo_radar.utils.team_utils import get_team_for_user
from repo_radar.github_client import get_github_and_repo


class Config(BaseModel, extra=Extra.allow):
    """
    Configuration for identifying large PRs.

    Parameters
    ----------
    start_date : str
        ISO format start date (e.g., "2024-01-01").
    end_date : str
        ISO format end date (e.g., "2024-12-31").
    pr_file_threshold : int, optional
        Minimum number of changed files to consider a PR large (default is 20).
    merged_only : bool, optional
        When True, only merged PRs are considered (default is True).
    include_open : bool, optional
        When True, open PRs are also included in the check (default is True).
    """

    start_date: str
    end_date: str
    pr_file_threshold: int = 20
    merged_only: bool = True
    include_open: bool = True


def get_large_prs(config: Config) -> List[Dict[str, Any]]:
    """
    Identify large pull requests by file count.

    Parameters
    ----------
    gh : Github
        An authenticated GitHub API client.
    repo : Repository
        The repository to inspect.
    config : Config
        Parameters controlling date range and thresholds. Refer the Config class description.

    Returns
    -------
    List[Dict[str, Any]]
        List of PR metadata exceeding the file threshold.
    """

    if type(config) == "dict":
        config = Config(**config)

    gh, repo = get_github_and_repo(config.model_dump())
    results = []
    file_threshold = config.pr_file_threshold

    # Closed PRs
    closed_query = f"repo:{repo.full_name} is:pr is:closed closed:{config.start_date}..{config.end_date}"
    closed_issues = gh.search_issues(closed_query)
    for issue in tqdm(
        closed_issues, total=closed_issues.totalCount, desc="🔍 Checking closed PRs"
    ):
        pr = repo.get_pull(issue.number)
        if config.merged_only and not pr.merged:
            continue
        if pr.changed_files > file_threshold:
            results.append(
                {
                    "number": pr.number,
                    "title": pr.title,
                    "user": pr.user.login,
                    "created_at": pr.created_at.isoformat(),
                    "closed_at": pr.closed_at.isoformat() if pr.closed_at else None,
                    "merged": pr.merged,
                    "state": pr.state,
                    "changed_files": pr.changed_files,
                    "html_url": pr.html_url,
                    "team": get_team_for_user(pr.user.login, config.get("teams", {})),
                }
            )

    # Open PRs
    if config.include_open:
        open_query = f"repo:{repo.full_name} is:pr is:open"
        open_issues = gh.search_issues(open_query)
        for i, issue in enumerate(
            tqdm(open_issues, total=open_issues.totalCount, desc="📂 Checking open PRs")
        ):
            pr = repo.get_pull(issue.number)
            if pr.changed_files > file_threshold:
                results.append(
                    {
                        "number": pr.number,
                        "title": pr.title,
                        "user": pr.user.login,
                        "created_at": pr.created_at.isoformat(),
                        "closed_at": None,
                        "merged": False,
                        "state": pr.state,
                        "changed_files": pr.changed_files,
                        "html_url": pr.html_url,
                        "team": get_team_for_user(
                            pr.user.login, getattr(config, "teams", {})
                        ),
                    }
                )
            if i >= getattr(config, "max_open_prs_to_analyse", 200):
                print(f"Too many open PRs, stopping analysis after {i+1} PRs")
                break

    return results
