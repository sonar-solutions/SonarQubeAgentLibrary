# 🤖 GitHub Copilot Agents Library [Unofficial/Experimental]

A **unofficial** and **experimental** collection of specialized agents designed to accelerate your development workflow. These agents provide expert-level assistance for specific domains like DevOps, CI/CD, and code quality automation.

## 📚 Available Agents

### 🏗️ SonarArchitect — SonarQube Integration Expert

**Persona:** Direct and efficient DevOps automation specialist that creates SonarQube pipeline configurations directly and efficiently.

**What it does:**
1. Detects your project structure and CI/CD platform
2. Gathers required prerequisites (SonarQube type, project key, organization)
3. Fetches current tool versions directly from official documentation
4. Creates all configuration files with correct, up-to-date values
5. Provides concise next steps for secrets configuration

**Source locations in this repo:**
- `agents/SonarArchitect.copilot_version.md` — Generic agent (GitHub Copilot compatible)
- `agents/sonar-architect.md` — Claude Code optimized (includes version fetching script)

**Quick Start (after installation):**
```
@SonarArchitect Set up SonarQube analysis for my project     # GitHub Copilot
@sonar-architect Set up SonarQube analysis for my project     # Claude Code
```

### 🧩 Modular Skill-Based Architecture

The agent uses a shared library of **13 specialized skills** located in `agents/skills/`:

**Core Skills:**
- `project-detection.md` - Detects project type, build system, and CI/CD platform
- `prerequisites-gathering.md` - Collects required information efficiently
- `pipeline-creation.md` - Creates CI/CD workflow files from resolved Output Contracts
- `security-practices.md` - Ensures secure credential management
- `devops-setup-instructions.md` - Platform-specific secret configuration steps

**Platform Skills:**
- `platform-github-actions.md` - GitHub Actions: determines scanner approach, fetches versions, produces Output Contract
- `platform-gitlab-ci.md` - GitLab CI: determines scanner approach, fetches versions, produces Output Contract
- `platform-azure-devops.md` - Azure DevOps: determines scanner approach, fetches versions, produces Output Contract
- `platform-bitbucket.md` - Bitbucket Pipelines: determines scanner approach, fetches versions, produces Output Contract

**Scanner Skills:**
- `scanner-gradle.md` - Gradle: fetches plugin version, verifies build file, produces Output Contract
- `scanner-maven.md` - Maven: fetches plugin version, verifies pom.xml, produces Output Contract
- `scanner-dotnet.md` - .NET: fetches scanner version, produces Output Contract
- `scanner-cli.md` - CLI scanner for JS/TS/Python and other languages, produces Output Contract

**Benefits of Skill-Based Design:**
- ✅ **Maintainability**: Update once in a skill, applies to all agents
- ✅ **Accuracy**: Skills fetch current versions directly from official documentation
- ✅ **Modularity**: Easy to add new platforms or scanners without duplicating logic
- ✅ **Traceability**: Output Contracts provide a clear, auditable handoff between skills

---

## 🚀 Installation

### Claude Code (plugin install — recommended)

This repository is a Claude Code plugin with a built-in marketplace. Two commands and you're done:

```
/plugin marketplace add sonar-solutions/SonarQubeAgentLibrary
/plugin install sonar-architect@sonar-solutions
```

Or install manually for project-level or global use:

```bash
# Project-level (committed to your repo, shared with your team)
mkdir -p /path/to/your-project/.claude/agents/scripts
cp -r agents/* /path/to/your-project/.claude/agents/
cp scripts/fetch-sonar-config.py /path/to/your-project/.claude/agents/scripts/

# Global (available in all your projects)
mkdir -p ~/.claude/agents/scripts
cp -r agents/* ~/.claude/agents/
cp scripts/fetch-sonar-config.py ~/.claude/agents/scripts/
```

Then invoke:
```
@sonar-architect Set up SonarQube for my project
```

> **Prerequisites:** Python 3.6+ (for the version fetching script)

---

### GitHub Copilot (manual install)

```bash
git clone https://github.com/sonar-solutions/SonarQubeAgentLibrary.git
mkdir -p /path/to/your-project/.github/agents
cp SonarQubeAgentLibrary/agents/SonarArchitect.copilot_version.md \
   /path/to/your-project/.github/agents/
cp -r SonarQubeAgentLibrary/agents/skills \
   /path/to/your-project/.github/agents/
```

Commit and invoke:
```
@SonarArchitect Set up SonarQube for my project
```

> **Prerequisites:** VS Code 1.85.0+, GitHub Copilot subscription, GitHub Copilot Chat extension

---

## 🤝 Contributing

Want to improve this agent or create new ones? See [AGENT_DEVELOPMENT.md](docs/AGENT_DEVELOPMENT.md) for:
- How to customize the agent for your organization
- Creating new skill-based agents
- Development guidelines and best practices

Contributions welcome! Report bugs, suggest features, or submit PRs.

---

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

---

**Happy Coding! 🚀**
