---
name: scanner-maven
description: Maven scanner configuration for SonarQube. Use this for Java projects using Maven build system.
---

# Maven Scanner Skill

This skill provides Maven-specific scanner documentation and configuration guidance.

**IMPORTANT - Scope of This Skill:**
- This skill is ONLY for SonarQube integration with Maven projects
- Assumes the project already has a working Maven build configuration
- DO NOT use this skill to troubleshoot Maven build issues
- DO NOT fetch Maven documentation for general build problems
- Focus exclusively on adding/updating SonarQube plugin and properties

## Official Documentation

### SonarQube Cloud
- https://docs.sonarsource.com/sonarqube-cloud/advanced-setup/ci-based-analysis/sonarscanner-for-maven

### SonarQube Server
- https://docs.sonarsource.com/sonarqube-server/analyzing-source-code/scanners/sonarscanner-for-maven

## Scanner Version Information

**Latest Maven Scanner Version:**
- Version URL: https://downloads.sonarsource.com/sonarqube/update/scannermaven.json
- **To get the latest version**: Make an HTTP GET request to the URL above
- The response is a JSON file containing the latest version information
- Extract the version number from the JSON response
- Use this version when configuring the `sonar-maven-plugin` in your pom.xml

**Example using curl:**
```bash
curl -s https://downloads.sonarsource.com/sonarqube/update/scannermaven.json
```

## Documentation Retrieval Strategy

**How to retrieve documentation:**
- **Documentation pages** (docs.sonarsource.com): Use a browser-capable fetch tool — these pages require JavaScript rendering and cannot be retrieved with curl or wget. Use whichever tool in your environment supports this (e.g., web/fetch, WebFetch, url_context, or equivalent).
- **Version JSON endpoints** (downloads.sonarsource.com): curl or wget work fine — these are static JSON files.

**CRITICAL: ONLY retrieve from official SonarQube sources.**

**Mandatory Rules:**
- **ONLY** retrieve from the official docs.sonarsource.com URLs and downloads.sonarsource.com URLs listed above
- **DO NOT** retrieve from Maven Central, GitHub repositories, or any other websites
- **DO NOT** search for version information outside official SonarQube sources
- **DO NOT** use general web search to find plugin versions

**Fallback Approach for Missing Information:**
- If working with SonarQube Cloud, first retrieve from the Cloud documentation URL above
- If the Cloud documentation lacks complete plugin version or configuration examples, also retrieve from the Server documentation URL as a fallback
- If working with SonarQube Server, first retrieve from the Server documentation URL above
- If the Server documentation lacks complete plugin version or configuration examples, also retrieve from the Cloud documentation URL as a fallback
- For latest version information, always check the Scanner Version Information URL
- If NEITHER official documentation URL contains the needed information, STOP and inform the user that the information is not available in official documentation

**What to Extract from Documentation:**
- Plugin version (groupId, artifactId, version)
- Configuration examples
- Property definitions
- Integration patterns

## Scanner Overview

The Maven SonarQube scanner is a Maven plugin that integrates SonarQube analysis into the Maven build lifecycle.

**CRITICAL: Maven projects do NOT use CI/CD scan actions/tasks (except Azure DevOps).**
- GitHub Actions: Do NOT use `sonarsource/sonarqube-scan-action` - run `mvn sonar:sonar` directly
- GitLab CI: Do NOT use sonar-scanner-cli Docker image - run `mvn sonar:sonar` directly
- Azure DevOps: Use SonarQubePrepare task in Maven mode (special case - wraps Maven integration)
- Bitbucket: Do NOT use SonarQube/SonarCloud pipes - run `mvn sonar:sonar` directly

### Key Concepts
- Scanner runs as part of Maven build using `mvn sonar:sonar` goal
- Properties can be configured in `pom.xml` or passed via command line
- Automatically detects source and test directories from Maven structure
- Works seamlessly with multi-module Maven projects
- Integrates with JaCoCo for code coverage reporting

### Configuration Options
- **Command line**: Pass properties via `-Dsonar.property=value`
- **pom.xml**: Add properties in `<properties>` section
- **Environment variables**: `SONAR_TOKEN`, `SONAR_HOST_URL`

### Coverage Integration
- Use JaCoCo Maven plugin to generate coverage reports
- Configure `sonar.coverage.jacoco.xmlReportPaths` to point to JaCoCo XML report
- Run tests before analysis: `mvn clean verify sonar:sonar`

## Environment Variables

**Required:**
- `SONAR_TOKEN`: Authentication token for SonarQube

**Optional:**
- `SONAR_HOST_URL`: SonarQube Server URL (not needed for Cloud)
- Properties can also be set in pom.xml or passed as command-line arguments

## Code Coverage

### JaCoCo Integration
- Add JaCoCo Maven plugin to generate coverage reports
- JaCoCo generates XML reports that SonarQube can read
- Configure coverage report path using `sonar.coverage.jacoco.xmlReportPaths`
- Run `verify` goal to execute tests and generate coverage before analysis

