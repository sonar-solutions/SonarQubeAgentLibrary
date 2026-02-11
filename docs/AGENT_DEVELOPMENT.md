# 🏗️ SonarQube Agent Development Guide

This guide helps you create, customize, and maintain skill-based GitHub Copilot Chat agents for this library.

## Prerequisites

Before developing or using these agents, ensure you have:

### Required
- ✅ **VS Code** (version 1.85.0 or later)
- ✅ **GitHub Copilot** subscription (Individual, Business, or Enterprise)
- ✅ **GitHub Copilot Chat** extension installed and enabled

### Recommended VS Code Extensions
- `GitHub.copilot` - GitHub Copilot core functionality
- `GitHub.copilot-chat` - GitHub Copilot Chat interface  
- `sonarsource.sonarlint-vscode` - SonarLint for real-time code quality feedback
- `yzhang.markdown-all-in-one` - For editing agent markdown files

Install recommended extensions:
```bash
code --install-extension GitHub.copilot
code --install-extension GitHub.copilot-chat
code --install-extension sonarsource.sonarlint-vscode
code --install-extension yzhang.markdown-all-in-one
```

## Quick Start - Using Agents

### Basic Usage

1. **Open GitHub Copilot Chat:**
   - Click chat icon in Activity Bar OR
   - Press `Cmd+Shift+I` (macOS) / `Ctrl+Shift+I` (Windows/Linux)

2. **Interact with an agent:**
   ```
   @SonarArchitectLight Set up SonarQube for my project
   # or
   @SonarArchitectGuide Explain SonarQube setup for GitHub Actions
   ```

3. **Common prompts:**
   - **Action-oriented** (Light): "Set up SonarQube", "Add analysis to my workflow", "Configure for Gradle"
   - **Learning-focused** (Guide): "Explain setup", "Show documentation", "Help me understand"

## Skill-Based Agent Architecture

This library uses a **modular skill-based architecture** where:
- **Agents** define workflow and personality
- **Skills** contain reusable domain knowledge
- Multiple agents can share the same skills
- Skills can be updated independently

### Benefits
- ✅ **Maintainability**: Update once in a skill, applies to all agents
- ✅ **Consistency**: Same information across different agent personalities
- ✅ **Accuracy**: Specialized skills contain verified, up-to-date information
- ✅ **Modularity**: Easy to add new platforms or scanners without duplicating code

### Architecture Diagram
```
Agent (Persona + Workflow)
    ↓ references
Skills (Domain Knowledge)
    ├── Core Skills (detection, prerequisites, documentation)
    ├── Platform Skills (GitHub Actions, GitLab CI, Azure DevOps, Bitbucket)
    └── Scanner Skills (Gradle, Maven, .NET, CLI)
```

## Customizing Agents

You can customize agents to fit your organization's specific needs without modifying the shared skills.

### Option 1: Customize Agent Personality

**Use Case**: Same underlying logic, but different tone/workflow for your team

1. **Clone an existing agent:**
   ```bash
   cp .github/agents/SonarArchitectLight.agent.md \
      .github/agents/MyCompanySonarSetup.agent.md
   ```

2. **Edit the agent file to customize:**
   - **Persona**: Change tone, communication style, and expertise level
   - **Core Workflow**: Adjust steps, add company-specific checks
   - **Key Reminders**: Add internal guidelines or processes
   - **Examples**: Show company-specific use cases
   - **Documentation links**: Add internal wiki or docs

3. **The agent still uses shared skills:**
   - Skills remain unchanged, ensuring consistency with upstream updates
   - Agent personality is customized to your needs
   - Knowledge stays accurate and up-to-date

**Example Customization:**
```markdown
# CompanyName SonarQube Setup

## Persona
You are **CompanyName's SonarQube Expert**, implementing our internal 
standards for code quality. You follow our company's specific conventions:
- All projects must use quality gate "CompanyName-Standard"
- Naming convention: {team}-{project}-{env}
- Required plugins: sonar-css, sonar-typescript

## Core Workflow
[Keep same structure but add company-specific steps]
### 1. Analyze Project
[Use project-detection skill as normal]

### 1.5 Apply Company Standards
Check for:
- Company naming conventions
- Required quality gate configuration
- Mandatory coverage thresholds (80% minimum)
```

### Option 2: Extend with Custom Skills

