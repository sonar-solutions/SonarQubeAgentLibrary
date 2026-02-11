---
name: platform-github-actions
description: GitHub Actions integration for SonarQube Cloud and Server. Use this when setting up SonarQube analysis with GitHub Actions workflows.
---

# GitHub Actions Platform Skill

This skill provides GitHub Actions-specific documentation and guidance for SonarQube integration.

## Official Documentation

### SonarQube Cloud
- **Main Documentation**: https://docs.sonarsource.com/sonarqube-cloud/advanced-setup/ci-based-analysis/github-actions-for-sonarcloud
- **GitHub Action Repository**: https://github.com/SonarSource/sonarqube-scan-action

### SonarQube Server
- **Main Documentation**: https://docs.sonarsource.com/sonarqube-server/devops-platform-integration/github-integration/adding-analysis-to-github-actions-workflow
- **GitHub Action Repository**: https://github.com/SonarSource/sonarqube-scan-action

## Scanner Selection by Language

**Use `web/fetch` to get current examples from official documentation.**
### When to Use SonarQube Scan Action

**ONLY use `sonarsource/sonarqube-scan-action` for CLI scanner projects:**
- **JavaScript/TypeScript**: Projects without Maven/Gradle/.NET
- **Python**: Projects without Maven/Gradle/.NET
- **PHP, Go, Ruby, etc.**: Projects using CLI scanner
- See: scanner-cli skill for configuration

**DO NOT use scan action for:**
- **Java (Maven)**: Use `mvn sonar:sonar` command directly
- **Java (Gradle)**: Use `./gradlew sonar` command directly
- **.NET**: Use `dotnet sonarscanner` begin/build/end commands directly

### Scanner-Specific Setup- **Java (Maven)**: Use Maven plugin within workflow. See: scanner-maven skill
- **Java (Gradle)**: Use Gradle plugin within workflow. See: scanner-gradle skill
- **.NET**: Use dotnet-sonarscanner begin/build/end pattern. See: scanner-dotnet` skill
- **JavaScript/TypeScript/Python/Other**: Use `sonarsource/sonarqube-scan-action`. See: scanner-cli skill

Fetch examples from GitHub Action Repository above to get latest versions and configuration.

## Platform-Specific Configuration

### Workflow Triggers
- Configure `on.push.branches` to include target branches
- Include `on.pull_request` for PR analysis and decoration

### Secrets Configuration
- **Location**: Repository → Settings → Secrets and variables → Actions
- **Required secrets**:
  - `SONAR_TOKEN` (both Cloud and Server)
  - `SONAR_HOST_URL` (Server only)
- See: security-practices and devops-setup-instructions skills

### Checkout Configuration
- Always use `fetch-depth: 0` for full git history (accurate blame information)
- Use `actions/checkout@v4` or latest

### Caching`
- Cache `~/.sonar/cache` to speed up analysis
- Use `actions/cache@v4` or latest with appropriate cache key

## Common Configurations

### Pull Request Decoration
Automatically enabled when using GitHub integration in SonarQube Cloud/Server.

### Quality Gate Status Check
The action automatically fails the workflow if quality gate fails.

## Best Practices

1. **Use latest action version**: Always fetch from https://github.com/SonarSource/sonarqube-scan-action to check latest version
2. **Matrix builds**: Run analysis only once, not in matrix strategy
3. **Branch protection**: Don't require SonarQube check on protected branches until setup is complete
4. **Permissions**: Ensure workflow has necessary permissions for PR comments

## Usage Instructions

**For SonarArchitectGuide:**
- Include documentation links in responses
- Explain GitHub Actions concepts when relevant

**For SonarArchitectLight:**
- Use `web/fetch` to check latest action version before creating workflows
- Create `.github/workflows/sonarqube.yml` with appropriate scanner
- Do NOT include links in responses
