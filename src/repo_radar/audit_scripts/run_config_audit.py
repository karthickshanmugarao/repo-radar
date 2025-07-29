# scripts/run_config_audit.py

import argparse
import json
from repo_radar.github_client import get_repo
from repo_radar.audit_runner import run_queries
from repo_radar.utils.team_utils import group_results_by_team

def save_output(team_summary: dict, config: dict) -> None:
    output_format = config.get("output_format", "json")
    output_path = config.get("output_path", f"audit_output.{output_format}")

    if output_format == "json":
        with open(output_path, "w") as f:
            json.dump(team_summary, f, indent=2)
    elif output_format == "markdown":
        with open(output_path, "w") as f:
            for team, checks in team_summary.items():
                f.write(f"# Team: {team}\n\n")
                for check_name, results in checks.items():
                    f.write(f"## {check_name.replace('_', ' ').title()}\n")
                    f.write("```\n")
                    f.write(json.dumps(results, indent=2))
                    f.write("\n```\n\n")
    else:
        raise ValueError("Unsupported output_format. Use 'json' or 'markdown'.")

    print(f"✅ Audit report saved to {output_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Path to config JSON file")
    args = parser.parse_args()

    with open(args.config) as f:
        config = json.load(f)

    repo = get_repo()
    print("🔍 Running audit checks...")

    # Step 1: Run all enabled queries and collect raw results
    raw_results = run_queries(config, repo)

    # Step 2: Group them by team
    team_summary = group_results_by_team(raw_results, config.get("teams", {}))

    # Step 3: Save output
    save_output(team_summary, config)


if __name__ == "__main__":
    main()
