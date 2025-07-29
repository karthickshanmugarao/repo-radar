from .queries import *

def run_queries(config: dict, repo):
    return {
        "tests_failing_checkall": get_failing_checkall_tests(repo, config),
        "closed_prs_with_test_failures": get_closed_prs_with_test_failures(repo, config),
        "non_main_branch_prs": get_non_main_branch_prs(repo, config),
        "old_open_prs": get_old_open_prs(repo, config),
        "weekly_open_prs_per_team": get_weekly_open_prs_per_team(repo, config),
        "weekly_closed_prs": get_weekly_closed_prs(repo, config),
        "large_closed_prs": get_large_closed_prs(repo, config),
        "prs_with_tests": get_prs_with_tests(repo, config),
        "total_unit_tests": get_total_unit_tests(repo, config)
    }
