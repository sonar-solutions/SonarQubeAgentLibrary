# 🤖 GitHub Copilot Agents Library

A curated collection of specialized agents designed to accelerate your development workflow. These agents provide expert-level assistance for specific domains like DevOps, CI/CD, and code quality automation.

## 📚 Available Agents

### 🏗️ SonarArchitect - SonarQube Integration Expert

**Expertise:** SonarQube setup, CI/CD integration, code quality automation

**Use Cases:**
- Setting up SonarQube for GitHub Actions, GitLab CI, or Azure DevOps
- Configuring code quality gates and coverage reports
- Troubleshooting scanner issues
- Implementing secure credential management
- Code quality best practices

**Location:** `.github/agents/sonarqube-helper.agent.md`

**Quick Start:**
```
@sonarqube-helper Analyze my project and recommend SonarQube setup
```

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
   - Example: `@sonarqube-helper help me set up SonarQube for GitHub Actions`

### Option 2: Copy Agents to Your Project

To add these agents to your own project:

1. **Create the agent directory in your project:**
   ```bash
   mkdir -p .github/agents
   ```

2. **Copy the agent file(s) you need:**
   ```bash
   # Copy SonarArchitect agent
   cp path/to/SonarQubeAgentLibrary/.github/agents/sonarqube-helper.agent.md \
      .github/agents/
   ```

3. **Commit to your repository:**
   ```bash
   git add .github/agents/
   git commit -m "Add GitHub Copilot agents"
   git push
   ```

4. **Start using the agent:**
   - Open your project in VS Code
   - Open GitHub Copilot Chat
   - Type `@sonarqube-helper` to interact with the agent

---

## 📋 Prerequisites

Before using these agents, ensure you have:

### Required
- ✅ **VS Code** (version 1.85.0 or later)
- ✅ **GitHub Copilot** subscription (Individual, Business, or Enterprise)
- ✅ **GitHub Copilot Chat** extension installed and enabled

### Recommended VS Code Extensions
- `GitHub.copilot` - GitHub Copilot core functionality
- `GitHub.copilot-chat` - GitHub Copilot Chat interface
- `sonarsource.sonarlint-vscode` - SonarLint for real-time code quality feedback
- `yzhang.markdown-all-in-one` - For editing agent markdown files

Install recommended extensions automatically:
```bash
code --install-extension GitHub.copilot
code --install-extension GitHub.copilot-chat
code --install-extension sonarsource.sonarlint-vscode
code --install-extension yzhang.markdown-all-in-one
```

---

## 🎯 How to Use Agents

### Basic Interaction

1. **Open GitHub Copilot Chat:**
   - Click the chat icon in the Activity Bar (left sidebar)
   - Or use keyboard shortcut: `Cmd+Shift+I` (macOS) / `Ctrl+Shift+I` (Windows/Linux)

2. **Mention the agent:**
   ```
   @sonarqube-helper <your question or request>
   ```

3. **Use suggested prompts:**
   Each agent provides suggested prompts to help you get started. For SonarArchitect:
   - "Analyze my project and recommend SonarQube setup"
   - "Help me set up SonarQube for GitHub Actions"
   - "Review my SonarQube configuration for security issues"
   - "Troubleshoot my SonarQube scanner failure"

### Example Conversations

#### Setting up SonarQube for a new project
```
You: @sonarqube-helper I need to add SonarQube analysis to my Node.js project

SonarArchitect: Let me analyze your project structure first...
[Scans your repository]
I can see you have a Node.js project with GitHub Actions. Here's how to set up SonarQube...
[Provides step-by-step guidance with official documentation links]
```

#### Troubleshooting
```
You: @sonarqube-helper My SonarQube scan is failing with "Unrecognized option: --define"

SonarArchitect: This error typically occurs when using an incompatible scanner version...
[Analyzes your configuration and provides solutions]
```

---

## 🏗️ Repository Structure

