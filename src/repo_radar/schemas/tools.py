from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class TeamConfig(BaseModel):
    """
    Configuration to assign users to teams.

    Example:
    {
        "teams": {
            "backend": ["alice", "bob"],
            "frontend": ["carol"]
        }
    }
    """
    teams: Optional[Dict[str, List[str]]] = Field(
        None, description="Mapping of team names to GitHub usernames"
    )


class DateRange(BaseModel):
    """
    Common date range for audit queries.

    Example:
    {
        "start_date": "2025-07-01",
        "end_date": "2025-07-28"
    }
    """
    start_date: str = Field(..., description="Start date in YYYY-MM-DD")
    end_date: str = Field(..., description="End date in YYYY-MM-DD")


class LargePRsOptions(BaseModel):
    """
    Configuration options for identifying large PRs.

    Example:
    {
        "pr_file_threshold": 25,
        "merged_only": true
    }
    """
    pr_file_threshold: int = Field(..., description="Min number of files to qualify as large PR")
    merged_only: Optional[bool] = Field(
        default=True,
        description="If true, only closed PRs that are merged will be considered"
    )


class StaleOrLongLivedPRsOptions(BaseModel):
    """
    Options to detect stale or long-lived PRs.

    Example:
    {
        "age_threshold_days": 14
    }
    """
    age_threshold_days: int = Field(
        ..., description="Number of days a PR must stay open to be considered long-lived"
    )


class GetLargePRsInput(DateRange, TeamConfig):
    """
    Full input for `get_large_prs` query.

    Example:
    {
        "start_date": "2025-07-01",
        "end_date": "2025-07-28",
        "teams": {
            "backend": ["alice", "bob"]
        },
        "get_large_prs": {
            "pr_file_threshold": 25,
            "merged_only": true
        }
    }
    """
    get_large_prs: LargePRsOptions


class GetStaleOrLongLivedPRsInput(DateRange, TeamConfig):
    """
    Full input for `get_stale_or_long_lived_prs` query.

    Example:
    {
        "start_date": "2025-07-01",
        "end_date": "2025-07-28",
        "teams": {
            "frontend": ["carol"]
        },
        "get_stale_or_long_lived_prs": {
            "age_threshold_days": 14
        }
    }
    """
    get_stale_or_long_lived_prs: StaleOrLongLivedPRsOptions
