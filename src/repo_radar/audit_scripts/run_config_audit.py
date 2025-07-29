import argparse
import json
from repo_radar.github_client import get_repo, get_github_and_repo
from repo_radar.audit_runner import run_queries
from repo_radar.utils.team_utils import ( group_results_by_team, 
                                          summarize_failure_counts,
                                          save_all_results,
                                          save_failure_counts
)
from typing import Dict, List, Any

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="Path to config JSON file",
                        default=r"E:\py_workspace\repo-radar\src\repo_radar\examples\config.example.json")
    args = parser.parse_args()

    with open(args.config) as f:
        config = json.load(f)

    gh, repo = get_github_and_repo(config)
    print("🔍 Running audit checks...")

    # Step 1: Run all enabled queries and collect raw results
    raw_results = run_queries(config, gh, repo)

    # Step 2: Group them by team
    team_results = group_results_by_team(raw_results, config.get("teams", {}))

    # Step 3: Save output
    save_all_results(team_results, config)
    save_failure_counts(team_results, config)


if __name__ == "__main__":
    main()