```
SonarQubeAgentLibrary/
├── .github/
│   └── copilot-agents/
│       └── sonarqube-helper.agent.md    # SonarArchitect agent definition
├── .vscode/
│   └── extensions.json                   # Recommended VS Code extensions
├── examples/
│   ├── github-actions/                   # Example GitHub Actions workflows
│   ├── gitlab-ci/                        # Example GitLab CI configurations
│   └── configurations/                   # Example sonar-project.properties files
├── docs/
│   ├── CONTRIBUTING.md                   # How to contribute new agents
│   └── AGENT_DEVELOPMENT.md              # Agent development guide
└── README.md                             # This file
```

---

## 🔧 Customizing Agents

You can customize agents to fit your organization's specific needs:

1. **Clone the agent file:**
   ```bash
   cp .github/copilot-agents/sonarqube-helper.agent.md \
      .github/copilot-agents/my-custom-agent.agent.md
   ```

2. **Edit the agent file:**
   - Modify the **Persona** section to change behavior
   - Update **Capabilities** to add/remove features
   - Customize **Suggested Prompts** for your use cases
   - Add company-specific guidelines or links

3. **Rename for your organization:**
   - The agent handle is based on the filename
   - `sonarqube-helper.agent.md` → `@sonarqube-helper`
   - `my-company-devops.agent.md` → `@my-company-devops`

---

## 🛠️ Creating New Agents

Want to create your own agents? Follow these steps:

1. **Create a new `.md` file** in `.github/copilot-agents/`
2. **Follow the agent structure:**
   ```markdown
   # Agent Name
   
   ## Persona
   Describe the agent's role, expertise, and communication style
   
   ## Welcome Message
   First message users see when invoking the agent
   
   ## Capabilities
   What the agent can do (tools it uses, analysis it performs)
   
   ## Suggested Prompts
   4-6 example prompts to help users get started
   
   ## Example Interactions
   Show typical conversations
   ```

3. **Test your agent:**
   - Reload VS Code window (`Cmd+Shift+P` → "Developer: Reload Window")
   - Open Copilot Chat and type `@your-agent-name`

4. **Share with the community:**
   - Submit a pull request to this repository
   - Help others benefit from your expertise!

---

## 📖 Additional Resources

### GitHub Copilot Documentation
- [GitHub Copilot Overview](https://docs.github.com/en/copilot)
- [Using GitHub Copilot Chat](https://docs.github.com/en/copilot/using-github-copilot/asking-github-copilot-questions-in-your-ide)
- [GitHub Copilot Chat Agents](https://docs.github.com/en/copilot/customizing-copilot/creating-custom-copilot-agents)

### SonarQube Resources
- [SonarQube Documentation](https://docs.sonarsource.com/sonarqube/latest/)
- [SonarQube CI/CD Integration](https://docs.sonarsource.com/sonarqube/latest/devops-platform-integration/github-actions/)
- [SonarLint for VS Code](https://www.sonarsource.com/products/sonarlint/features/visual-studio-code/)

---

## 🤝 Contributing

We welcome contributions! Whether you want to:
- 🐛 Report a bug in an agent
- 💡 Suggest a new agent idea
- 🔧 Improve existing agents
- 📝 Enhance documentation

Please see [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

---

## 📄 License

This repository is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## 🙋 Support

### Getting Help
- **Issues with agents:** Open an issue in this repository
- **GitHub Copilot questions:** Visit [GitHub Support](https://support.github.com/)
- **SonarQube questions:** Visit [SonarSource Community](https://community.sonarsource.com/)

### Feedback
We'd love to hear how you're using these agents! Share your experience:
- ⭐ Star this repository if you find it useful
- 💬 Open a discussion to share use cases
- 🐦 Tweet about your experience with #GitHubCopilot

---

## 🎉 Acknowledgments

Special thanks to:
- The GitHub Copilot team for enabling custom agents
- SonarSource for comprehensive CI/CD documentation
- The DevOps community for sharing best practices

---

**Happy Coding! 🚀**

*Built with ❤️ for the developer community*