**Use Case**: Add organization-specific knowledge while keeping shared skills

1. **Create organization-specific skills:**
   ```bash
   # Create custom skills directory
   mkdir -p .github/agents/skills/custom
   
   # Create custom skill
   cat > .github/agents/skills/custom/company-standards.md << 'EOF'
   # Company Standards Skill
   
   ## Purpose
   Enforce CompanyName's SonarQube configuration standards
   
   ## Quality Gate Requirements
   - Minimum coverage: 80%
   - Maximum code smells: 50
   - No critical or blocker issues
   
   ## Naming Conventions
   Project Key Format: {team}-{project}-{environment}
   Examples:
   - platform-authservice-prod
   - mobile-ios-dev
   
   ## Required Properties
   All projects must include:
   - sonar.projectKey (following naming convention)
   - sonar.qualitygate (CompanyName-Standard)
   - sonar.coverage.exclusions (test/**, mock/**)
   EOF
   ```

2. **Reference custom skill in your agent:**
   ```markdown
   ### 5. Apply Company Standards
   Use the **custom/company-standards** skill to:
   - Validate project key naming convention
   - Set quality gate to "CompanyName-Standard"
   - Configure mandatory coverage thresholds
   - Add required exclusion patterns
   ```

3. **Benefits:**
   - Shared skills get community updates automatically
   - Custom skills maintain your organization's specific requirements
   - Clear separation between universal and company-specific knowledge
   - Easy to merge upstream changes without conflicts

## Creating New Skill-Based Agents

Want to create agents for other tools or domains? Follow this modular approach.

### Step 1: Design Your Skills

1. **Identify discrete knowledge domains:**
   
   **Questions to ask:**
   - What specific expertise does your agent need?
   - Can expertise be broken into reusable skills?
   - Which skills might be shared across agents?
   - What's universal vs. what's specific to your agent?
   
   **Example for Kubernetes agent:**
   - ✅ Universal: "kubernetes-deployment" skill
   - ✅ Universal: "security-scanning" skill  
   - ✅ Universal: "aws-configuration" skill
   - ❌ Too broad: "devops" skill (break it down)

2. **Create skill files in `.github/agents/skills/`:**
   ```bash
   touch .github/agents/skills/kubernetes-deployment.md
   touch .github/agents/skills/security-scanning.md
   touch .github/agents/skills/aws-configuration.md
   ```

3. **Structure each skill with this template:**
   ```markdown
   # Skill Name
   
   ## Purpose
   What this skill provides and why it exists.
   
   ## When to Use This Skill
   Specific conditions or scenarios that trigger using this skill.
   
   ## Key Information
   
   ### Best Practices
   - Best practice 1
   - Best practice 2
   
   ### Common Patterns
   - Pattern description
   - When to use each pattern
   
   ### Platform-Specific Guidance
   **GitHub Actions:**
   - Specific guidance
   
   **GitLab CI:**
   - Specific guidance
   
   ## Important Links
   - [Official Documentation](https://example.com)
   - [Best Practices Guide](https://example.com)
   
   ## Example Usage
   Show how this skill applies in practice with a realistic scenario.
   ```

### Step 2: Create Your Agent

1. **Create agent file in `.github/agents/`:**
   ```bash
   touch .github/agents/MyAgent.agent.md
   ```

2. **Define the agent structure:**
   ```markdown
   # Agent Name - Short Tagline
   
   ## Persona
   You are **AgentName**, a [role] specializing in [domain].
   
   You have expertise in:
   - Expertise area 1
   - Expertise area 2
   - Expertise area 3
   
   Your communication style:
   - **Direct**: Get to solutions quickly
   - **Educational**: Explain the "why" behind recommendations
   - **Security-focused**: Always consider security implications
   
   ## Core Workflow
   
   ### 1. Analyze the Project
   Use the **skill-name** skill to:
   - Detect specific elements
   - Identify configuration files
   - Check for existing setup
   
   ### 2. Gather Information
   Use the **another-skill** skill to:
   - Ask for required details
   - Validate prerequisites
   
   ### 3. Provide Solution
   Use the **action-skill** skill to:
   - Create configuration
   - Apply best practices
   
   ## Key Reminders
   - Important guideline 1
   - Critical check 2
   - Security practice 3
   
   ## Example Interaction Flow
   [Show realistic conversation]
   ```

