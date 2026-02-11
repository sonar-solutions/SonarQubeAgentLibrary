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
   - Open your project in VS Code
   - Open GitHub Copilot Chat
   - Type `@SonarArchitectLight` for action-oriented setup
   - Or type `@SonarArchitectGuide` for documentation-focused guidance

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
   @SonarArchitectLight <your question or request>
   # or
   @SonarArchitectGuide <your question or request>
   ```

3. **Use suggested prompts:**
   
   **For SonarArchitectLight (action-oriented):**
   - "Set up SonarQube for my project"
   - "Add SonarQube analysis to my GitHub Actions workflow"
   - "Configure SonarQube for my Gradle project"
   - "Create SonarQube configuration for GitLab CI"
   
   **For SonarArchitectGuide (documentation-focused):**
   - "Explain how to set up SonarQube for GitHub Actions"
   - "Show me SonarQube documentation for Gradle projects"
   - "Help me understand SonarQube Cloud vs Server setup"
   - "Guide me through configuring SonarQube secrets"

### Example Conversations

#### Setting up SonarQube with SonarArchitectLight
```
You: @SonarArchitectLight Set up SonarQube for my project

SonarArchitectLight: Let me analyze your project...
I detected:
- build.gradle (Gradle project)
- .github/workflows/ (GitHub Actions)

Is GitHub Actions correct, or would you like to use a different platform?

You: GitHub Actions is correct

SonarArchitectLight: I need a few details:
- Are you using SonarQube Cloud or Server?
- What's your project key?
- If Cloud: Organization key and instance (US/EU)?

You: Cloud, my-project, my-org, US

SonarArchitectLight:
✅ Updated build.gradle with SonarQube plugin 6.1.0.5171
✅ Created .github/workflows/sonarqube.yml

🔐 Next Steps:
1. Add SONAR_TOKEN secret in GitHub Settings
2. Generate token at https://sonarqube.us
```

#### Learning SonarQube with SonarArchitectGuide
```
You: @SonarArchitectGuide Explain SonarQube setup for Maven

SonarArchitectGuide: I detected:
- pom.xml (Maven project)
- .github/workflows/ (GitHub Actions)

Is this correct?

You: Yes

SonarArchitectGuide: Here's the official documentation for your setup:
📚 https://docs.sonarsource.com/sonarqube-cloud/...

The setup involves:
1. Adding SonarQube Maven plugin to pom.xml
2. Configuring GitHub Actions workflow
3. Setting up secrets for authentication

Would you like me to create the configuration files?
```

---

## 🏗️ Repository Structure

```
SonarQubeAgentLibrary/
├── .github/
│   └── agents/
│       ├── SonarArchitectLight.agent.md     # Action-oriented agent
│       ├── SonarArchitectGuide.agent.md     # Documentation-focused agent
│       └── skills/                          # Shared modular skills
│           ├── project-detection.md         # Project analysis
│           ├── prerequisites-gathering.md   # Info collection
│           ├── documentation-links.md       # Official docs
│           ├── pipeline-creation.md         # CI/CD file creation
│           ├── security-practices.md        # Credential security
│           ├── devops-setup-instructions.md # Secret configuration
│           ├── platform-github-actions.md   # GitHub Actions guidance
│           ├── platform-gitlab-ci.md        # GitLab CI guidance
│           ├── platform-azure-devops.md     # Azure DevOps guidance
│           ├── platform-bitbucket.md        # Bitbucket guidance
│           ├── scanner-gradle.md            # Gradle configuration
│           ├── scanner-maven.md             # Maven configuration
│           ├── scanner-dotnet.md            # .NET configuration
│           └── scanner-cli.md               # CLI scanner configuration
├── .vscode/
│   └── extensions.json                       # Recommended VS Code extensions
├── examples/
│   ├── github-actions/                       # Example workflows
│   ├── gitlab-ci/                            # Example pipelines
│   └── configurations/                       # Example sonar configs
├── docs/
│   ├── CONTRIBUTING.md                       # Contribution guidelines
│   └── AGENT_DEVELOPMENT.md                  # Agent development guide
├── LICENSE                                    # MIT License
└── README.md                                  # This file
```

---

## 🔧 Customizing Agents

You can customize agents to fit your organization's specific needs:

### Option 1: Customize Agent Personality

1. **Clone an agent file:**
   ```bash
   cp .github/agents/SonarArchitectLight.agent.md \
      .github/agents/MyCompanySonarSetup.agent.md
   ```

2. **Edit the agent file:**
   - Modify the **Persona** section to change tone and behavior
   - Update **Core Workflow** to adjust steps
   - Customize **Key Reminders** for your team's practices
   - Add company-specific guidelines or internal documentation links

3. **The agent still uses shared skills:**
   - Skills remain unchanged, ensuring consistency
   - Agent personality is customized, but knowledge stays accurate

### Option 2: Extend Skills

1. **Add organization-specific skills:**
   ```bash
   # Create a custom skill
   touch .github/agents/skills/company-standards.md
   ```

2. **Reference in agent:**
   ```markdown
   ### Additional Step
   Use the **company-standards** skill to apply:
   - Internal naming conventions
   - Required quality gate thresholds
   - Mandatory security configurations
   ```

3. **Benefits:**
   - Shared skills get community updates
   - Custom skills maintain your organization's requirements
   - Clear separation between universal and company-specific knowledge

---

## 🛠️ Creating New Agents

Want to create your own skill-based agents? Follow the modular architecture:

### Step 1: Design Your Skills

1. **Identify discrete knowledge domains:**
   - What specific expertise does your agent need?
   - Can it be broken into reusable skills?
   - Example: "Kubernetes deployment" + "Security scanning" + "AWS configuration"

2. **Create skill files in `.github/agents/skills/`:**
   ```bash
   touch .github/agents/skills/kubernetes-deployment.md
   touch .github/agents/skills/security-scanning.md
   touch .github/agents/skills/aws-configuration.md
   ```

3. **Structure each skill:**
   ```markdown
   # Skill Name
   
   ## Purpose
   What this skill provides
   
   ## When to Use
   Conditions that trigger this skill
   
   ## Key Information
   - Specific knowledge
   - Best practices
   - Common patterns
   
   ## Example Usage
   How this skill applies in practice
   ```

### Step 2: Create Your Agent

1. **Create agent file in `.github/agents/`:**
   ```bash
   touch .github/agents/MyAgent.agent.md
   ```

2. **Define the agent structure:**
   ```markdown
   # Agent Name
   
   ## Persona
   Describe role, expertise, and communication style
   
   ## Core Workflow
   ### 1. Step One
   Use the **skill-name** skill to:
   - Action 1
   - Action 2
   
   ### 2. Step Two
   Use the **another-skill** skill to:
   - Action 1
   
   ## Key Reminders
   - Important guidelines
   - Critical checks
   ```

3. **Test your agent:**
   - Reload VS Code (`Cmd+Shift+P` → "Developer: Reload Window")
   - Test with: `@MyAgent <test prompt>`
   - Verify skills are referenced correctly

### Step 3: Maintain and Evolve

- **Update skills independently** - changes propagate to all agents
- **Version control skills** - track what changed and when
- **Share successful skills** - contribute back to the community
- **Create agent variants** - same skills, different personalities

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
