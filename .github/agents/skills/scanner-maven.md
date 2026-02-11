---
name: scanner-maven
description: Maven scanner configuration for SonarQube. Use this for Java projects using Maven build system.
---

# Maven Scanner Skill

This skill provides Maven-specific scanner documentation and configuration guidance.

## Official Documentation

### SonarQube Cloud
- https://docs.sonarsource.com/sonarqube-cloud/advanced-setup/ci-based-analysis/sonarscanner-for-maven

### SonarQube Server
- https://docs.sonarsource.com/sonarqube-server/analyzing-source-code/scanners/sonarscanner-for-maven

## Scanner Overview

**Use `web/fetch` to get current examples and versions from official documentation.**

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

**Fetch JaCoCo configuration examples from official documentation.**

## Common Configuration Properties

**Fetch current property examples from official documentation.**

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
10. **Check versions**: Use `web/fetch` to verify latest plugin versions before specifying

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
   - If plugin exists: Use `web/fetch` to get latest version, compare and UPDATE if needed
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
- **Step 3**: Use `web/fetch` to get latest plugin version from official documentation
- **Step 4**: Check if `<sonar.*>` properties exist in `<properties>` section
- **Step 5**: Update plugin version if needed, add if best practice
- **Step 6**: Add or update SonarQube properties (don't duplicate existing ones)
- **Step 7**: In CI/CD workflow, set working-directory to match pom.xml location
