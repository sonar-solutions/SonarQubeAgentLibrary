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
- Access pipeline examples from documentation, adapt scanner configuration from scanner skills

## Official Documentation

### SonarQube Cloud
- **Main Documentation**: https://docs.sonarsource.com/sonarqube-cloud/advanced-setup/ci-based-analysis/azure-pipelines/adding-analysis-to-build-pipeline

### SonarQube Server
- **Main Documentation**: https://docs.sonarsource.com/sonarqube-server/devops-platform-integration/azure-devops-integration/adding-analysis-to-pipeline

## Documentation Fetching Strategy

**IMPORTANT - SonarQube documentation pages require JavaScript rendering:**
SonarQube documentation pages are dynamically rendered. A raw HTTP request (curl, wget) will NOT return the actual page content.

Use your environment's browser-capable fetch tool to access these URLs:
- ❌ Do NOT use curl or wget for docs.sonarsource.com pages
- ✅ USE whichever tool in your environment can render JavaScript pages (e.g., web/fetch, WebFetch, url_context, or equivalent)

**Fallback Approach:**
- If working with SonarQube Cloud, first fetch from the Cloud documentation URL
- If the Cloud documentation lacks complete pipeline examples, also fetch from the Server documentation URL as a fallback
- If working with SonarQube Server, first fetch from the Server documentation URL
- If the Server documentation lacks complete pipeline examples, also fetch from the Cloud documentation URL as a fallback
- Adapt any server-specific or cloud-specific details when using fallback documentation

## Azure DevOps Implementation

## Prerequisites

**Required Extension:**
- Install **SonarQube** extension from Azure DevOps Marketplace
- Extension provides tasks: `SonarQubePrepare`, `SonarQubeAnalyze`, `SonarQubePublish`, `SonarCloudPrepare`, `SonarCloudAnalyze`, `SonarCloudPublish`

### Scanner Approach Determination

Based on the project type identified in prerequisites-gathering, determine the scanner mode **before** invoking pipeline-creation. Azure DevOps uses SonarQube extension tasks for ALL project types — the mode passed to `SonarQubePrepare` determines how the scanner runs:

- **Maven project** → `scanner_approach: maven` — `SonarQubePrepare` in Maven mode + Maven task + `SonarQubePublish`
- **Gradle project** → `scanner_approach: gradle` — `SonarQubePrepare` in Gradle mode + Gradle task + `SonarQubePublish`
- **.NET project** → `scanner_approach: dotnet` — `SonarQubePrepare` in MSBuild mode + build task + `SonarQubeAnalyze` + `SonarQubePublish`
- **All others (JavaScript/TypeScript/Python/PHP/Go/Ruby...)** → `scanner_approach: cli` — `SonarQubePrepare` in CLI mode + `SonarQubeAnalyze` + `SonarQubePublish`

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

## Processing Steps

**Execute these steps in order before handing off to pipeline-creation:**

1. Determine `scanner_approach` from the project type (see Scanner Approach Determination above)
2. ⛔ STOP — Fetch the **Main Documentation** URL and extract the latest version numbers for `SonarQubePrepare`, `SonarQubeAnalyze`, and `SonarQubePublish` tasks (applies to ALL scanner approaches — Azure DevOps always uses extension tasks). Do NOT proceed until these versions are known.
3. Collect pipeline structure details (triggers, checkout, service connection) per Platform-Specific Configuration section above
4. List required secrets/variables based on SonarQube type (Cloud vs Server)
5. Pass all collected values to pipeline-creation via the Output Contract below

## Output Contract

After processing this skill, provide the following to pipeline-creation:

- `scanner_approach`: one of `maven`, `gradle`, `dotnet`, `cli`
- `tool_version`: version numbers for `SonarQubePrepare`, `SonarQubeAnalyze`, `SonarQubePublish` tasks — **must be fetched in Processing Steps above before reporting**
- `workflow_structure`:
  - Trigger branches and PR config
  - Checkout: `fetchDepth: 0`
  - Service connection name
- `required_secrets`:
  - Service connection configured in Project Settings (always)
  - `SONAR_TOKEN` as pipeline variable (alternative if no service connection)
  - `SONAR_HOST_URL` (Server only)
- `reference_docs`: documentation URLs fetched during processing — for use by pipeline-creation if additional detail is needed:
  - SonarQube Cloud: https://docs.sonarsource.com/sonarqube-cloud/advanced-setup/ci-based-analysis/azure-pipelines/adding-analysis-to-build-pipeline
  - SonarQube Server: https://docs.sonarsource.com/sonarqube-server/devops-platform-integration/azure-devops-integration/adding-analysis-to-pipeline

## Usage Instructions

**For SonarArchitectGuide:**
- Include documentation links in responses
- Explain Azure DevOps concepts when relevant
- Mention service connection setup

**For SonarArchitectLight:**
- Use a browser-capable fetch tool to check latest task versions in official documentation
- Update or create `azure-pipelines.yml` with appropriate scanner
- Remind users to install extension and set up service connection
- Do NOT include links in responses
