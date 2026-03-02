---
name: platform-gitlab-ci
description: GitLab CI integration for SonarQube Cloud and Server. Determines scanner approach, fetches current documentation, and produces an Output Contract for pipeline-creation.
---

# GitLab CI Platform Skill

## IMPORTANT — Scope

This skill is responsible for:
1. **Determining** the scanner approach for GitLab CI based on build system
2. **Fetching** current pipeline examples and image versions from official documentation
3. **Producing** a complete Output Contract before pipeline-creation runs

This skill does **not** explain concepts or include documentation links in responses. It acts.

## Official Documentation

| SonarQube Type | Documentation URL |
|---|---|
| Cloud | `https://docs.sonarsource.com/sonarqube-cloud/advanced-setup/ci-based-analysis/gitlab-ci` |
| Server | `https://docs.sonarsource.com/sonarqube-server/devops-platform-integration/gitlab-integration/adding-analysis-to-gitlab-ci-cd` |

## Documentation Fetching Strategy

| URL pattern | Required tool |
|---|---|
| `docs.sonarsource.com` | Use your environment's **browser-capable fetch tool** (e.g., web/fetch, WebFetch, url_context, or equivalent). **NOT curl.** |
| `downloads.sonarsource.com` JSON files | curl or wget is acceptable |

**Never use curl to access docs.sonarsource.com.** Those pages require JavaScript rendering; only a browser-capable fetch tool can retrieve them correctly.

## Scanner Approach Determination

Select the scanner approach based on the build system detected by project-detection:

| Build system | Scanner approach | What runs in the job |
|---|---|---|
| Maven (`pom.xml`) | maven | `mvn clean verify sonar:sonar` in a `maven` Docker image |
| Gradle (`build.gradle` / `build.gradle.kts`) | gradle | `./gradlew test jacocoTestReport sonar` in a `gradle` Docker image |
| .NET (`.csproj` / `.sln`) | dotnet | `dotnet sonarscanner begin` → `dotnet build` → `dotnet sonarscanner end` in a `.NET SDK` image |
| Everything else (JS, TS, Python, Go, PHP, Ruby, etc.) | cli | `sonar-scanner` CLI inside `sonarsource/sonar-scanner-cli` image |

**Scanner approach is decided here, not in pipeline-creation.**

**Critical:** Do **not** use `:latest` image tags. Always pin to a specific version extracted from documentation.

## Processing Steps

Execute these steps in order. Do not skip any step.

**Step 1:** Determine scanner approach from the table above using the project-detection output.

**Step 2:** ⛔ STOP — Fetch the appropriate documentation page NOW using your environment's browser-capable fetch tool.
- For Cloud: fetch the Cloud documentation URL above
- For Server: fetch the Server documentation URL above
- If the primary URL lacks complete examples, fetch the other URL as fallback and adapt
- **Do not proceed until you have fetched the documentation page.**

**Step 3:** From the fetched documentation, extract:
- For `cli` approach: extract the latest `sonarsource/sonar-scanner-cli` image tag from the examples in the documentation — this is the `tool_version`. Do not use `:latest`; use the pinned version shown in the example (e.g., `5.0`).
- For `maven`, `gradle`, or `dotnet` approach: extract the corresponding job example from the documentation — use this as the reference template when creating the pipeline. No image version applies.

**Completion condition:** Do not proceed to Step 4 until you have extracted a specific, pinned image version for `cli`, or the job template for build-tool approaches. If the page could not be fetched, stop and inform the user.

**Step 4:** Read the corresponding scanner skill file to get scanner-specific configuration details.

Wait for the scanner skill's Output Contract before completing this skill's Output Contract.

**Step 5:** Populate the Output Contract below with all resolved values. Use the **Reference: Platform-Specific Configuration Defaults** section below for git depth, caching, pipeline triggers, and variables.

## Reference: Platform-Specific Configuration Defaults

### Git Depth
```yaml
variables:
  GIT_DEPTH: "0"  # Required for accurate blame information and new code detection
```

### Caching
```yaml
cache:
  key: "${CI_JOB_NAME}"
  paths:
    - .sonar/cache
```

For Maven projects, also cache:
```yaml
    - ~/.m2/repository
```

For Gradle projects, also cache:
```yaml
    - ~/.gradle/caches
```

### Pipeline Triggers (use `rules`, not deprecated `only`)
```yaml
rules:
  - if: $CI_COMMIT_BRANCH == "main"
  - if: $CI_COMMIT_BRANCH == "master"
  - if: $CI_PIPELINE_SOURCE == "merge_request_event"
```

### Required Variables

| Variable | Flags | When required |
|---|---|---|
| `$SONAR_TOKEN` | Masked, Protected | Always |
| `$SONAR_HOST_URL` | Protected | Always |

## Output Contract

This contract must be fully populated before pipeline-creation runs. No field may contain "TODO", "fetch from docs", or a placeholder.

```
platform: gitlab-ci
scanner_approach: [maven | gradle | dotnet | cli]       ← resolved in Step 1
tool_version: [exact pinned image tag]                   ← resolved in Step 3 (e.g., "5.0" for sonar-scanner-cli)
pipeline_file: .gitlab-ci.yml
build_commands: [exact commands to run]                  ← resolved from scanner skill Output Contract
docker_image: [full image:tag string]                    ← resolved in Step 3
sonar_project_key: [value from prerequisites]
sonar_organization: [value from prerequisites, or "N/A" for Server]
sonar_host_url: [resolved instance URL or Server URL]
required_variables: [SONAR_TOKEN, SONAR_HOST_URL]
required_files: [list of files to create or modify]
```

`tool_version` MUST be a specific pinned version fetched in Processing Steps above. Do not use `:latest`.

## Usage Instructions

**For SonarArchitectGuide:** Include documentation links and explain GitLab CI concepts when relevant.

**For SonarArchitectLight:** Execute all Processing Steps silently. Produce the Output Contract. Do not include links or explanations in responses.
