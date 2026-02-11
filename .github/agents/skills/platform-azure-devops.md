---
name: platform-azure-devops
description: Azure DevOps integration for SonarQube Cloud and Server. Use this when setting up SonarQube analysis with Azure Pipelines.
---

# Azure DevOps Platform Skill

This skill provides Azure DevOps-specific documentation and guidance for SonarQube integration.

## Official Documentation

### SonarQube Cloud
- **Main Documentation**: https://docs.sonarsource.com/sonarqube-cloud/advanced-setup/ci-based-analysis/azure-pipelines/adding-analysis-to-build-pipeline

### SonarQube Server
- **Main Documentation**: https://docs.sonarsource.com/sonarqube-server/devops-platform-integration/azure-devops-integration/adding-analysis-to-pipeline

## Prerequisites

**Required Extension:**
- Install **SonarQube** extension from Azure DevOps Marketplace
- Extension provides tasks: `SonarQubePrepare`, `SonarQubeAnalyze`, `SonarQubePublish`

## Scanner Selection by Language

**Use `web/fetch` to get current examples from official documentation.**

- **Java (Maven)**: Use SonarQubePrepare + Maven task + SonarQubePublish. See: scanner-maven skill
- **Java (Gradle)**: Use SonarQubePrepare + Gradle task + SonarQubePublish. See: scanner-gradle skill
- **.NET**: Use SonarQubePrepare (MSBuild mode) + build + SonarQubeAnalyze + SonarQubePublish. See: scanner-dotnet skill
- **JavaScript/TypeScript/Python/Other**: Use SonarQubePrepare (CLI mode) + SonarQubeAnalyze + SonarQubePublish. See: scanner-cli skill

Fetch examples from official documentation above to get latest task versions and configuration.

## Platform-Specific Configuration

### Service Connection Setup
1. **Location**: Project Settings → Service connections
2. Create new service connection → SonarQube
3. **Configure**:
   - Server URL: Your SonarQube URL or `https://sonarcloud.io`
   - Token: Your SonarQube token
   - Connection name: e.g., `SonarQube-Connection`
- See: devops-setup-instructions skill

### Variable Configuration (Alternative)
- **Location**: Pipelines → Library → Variable groups
- **Required variables**:
  - `SONAR_TOKEN` (mark as Secret)
  - `SONAR_HOST_URL` (Server only)
- See: security-practices skill

### Pipeline Triggers
- Configure `trigger.branches` for push events
- Configure `pr.branches` for pull request events

### Checkout Configuration
- Use `fetchDepth: 0` for full git history

## Common Configurations

### Quality Gate
The `SonarQubePublish` task automatically waits for quality gate results.

### Pull Request Decoration
Configure Azure DevOps integration in SonarQube for automatic PR decoration.

## Best Practices

1. **Use service connection**: Preferred over manual variables
2. **Fetch full history**: Always set `fetchDepth: 0`
3. **Mark secrets**: Mark `SONAR_TOKEN` as Secret
4. **Version tasks**: Use specific task versions (e.g., `@5`)
5. **Separate jobs**: Run analysis in dedicated job for clarity

## Task Versions

**Check latest versions before use:**
- Use `web/fetch` to verify current task versions in documentation
- Typical format: `SonarQubePrepare@5`, `SonarQubeAnalyze@5`, `SonarQubePublish@5`

## Usage Instructions

**For SonarArchitectGuide:**
- Include documentation links in responses
- Explain Azure DevOps concepts when relevant
- Mention service connection setup

**For SonarArchitectLight:**
- Use `web/fetch` to check latest task versions
- Update or create `azure-pipelines.yml` with appropriate scanner
- Remind users to install extension and set up service connection
- Do NOT include links in responses
