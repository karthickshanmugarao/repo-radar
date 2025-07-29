

from datetime import datetime, timedelta

def get_failing_checkall_tests(repo, config):
    return [{"date": config["start_date"], "status": "failed", "pr": "#123"}]

def get_closed_prs_with_test_failures(repo, config):
    prs = repo.get_pulls(state="closed")
    failures = []
    for pr in prs:
        if config["start_date"] <= pr.closed_at.strftime("%Y-%m-%d") <= config["end_date"]:
            if any(c.conclusion != "success" for c in pr.get_check_runs()):
                failures.append({"pr": pr.number})
    return failures

def get_non_main_branch_prs(repo, config):
    return [{"pr": pr.number} for pr in repo.get_pulls(state="all") 
            if pr.base.ref != "main" and config["start_date"] <= pr.created_at.strftime("%Y-%m-%d") <= config["end_date"]]

def get_old_open_prs(repo, config):
    one_week_ago = datetime.now() - timedelta(days=7)
    return [{"pr": pr.number} for pr in repo.get_pulls(state="open") if pr.created_at < one_week_ago]

def get_weekly_open_prs_per_team(repo, config):
    team_map = {k: set(v) for k, v in config["teams"].items()}
    results = {team: [] for team in team_map}
    for pr in repo.get_pulls(state="open"):
        for team, users in team_map.items():
            if pr.user.login in users:
                results[team].append(pr.number)
    return results

def get_weekly_closed_prs(repo, config):
    return [{"pr": pr.number} for pr in repo.get_pulls(state="closed") 
            if config["start_date"] <= pr.closed_at.strftime("%Y-%m-%d") <= config["end_date"]]

def get_large_closed_prs(repo, config):
    return [{"pr": pr.number, "files": pr.changed_files}
            for pr in repo.get_pulls(state="closed")
            if config["start_date"] <= pr.closed_at.strftime("%Y-%m-%d") <= config["end_date"] and pr.changed_files > 20]

def get_prs_with_tests(repo, config):
    prs_with_tests = []
    for pr in repo.get_pulls(state="closed"):
        if config["start_date"] <= pr.closed_at.strftime("%Y-%m-%d") <= config["end_date"]:
            if any("test" in f.filename.lower() for f in pr.get_files()):
                prs_with_tests.append({"pr": pr.number})
    return prs_with_tests

def get_total_unit_tests(repo, config):
    count = 0
    for pr in repo.get_pulls(state="closed"):
        if config["start_date"] <= pr.closed_at.strftime("%Y-%m-%d") <= config["end_date"]:
            count += sum(1 for f in pr.get_files() if "test" in f.filename.lower())
    return {"total_tests": count}
