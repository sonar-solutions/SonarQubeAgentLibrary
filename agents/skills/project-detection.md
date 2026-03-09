---
name: project-detection
description: Autonomously detects project type, build system, and CI/CD platform from project files. Use this first in every workflow to analyze the project structure before asking the user anything.
---

# Project Detection Skill

## Purpose

Autonomously detect the project's build system, language, CI/CD platform, and existing SonarQube configuration from file analysis alone. This skill asks no questions — it only reads and reports findings.

## Execution Guidelines

Use your environment's file search and read tools (e.g., file search, glob, read) to inspect the repository. Do not ask the user what build system they use — detect it from files.

Look for:
- Build descriptor files (pom.xml, build.gradle, etc.)
- CI/CD pipeline files (.github/workflows/, .gitlab-ci.yml, etc.)
- Existing SonarQube configuration files (sonar-project.properties, sonar.* properties)
- Test and coverage configuration files

## Technology Stack Analysis

Inspect these files to determine the build system:

| Build System | Files to Detect |
|---|---|
| Maven | `pom.xml` |
| Gradle | `build.gradle`, `build.gradle.kts` |
| .NET | `*.csproj`, `*.sln`, `*.vbproj`, `*.fsproj` |
| JavaScript / TypeScript | `package.json`, `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml` |
| Python | `requirements.txt`, `setup.py`, `pyproject.toml`, `Pipfile` |
| Go | `go.mod` |
| Ruby | `Gemfile` |
| PHP | `composer.json` |

**Priority rule:** If `pom.xml` is present, the scanner is Maven. If `build.gradle` or `build.gradle.kts` is present (and no `pom.xml`), the scanner is Gradle. If `.csproj` or `.sln` is present, the scanner is .NET. All others use the CLI scanner.

## CI/CD Platform Detection

Check for these files to identify the CI/CD platform:

| Platform | Files to Detect |
|---|---|
| GitHub Actions | `.github/workflows/*.yml` or `.github/workflows/*.yaml` |
| GitLab CI | `.gitlab-ci.yml` |
| Azure DevOps | `azure-pipelines.yml` |
| Bitbucket Pipelines | `bitbucket-pipelines.yml` |

**Note:** Jenkins is not supported. If a `Jenkinsfile` is detected, report it but do not select Jenkins as the target platform — ask the user to choose a supported platform.

## Existing Pipeline File Analysis

When CI/CD platform files are detected, read each file and record:
- Whether any SonarQube-related steps or references already exist in it (look for `sonarqube-scan-action`, `SonarQubePrepare`, `sonar-scanner`, `SONAR_TOKEN`, `sonar:sonar`, `sonarqube`)

This information is used by `pipeline-creation` to decide whether to use the file as the base for the new SonarQube pipeline.

## Existing SonarQube Configuration Detection

Check for existing SonarQube configuration:

- `sonar-project.properties` — CLI scanner properties file
- `pom.xml` — look for `sonar-maven-plugin` in `<plugins>` or `sonar.*` in `<properties>`
- `build.gradle` / `build.gradle.kts` — look for `id("org.sonarqube")` or `id 'org.sonarqube'`
- Existing CI/CD files — look for `sonarqube-scan-action`, `SonarQubePrepare`, `sonar-scanner-cli`, or `SONAR_TOKEN` references

## Detection Output

After running this skill, report findings using these fields:

```
project_type: [Maven | Gradle | .NET | JavaScript | TypeScript | Python | Go | Ruby | PHP | Other]
build_system_file: [path to detected build descriptor, e.g., pom.xml, build.gradle]
scanner_approach: [maven | gradle | dotnet | cli]
ci_platform: [github-actions | gitlab-ci | azure-devops | bitbucket | none-detected]
ci_platform_file: [path to detected CI/CD file, or "none"]
existing_pipeline_files:
  - file: [path]
    has_sonarqube: [yes | no]
  # one entry per detected CI/CD file; omit this block if ci_platform_file is "none"
existing_sonar_config: [yes | no]
existing_sonar_config_file: [path to detected sonar config, or "none"]
```

Report these findings to the user and ask them to confirm the CI/CD platform before proceeding to prerequisites-gathering.
