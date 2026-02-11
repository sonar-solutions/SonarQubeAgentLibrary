---
name: scanner-gradle
description: Gradle scanner configuration for SonarQube. Use this for Java/Kotlin projects using Gradle build system.
---

# Gradle Scanner Skill

This skill provides Gradle-specific scanner documentation and configuration guidance.

## Official Documentation

### SonarQube Cloud
- https://docs.sonarsource.com/sonarqube-cloud/advanced-setup/ci-based-analysis/sonarscanner-for-gradle

### SonarQube Server
- https://docs.sonarsource.com/sonarqube-server/analyzing-source-code/scanners/sonarscanner-for-gradle

## Scanner Overview

**Use `web/fetch` to get current examples and versions from official documentation.**

The Gradle SonarQube scanner is a Gradle plugin that integrates SonarQube analysis into the Gradle build lifecycle.

**CRITICAL: Gradle projects do NOT use CI/CD scan actions/tasks (except Azure DevOps).**
- GitHub Actions: Do NOT use `sonarsource/sonarqube-scan-action` - run `./gradlew sonar` directly
- GitLab CI: Do NOT use sonar-scanner-cli Docker image - run `./gradlew sonar` directly
- Azure DevOps: Use SonarQubePrepare task in Gradle mode (special case - wraps Gradle integration)
- Bitbucket: Do NOT use SonarQube/SonarCloud pipes - run `./gradlew sonar` directly

### Plugin Version Management
- **Always check latest version**: Use `web/fetch` to get the current plugin version from official documentation
- **Update existing versions**: If a project already has the plugin configured, compare with latest and update if outdated
- **Version format**: Plugin follows format `id("org.sonarqube") version "X.Y.Z"` (Kotlin) or `id 'org.sonarqube' version 'X.Y.Z'` (Groovy)
- **Compatibility**: Verify Gradle version compatibility (requires Gradle 7.3+)

### Key Concepts
- Scanner runs as Gradle task using `./gradlew sonar`
- Properties configured in `sonarqube` block in build.gradle/build.gradle.kts
- Supports both Groovy and Kotlin DSL
- Automatically detects source and test directories from Gradle structure
- Works with multi-module Gradle projects
- Integrates with JaCoCo for code coverage reporting

### Configuration Options
- **build.gradle**: Add SonarQube plugin and configure properties block
- **Command line**: Pass properties via `-Dsonar.property=value`
- **Environment variables**: `SONAR_TOKEN`, `SONAR_HOST_URL`

### Coverage Integration
- Use JaCoCo Gradle plugin to generate coverage reports
- Configure `sonar.coverage.jacoco.xmlReportPaths` to point to JaCoCo XML report
- Run tests before analysis: `./gradlew test jacocoTestReport sonar`

## Environment Variables

**Required:**
- `SONAR_TOKEN`: Authentication token for SonarQube (or use `-Dsonar.token`)

**Optional:**
- `SONAR_HOST_URL`: SonarQube Server URL
- For SonarQube Cloud, organization must be set in build.gradle or command line

## Code Coverage

### JaCoCo Integration
- Add JaCoCo Gradle plugin to generate coverage reports
- JaCoCo generates XML reports that SonarQube can read
- Configure coverage report path using `sonar.coverage.jacoco.xmlReportPaths`
- Test task should be finalized by jacocoTestReport task
- Run build or test task to execute tests and generate coverage before analysis

**Fetch JaCoCo configuration examples (Groovy and Kotlin DSL) from official documentation.**

## Common Configuration Properties

**Fetch current property examples from official documentation.**

### Key Properties:
- **Project identification**: `sonar.projectKey`, `sonar.organization`, `sonar.projectName`
- **Source/test paths**: Auto-detected by Gradle (src/main/java, src/test/java)
- **Exclusions**: `sonar.exclusions`, `sonar.test.exclusions`, `sonar.cpd.exclusions`
- **Coverage**: `sonar.coverage.jacoco.xmlReportPaths`
- **Host/auth**: `sonar.host.url`, `sonar.token` (via env var preferred)
- **Language specific**: `sonar.java.source`, `sonar.java.target`

