---
name: scanner-cli
description: SonarScanner CLI configuration for JavaScript, TypeScript, Python, Go, PHP, Ruby, and any language not using Maven, Gradle, or .NET. Produces an Output Contract including sonar-project.properties content.
---

# SonarScanner CLI Skill

## Purpose

Configure SonarQube integration for projects using the SonarScanner CLI. This skill applies to JavaScript, TypeScript, Python, Go, PHP, Ruby, and any other language that does not use Maven, Gradle, or .NET as a build system.

For CLI scanner projects, the scanner tool version is resolved by the platform skill (action version, image tag, or pipe version) — not by this skill.

## Official Documentation

| SonarQube Type | Documentation URL |
|---|---|
| Cloud | `https://docs.sonarsource.com/sonarqube-cloud/advanced-setup/ci-based-analysis/sonarscanner-cli` |
| Server | `https://docs.sonarsource.com/sonarqube-server/analyzing-source-code/scanners/sonarscanner` |

Follow the fetch policy defined in `SonarArchitect.agent.md` (Available Tools section).

## Processing Steps

Execute these steps in order. Do not skip any step.

**Step 1:** Check for an existing `sonar-project.properties` file using file search tools.
- If found: read its complete contents and note what is already configured
- If not found: the file will be created

**Step 2:** Determine language-specific configuration:
- Identify the primary language from the project-detection output
- Determine the correct `sonar.sources` path
- Determine the coverage report path and property name (see Language-Specific section below)

**Step 3:** ⛔ STOP — Verify the `sonar-project.properties` content is correct and complete.

Required properties that MUST be present:
- `sonar.projectKey` — from prerequisites
- `sonar.organization` — from prerequisites (Cloud only)
- `sonar.sources` — path to source files (not test files)
- `sonar.host.url` — the Cloud instance URL or Server URL
- Language-specific coverage path property (if coverage is configured)

**Completion condition:** Do not proceed to Step 4 until you have confirmed all required properties are present and correct. Do not leave any property with a placeholder value.

**Step 4:** If the file does not exist, create it. If it exists, add only missing properties — never duplicate existing ones.

**Step 5:** Populate the Output Contract below.

## sonar-project.properties Template

```properties
# SonarQube project identification
sonar.projectKey=YOUR_PROJECT_KEY
sonar.organization=YOUR_ORG_KEY        # Cloud only — remove for Server
sonar.projectName=My Project           # optional, defaults to projectKey

# SonarQube host
sonar.host.url=https://sonarcloud.io   # Cloud EU; use https://sonarqube.us for Cloud US; or your Server URL

# Source configuration
sonar.sources=src                      # adjust to match actual source directory
sonar.sourceEncoding=UTF-8

# Exclusions (adjust as needed)
sonar.exclusions=node_modules/**,dist/**,build/**,coverage/**,**/*.test.*,**/*.spec.*
```

## Language-Specific Coverage Configuration

| Language | Coverage tool | Coverage property | Report format |
|---|---|---|---|
| JavaScript / TypeScript | Jest / Istanbul / nyc | `sonar.javascript.lcov.reportPaths` | LCOV (`coverage/lcov.info`) |
| Python | coverage.py / pytest-cov | `sonar.python.coverage.reportPaths` | XML (`coverage.xml`) |
| Go | built-in `go test` | `sonar.go.coverage.reportPaths` | Go coverage profile (`coverage.out`) |
| PHP | PHPUnit | `sonar.php.coverage.reportPaths` | Clover XML |
| Ruby | SimpleCov | `sonar.ruby.coverage.reportPaths` | JSON resultset |

### Coverage commands by language

**JavaScript / TypeScript (Jest):**
```bash
npx jest --coverage --coverageReporters=lcov
```
Add to `sonar-project.properties`:
```properties
sonar.javascript.lcov.reportPaths=coverage/lcov.info
```

**Python (pytest-cov):**
```bash
pytest --cov=. --cov-report=xml:coverage.xml
```
Add to `sonar-project.properties`:
```properties
sonar.python.coverage.reportPaths=coverage.xml
```

**Go:**
```bash
go test ./... -coverprofile=coverage.out
```
Add to `sonar-project.properties`:
```properties
sonar.go.coverage.reportPaths=coverage.out
```

## Platform Integration

The CLI scanner runs through the platform's native integration:

| Platform | How it runs |
|---|---|
| GitHub Actions | `sonarsource/sonarqube-scan-action` (version from platform skill) |
| GitLab CI | `sonarsource/sonar-scanner-cli` Docker image (pinned version from platform skill) |
| Azure DevOps | `SonarQubePrepare@N` + `SonarQubeAnalyze@N` tasks (version from platform skill) |
| Bitbucket | `sonarsource/sonarcloud-scan` or `sonarsource/sonarqube-scan` pipe (version from platform skill) |

The scanner tool version is resolved by the platform skill — not this skill. This skill's `tool_version` field is always `n/a`.

## Output Contract

This contract must be fully populated before pipeline-creation runs. No field may contain "TODO", "fetch from docs", or a placeholder.

```
scanner: cli
tool_version: n/a                        ← always n/a; version is resolved by platform skill
build_commands: ["sonar-scanner"]        ← the platform action/image/pipe handles this
sonar_properties_file: sonar-project.properties
working_directory: [path relative to repository root, or "." for root]
sonar_project_key: [value from prerequisites]
sonar_organization: [value from prerequisites, or "N/A" for Server]
sonar_host_url: [resolved instance URL or Server URL]
sources_path: [e.g., "src"]
coverage_property: [language-specific property name, or "N/A" if not configured]
coverage_report_path: [e.g., "coverage/lcov.info", or "N/A" if not configured]
required_files:
  - sonar-project.properties (create or update)
  - [list of additional files modified]
sonar_project_properties_content: |
  sonar.projectKey=ACTUAL_VALUE
  sonar.organization=ACTUAL_VALUE    # Cloud only
  sonar.host.url=ACTUAL_VALUE
  sonar.sources=ACTUAL_VALUE
  [other properties]
```

`sonar_project_properties_content` must contain the actual resolved values — not placeholders.

## Usage Instructions

**For SonarArchitect:** Execute all Processing Steps silently. Produce the Output Contract including the complete `sonar-project.properties` content with resolved values. Do not include links or explanations in responses.
