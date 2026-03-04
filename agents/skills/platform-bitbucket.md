---
name: platform-bitbucket
description: Bitbucket Pipelines integration for SonarQube Cloud and Server. Determines scanner approach, fetches current pipe versions, and produces an Output Contract for pipeline-creation.
---

# Bitbucket Pipelines Platform Skill

## IMPORTANT — Scope

This skill is responsible for:
1. **Determining** the scanner approach for Bitbucket Pipelines based on build system
2. **Fetching** current pipe versions from official documentation or pipe repositories
3. **Producing** a complete Output Contract before pipeline-creation runs

This skill does **not** explain concepts or include documentation links in responses. It acts.

## Official Documentation

| SonarQube Type | Documentation URL |
|---|---|
| Cloud | `https://docs.sonarsource.com/sonarqube-cloud/advanced-setup/ci-based-analysis/bitbucket-pipelines-for-sonarcloud` |
| Server | `https://docs.sonarsource.com/sonarqube-server/devops-platform-integration/bitbucket-integration/bitbucket-cloud-integration/bitbucket-pipelines` |

**Pipe repositories** (version tags are listed on these pages):

| Pipe | Repository |
|---|---|
| Cloud scan | `https://bitbucket.org/sonarsource/sonarcloud-scan/src/master/` |
| Cloud quality gate | `https://bitbucket.org/sonarsource/sonarcloud-quality-gate/src/master/` |
| Server scan | `https://bitbucket.org/sonarsource/sonarqube-scan/src/master/` |
| Server quality gate | `https://bitbucket.org/sonarsource/sonarqube-quality-gate/src/master/` |

## Documentation Fetching Strategy

| URL pattern | Required tool |
|---|---|
| `docs.sonarsource.com` | Append `.md` to the URL and fetch with **curl** (e.g., `curl "https://docs.sonarsource.com/...page.md"`) — returns the full page content as Markdown |
| `bitbucket.org` pages | Use your environment's **browser-capable fetch tool**. **NOT curl.** |
| `downloads.sonarsource.com` JSON files | curl or wget is acceptable |

**Never use curl to access bitbucket.org.** Those pages require JavaScript rendering; only a browser-capable fetch tool can retrieve them correctly.

## Scanner Approach Determination

| Build system | Scanner approach | How the scan runs |
|---|---|---|
| Maven (`pom.xml`) | maven | `mvn clean verify sonar:sonar` — run directly in pipeline step |
| Gradle (`build.gradle` / `build.gradle.kts`) | gradle | `./gradlew test jacocoTestReport sonar` — run directly in pipeline step |
| .NET (`.csproj` / `.sln`) | dotnet | `dotnet sonarscanner begin/build/end` — run directly in pipeline step |
| Everything else (JS, TS, Python, Go, PHP, Ruby, etc.) | cli | Official SonarQube pipe |

**For Maven, Gradle, and .NET:** Run commands directly in Bitbucket pipeline steps. Do **not** use the scan pipe.

**For CLI scanner projects:** Use the official pipe:
- Cloud: `sonarsource/sonarcloud-scan`
- Server: `sonarsource/sonarqube-scan`

**Scanner approach is decided here, not in pipeline-creation.**

## Processing Steps

Execute these steps in order. Do not skip any step.

**Step 1:** Determine scanner approach from the table above using the project-detection output.

**Step 2:** ⛔ STOP — Fetch the appropriate documentation page and pipe repository page NOW.
- Fetch the documentation URL for the detected SonarQube type (Cloud or Server) using curl with `.md` appended to the URL
- If scanner approach is `cli`: also fetch the appropriate pipe repository page (bitbucket.org) using your environment's browser-capable fetch tool
- **Do not proceed until you have fetched at least the documentation page.**

**Step 3:** From the fetched pages, extract:
- For `cli` approach: fetch the appropriate **Scan Pipe Repository** URL (from the table above) and extract the latest pipe version tag — this is the `tool_version`. Use the version tag shown in the repository, not `:latest`.
- For `maven`, `gradle`, or `dotnet` approach: extract the corresponding step example from the documentation — use this as the reference template when creating the pipeline. No pipe version applies.

**Completion condition:** Do not proceed to Step 4 until you have extracted a specific pipe version tag for `cli`, or the step template for build-tool approaches. If the page could not be fetched, stop and inform the user.

**Step 4:** Read the corresponding scanner skill file to get scanner-specific configuration details.

Wait for the scanner skill's Output Contract before completing this skill's Output Contract.

**Step 5:** Populate the Output Contract below with all resolved values. Use the **Reference: Platform-Specific Configuration Defaults** section below for clone configuration, caching, variables, and pipeline structure.

## Reference: Platform-Specific Configuration Defaults

### Clone Configuration (full depth for accurate blame)
```yaml
clone:
  depth: full  # Required for accurate blame information and new code detection
```

### Caching
```yaml
definitions:
  caches:
    sonar: ~/.sonar/cache
```

### Repository Variables

| Variable | Flags | When required |
|---|---|---|
| `$SONAR_TOKEN` | Secured | Always |
| `$SONAR_HOST_URL` | Secured | Always |

Mark all variables as **Secured** so they are masked in pipeline logs.

### Pipeline Structure (CLI scanner with pipe)
```yaml
pipelines:
  default:
    - step:
        name: SonarQube Analysis
        caches:
          - sonar
        script:
          - pipe: sonarsource/sonarcloud-scan:X.Y.Z   # version resolved from pipe repo
            variables:
              SONAR_TOKEN: $SONAR_TOKEN
```

### Pipeline Structure (Maven/Gradle/.NET — direct commands)
```yaml
pipelines:
  default:
    - step:
        name: SonarQube Analysis
        caches:
          - sonar
        script:
          - [build and scan commands from scanner skill Output Contract]
```

## Output Contract

This contract must be fully populated before pipeline-creation runs. No field may contain "TODO", "fetch from docs", or a placeholder.

```
platform: bitbucket
scanner_approach: [maven | gradle | dotnet | cli]       ← resolved in Step 1
tool_version: [exact pipe version tag, or "N/A" for build-tool scanners]  ← resolved in Step 3
pipe_name: [e.g., "sonarsource/sonarcloud-scan", or "N/A"]  ← resolved in Step 1+3
pipeline_file: bitbucket-pipelines.yml
build_commands: [exact commands or pipe config]          ← resolved from scanner skill Output Contract
sonar_project_key: [value from prerequisites]
sonar_organization: [value from prerequisites, or "N/A" for Server]
sonar_host_url: [resolved instance URL or Server URL]
required_variables: [SONAR_TOKEN, SONAR_HOST_URL]
required_files: [list of files to create or modify]
```

`tool_version` MUST be a specific version tag fetched from the pipe repository page. Do not use `:latest` or guess a version.

## Usage Instructions

**For SonarArchitect:** Execute all Processing Steps silently. Produce the Output Contract. Do not include links or explanations in responses.
