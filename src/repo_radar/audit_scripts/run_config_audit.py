# scripts/run_config_audit.py

import argparse
import json
from repo_radar.github_client import get_repo
from repo_radar.audit_runner import run_queries

def save_output(results, config):
    output_format = config.get("output_format", "json")
    output_path = config.get("output_path", f"audit_output.{output_format}")

    if output_format == "json":
        with open(output_path, "w") as f:
            json.dump(results, f, indent=2)
    elif output_format == "markdown":
        with open(output_path, "w") as f:
            for key, value in results.items():
                f.write(f"## {key.replace('_', ' ').title()}\n")
                f.write("```\n")
                f.write(json.dumps(value, indent=2))
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
    print("🔍 Running audit...")
    results = run_queries(config, repo)
    save_output(results, config)


if __name__ == "__main__":
    main()
