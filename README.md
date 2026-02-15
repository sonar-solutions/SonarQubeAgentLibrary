# 🤖 GitHub Copilot Agents Library [Unofficial/Experimental]

A **unofficial** and **experimental** collection of specialized agents designed to accelerate your development workflow. These agents provide expert-level assistance for specific domains like DevOps, CI/CD, and code quality automation.

## 📚 Available Agents

This library provides two specialized SonarQube integration agents, each optimized for different workflow preferences:

### 🏗️ SonarArchitectLight - Action-Oriented SonarQube Expert

**Persona:** Direct and efficient action-taker that creates configuration files immediately

**Best For:**
- Users who want quick, automatic setup
- Teams that prefer implementation over explanation
- Fast prototyping and getting started quickly

**Workflow:**
1. Detects your project and CI/CD platform
2. Asks essential prerequisites (SonarQube type, project key, organization)
3. Creates all configuration files directly with latest versions
4. Provides concise next steps for secrets configuration

**Location:** `.github/agents/SonarArchitectLight.agent.md`

**Quick Start:**
```
@SonarArchitectLight Set up SonarQube analysis for my project
```

### 📖 SonarArchitectGuide - Documentation-Focused SonarQube Expert

**Persona:** Educational guide that prioritizes official documentation and learning

**Best For:**
- Users who want to understand what they're configuring
- Teams learning SonarQube for the first time
- Organizations that need to customize configurations

**Workflow:**
1. Detects your project and CI/CD platform
2. Asks essential prerequisites
3. Provides links to official SonarQube documentation
4. Creates configuration files when requested
5. Explains concepts and best practices

**Location:** `.github/agents/SonarArchitectGuide.agent.md`

**Quick Start:**
```
@SonarArchitectGuide Help me understand SonarQube analysis setup for GitHub Actions for my project
```

### 🧩 Modular Skill-Based Architecture

Both agents use a shared library of **13 specialized skills** located in `.github/agents/skills/`:

**Core Skills:**
- `project-detection.md` - Detects project type, build system, and CI/CD platform
- `prerequisites-gathering.md` - Collects required information efficiently
- `documentation-links.md` - Provides official SonarQube documentation URLs
- `pipeline-creation.md` - Creates CI/CD workflow files with latest versions
- `security-practices.md` - Ensures secure credential management
- `devops-setup-instructions.md` - Platform-specific secret configuration steps

**Platform Skills:**
- `platform-github-actions.md` - GitHub Actions specific guidance
- `platform-gitlab-ci.md` - GitLab CI specific guidance
- `platform-azure-devops.md` - Azure DevOps specific guidance
- `platform-bitbucket.md` - Bitbucket Pipelines specific guidance

**Scanner Skills:**
- `scanner-gradle.md` - Gradle project configuration
- `scanner-maven.md` - Maven project configuration
- `scanner-dotnet.md` - .NET project configuration
- `scanner-cli.md` - CLI scanner for JS/TS/Python/other languages

**Benefits of Skill-Based Design:**
- ✅ **Maintainability**: Update once in a skill, applies to all agents
- ✅ **Consistency**: Same information across different agent personalities
- ✅ **Accuracy**: Specialized skills contain verified, up-to-date information
- ✅ **Modularity**: Easy to add new platforms or scanners without duplicating code

---

## 🚀 Installation & Usage

GitHub Copilot Agents can be used in two ways:

### Option 1: Use Directly from This Repository (Recommended)

If you want to try these agents without adding them to your project:

1. **Clone this repository:**
   ```bash
   git clone https://github.com/your-org/SonarQubeAgentLibrary.git
   cd SonarQubeAgentLibrary
   ```

2. **Open in VS Code:**
   ```bash
   code .
   ```

3. **Use the agents:**
   - Open GitHub Copilot Chat (`Cmd+Shift+I` on macOS, `Ctrl+Shift+I` on Windows/Linux)
   - Reference an agent by typing `@` followed by the agent name
   - Example: `@SonarArchitectLight help me set up SonarQube for GitHub Actions`

### Option 2: Copy Agents to Your Project

To add these agents to your own project:

1. **Create the agent directory in your project:**
   ```bash
   mkdir -p .github/agents
   ```

2. **Copy the agent files and skills you need:**
   ```bash
   # Copy both agents (or choose one)
   cp path/to/SonarQubeAgentLibrary/.github/agents/SonarArchitectLight.agent.md \
      .github/agents/
   cp path/to/SonarQubeAgentLibrary/.github/agents/SonarArchitectGuide.agent.md \
      .github/agents/
   
   # Copy all skill files (required for agents to work)
   cp -r path/to/SonarQubeAgentLibrary/.github/agents/skills \
      .github/agents/
   ```

3. **Commit to your repository:**
   ```bash
   git add .github/agents/
   git commit -m "Add GitHub Copilot agents"
   git push
   ```

4. **Start using the agents:**
   - Open your project in VS Code with GitHub Copilot enabled
   - Open GitHub Copilot Chat (`Cmd+Shift+I` or `Ctrl+Shift+I`)
   - Type `@SonarArchitectLight` or `@SonarArchitectGuide` followed by your request

> **Prerequisites:** VS Code 1.85.0+, GitHub Copilot subscription, GitHub Copilot Chat extension

---

## 🤝 Contributing

Want to improve these agents or create new ones? See [AGENT_DEVELOPMENT.md](docs/AGENT_DEVELOPMENT.md) for:
- How to customize agents for your organization
- Creating new skill-based agents
- Development guidelines and best practices

Contributions welcome! Report bugs, suggest features, or submit PRs.

---

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

---

**Happy Coding! 🚀**
