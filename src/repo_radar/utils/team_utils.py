from typing import Dict, List, Any

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


