# Plan

## Current Goal
Optimize the SonarArchitect agent for Claude Code with a version fetching script and LLM-specific directory structure.

## Completed
- Fixed agent frontmatter (name, tools format, skill discovery)
- Created `scripts/fetch-sonar-config.py` — reduces ~120KB fetched content to ~5KB JSON
- Created `claude-code/` directory with optimized agent and skills
- Updated 4 platform skills to call the script
- Updated 3 scanner skills to reuse script output
- Updated README.md with Claude Code installation instructions
- Updated CHANGELOG.md

## Branch
`feature/claude-code-agent-optimization`

## Next Steps
- Sync claude-code/ to ~/.claude/agents/ and test in a real project
- Consider adding `permissionMode: acceptEdits` if the agent still prompts for each file change
