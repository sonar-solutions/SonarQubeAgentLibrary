---
name: platform-github-actions
description: GitHub Actions integration for SonarQube Cloud and Server. Determines scanner approach, fetches current documentation, and produces an Output Contract for pipeline-creation.
---

# GitHub Actions Platform Skill

## IMPORTANT — Scope

This skill is responsible for:
1. **Determining** the scanner approach for GitHub Actions based on build system
2. **Fetching** current workflow examples and tool versions from official documentation
3. **Producing** a complete Output Contract before pipeline-creation runs

This skill does **not** explain concepts or include documentation links in responses. It acts.

## Official Documentation

| SonarQube Type | Documentation URL |
|---|---|
| Cloud | `https://docs.sonarsource.com/sonarqube-cloud/advanced-setup/ci-based-analysis/github-actions-for-sonarcloud` |
| Server | `https://docs.sonarsource.com/sonarqube-server/devops-platform-integration/github-integration/adding-analysis-to-github-actions-workflow` |
| Action repository | `https://github.com/SonarSource/sonarqube-scan-action` |

## Documentation Fetching Strategy

| URL pattern | Required tool |
|---|---|
| `docs.sonarsource.com` | Append `.md` to the URL and fetch with **curl** (e.g., `curl "https://docs.sonarsource.com/...page.md"`) — returns the full page content as Markdown |
| `downloads.sonarsource.com` JSON files | curl or wget is acceptable |

## Scanner Approach Determination

Select the scanner approach based on the build system detected by project-detection:

| Build system | Scanner approach | What runs in the workflow |
|---|---|---|
| Maven (`pom.xml`) | maven | `mvn clean verify sonar:sonar` |
| Gradle (`build.gradle` / `build.gradle.kts`) | gradle | `./gradlew test jacocoTestReport sonar` |
| .NET (`.csproj` / `.sln`) | dotnet | `dotnet sonarscanner begin` → `dotnet build` → `dotnet sonarscanner end` |
| Everything else (JS, TS, Python, Go, PHP, Ruby, etc.) | cli | `sonarsource/sonarqube-scan-action` |

**Scanner approach is decided here, not in pipeline-creation.**

## Processing Steps

Execute these steps in order. Do not skip any step.

**Step 1:** Determine scanner approach from the table above using the project-detection Output.

**Step 2:** ⛔ STOP — Fetch the appropriate documentation page NOW using curl with `.md` appended to the URL.
- For Cloud: fetch the Cloud documentation URL above with `.md` appended
- For Server: fetch the Server documentation URL above with `.md` appended
- If the primary URL lacks complete examples, fetch the other URL as fallback and adapt
- **Do not proceed until you have fetched the documentation page.**

**Step 3:** From the fetched documentation, extract:
- For `cli` scanner approach: look in the **"Setting up your workflow file"** section — extract the latest version tag of `sonarsource/sonarqube-scan-action` used in the example (e.g., `v5`). This is the `tool_version`.
- For `maven`, `gradle`, or `dotnet` approach: look in the **"Configuring the build.yml file"** section — extract the corresponding `SonarScanner for Maven` / `SonarScanner for Gradle` / `SonarScanner for .NET` workflow example. Use this as the reference template. No action version applies.
- The recommended `actions/checkout` version (typically `v4`)
- The recommended `actions/cache` version (typically `v4`) if caching is shown

**Completion condition:** Do not proceed to Step 4 until you have extracted the tool version or workflow template from the documentation. If the page could not be fetched, stop and inform the user.

**Step 4:** Read the corresponding scanner skill file to get scanner-specific configuration details:
- `scanner-maven.md` for maven approach
- `scanner-gradle.md` for gradle approach
- `scanner-dotnet.md` for dotnet approach
- `scanner-cli.md` for cli approach

Wait for the scanner skill's Output Contract before completing this skill's Output Contract.

**Step 5:** Populate the Output Contract below with all resolved values. Use the **Reference: Platform-Specific Configuration Defaults** section below for checkout, caching, branch triggers, and secrets.

## Reference: Platform-Specific Configuration Defaults

### Checkout
```yaml
- uses: actions/checkout@v4
  with:
    fetch-depth: 0  # Required for accurate blame information and new code detection
```

### Caching (recommended)
```yaml
- uses: actions/cache@v4
  with:
    path: ~/.sonar/cache
    key: ${{ runner.os }}-sonar
    restore-keys: ${{ runner.os }}-sonar
```

### Branch Triggers
```yaml
on:
  push:
    branches:
      - main
      - master
      - "develop/**"
      - "feature/**"
  pull_request:
    branches:
      - main
      - master
```

### Required Secrets

| Secret | When required |
|---|---|
| `SONAR_TOKEN` | Always |
| `SONAR_HOST_URL` | Server only, or Cloud (set to the instance URL) |

## Output Contract

This contract must be fully populated before pipeline-creation runs. No field may contain "TODO", "fetch from docs", or a placeholder.

```
platform: github-actions
scanner_approach: [maven | gradle | dotnet | cli]       ← resolved in Step 1
tool_version: [exact version string]                     ← resolved in Step 3 (e.g., "v5" for action, or "N/A" for build-tool scanners)
checkout_action_version: [e.g., "v4"]                   ← resolved in Step 3
cache_action_version: [e.g., "v4"]                      ← resolved in Step 3
workflow_file: .github/workflows/sonarqube.yml
build_commands: [exact commands to run]                  ← resolved from scanner skill Output Contract
sonar_project_key: [value from prerequisites]
sonar_organization: [value from prerequisites, or "N/A" for Server]
sonar_host_url: [resolved instance URL or Server URL]
required_secrets: [SONAR_TOKEN, SONAR_HOST_URL]
required_files: [list of files to create or modify]
```

`tool_version` MUST be fetched in Processing Steps above before this field is populated. Do not guess or use a stale version.

## Usage Instructions

**For SonarArchitectGuide:** Include documentation links and explain GitHub Actions concepts when relevant.

**For SonarArchitectLight:** Execute all Processing Steps silently. Produce the Output Contract. Do not include links or explanations in responses.
