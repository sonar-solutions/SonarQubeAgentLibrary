---
name: platform-gitlab-ci
description: GitLab CI integration for SonarQube Cloud and Server. Use this when setting up SonarQube analysis with GitLab CI/CD pipelines.
---

# GitLab CI Platform Skill

This skill provides GitLab CI-specific documentation and guidance for SonarQube integration.

## Official Documentation

### SonarQube Cloud
- **Main Documentation**: https://docs.sonarsource.com/sonarqube-cloud/advanced-setup/ci-based-analysis/gitlab-ci

### SonarQube Server
- **Main Documentation**: https://docs.sonarsource.com/sonarqube-server/devops-platform-integration/gitlab-integration/adding-analysis-to-gitlab-ci-cd

## Scanner Selection by Language

**Use `web/fetch` to get current examples from official documentation.**

- **Java (Maven)**: Use Maven within GitLab CI job. See: scanner-maven skill
- **Java (Gradle)**: Use Gradle within GitLab CI job. See: scanner-gradle skill
- **.NET**: Use dotnet-sonarscanner within GitLab CI job. See: scanner-dotnet skill
- **JavaScript/TypeScript/Python/Other**: Use sonar-scanner-cli Docker image. See: scanner-cli skill

Fetch examples from official documentation above to get latest versions and configuration.

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
- Use `web/fetch` to check latest scanner versions
- Update or create `.gitlab-ci.yml` with appropriate scanner
- Do NOT include links in responses
