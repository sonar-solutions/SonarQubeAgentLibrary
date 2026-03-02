---
name: platform-azure-devops
description: Azure DevOps integration for SonarQube Cloud and Server. Determines scanner approach, fetches current task versions from documentation, and produces an Output Contract for pipeline-creation.
---

# Azure DevOps Platform Skill

## IMPORTANT — Scope

This skill is responsible for:
1. **Determining** the scanner approach for Azure DevOps based on build system
2. **Fetching** current task versions from official documentation
3. **Producing** a complete Output Contract before pipeline-creation runs

This skill does **not** explain concepts or include documentation links in responses. It acts.

## Prerequisites

The **SonarQube extension** must be installed from the Azure DevOps Marketplace before the pipeline can run. This provides the `SonarQubePrepare`, `SonarQubeAnalyze`, and `SonarQubePublish` tasks.

## Official Documentation

| SonarQube Type | Documentation URL |
|---|---|
| Cloud | `https://docs.sonarsource.com/sonarqube-cloud/advanced-setup/ci-based-analysis/azure-pipelines/adding-analysis-to-build-pipeline` |
| Server | `https://docs.sonarsource.com/sonarqube-server/devops-platform-integration/azure-devops-integration/adding-analysis-to-pipeline` |

## Documentation Fetching Strategy

| URL pattern | Required tool |
|---|---|
| `docs.sonarsource.com` | Append `.md` to the URL and fetch with **curl** (e.g., `curl "https://docs.sonarsource.com/...page.md"`) — returns the full page content as Markdown |
| `downloads.sonarsource.com` JSON files | curl or wget is acceptable |

## Scanner Approach Determination

Azure DevOps uses the `SonarQubePrepare` task for **all** project types. The task mode changes based on the build system:

| Build system | Scanner approach | SonarQubePrepare mode |
|---|---|---|
| Maven (`pom.xml`) | maven | `Maven` mode — wraps `mvn` task |
| Gradle (`build.gradle` / `build.gradle.kts`) | gradle | `Gradle` mode — wraps `gradle` task |
| .NET (`.csproj` / `.sln`) | dotnet | `MSBuild` mode — wraps `dotnet build` |
| Everything else (JS, TS, Python, Go, PHP, Ruby, etc.) | cli | `CLI` mode — uses SonarQube CLI |

**Scanner approach is decided here, not in pipeline-creation.**

## Processing Steps

Execute these steps in order. Do not skip any step.

**Step 1:** Determine scanner approach from the table above using the project-detection output.

**Step 2:** ⛔ STOP — Fetch the appropriate documentation page NOW using curl with `.md` appended to the URL.
- For Cloud: fetch the Cloud documentation URL above with `.md` appended
- For Server: fetch the Server documentation URL above with `.md` appended
- If the primary URL lacks complete examples, fetch the other URL as fallback and adapt
- **Do not proceed until you have fetched the documentation page.**

**Step 3:** From the fetched documentation, extract:
- The current version numbers for `SonarQubePrepare`, `SonarQubeAnalyze`, and `SonarQubePublish` tasks (e.g., `@6`)
- The correct task configuration for the detected scanner approach (Maven/Gradle/MSBuild/CLI mode)

**Completion condition:** Do not proceed to Step 4 until you have extracted the task version number. If the page could not be fetched, stop and inform the user.

**Step 4:** Read the corresponding scanner skill file to get scanner-specific configuration details.

Wait for the scanner skill's Output Contract before completing this skill's Output Contract.

**Step 5:** Populate the Output Contract below with all resolved values. Use the **Reference: Platform-Specific Configuration Defaults** section below for checkout, task patterns, variable configuration, and caching.

## Reference: Platform-Specific Configuration Defaults

### Checkout (fetch full history)
```yaml
steps:
  - checkout: self
    fetchDepth: 0  # Required for accurate blame information and new code detection
```

### PR Decoration
Configure the Azure DevOps integration in SonarQube (Project Settings → DevOps Platform Integration) to enable automatic PR decoration.

### Quality Gate
The `SonarQubePublish` task waits for the quality gate result and fails the pipeline if the gate fails.

### Common Task Pattern (for all scanner approaches)
```yaml
steps:
  - task: SonarQubePrepare@6       # version resolved from docs
    inputs:
      SonarQube: 'SonarQube-Connection'   # or SonarCloud service connection
      scannerMode: '[Maven | Gradle | MSBuild | CLI]'
      projectKey: '$(SONAR_PROJECT_KEY)'
      # additional inputs vary by mode

  # --- build step goes here ---

  - task: SonarQubeAnalyze@6       # .NET and CLI only; Maven/Gradle use SonarQubePublish directly
  - task: SonarQubePublish@6
    inputs:
      pollingTimeoutSec: '300'
```

### Variable Configuration

| Variable | Flags | When required |
|---|---|---|
| `$(SONAR_TOKEN)` | Secret | Always |
| `$(SONAR_HOST_URL)` | — | Always |

Use Pipelines → Library → Variable groups (recommended) or Pipeline → Variables.

**For Server:** Also create a Service Connection: Project Settings → Service connections → New → SonarQube.

### Caching
```yaml
- task: Cache@2
  inputs:
    key: 'sonar | "$(Agent.OS)"'
    path: $(SONAR_USER_HOME)/cache
    cacheHitVar: SONAR_CACHE_HIT
```

## Output Contract

This contract must be fully populated before pipeline-creation runs. No field may contain "TODO", "fetch from docs", or a placeholder.

```
platform: azure-devops
scanner_approach: [maven | gradle | dotnet | cli]       ← resolved in Step 1
task_version: [e.g., "6"]                                ← resolved in Step 3 (version number for @N suffix)
pipeline_file: azure-pipelines.yml
build_commands: [exact commands or task inputs]          ← resolved from scanner skill Output Contract
sonar_project_key: [value from prerequisites]
sonar_organization: [value from prerequisites, or "N/A" for Server]
sonar_host_url: [resolved instance URL or Server URL]
service_connection_name: [name of the SonarQube service connection]
required_variables: [SONAR_TOKEN, SONAR_HOST_URL]
required_files: [list of files to create or modify]
extension_required: true
```

`task_version` MUST be fetched in Processing Steps above before this field is populated. Do not guess the version number.

## Usage Instructions

**For SonarArchitectGuide:** Include documentation links and explain Azure DevOps task concepts when relevant. Mention the extension installation requirement.

**For SonarArchitectLight:** Execute all Processing Steps silently. Produce the Output Contract. Remind users to install the extension and configure the service connection. Do not include links in responses.