3. **Test your agent:**
   ```bash
   # Reload VS Code
   # Cmd+Shift+P → "Developer: Reload Window"
   
   # Test in Copilot Chat:
   # @MyAgent help me set up X
   ```

### Step 3: Maintain and Evolve

**Update skills independently:**
```bash
# Update a skill with new information
vim .github/agents/skills/my-skill.md

# All agents using this skill benefit immediately
# No need to update multiple agent files
```

**Track what changed:**
```bash
git log -p .github/agents/skills/my-skill.md
# See exactly what information was updated and when
```

**Share successful patterns:**
- Contribute useful skills back to this library
- Help the community benefit from your experience
- Get feedback and improvements from others

**Create agent variants:**
```
Same Skills → Different Personalities
├── ActionAgent (creates files immediately)
├── GuideAgent (explains first, creates on request)
└── AuditAgent (reviews existing setup only)
```

## File Structure and Naming

### Directory Structure
```
.github/agents/
├── AgentName.agent.md              # Agent definition
├── AnotherAgent.agent.md           # Another agent
└── skills/                         # Shared skills
    ├── core-skill.md
    ├── platform-specific.md
    └── custom/                     # Organization-specific skills
        └── company-standards.md
```

### File Naming Convention

**Agents:**
- **Location**: `.github/agents/`
- **Pattern**: `AgentName.agent.md` or `AgentName.md`
- **Examples**:
  - `SonarArchitectLight.agent.md` → `@SonarArchitectLight`
  - `DockerExpert.agent.md` → `@DockerExpert`
  - `TerraformGuide.agent.md` → `@TerraformGuide`

**Skills:**
- **Location**: `.github/agents/skills/`
- **Pattern**: `descriptive-name.md`
- **Examples**:
  - `project-detection.md`
  - `platform-github-actions.md`
  - `scanner-gradle.md`

## Key Principles

### 1. Clear Persona
Define the agent's expertise and communication style:

```markdown
## Persona
You are **AgentName**, a [Senior Role] specializing in [Domain].
You have deep expertise in [Technologies/Practices].

Your communication style is:
- **Trait 1** - Explanation
- **Trait 2** - Explanation
- **Trait 3** - Explanation
```

### 2. Actionable Capabilities
Specify what tools and approaches the agent uses:

```markdown
## Capabilities

### Analysis
Use `list_files` and `read_file` to:
- Detect project type
- Identify configuration files
- Scan dependencies

### Guidance
- Provide official documentation links
- Create step-by-step checklists
- Offer troubleshooting assistance
```

### 3. Useful Suggested Prompts
Provide 4-6 prompts that cover common use cases:

```markdown
## Suggested Prompts

1. **"Action-oriented prompt"**
   - What it does
   - Expected outcome

2. **"Another helpful prompt"**
   - Description
   - Use case
```

### 4. Reference Official Documentation
**Always** link to authoritative sources rather than providing potentially outdated code:

✅ **Good:**
```markdown
For the latest configuration, see:
- [Official Guide](https://example.com/docs)
```

❌ **Avoid:**
```markdown
Here's the YAML you need:
[hardcoded configuration that might become outdated]
```

### 5. Emphasize Security
Always highlight security best practices:

```markdown
⚠️ **Security Reminder:**
- NEVER hardcode credentials
- Use secrets management (GitHub Secrets, vault, etc.)
- Follow principle of least privilege
```

## Testing Your Agent

### 1. Local Testing

1. Create your agent file in `.github/copilot-agents/`
2. Reload VS Code: `Cmd+Shift+P` → "Developer: Reload Window"
3. Open Copilot Chat
4. Test with: `@your-agent-name test prompt`

### 2. Test Checklist

- [ ] Agent responds to its name
- [ ] Welcome message displays correctly
- [ ] All suggested prompts work
- [ ] Links are valid and current
- [ ] Persona is consistent
- [ ] Security guidance is clear
- [ ] Examples are helpful
- [ ] Grammar and spelling are correct

### 3. Test Scenarios

Test with different types of questions:
- General help: `@agent what can you help me with?`
- Specific task: `@agent [suggested prompt]`
- Troubleshooting: `@agent I'm getting error X`
- Configuration: `@agent review my setup`

## Agent Templates

### DevOps/Infrastructure Agent

