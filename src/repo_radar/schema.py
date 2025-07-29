def get_tool_schemas():
    queries = [
        ("get_failing_checkall_tests", "Failures in checkall test run."),
        ("get_closed_prs_with_test_failures", "Closed PRs with failed checks."),
        ("get_non_main_branch_prs", "PRs targeting non-main branches."),
        ("get_old_open_prs", "Open PRs older than 1 week."),
        ("get_weekly_open_prs_per_team", "Open PRs per team."),
        ("get_weekly_closed_prs", "Closed PRs in timeframe."),
        ("get_large_closed_prs", "Closed PRs with >20 files."),
        ("get_prs_with_tests", "Closed PRs with unit tests."),
        ("get_total_unit_tests", "Total unit test files in timeframe.")
    ]

    return [{
        "type": "function",
        "function": {
            "name": name,
            "description": desc,
            "parameters": {
                "type": "object",
                "properties": {
                    "start_date": {"type": "string"},
                    "end_date": {"type": "string"},
                    "teams": {
                        "type": "object",
                        "additionalProperties": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    }
                },
                "required": ["start_date", "end_date", "teams"]
            }
        }
    } for name, desc in queries]
