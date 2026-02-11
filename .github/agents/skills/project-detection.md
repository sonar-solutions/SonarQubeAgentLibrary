---
name: project-detection
description: Identifies project type, build system, and CI/CD platform. Use this to analyze project structure and detect technology stack.
---

# Project Detection Skill

This skill helps identify the project type, build system, and CI/CD platform.

## Technology Stack Analysis

Use `search` and `read` tools to identify:

### Java Projects
- **Maven**: Look for `pom.xml`
- **Gradle**: Look for `build.gradle` or `build.gradle.kts`
- **Ant**: Look for `build.xml`

### JavaScript/TypeScript Projects
- **npm**: Look for `package.json` and `package-lock.json`
- **Yarn**: Look for `package.json` and `yarn.lock`
- **pnpm**: Look for `pnpm-lock.yaml`

### Python Projects
- Look for `requirements.txt`, `setup.py`, `pyproject.toml`, `Pipfile`

### .NET Projects
- Look for `.csproj`, `.sln`, `*.vbproj`

### Other Languages
- **Go**: `go.mod`
- **Ruby**: `Gemfile`
- **PHP**: `composer.json`

## CI/CD Platform Detection

Check for the following files:
- **GitHub Actions**: `.github/workflows/*.yml`
- **GitLab CI**: `.gitlab-ci.yml`
- **Azure DevOps**: `azure-pipelines.yml`
- **Bitbucket**: `bitbucket-pipelines.yml`
- **Jenkins**: `Jenkinsfile`

## Existing SonarQube Configuration Detection

Check for:
- `sonar-project.properties`
- `pom.xml` with SonarQube Maven plugin
- `build.gradle` with SonarQube Gradle plugin

## Test and Coverage Configuration

Look for:
- Test directories: `test/`, `tests/`, `__tests__/`, `spec/`
- Coverage configuration in `package.json`, `pytest.ini`, `.coveragerc`
- Coverage report paths: `coverage/`, `target/site/jacoco/`
