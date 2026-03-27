# Changelog

## 2026-03-27 — Claude Code Agent Optimization

### LLM-Specific Agent Structure
- **Added `claude-code/` directory** — Contains a Claude Code-optimized variant of the agent with proper frontmatter (`name: sonar-architect`, `tools: Read, Edit, Write, Bash, Glob, Grep`) and a version fetching script.
- **Generic `agents/` preserved** — Backward compatible for GitHub Copilot users.

### Version Fetching Script (`scripts/fetch-sonar-config.py`)
- **Created Python script** — Single stdlib-only script that fetches all documentation pages, extracts YAML templates and version strings, and returns compact JSON. Reduces ~120KB of raw fetched content to ~5KB structured output (~95% token reduction).
- **Handles Cloud URL migration** — SonarSource moved Cloud docs from `advanced-setup/` to `analyzing-source-code/`; script tries both paths automatically.
- **Fetches all sources in one call** — Platform docs, scanner version JSONs, and Bitbucket pipe versions are all fetched in a single script invocation.

### Skill Updates (Claude Code variant only)
- **4 platform skills updated** — `platform-github-actions.md`, `platform-gitlab-ci.md`, `platform-azure-devops.md`, `platform-bitbucket.md` now call the script instead of raw curl commands.
- **3 scanner skills updated** — `scanner-maven.md`, `scanner-gradle.md`, `scanner-dotnet.md` now reuse the script output from the platform skill instead of fetching version JSONs separately.

### Agent Frontmatter Fixes
- **Fixed agent name** — `name: SonarArchitect` → `name: sonar-architect` (Claude Code requires lowercase with hyphens).
- **Fixed tools format** — JSON array with wrong names → comma-separated with correct names.
- **Fixed skill file discovery** — Added Glob-based discovery with common location hints.

### Files Created
- `scripts/fetch-sonar-config.py`
- `claude-code/agents/sonar-architect.agent.md`
- `claude-code/agents/scripts/fetch-sonar-config.py`
- `claude-code/agents/skills/*.md` (13 files, 7 modified)

### Files Modified
- `agents/SonarArchitect.agent.md` (frontmatter fixes only)
- `README.md` (Claude Code installation instructions)
