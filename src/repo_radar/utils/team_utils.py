from typing import Dict, List, Any
import json, os
from repo_radar.utils.path_utils import resolve_path

def get_team_for_user(username: str, teams: Dict[str, List[str]]) -> str:
    for team, members in teams.items():
        if username.lower() in [m.lower() for m in members]:
            return team
    return "NA"

def group_results_by_team(
    raw_results: Dict[str, List[Dict[str, Any]]],
    teams: Dict[str, List[str]]
) -> Dict[str, Dict[str, List[Dict[str, Any]]]]:
    summary: Dict[str, Dict[str, List[Dict[str, Any]]]] = {}

    for check_name, results in raw_results.items():
        for item in results:
            team = item.get("team", "NA")
            if team not in summary:
                summary[team] = {}
            if check_name not in summary[team]:
                summary[team][check_name] = []
            summary[team][check_name].append(item)

    return summary

def summarize_failure_counts(team_results: Dict[str, Dict[str, List[Dict[str, Any]]]]) -> Dict[str, Dict[str, int]]:
    summary = {}

    for team, checks in team_results.items():
        summary[team] = {}
        for check_name, failures in checks.items():
            summary[team][check_name] = len(failures)

    return summary

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
    summary_format = config.get("summary_format", "json")
    summary_path = resolve_path(config.get("summary_output_path", "summary_output.json"))

    summary = summarize_failure_counts(team_results)
    if summary_format == "json":
        # Save failure counts JSON
        summary_path = config.get("summary_output_path", "summary_output.json")
        with open(summary_path, "w") as f:
            json.dump(summary, f, indent=2)
        
    elif summary_format == "markdown":
        with open(summary_path, "w") as f:
            f.write(generate_markdown_summary(summary))

    else:
        raise ValueError("Unsupported summary_format. Use 'json' or 'markdown'.")
    
    print(f"📊 Summary report saved to {summary_path}")

def save_all_results(team_results: dict, config: dict) -> None:
    output_format = config.get("output_format", "json")
    output_path = resolve_path(config.get("output_path", f"audit_output.{output_format}"))

    if output_format == "json":
        # Save all results
        with open(output_path, "w") as f:
            json.dump(team_results, f, indent=2)

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
