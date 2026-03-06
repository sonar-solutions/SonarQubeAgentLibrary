---
name: pipeline-creation
description: Assembles configuration files from platform and scanner Output Contracts. Assembly only — makes zero decisions. Use this after both platform and scanner Output Contracts are complete.
---

# Pipeline Creation Skill

## Assembly Contract (CRITICAL)

**pipeline-creation makes zero decisions.** It assembles files using values from Output Contracts.

Before running this skill, verify:
- Platform skill Output Contract is **complete** (no placeholders, no TODOs)
- Scanner skill Output Contract is **complete** (no placeholders, no TODOs)

**If `scanner_approach`, `build_commands`, or the required platform version field (`tool_version` for GitHub/GitLab/Bitbucket, `task_version` for Azure DevOps) is missing from the Output Contracts: STOP and invoke the appropriate platform or scanner skill first.**

Do not re-derive any values. Do not re-fetch any URLs. Every value in created files comes verbatim from an Output Contract or the prerequisites.

## Input Requirements

This skill requires both contracts to be present and fully populated:

**From platform skill Output Contract:**
- `platform`
- `scanner_approach`
- `tool_version` (or `task_version` for Azure DevOps)
- `workflow_file` / `pipeline_file`
- `build_commands`
- `sonar_project_key`
- `sonar_organization`
- `sonar_host_url`
- `required_secrets` / `required_variables`

**From scanner skill Output Contract:**
- `scanner`
- `build_commands`
- `working_directory`
- `required_files`
- Coverage configuration (if applicable)
- For CLI scanner: `sonar_project_properties_content`

## File Creation Map

| Platform | Files to create or modify |
|---|---|
| GitHub Actions | `.github/workflows/sonarqube.yml` (create); `pom.xml` / `build.gradle` / `build.gradle.kts` (modify if scanner is maven/gradle); `sonar-project.properties` (create if scanner is cli) |
| GitLab CI | `.gitlab-ci.yml` (create or add stage); build files as above |
| Azure DevOps | `azure-pipelines.yml` (create or modify); build files as above |
| Bitbucket | `bitbucket-pipelines.yml` (create or modify); build files as above |

## Security Rules

Before creating any file, apply these rules (from security-practices skill):
- If `security-practices.md` is not already loaded in this run, read it before applying secret syntax
- Never write a literal token value — always use the platform secret syntax
- Confirm the correct secret syntax in `security-practices` (single source of truth) and use the platform's Output Contract

## Existing Pipeline as Base (CRITICAL)

⛔ **STOP** — Before creating any new pipeline file, check whether existing pipeline files were detected during project-detection (Step 1).

### If an existing pipeline file is found with `has_sonarqube: no`

⛔ **You MUST use the existing file as the base. Do NOT create a pipeline from scratch when an existing pipeline exists.**

1. **Read** the existing pipeline file in full using the `read` tool.
2. **Copy** its entire content **verbatim** as the starting point for the new pipeline file. Use the exact content of the existing file — every trigger, every step, every env var, every runner, every cache entry. Do not reconstruct or rewrite from memory. Do not omit environment variables, steps, or configuration because they seem unrelated to SonarQube — they are part of the project's pipeline and must be preserved.
3. **Update the `name:` field** at the top of the copied file to reflect SonarQube analysis (e.g. `SonarQube Analysis`).
4. **Insert the SonarQube steps** into the existing job at the correct position for the detected scanner approach:

   | Scanner approach | Where to insert |
   |---|---|
   | `maven` | Replace the existing `mvn` command with the SonarQube-enabled Maven command (`mvn clean verify sonar:sonar` with all required `-D` properties). Keep all other steps untouched. |
   | `gradle` | Append the `sonar` task to the existing Gradle command (e.g. `./gradlew test jacocoTestReport sonar`). Keep all other steps untouched. |
   | `dotnet` | Wrap the existing build step: insert `dotnet sonarscanner begin` before the build, insert `dotnet sonarscanner end` after. Keep restore, test, and publish steps untouched. |
   | `cli` | Append the `sonarsource/sonarqube-scan-action` step after all existing build/test steps. |

5. **Add any required secrets/env vars** referenced by the inserted steps using the correct platform secret syntax from `security-practices`.
6. Do **not** remove or alter any existing steps, triggers, environment variables, runners, or caches — only add what is needed for SonarQube.

### If an existing pipeline file already has `has_sonarqube: yes`

Do not overwrite or duplicate it. Report to the user what was found and ask whether they want to update the existing SonarQube configuration.

### If no existing pipeline files were detected

Create the new pipeline file from the standard template in this skill.

## Editing Workflow

1. State the files that will be created or modified (no explanations, just the list)
2. If an existing pipeline file was found, read it before writing the new file
3. Create or edit each file using the `edit` tool, using verbatim values from Output Contracts
4. Validate YAML syntax and properties file syntax
5. Do **not** explain configuration options — this skill assembles files, not explanations

## File Structural Notes

### GitHub Actions (`.github/workflows/sonarqube.yml`)

```yaml
name: SonarQube Analysis

on:
  push:
    branches: [main, master, "develop/**", "feature/**"]
  pull_request:
    branches: [main, master]

jobs:
  sonarqube:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@[checkout_action_version from contract]
        with:
          fetch-depth: 0

      # --- cache step (from contract) ---
      # --- build/scan steps (from scanner build_commands) ---
```

For `cli` scanner approach, the scan step uses the action version from the platform Output Contract:
```yaml
      - uses: sonarsource/sonarqube-scan-action@[tool_version from contract]
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
          SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}
```

---

### GitLab CI (`.gitlab-ci.yml`)

```yaml
sonarqube-check:
  image: [docker_image from contract]
  variables:
    SONAR_TOKEN: $SONAR_TOKEN
    SONAR_HOST_URL: $SONAR_HOST_URL
    GIT_DEPTH: "0"
  cache:
    key: "${CI_JOB_NAME}"
    paths:
      - .sonar/cache
  script:
    - [build_commands from scanner contract]
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
    - if: $CI_COMMIT_BRANCH == "master"
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
```

---

### Azure DevOps (`azure-pipelines.yml`)

```yaml
trigger:
  branches:
    include: [main, master, develop/*, feature/*]
pr:
  branches:
    include: [main, master]

pool:
  vmImage: ubuntu-latest

steps:
  - checkout: self
    fetchDepth: 0

  - task: SonarQubePrepare@[task_version from contract]
    inputs:
      SonarQube: '[service_connection_name from contract]'
      scannerMode: '[mode from contract]'
      projectKey: '[sonar_project_key from contract]'

  # --- build step ---

  - task: SonarQubeAnalyze@[task_version from contract]   # .NET and CLI only

  - task: SonarQubePublish@[task_version from contract]
    inputs:
      pollingTimeoutSec: '300'
```

---

### Bitbucket (`bitbucket-pipelines.yml`)

```yaml
clone:
  depth: full

definitions:
  caches:
    sonar: ~/.sonar/cache

pipelines:
  default:
    - step:
        name: SonarQube Analysis
        caches:
          - sonar
        script:
          # For CLI scanner:
          - pipe: [pipe_name from contract]:[tool_version from contract]
            variables:
              SONAR_TOKEN: $SONAR_TOKEN
          # For build-tool scanners: use build_commands from scanner contract
```

---

### sonar-project.properties

Use the exact `sonar_project_properties_content` from the scanner (CLI) Output Contract. Do not alter any property values.
