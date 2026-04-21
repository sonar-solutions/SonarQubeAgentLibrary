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

Follow the fetch policy defined in `sonar-architect.md` (Available Tools section).

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

**Step 2:** ⛔ STOP — Fetch versions and templates NOW using the `fetch-sonar-config.py` script via Bash:

```bash
python3 <SCRIPT_PATH>/fetch-sonar-config.py --platform azure-devops --scanner-approach <from Step 1> --sonarqube-type <cloud|server>
```

To find the script, use Glob: `glob("**/scripts/fetch-sonar-config.py")`.

**Do not proceed until the script has returned its JSON output.**

**Step 3:** From the script's JSON output, extract:
- `platform.task_versions` — contains task version numbers (e.g., `SonarQubePrepare`, `SonarQubeAnalyze`, `SonarQubePublish`, `Cache`). Use the version numbers for the `@N` suffix in task references.
- `platform.yaml_templates.<scanner_approach>` — reference pipeline template from official docs (if available). Use as the structural reference when creating the pipeline.
- `scanner.version` — latest scanner plugin version (for maven/gradle/dotnet). Pass this to the scanner skill.

**Note:** Azure DevOps documentation may not contain YAML code blocks. If `platform.yaml_templates` is empty, use the Reference section below for the pipeline structure. If `platform.task_versions` is also empty, use the task version reference from the Reference section as a starting point but note this in the Output Contract.

**Completion condition:** If `platform.fetch_status` is not `"ok"`, or if `errors` is non-empty, stop and inform the user.

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

**Task versions below are illustrative only.** Always use the versions extracted from the fetched documentation in Step 3 — the documentation is the source of truth for all task versions.

```yaml
steps:
  - task: SonarQubePrepare@[version from docs]
    inputs:
      SonarQube: 'SonarQube-Connection'   # or SonarCloud service connection
      scannerMode: '[Maven | Gradle | MSBuild | CLI]'
      projectKey: '$(SONAR_PROJECT_KEY)'
      # additional inputs vary by mode

  # --- build step goes here ---

  - task: SonarQubeAnalyze@[version from docs]       # .NET and CLI only; Maven/Gradle use SonarQubePublish directly
  - task: SonarQubePublish@[version from docs]
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
- task: Cache@[version from docs]
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

**For SonarArchitect:** Execute all Processing Steps silently. Produce the Output Contract. Remind users to install the extension and configure the service connection. Do not include links in responses.
