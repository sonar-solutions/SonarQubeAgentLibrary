---
name: platform-bitbucket
description: Bitbucket Pipelines integration for SonarQube Cloud and Server. Use this when setting up SonarQube analysis with Bitbucket Cloud Pipelines.
---

# Bitbucket Pipelines Platform Skill

This skill provides Bitbucket Pipelines-specific documentation and guidance for SonarQube integration.

**IMPORTANT - Scope of This Skill:**
- This skill is ONLY for Bitbucket Pipelines structure and platform-specific configuration
- Provides pipeline examples, step syntax, triggers, repository variables setup, and Bitbucket Pipelines-specific features
- For scanner parameters, properties, and configuration: Refer to scanner-* skills (scanner-maven, scanner-gradle, scanner-dotnet, scanner-cli)
- Fetch pipeline examples from documentation, adapt scanner configuration from scanner skills

## Official Documentation

### SonarQube Cloud
- **Main Documentation**: https://docs.sonarsource.com/sonarqube-cloud/advanced-setup/ci-based-analysis/bitbucket-pipelines-for-sonarcloud
- **Scan Pipe Repository**: https://bitbucket.org/sonarsource/sonarcloud-scan/src/master/
- **Quality Gate Pipe**: https://bitbucket.org/sonarsource/sonarcloud-quality-gate/src/master/

### SonarQube Server
- **Main Documentation**: https://docs.sonarsource.com/sonarqube-server/devops-platform-integration/bitbucket-integration/bitbucket-cloud-integration/bitbucket-pipelines
- **Scan Pipe Repository**: https://bitbucket.org/sonarsource/sonarqube-scan/src/master/
- **Quality Gate Pipe**: https://bitbucket.org/sonarsource/sonarqube-quality-gate/src/master/

## Documentation Fetching Strategy

**Use `web/fetch` to get current examples and versions from official documentation and pipe repositories.**

**Fallback Approach:**
- If working with SonarQube Cloud, first fetch from the Cloud documentation URL
- If the Cloud documentation lacks complete pipeline examples, also fetch from the Server documentation URL as a fallback
- If working with SonarQube Server, first fetch from the Server documentation URL
- If the Server documentation lacks complete pipeline examples, also fetch from the Cloud documentation URL as a fallback
- Adapt any server-specific or cloud-specific details when using fallback documentation

## Bitbucket Pipelines Implementation

### Scanner Implementation

**Scanner selection is defined in pipeline-creation skill. This section covers Bitbucket-specific implementation.**

### When to Use SonarQube Pipes

Use official SonarCloud/SonarQube pipes for **CLI scanner projects only**:
- JavaScript/TypeScript/Python/PHP/Go/Ruby (without Maven/Gradle/.NET)
- Projects that require `sonar-project.properties`
- **Pipes available**:
  - SonarQube Cloud: `sonarsource/sonarcloud-scan` and `sonarsource/sonarcloud-quality-gate`
  - SonarQube Server: `sonarsource/sonarqube-scan` and `sonarsource/sonarqube-quality-gate`
- See: scanner-cli skill

**Example:**
```yaml
- pipe: sonarsource/sonarcloud-scan:1.0.0
  variables:
    SONAR_TOKEN: $SONAR_TOKEN
```

### Build Tool Integration

**For Maven/Gradle/.NET projects, run scanner commands directly in Bitbucket steps:**
- **Maven**: Run `mvn sonar:sonar` in step (see: scanner-maven skill)
- **Gradle**: Run `./gradlew sonar` in step (see: scanner-gradle skill)
- **.NET**: Run `dotnet sonarscanner begin/build/end` in step (see: scanner-dotnet skill)

Check pipe repositories for latest versions.

## Platform-Specific Configuration

### Repository Variables
- **Location**: Repository settings → Pipelines → Repository variables
- **Required variables**:
  - `SONAR_TOKEN` (mark as Secured)
  - `SONAR_HOST_URL` (Server only, mark as Secured)
  - `SONAR_PROJECT_KEY` (optional, can be in sonar-project.properties)
- See: security-practices and devops-setup-instructions skills

### Clone Configuration
- Bitbucket Pipelines uses shallow clone by default
- For better analysis, use `clone.depth: full`

### Caching
- Define caches in `definitions.caches` section
- Cache `.sonar/cache` and build dependencies

### Branch Configuration
- Use `pipelines.branches` for branch-specific pipelines
- Use `pipelines.pull-requests` for PR analysis

## Common Configurations

### Pull Request Decoration
Configure Bitbucket integration in SonarQube for automatic PR decoration.

### Using Pipes vs Direct Scanner
- **Pipes**: Easier for JavaScript/TypeScript/Python, less configuration
- **Direct scanner**: More control, better for Java/Gradle/Maven

## Best Practices

1. **Use pipes when possible**: Simpler configuration for CLI scanner
2. **Check pipe versions**: Use `web/fetch` to verify latest pipe versions
3. **Secure variables**: Always mark sensitive variables as Secured
4. **Full clone**: Use `depth: full` for accurate blame information
5. **Cache appropriately**: Cache `.sonar/cache` and build dependencies
6. **Quality gate step**: Add separate step for quality gate check

## Usage Instructions

**For SonarArchitectGuide:**
- Include documentation links in responses
- Explain Bitbucket Pipelines concepts when relevant
- Mention pipes vs direct scanner options

**For SonarArchitectLight:**
- Use `web/fetch` to check latest pipe versions
- Create or update `bitbucket-pipelines.yml` with appropriate scanner
- Prefer pipes for CLI scanner projects
- Do NOT include links in responses
