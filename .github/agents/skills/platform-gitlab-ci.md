---
name: platform-gitlab-ci
description: GitLab CI integration for SonarQube Cloud and Server. Use this when setting up SonarQube analysis with GitLab CI/CD pipelines.
---

# GitLab CI Platform Skill

This skill provides GitLab CI-specific documentation and guidance for SonarQube integration.

**IMPORTANT - Scope of This Skill:**
- This skill is ONLY for GitLab CI pipeline structure and platform-specific configuration
- Provides pipeline examples, job syntax, triggers, variables setup, and GitLab CI-specific features
- For scanner parameters, properties, and configuration: Refer to scanner-* skills (scanner-maven, scanner-gradle, scanner-dotnet, scanner-cli)
- Access pipeline examples from documentation, adapt scanner configuration from scanner skills

## Official Documentation

### SonarQube Cloud
- **Main Documentation**: https://docs.sonarsource.com/sonarqube-cloud/advanced-setup/ci-based-analysis/gitlab-ci

### SonarQube Server
- **Main Documentation**: https://docs.sonarsource.com/sonarqube-server/devops-platform-integration/gitlab-integration/adding-analysis-to-gitlab-ci-cd

## Documentation Fetching Strategy

**Invoke `web/fetch` TOOL to retrieve current examples and versions from official documentation.**

**Fallback Approach:**
- If working with SonarQube Cloud, first fetch from the Cloud documentation URL
- If the Cloud documentation lacks complete pipeline examples, also fetch from the Server documentation URL as a fallback
- If working with SonarQube Server, first fetch from the Server documentation URL
- If the Server documentation lacks complete pipeline examples, also fetch from the Cloud documentation URL as a fallback
- Adapt any server-specific or cloud-specific details when using fallback documentation

## GitLab CI Implementation

### Scanner Implementation

**Scanner selection is defined in pipeline-creation skill. This section covers GitLab CI-specific implementation.**

### When to Use sonar-scanner-cli Docker Image

Use `sonarsource/sonar-scanner-cli` Docker image for **CLI scanner projects only**:
- JavaScript/TypeScript/Python/PHP/Go/Ruby (without Maven/Gradle/.NET)
- Projects that require `sonar-project.properties`
- See: scanner-cli skill for configuration

**Example:**
```yaml
sonarqube-check:
  image: sonarsource/sonar-scanner-cli:latest
  variables:
    SONAR_TOKEN: $SONAR_TOKEN
  script:
    - sonar-scanner
```

### Build Tool Integration

**For Maven/Gradle/.NET projects, use appropriate Docker images and run scanner commands:**
- **Maven**: Use `maven` image with `mvn sonar:sonar` (see: scanner-maven skill)
- **Gradle**: Use `gradle` image with `./gradlew sonar` (see: scanner-gradle skill)
- **.NET**: Use `mcr.microsoft.com/dotnet/sdk` image with `dotnet sonarscanner` (see: scanner-dotnet skill)

Fetch examples from official documentation to get latest versions and configuration.

## Platform-Specific Configuration

### Variables Configuration
- **Location**: Project → Settings → CI/CD → Variables
- **Required variables**:
  - `SONAR_TOKEN` (mark as Masked and Protected)
  - `SONAR_HOST_URL` (Server only, mark as Protected)
- See: security-practices and devops-setup-instructions skills

### Git Depth
- Always set `GIT_DEPTH: "0"` for full git history
- Can be set as variable or in job

### Caching
- Cache `.sonar/cache` to speed up analysis
- Define cache key and paths in job configuration

### Pipeline Triggers
- Use `only` or `rules` to trigger on specific branches
- Include `merge_requests` for MR analysis

## Common Configurations

### Pull Request Decoration
Configure GitLab integration in SonarQube for automatic MR decoration.

### Quality Gate Integration
Add a separate job to check quality gate status if needed.

## Best Practices

1. **Use specific Docker images**: Pin to major versions (e.g., `maven:3.9-openjdk-17`)
2. **Cache appropriately**: Cache `.sonar/cache` to speed up subsequent runs
3. **Protect variables**: Mark `SONAR_TOKEN` as Masked and Protected
4. **Full git history**: Always set `GIT_DEPTH: "0"`
5. **Merge request analysis**: Include `merge_requests` in `only` clause

## Usage Instructions

**For SonarArchitectGuide:**
- Include documentation links in responses
- Explain GitLab CI concepts when relevant

**For SonarArchitectLight:**
- Invoke `web/fetch` TOOL to check latest scanner versions
- Update or create `.gitlab-ci.yml` with appropriate scanner
- Do NOT include links in responses
