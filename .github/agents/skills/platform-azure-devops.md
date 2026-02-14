---
name: platform-azure-devops
description: Azure DevOps integration for SonarQube Cloud and Server. Use this when setting up SonarQube analysis with Azure Pipelines.
---

# Azure DevOps Platform Skill

This skill provides Azure DevOps-specific documentation and guidance for SonarQube integration.

**IMPORTANT - Scope of This Skill:**
- This skill is ONLY for Azure Pipelines structure and platform-specific configuration
- Provides pipeline examples, task syntax, triggers, service connections, and Azure DevOps-specific features
- For scanner parameters, properties, and configuration: Refer to scanner-* skills (scanner-maven, scanner-gradle, scanner-dotnet, scanner-cli)
- Fetch pipeline examples from documentation, adapt scanner configuration from scanner skills

## Official Documentation

### SonarQube Cloud
- **Main Documentation**: https://docs.sonarsource.com/sonarqube-cloud/advanced-setup/ci-based-analysis/azure-pipelines/adding-analysis-to-build-pipeline

### SonarQube Server
- **Main Documentation**: https://docs.sonarsource.com/sonarqube-server/devops-platform-integration/azure-devops-integration/adding-analysis-to-pipeline

## Prerequisites

**Required Extension:**
- Install **SonarQube** extension from Azure DevOps Marketplace
- Extension provides tasks: `SonarQubePrepare`, `SonarQubeAnalyze`, `SonarQubePublish`

## Documentation Fetching Strategy

**Use `web/fetch` to get current examples and versions from official documentation.**

**Fallback Approach:**
- If working with SonarQube Cloud, first fetch from the Cloud documentation URL
- If the Cloud documentation lacks complete pipeline examples, also fetch from the Server documentation URL as a fallback
- If working with SonarQube Server, first fetch from the Server documentation URL
- If the Server documentation lacks complete pipeline examples, also fetch from the Cloud documentation URL as a fallback
- Adapt any server-specific or cloud-specific details when using fallback documentation

## Azure DevOps Implementation

### Scanner Implementation

**Scanner selection is defined in pipeline-creation skill. This section covers Azure DevOps-specific implementation.**

**IMPORTANT: Azure DevOps uses SonarQube extension tasks for ALL project types.**
The extension tasks adapt based on the scanner mode selected:

### Extension Task Pattern

All scanners use the same task pattern with different modes:

1. **Maven Projects**
   - `SonarQubePrepare` (scanner mode: Maven) + Maven task + `SonarQubePublish`
   - See: scanner-maven skill

2. **Gradle Projects**
   - `SonarQubePrepare` (scanner mode: Gradle) + Gradle task + `SonarQubePublish`
   - See: scanner-gradle skill

3. **.NET Projects**
   - `SonarQubePrepare` (scanner mode: MSBuild) + build task + `SonarQubeAnalyze` + `SonarQubePublish`
   - See: scanner-dotnet skill

4. **CLI Scanner Projects** (JavaScript/TypeScript/Python/Other)
   - `SonarQubePrepare` (scanner mode: CLI) + `SonarQubeAnalyze` + `SonarQubePublish`
   - Extension handles scanner installation and execution
   - See: scanner-cli skill

Fetch examples from official documentation to get latest task versions and configuration.

## Platform-Specific Configuration

### Service Connection Setup
1. **Location**: Project Settings → Service connections
2. Create new service connection → SonarQube
3. **Configure**:
   - Server URL: Your SonarQube URL or `https://sonarcloud.io` (EU) / `https://sonarqube.us` (US)
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
