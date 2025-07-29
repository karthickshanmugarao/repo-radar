# scripts/run_config_audit.py

import argparse
import json
from repo_radar.github_client import get_repo, get_github_and_repo
from repo_radar.audit_runner import run_queries
from repo_radar.utils.team_utils import group_results_by_team, summarize_failure_counts
from typing import Dict, List, Any

def generate_markdown_summary(summary: Dict[str, Dict[str, int]]) -> str:
    lines = ["# 🔍 Team-wise Audit Summary\n"]

    for team, checks in summary.items():
        lines.append(f"## 🧑‍🤝‍🧑 {team}")
        if not checks:
            lines.append("_No failures_\n")
            continue

        for check, count in checks.items():
            lines.append(f"- **{check}**: {count} failure(s)")

        lines.append("")  # add a blank line between teams

    return "\n".join(lines)

def save_failure_counts(team_results:dict, config: dict) -> None:
    summary_path = config.get("summary_output_path", "summary_output.json")
    summary_format = config.get("summary_format", "json")

    summary = summarize_failure_counts(team_results)
    if summary_format == "json":
        # Save failure counts JSON
        summary_path = config.get("summary_output_path", "summary_output.json")
        with open(summary_path, "w") as f:
            json.dump(summary, f, indent=2)
        print(f"📊 Summary report saved to {summary_path}")
    elif summary_format == "markdown":
        with open(summary_path, "w") as f:
            f.write(generate_markdown_summary(summary))

def save_all_results(team_results: dict, config: dict) -> None:
    output_format = config.get("output_format", "json")
    output_path = config.get("output_path", f"audit_output.{output_format}")

    if output_format == "json":
        # Save all results
        with open(output_path, "w") as f:
            json.dump(team_results, f, indent=2)
        
        summary = summarize_failure_counts(team_results)
        # Save failure counts JSON
        summary_path = config.get("summary_output_path", "summary_output.json")
        with open(summary_path, "w") as f:
            json.dump(summary, f, indent=2)
        print(f"📊 Summary report saved to {summary_path}")

    elif output_format == "markdown":
        with open(output_path, "w") as f:
            for team, checks in team_results.items():
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
