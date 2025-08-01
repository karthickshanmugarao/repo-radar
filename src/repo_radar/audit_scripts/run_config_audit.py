import argparse
import json
from repo_radar.github_client import get_repo, get_github_and_repo
from repo_radar.audit_runner import run_dynamic_query
from repo_radar.utils.team_utils import (
    group_results_by_team,
    summarize_failure_counts,
    save_all_results,
    save_failure_counts,
)
from typing import Dict, List, Any
from dotenv import load_dotenv
import os


def load_cli_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="Path to config JSON file", default=r"")
    parser.add_argument(
        "--enabled_checks_config",
        help="Path to the enabled checks config JSON file",
        default=r"",
    )
    args = parser.parse_args()

    config_path: str = args.config
    enabled_checks_config: str = args.enabled_checks_config

    load_dotenv()

    repo_radar_config_dir = os.getenv("REPO_RADAR_CONFIG_DIR")

    config_path = (
        config_path
        if config_path
        else os.path.join(repo_radar_config_dir, "config.json")
    )
    enabled_checks_config = (
        enabled_checks_config
        if enabled_checks_config
        else os.path.join(repo_radar_config_dir, "enabled_checks_config.json")
    )

    return config_path, enabled_checks_config


def run_config_audit(raw_config, enabled_checks_config) -> dict:
    results = {}
    for check_name in enabled_checks_config["enabled_checks"]:
        print(f"🔍 Running audit check: {check_name}...")
        results[check_name] = run_dynamic_query(check_name, raw_config)

    return results


def main():
    config_path, enabled_checks_config_path = load_cli_arguments()

    with open(config_path) as f:
        raw_config = json.load(f)

    with open(enabled_checks_config_path) as f:
        enabled_checks_config = json.load(f)

    # Step 1: Run all enabled queries and collect raw results
    raw_results = run_config_audit(raw_config, enabled_checks_config)

    # Step 2: Group them by team
    team_results = group_results_by_team(raw_results, raw_config.get("teams", {}))

    # Step 3: Save output
    save_all_results(team_results, raw_config)
    save_failure_counts(team_results, raw_config)


if __name__ == "__main__":
    main()
