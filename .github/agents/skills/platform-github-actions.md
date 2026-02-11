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

## GitHub Actions Implementation

**Use `web/fetch` to get current examples and versions from official documentation.**

### Scanner Implementation

**Scanner selection is defined in pipeline-creation skill. This section covers GitHub Actions-specific implementation.**

### When to Use SonarQube Scan Action

Use `sonarsource/sonarqube-scan-action` for **CLI scanner projects only**:
- JavaScript/TypeScript/Python/PHP/Go/Ruby (without Maven/Gradle/.NET)
- Projects that require `sonar-project.properties`
- See: scanner-cli skill for configuration

**Example:**
```yaml
- uses: sonarsource/sonarqube-scan-action@v7  # Check latest version
  env:
    SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

### Build Tool Integration

**For Maven/Gradle/.NET projects, run scanner commands directly in workflow:**
- **Maven**: Run `mvn sonar:sonar` (see: scanner-maven skill)
- **Gradle**: Run `./gradlew sonar` (see: scanner-gradle skill)
- **.NET**: Run `dotnet sonarscanner begin/build/end` (see: scanner-dotnet skill)

Fetch examples from official documentation to get latest versions and configuration.

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