```markdown
# AgentName - Infrastructure Expert

## Persona
You are **AgentName**, a Senior Infrastructure Engineer...

## Capabilities
- Detect infrastructure as code files (Terraform, CloudFormation, etc.)
- Analyze CI/CD configurations
- Provide security best practices
- Guide cloud platform integrations

## Tools
Use `list_files`, `read_file`, and `grep_search` to analyze infrastructure code.

## Suggested Prompts
1. "Analyze my infrastructure configuration"
2. "Help me set up CI/CD for my infrastructure"
3. "Review my configuration for security issues"
4. "Troubleshoot my deployment failure"
```

### Language/Framework Agent

```markdown
# AgentName - [Framework] Expert

## Persona
You are **AgentName**, a Senior [Framework] Developer...

## Capabilities
- Detect [framework] project structure
- Analyze dependencies and versions
- Suggest best practices
- Help with configuration and optimization

## Tools
Use `list_files` and `read_file` to examine project structure.

## Suggested Prompts
1. "Analyze my [framework] project structure"
2. "Help me optimize my [framework] configuration"
3. "Suggest best practices for my project"
4. "Troubleshoot [framework] issue"
```

## Best Practices

### Do's ✅

- **Be specific**: Clearly define the agent's domain expertise
- **Use tools**: Leverage `list_files`, `read_file`, `grep_search`
- **Link to docs**: Reference official, up-to-date documentation
- **Emphasize security**: Always mention secure practices
- **Provide examples**: Show typical interactions
- **Keep current**: Review and update agents regularly

### Don'ts ❌

- **Don't hardcode configs**: Avoid lengthy code blocks that become outdated
- **Don't be vague**: Clearly define what the agent can and cannot do
- **Don't duplicate**: Create agents for distinct use cases
- **Don't forget prompts**: Always include 4-6 suggested prompts
- **Don't skip testing**: Test all functionality before submitting

## Advanced Features

### Context-Aware Analysis

Use the available tools to make agents intelligent:

```markdown
1. **Analyze Project Structure**
   - Use `list_files` to scan directory structure
   - Use `read_file` to check configuration files
   - Use `grep_search` to find specific patterns

2. **Provide Tailored Guidance**
   Based on detected project type, provide specific guidance.
```

### Multi-Platform Support

Design agents to work across different platforms:

```markdown
## Platform Detection
Check for:
- `.github/workflows/` → GitHub Actions
- `.gitlab-ci.yml` → GitLab CI
- `azure-pipelines.yml` → Azure DevOps
- `Jenkinsfile` → Jenkins

Provide platform-specific guidance based on detection.
```

## Publishing Your Agent

### Pre-Submission Checklist

- [ ] Agent file named correctly: `name.agent.md`
- [ ] Located in: `.github/copilot-agents/`
- [ ] All sections complete (Persona, Welcome, Capabilities, Prompts)
- [ ] Links verified and working
- [ ] Tested locally in VS Code
- [ ] No hardcoded credentials or sensitive data
- [ ] Grammar and spelling checked
- [ ] Security guidance included

### Submission Process

1. Fork this repository
2. Create your agent file
3. Test thoroughly
4. Update main README.md to list your agent
5. Submit pull request with:
   - Clear description of the agent's purpose
   - Examples of prompts and responses
   - Any special requirements or dependencies

## Maintenance

### Keeping Agents Current

- **Review quarterly**: Check if documentation links are still valid
- **Update for new features**: Add support for new tools/platforms
- **Respond to feedback**: Address user issues and suggestions
- **Test regularly**: Ensure agents still work with latest VS Code/Copilot

### Deprecating Agents

If an agent becomes obsolete:
1. Mark as deprecated in README
2. Add deprecation notice in agent file
3. Suggest alternative agents
4. Maintain for 2 versions before removal

## Resources

### GitHub Copilot
- [GitHub Copilot Chat Documentation](https://docs.github.com/en/copilot/using-github-copilot/using-github-copilot-chat)
- [Custom Agents Guide](https://docs.github.com/en/copilot/customizing-copilot/creating-custom-copilot-agents)

### Markdown
- [Markdown Guide](https://www.markdownguide.org/)
- [GitHub Flavored Markdown](https://github.github.com/gfm/)

## Questions?

Open a discussion or contact the maintainers!

Happy agent building! 🚀
