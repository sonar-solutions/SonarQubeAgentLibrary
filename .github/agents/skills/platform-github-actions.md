---
name: platform-github-actions
description: GitHub Actions integration for SonarQube Cloud and Server. Use this when setting up SonarQube analysis with GitHub Actions workflows.
---

# GitHub Actions Platform Skill

This skill provides GitHub Actions-specific documentation and guidance for SonarQube integration.

**IMPORTANT - Scope of This Skill:**
- This skill is ONLY for GitHub Actions workflow structure and platform-specific configuration
- Provides pipeline examples, workflow syntax, triggers, secrets setup, and GitHub Actions-specific features
- For scanner parameters, properties, and configuration: Refer to scanner-* skills (scanner-maven, scanner-gradle, scanner-dotnet, scanner-cli)
- Access pipeline examples from documentation, adapt scanner configuration from scanner skills

## Official Documentation

### SonarQube Cloud
- **Main Documentation**: https://docs.sonarsource.com/sonarqube-cloud/advanced-setup/ci-based-analysis/github-actions-for-sonarcloud
- **GitHub Action Repository**: https://github.com/SonarSource/sonarqube-scan-action

### SonarQube Server
- **Main Documentation**: https://docs.sonarsource.com/sonarqube-server/devops-platform-integration/github-integration/adding-analysis-to-github-actions-workflow
- **GitHub Action Repository**: https://github.com/SonarSource/sonarqube-scan-action

## Documentation Fetching Strategy

**IMPORTANT - SonarQube documentation pages require JavaScript rendering:**
SonarQube documentation pages are dynamically rendered. A raw HTTP request (curl, wget) will NOT return the actual page content.

Use your environment's browser-capable fetch tool to access these URLs (including github actions documentation pages):
- ❌ Do NOT use curl or wget for docs.sonarsource.com pages
- ✅ USE whichever tool in your environment can render JavaScript pages (e.g., web/fetch, WebFetch, url_context, or equivalent)

**Fallback Approach:**
- If working with SonarQube Cloud, first fetch from the Cloud documentation URL
- If the Cloud documentation lacks complete pipeline examples, also fetch from the Server documentation URL as a fallback
- If working with SonarQube Server, first fetch from the Server documentation URL
- If the Server documentation lacks complete pipeline examples, also fetch from the Cloud documentation URL as a fallback
- Adapt any server-specific or cloud-specific details when using fallback documentation

## GitHub Actions Implementation

### Scanner Approach Determination

Based on the project type identified in prerequisites-gathering, determine the scanner approach **before** invoking pipeline-creation:

- **Maven project** → `scanner_approach: maven` — run `mvn sonar:sonar` directly, do NOT use `sonarqube-scan-action`
- **Gradle project** → `scanner_approach: gradle` — run `./gradlew sonar` directly, do NOT use `sonarqube-scan-action`
- **.NET project** → `scanner_approach: dotnet` — run `dotnet sonarscanner` begin/build/end directly, do NOT use `sonarqube-scan-action`
- **All others (JavaScript/TypeScript/Python/PHP/Go/Ruby...)** → `scanner_approach: sonarqube-scan-action` — use `sonarsource/sonarqube-scan-action`

### When to Use SonarQube Scan Action

Use `sonarsource/sonarqube-scan-action` for **CLI scanner projects only**:
- JavaScript/TypeScript/Python/PHP/Go/Ruby (without Maven/Gradle/.NET)
- Projects that require `sonar-project.properties`
- See: scanner-cli skill for configuration
- To get the latest version use **Main Documentation** link and check in the **Setting up your workflow file** section example. Use the version used in this example. 

### Build Tool Integration

**For Maven/Gradle/.NET projects**, fetch the official docs page and use the examples in the **Configuring the build.yml file** section:
- **Maven**: `SonarScanner for Maven` example
- **Gradle**: `SonarScanner for Gradle` example
- **.NET**: `SonarScanner for .NET` example

See: https://docs.sonarsource.com/sonarqube-server/devops-platform-integration/github-integration/adding-analysis-to-github-actions-workflow

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

1. **Use latest action version**: Always access https://github.com/SonarSource/sonarqube-scan-action to check latest version
2. **Matrix builds**: Run analysis only once, not in matrix strategy
3. **Branch protection**: Don't require SonarQube check on protected branches until setup is complete

## Output Contract

After processing this skill, provide the following to pipeline-creation:

- `scanner_approach`: one of `sonarqube-scan-action`, `maven`, `gradle`, `dotnet`
- `tool_version`: latest version of `sonarsource/sonarqube-scan-action` (only when `scanner_approach` is `sonarqube-scan-action`) — fetch from Main Documentation
- `workflow_structure`:
  - Trigger branches: `main`, `master`, `develop/*`, `feature/*`
  - Pull request trigger: yes
  - Checkout: `actions/checkout@v4` with `fetch-depth: 0`
  - Cache: `~/.sonar/cache` using `actions/cache@v4`
- `required_secrets`:
  - `SONAR_TOKEN` (always)
  - `SONAR_HOST_URL` (Server only)
4. **Permissions**: Ensure workflow has necessary permissions for PR comments

## Usage Instructions

⚠️ Reminder: This skill contains docs.sonarsource.com URLs — fetch them with a browser-capable tool (NOT curl), as instructed in your agent configuration.

Create `.github/workflows/sonarqube.yml` (or the filename specified by the user) with the appropriate scanner configuration and any other files or changes required for the pipeline to work.

**For SonarArchitectGuide:** Include documentation links in responses. Explain GitHub Actions concepts when relevant.

**For SonarArchitectLight:** Do NOT include documentation links or explanations in responses.
