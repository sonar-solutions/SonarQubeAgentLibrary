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

**Source location in this repo:** `agents/SonarArchitect.agent.md`

**Quick Start (after installation):**
```
@SonarArchitect Set up SonarQube analysis for my project
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

Copy the agent files into your project's agent directory. The destination depends on your AI assistant:

| AI assistant | Agent directory |
|---|---|
| GitHub Copilot | `.github/agents/` |
| Claude Code | `.claude/agents/` |
| Other | Check your platform's documentation |

### Steps

1. **Clone or download this repository:**
   ```bash
   git clone https://github.com/sonar-solutions/SonarQubeAgentLibrary.git
   ```

2. **Copy the agent and skills into your project:**

   **GitHub Copilot:**
   ```bash
   mkdir -p /path/to/your-project/.github/agents
   cp SonarQubeAgentLibrary/agents/SonarArchitect.agent.md \
      /path/to/your-project/.github/agents/
   cp -r SonarQubeAgentLibrary/agents/skills \
      /path/to/your-project/.github/agents/
   ```

   **Claude Code:**
   ```bash
   mkdir -p /path/to/your-project/.claude/agents
   cp SonarQubeAgentLibrary/agents/SonarArchitect.agent.md \
      /path/to/your-project/.claude/agents/
   cp -r SonarQubeAgentLibrary/agents/skills \
      /path/to/your-project/.claude/agents/
   ```

3. **Commit to your repository:**
   ```bash
   git add .github/agents/   # or .claude/agents/
   git commit -m "Add SonarArchitect agent"
   git push
   ```

4. **Open your project and start the agent:**
   ```
   @SonarArchitect Set up SonarQube for my project
   ```

> **GitHub Copilot prerequisites:** VS Code 1.85.0+, GitHub Copilot subscription, GitHub Copilot Chat extension

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