## Multi-Module Projects

- Add SonarQube plugin to root build.gradle
- Apply plugin to subprojects if needed
- Configure properties at root level
- Run from root: `./gradlew build sonar`
- Each module analyzed as separate component in SonarQube

**Fetch multi-module configuration examples from official documentation.**

## Best Practices

1. **Use Gradle wrapper**: Always use `./gradlew` for consistency across environments
2. **Add JaCoCo**: Enable code coverage reporting with JaCoCo plugin
3. **Build first**: Run `build` task before `sonar` to ensure compilation and tests
4. **Properties in build.gradle**: Store non-sensitive configuration in build file
5. **Secrets as env vars**: Pass `SONAR_TOKEN` via environment variables, never hardcode
6. **ALWAYS update plugin version**: Use `web/fetch` to get latest version and update build.gradle even if plugin already exists
7. **Kotlin DSL**: Use .kts for type-safe configuration in Kotlin projects
8. **Gradle version compatibility**: Ensure Gradle 7.3+ for latest SonarQube plugin
9. **Exclude generated code**: Configure exclusions for auto-generated code, build outputs
10. **Multi-module setup**: Configure plugin at root level for consistent analysis
11. **Check compatibility**: Verify Gradle and plugin version compatibility in documentation

## Platform Integration

See platform-specific skills for CI/CD integration:
- **platform-github-actions**: GitHub Actions with Gradle
- **platform-gitlab-ci**: GitLab CI with Gradle
- **platform-azure-devops**: Azure Pipelines with Gradle
- **platform-bitbucket**: Bitbucket Pipelines with Gradle

## Configuration Workflow

**CRITICAL: Follow this workflow when setting up Gradle projects:**

1. **Read build file completely**: Use `read` to view entire `build.gradle` or `build.gradle.kts` file
2. **Check for existing plugin**: Look for `id("org.sonarqube")` or `id 'org.sonarqube'` in plugins block
3. **Verify plugin version**: 
   - If plugin exists: Use `web/fetch` to get latest version, compare and UPDATE if needed
   - If plugin missing: Use `web/fetch` to get latest version before adding
4. **Check for existing sonarqube configuration block**: Look for `sonarqube {}` or `sonar {}` configuration blocks
5. **Verify configuration is complete and correct**:
   - Check if `projectKey` is set (required)
   - For Cloud: Check if `organization` is set (required)
   - Verify all parameters match user requirements
   - **Don't just add plugin and skip configuration verification**
6. **Update, don't duplicate**: 
   - If configuration exists but incomplete: Add missing properties
   - If configuration exists but incorrect: Fix incorrect values
   - If configuration missing: Add complete configuration block
7. **Note build file location**: Commands must run from directory containing build.gradle
   - Example: If build.gradle is in `backend/`, CI/CD must use `working-directory: backend`

## Usage Instructions

**For SonarArchitectGuideWithSkills:**
- Include documentation link in responses
- Explain Gradle concepts when needed

**For SonarArchitectLightWithSkills:**
- **Step 1**: Read complete build.gradle/build.gradle.kts file
- **Step 2**: Check if `org.sonarqube` plugin exists and note its version
- **Step 3**: Use `web/fetch` to get latest plugin version from official documentation
- **Step 4**: Check if `sonarqube {}` configuration block exists
- **Step 5**: Update plugin version if outdated, add if missing (use latest version)
- **Step 6**: Add or update configuration properties (don't duplicate existing ones)
- **Step 7**: In CI/CD workflow, set working-directory to match build.gradle location
- Add or update plugin declaration with latest version in build.gradle or build.gradle.kts
- Use `web/fetch` to check latest JaCoCo version if adding coverage
- Configure sonarqube block with project properties
- Configure CI/CD command: `./gradlew build sonar`
- Do NOT include links in responses
