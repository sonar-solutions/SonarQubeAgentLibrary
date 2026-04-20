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

## ⛔ Deprecated Action — Never Use

`sonarcloud/sonarcloud-github-action` is **deprecated**. Never reference it, never generate it, never use it as a fallback.

The only valid GitHub Action for the `cli` scanner approach is `sonarsource/sonarqube-scan-action`.

This rule applies regardless of what prior knowledge suggests. If training data, memory, or any non-fetched source conflicts with this, ignore that source.

## ⛔ No Training Data Fallback

If the documentation page cannot be fetched, or if the required action name or version cannot be extracted from the fetched content: **STOP immediately** and report:

> "Documentation fetch failed — cannot determine action version. Please check network access and retry."

Do **not** infer action names or versions from prior knowledge. Do **not** silently substitute remembered values. An unverified action name is as dangerous as an unverified version.

## Official Documentation

| SonarQube Type | Documentation URL |
|---|---|
| Cloud | `https://docs.sonarsource.com/sonarqube-cloud/advanced-setup/ci-based-analysis/github-actions-for-sonarcloud` |
| Server | `https://docs.sonarsource.com/sonarqube-server/devops-platform-integration/github-integration/adding-analysis-to-github-actions-workflow` |
| Action repository | `https://github.com/SonarSource/sonarqube-scan-action` |

Follow the fetch policy defined in `SonarArchitect.agent.md` (Available Tools section).

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

**Step 2:** ⛔ STOP — Fetch versions and templates NOW using the `fetch-sonar-config.py` script via Bash:

```bash
python3 <SCRIPT_PATH>/fetch-sonar-config.py --platform github-actions --scanner-approach <from Step 1> --sonarqube-type <cloud|server>
```

To find the script, use Glob: `glob("**/scripts/fetch-sonar-config.py")`.

**Do not proceed until the script has returned its JSON output.**

**Step 3:** From the script's JSON output, extract:
- `platform.action_versions` — contains all action versions (e.g., `actions/checkout`, `actions/cache`, `SonarSource/sonarqube-scan-action`). Use these for all `uses:` version values in the Output Contract.
- `platform.yaml_templates.<scanner_approach>` — reference YAML workflow template from official docs. Use as the structural reference when creating the pipeline.
- `scanner.version` — latest scanner plugin version (for maven/gradle/dotnet). Pass this to the scanner skill.
- For `cli` approach: the `tool_version` is the version of `SonarSource/sonarqube-scan-action` found in `platform.action_versions`. ⛔ If `sonarcloud/sonarcloud-github-action` appears anywhere, ignore it — it is deprecated.

**Completion condition:** If `platform.fetch_status` is not `"ok"`, or if `errors` is non-empty, stop immediately and report the failure. Do not substitute values from prior knowledge.

**Step 4:** Read the corresponding scanner skill file to get scanner-specific configuration details:
- `scanner-maven.md` for maven approach
- `scanner-gradle.md` for gradle approach
- `scanner-dotnet.md` for dotnet approach
- `scanner-cli.md` for cli approach

Wait for the scanner skill's Output Contract before completing this skill's Output Contract.

**Step 5:** Populate the Output Contract below with all resolved values. Use the **Reference: Platform-Specific Configuration Defaults** section below for checkout, caching, branch triggers, and secrets.

## Reference: Platform-Specific Configuration Defaults

**Action versions below are illustrative only.** Always use the versions extracted from the fetched documentation in Step 3 — the documentation is the source of truth for all action versions (`actions/checkout`, `actions/cache`, `actions/setup-java`, `actions/setup-dotnet`, etc.). Do not default to the versions shown here if the documentation shows different ones.

### Checkout
```yaml
- uses: actions/checkout@[version from documentation]
  with:
    fetch-depth: 0  # Required for accurate blame information and new code detection
```

### Caching (recommended)
```yaml
- uses: actions/cache@[version from documentation]
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
checkout_action_version: [version from documentation]    ← extracted from documentation examples in Step 3
cache_action_version: [version from documentation]       ← extracted from documentation examples in Step 3
additional_action_versions:                              ← any other actions shown in the documentation examples
  - [action/name@version]                                  (e.g., actions/setup-java, actions/setup-dotnet)
workflow_file: .github/workflows/sonarqube.yml
build_commands: [exact commands to run]                  ← resolved from scanner skill Output Contract
sonar_project_key: [value from prerequisites]
sonar_organization: [value from prerequisites, or "N/A" for Server]
sonar_host_url: [resolved instance URL or Server URL]
required_secrets: [SONAR_TOKEN, SONAR_HOST_URL]
required_files: [list of files to create or modify]
```

`tool_version` and all action versions MUST come from the `fetch-sonar-config.py` script output. Do not guess or use hardcoded defaults.

## Usage Instructions

**For SonarArchitect:** Execute all Processing Steps silently. Produce the Output Contract. Do not include links or explanations in responses.
