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

## 📦 Installation

### ⬇️ Clone and install dependencies:

```bash
git clone https://github.com/karthickshanmugarao/repo-radar.git
cd repo-radar
pip install -r requirements.txt