**Use Documentation Retrieval Strategy above to get JaCoCo configuration examples from official SonarQube documentation only.**

## Common Configuration Properties

**Use Documentation Retrieval Strategy above to get current property examples from official SonarQube documentation only.**

### Key Properties:
- **Project identification**: `sonar.projectKey`, `sonar.organization`, `sonar.projectName`
- **Source/test paths**: Auto-detected by Maven (src/main/java, src/test/java)
- **Exclusions**: `sonar.exclusions`, `sonar.test.exclusions`, `sonar.cpd.exclusions`
- **Coverage**: `sonar.coverage.jacoco.xmlReportPaths`
- **Host/auth**: `sonar.host.url`, `sonar.token` (via env var preferred)

## Multi-Module Projects

- Maven automatically handles multi-module projects
- Run analysis from parent directory
- Each module analyzed as separate component in SonarQube
- Aggregated quality gate and metrics at parent level
- Use `mvn clean verify sonar:sonar` from root

## Best Practices

1. **Use `verify` not `install`**: Run tests and package without installing to local repository
2. **Enable JaCoCo**: Add JaCoCo plugin for code coverage reporting
3. **Clean before analysis**: Always run `clean` goal to ensure fresh build
4. **Properties in pom.xml**: Store non-sensitive configuration in pom.xml
5. **Secrets as env vars**: Pass `SONAR_TOKEN` via environment variables, never hardcode
6. **Maven wrapper**: Use `./mvnw` for consistent Maven versions across environments
7. **Exclude generated code**: Configure exclusions for auto-generated code, build outputs
8. **Run tests first**: Use `verify` goal to ensure tests run and coverage is collected
9. **Multi-module setup**: Run from parent POM for consistent analysis across modules
10. **Check versions**: Follow Documentation Retrieval Strategy section to verify latest plugin versions from official SonarQube documentation only

## Output Contract

After processing this skill, provide the following to pipeline-creation:

- `build_commands`: `mvn clean verify sonar:sonar` (or `./mvnw clean verify sonar:sonar` if Maven wrapper present)
- `scanner_parameters`:
  - `sonar.projectKey` (required)
  - `sonar.organization` (Cloud only)
  - `sonar.coverage.jacoco.xmlReportPaths` (if JaCoCo configured)
- `required_files`: any changes needed in `pom.xml` (plugin declaration, properties block)
- `working_directory`: directory containing `pom.xml` (if not project root)
- `runtime_requirements`: JDK version required by the project
- `tool_version`: latest `sonar-maven-plugin` version — fetch from Scanner Version Information URL

## Platform Integration

See platform-specific skills for CI/CD integration:
- **platform-github-actions**: GitHub Actions with Maven
- **platform-gitlab-ci**: GitLab CI with Maven
- **platform-azure-devops**: Azure Pipelines with Maven
- **platform-bitbucket**: Bitbucket Pipelines with Maven

## Configuration Workflow

**CRITICAL: Follow this workflow when setting up Maven projects:**

1. **Read POM file completely**: Use `read` to view entire `pom.xml` file
2. **Check for existing plugin**: Look for `sonar-maven-plugin` in `<plugins>` or `<pluginManagement>`
3. **Verify plugin version**: 
   - If plugin exists: Retrieve latest version from Scanner Version Information URL (https://downloads.sonarsource.com/sonarqube/update/scannermaven.json), compare and UPDATE if needed
   - If plugin missing: Maven uses default version, but explicit version recommended
4. **Check for existing properties**: Look for `<sonar.*>` properties in `<properties>` section
5. **Verify configuration is complete and correct**:
   - Check if `sonar.projectKey` is set (required)
   - For Cloud: Check if `sonar.organization` is set (required)
   - Verify all parameters match user requirements
   - **Don't just check plugin version and skip properties verification**
6. **Update, don't duplicate**: 
   - If properties exist but incomplete: Add missing properties
   - If properties exist but incorrect: Fix incorrect values
   - If properties missing: Add complete properties block
7. **Note POM location**: Commands must run from directory containing pom.xml
   - Example: If pom.xml is in `backend/`, CI/CD must use `working-directory: backend`

## Usage Instructions

**For SonarArchitectGuide:**
- Include documentation link in responses
- Explain Maven concepts when needed

**For SonarArchitectLight:**
- **Step 1**: Read complete pom.xml file
- **Step 2**: Check if `sonar-maven-plugin` exists and note its version
- **Step 3**: ⛔ STOP - Retrieve latest version from Scanner Version Information URL - Follow "Documentation Retrieval Strategy" section above - ONLY use official SonarQube sources to obtain latest plugin version
- **Step 4**: Check if `<sonar.*>` properties exist in `<properties>` section
- **Step 5**: Update plugin version if needed, add if best practice
- **Step 6**: Add or update SonarQube properties (don't duplicate existing ones)
- **Step 7**: In CI/CD workflow, set working-directory to match pom.xml location
- **CRITICAL**: If documentation does not contain needed information, STOP - do NOT search elsewhere
