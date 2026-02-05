# 🏗️ SonarQube Agent Development Guide

This guide helps you create high-quality GitHub Copilot Chat agents for this library.

## Agent Architecture

### File Structure

GitHub Copilot agents are markdown files with a specific structure:

```markdown
# Agent Name - Tagline

## Persona
Defines who the agent is and how it communicates

## Welcome Message
First message users see

## Capabilities
What the agent can do and how

## Suggested Prompts
Example prompts to guide users

## Additional Sections
Examples, troubleshooting, etc.
```

### File Naming Convention

- **Location**: `.github/copilot-agents/`
- **Pattern**: `descriptive-name.agent.md`
- **Examples**:
  - `sonarqube-helper.agent.md` → `@sonarqube-helper`
  - `docker-expert.agent.md` → `@docker-expert`
  - `terraform-guide.agent.md` → `@terraform-guide`

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
