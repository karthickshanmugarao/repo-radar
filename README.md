# RepoRadar 🛰️

**RepoRadar** is a GitHub Pull Request audit and analytics toolkit built with Python.

It can be run in two modes:
- ✅ **Standalone** CLI-based audit with simple config input.
- 🤖 **LLM-integrated** server (via MCP protocol) for natural language-driven code review analytics.

---

## 🔧 Features

- 📊 Pull request insights by team, author, or date range
- ✅ Track test failures, large PRs, non-main merges
- 🧠 LLM integration (e.g., GPT-4o / o3-mini) via MCP (Model Context Protocol)
- 📁 Output as JSON or Markdown
- 🔌 GitHub API (via `PyGithub`)
- ⚙️ Designed for CI, cron, or local use

---

## 📦 How to Install and Use
1. Install using the below command
```bash
pip install repo-radar
```
2. Copy and use the example json to include required configurations.
config.example.json at repo_radar/examples
3. Run the CLI by passing the config.json path
```bash
repo-radar-config-audit --config path/to/config.json
```

### ⬇️ To Contribute: Clone the repository and install the dependencies as follows:

```bash
git clone https://github.com/karthickshanmugarao/repo-radar.git
cd repo-radar
pip install uv
uv pip install .
