---
name: scanner-gradle
description: Gradle scanner configuration for SonarQube. Use this for Java/Kotlin projects using Gradle build system.
---

# Gradle Scanner Skill

This skill provides Gradle-specific scanner documentation and configuration guidance.

**IMPORTANT - Scope of This Skill:**
- This skill is ONLY for SonarQube integration with Gradle projects
- Assumes the project already has a working Gradle build configuration
- DO NOT use this skill to troubleshoot Gradle build issues
- DO NOT fetch Gradle documentation for general build problems
- Focus exclusively on adding/updating SonarQube plugin and configuration

## Official Documentation

### SonarQube Cloud
- https://docs.sonarsource.com/sonarqube-cloud/advanced-setup/ci-based-analysis/sonarscanner-for-gradle

### SonarQube Server
- https://docs.sonarsource.com/sonarqube-server/analyzing-source-code/scanners/sonarscanner-for-gradle

## Scanner Version Information

**Latest Gradle Scanner Version:**
- Version URL: https://downloads.sonarsource.com/sonarqube/update/scannergradle.json
- **To get the latest version**: Make an HTTP GET request to the URL above
- The response is a JSON file containing the latest version information
- Extract the version number from the JSON response
- Use this version when configuring the SonarQube plugin in your build.gradle or build.gradle.kts

**Example using curl:**
```bash
curl -s https://downloads.sonarsource.com/sonarqube/update/scannergradle.json
```

## Documentation Retrieval Strategy

**How to retrieve documentation:**
- **Documentation pages** (docs.sonarsource.com): Use a browser-capable fetch tool — these pages require JavaScript rendering and cannot be retrieved with curl or wget. Use whichever tool in your environment supports this (e.g., web/fetch, WebFetch, url_context, or equivalent).
- **Version JSON endpoints** (downloads.sonarsource.com): curl or wget work fine — these are static JSON files.

**CRITICAL: ONLY retrieve from official SonarQube sources.**

**Mandatory Rules:**
- **ONLY** retrieve from the official docs.sonarsource.com URLs and downloads.sonarsource.com URLs listed above
- **DO NOT** fetch from Gradle Plugin Portal, GitHub repositories, or any other websites
- **DO NOT** search for plugin version information outside official SonarQube sources
- **DO NOT** use general web search to find plugin versions

**Fallback Approach for Missing Information:**
- If working with SonarQube Cloud, first retrieve from the Cloud documentation URL above
- If the Cloud documentation lacks complete plugin version or configuration examples, also retrieve from the Server documentation URL as a fallback
- If working with SonarQube Server, first retrieve from the Server documentation URL above
- If the Server documentation lacks complete plugin version or configuration examples, also retrieve from the Cloud documentation URL as a fallback
- For latest version information, always check the Scanner Version Information URL
- If NEITHER official documentation URL contains the needed information, STOP and inform the user that the information is not available in official documentation

**What to Extract from Documentation:**
- Plugin version and syntax
- Configuration examples
- Property definitions
- Integration patterns

## Scanner Overview

The Gradle SonarQube scanner is a Gradle plugin that integrates SonarQube analysis into the Gradle build lifecycle.

**CRITICAL: Gradle projects do NOT use CI/CD scan actions/tasks (except Azure DevOps).**
- GitHub Actions: Do NOT use `sonarsource/sonarqube-scan-action` - run `./gradlew sonar` directly
- GitLab CI: Do NOT use sonar-scanner-cli Docker image - run `./gradlew sonar` directly
- Azure DevOps: Use SonarQubePrepare task in Gradle mode (special case - wraps Gradle integration)
- Bitbucket: Do NOT use SonarQube/SonarCloud pipes - run `./gradlew sonar` directly

### Plugin Version Management
- **Always check latest version**: Retrieve the current plugin version from Scanner Version Information URL (https://downloads.sonarsource.com/sonarqube/update/scannergradle.json)
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

**Retrieve JaCoCo configuration examples (Groovy and Kotlin DSL) from official documentation.**

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
6. **ALWAYS update plugin version**: Retrieve latest version from Scanner Version Information URL and update build.gradle even if plugin already exists
7. **Kotlin DSL**: Use .kts for type-safe configuration in Kotlin projects
8. **Gradle version compatibility**: Ensure Gradle 7.3+ for latest SonarQube plugin
9. **Exclude generated code**: Configure exclusions for auto-generated code, build outputs
10. **Multi-module setup**: Configure plugin at root level for consistent analysis
11. **Check compatibility**: Verify Gradle and plugin version compatibility in documentation

## Output Contract

After processing this skill, provide the following to pipeline-creation:

- `build_commands`: `./gradlew build sonar` (or with JaCoCo: `./gradlew test jacocoTestReport sonar`)
- `scanner_parameters`:
  - `sonar.projectKey` (required)
  - `sonar.organization` (Cloud only)
  - `sonar.coverage.jacoco.xmlReportPaths` (if JaCoCo configured)
- `required_files`: changes needed in `build.gradle` or `build.gradle.kts` (plugin declaration + `sonarqube {}` block)
- `working_directory`: directory containing `build.gradle` (if not project root)
- `runtime_requirements`: JDK version required by the project
- `tool_version`: latest `org.sonarqube` plugin version — fetch from Scanner Version Information URL

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
   - If plugin exists: Retrieve latest version from Scanner Version Information URL (https://downloads.sonarsource.com/sonarqube/update/scannergradle.json), compare and UPDATE if needed
   - If plugin missing: Retrieve latest version from Scanner Version Information URL before adding
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
- **Step 3**: ⛔ STOP - Retrieve latest SonarQube plugin version from Scanner Version Information URL (https://downloads.sonarsource.com/sonarqube/update/scannergradle.json)
- **Step 4**: Check if `sonarqube {}` configuration block exists
- **Step 5**: Update plugin version if outdated, add if missing (use latest version)
- **Step 6**: Add or update SonarQube configuration properties (don't duplicate existing ones)
- **Step 7**: In CI/CD workflow, set working-directory to match build.gradle location
- **IMPORTANT**: Only fetch SonarQube documentation, do NOT fetch Gradle build tool documentation
- Add or update plugin declaration with latest version in build.gradle or build.gradle.kts
- Retrieve latest JaCoCo version if adding coverage
- Configure sonarqube block with project properties
- Configure CI/CD command: `./gradlew build sonar`
- Do NOT include links in responses
