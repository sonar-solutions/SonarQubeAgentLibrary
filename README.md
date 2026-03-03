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

**Location:** `.github/agents/SonarArchitect.agent.md`

**Quick Start:**
```
@SonarArchitect Set up SonarQube analysis for my project
```

### 🧩 Modular Skill-Based Architecture

The agent uses a shared library of **13 specialized skills** located in `.github/agents/skills/`:

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

## 🚀 Installation & Usage

GitHub Copilot Agents can be used in two ways:

### Option 1: Use Directly from This Repository (Recommended)

If you want to try the agent without adding it to your project:

1. **Clone this repository:**
   ```bash
   git clone https://github.com/your-org/SonarQubeAgentLibrary.git
   cd SonarQubeAgentLibrary
   ```

2. **Open in VS Code:**
   ```bash
   code .
   ```

3. **Use the agent:**
   - Open GitHub Copilot Chat (`Cmd+Shift+I` on macOS, `Ctrl+Shift+I` on Windows/Linux)
   - Type `@SonarArchitect` followed by your request
   - Example: `@SonarArchitect Set up SonarQube for my GitHub Actions project`

### Option 2: Copy the Agent to Your Project

To add the agent to your own project:

1. **Create the agent directory in your project:**
   ```bash
   mkdir -p .github/agents
   ```

2. **Copy the agent file and skills:**
   ```bash
   cp path/to/SonarQubeAgentLibrary/.github/agents/SonarArchitect.agent.md \
      .github/agents/

   # Copy all skill files (required for the agent to work)
   cp -r path/to/SonarQubeAgentLibrary/.github/agents/skills \
      .github/agents/
   ```

3. **Commit to your repository:**
   ```bash
   git add .github/agents/
   git commit -m "Add SonarArchitect GitHub Copilot agent"
   git push
   ```

4. **Start using the agent:**
   - Open your project in VS Code with GitHub Copilot enabled
   - Open GitHub Copilot Chat (`Cmd+Shift+I` or `Ctrl+Shift+I`)
   - Type `@SonarArchitect` followed by your request

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
