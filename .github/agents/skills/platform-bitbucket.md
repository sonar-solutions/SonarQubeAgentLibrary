---
name: platform-bitbucket
description: Bitbucket Pipelines integration for SonarQube Cloud and Server. Use this when setting up SonarQube analysis with Bitbucket Cloud Pipelines.
---

# Bitbucket Pipelines Platform Skill

This skill provides Bitbucket Pipelines-specific documentation and guidance for SonarQube integration.

## Official Documentation

### SonarQube Cloud
- **Main Documentation**: https://docs.sonarsource.com/sonarqube-cloud/advanced-setup/ci-based-analysis/bitbucket-pipelines-for-sonarcloud
- **Scan Pipe Repository**: https://bitbucket.org/sonarsource/sonarcloud-scan/src/master/
- **Quality Gate Pipe**: https://bitbucket.org/sonarsource/sonarcloud-quality-gate/src/master/

### SonarQube Server
- **Main Documentation**: https://docs.sonarsource.com/sonarqube-server/devops-platform-integration/bitbucket-integration/bitbucket-cloud-integration/bitbucket-pipelines
- **Scan Pipe Repository**: https://bitbucket.org/sonarsource/sonarqube-scan/src/master/
- **Quality Gate Pipe**: https://bitbucket.org/sonarsource/sonarqube-quality-gate/src/master/

## Scanner Selection by Language

**Use `web/fetch` to get current examples from official documentation and pipe repositories.**

### When to Use SonarQube Pipes

**ONLY use SonarQube/SonarCloud pipes for CLI scanner projects:**
- **JavaScript/TypeScript**: Projects without Maven/Gradle/.NET
- **Python**: Projects without Maven/Gradle/.NET
- **PHP, Go, Ruby, etc.**: Projects using CLI scanner
- **Pipes available**:
  - SonarQube Cloud: `sonarsource/sonarcloud-scan` and `sonarsource/sonarcloud-quality-gate`
  - SonarQube Server: `sonarsource/sonarqube-scan` and `sonarsource/sonarqube-quality-gate`
- See: scanner-cli skill

**DO NOT use pipes for Maven/Gradle/.NET projects:**
- These use their own build tools to run analysis
- Pipes are not needed and should not be used

### Scanner-Specific Setup

**Build Tool Projects (run commands directly):**
- **Java (Maven)**: Use Maven within Bitbucket step with `mvn sonar:sonar`. See: scanner-maven skill
- **Java (Gradle)**: Use Gradle within Bitbucket step with `./gradlew sonar`. See: scanner-gradle skill
- **.NET**: Use dotnet-sonarscanner within Bitbucket step. See: scanner-dotnet skill

**CLI Scanner Projects (use pipes):**
- **JavaScript/TypeScript/Python/Other**: Use official SonarCloud/SonarQube pipes. See: scanner-cli skill

**Check pipe repositories above for latest versions.**

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
