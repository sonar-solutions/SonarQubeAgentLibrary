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

**IMPORTANT - SonarQube documentation pages require JavaScript rendering:**
SonarQube documentation pages are dynamically rendered. A raw HTTP request (curl, wget) will NOT return the actual page content.

Use your environment's browser-capable fetch tool to access these URLs:
- ❌ Do NOT use curl or wget for docs.sonarsource.com pages
- ✅ USE whichever tool in your environment can render JavaScript pages (e.g., web/fetch, WebFetch, url_context, or equivalent)

**Fallback Approach:**
- If working with SonarQube Cloud, first fetch from the Cloud documentation URL
- If the Cloud documentation lacks complete pipeline examples, also fetch from the Server documentation URL as a fallback
- If working with SonarQube Server, first fetch from the Server documentation URL
- If the Server documentation lacks complete pipeline examples, also fetch from the Cloud documentation URL as a fallback
- Adapt any server-specific or cloud-specific details when using fallback documentation

## GitLab CI Implementation

### Scanner Approach Determination

Based on the project type identified in prerequisites-gathering, determine the scanner approach **before** invoking pipeline-creation:

- **Maven project** → `scanner_approach: maven` — use `maven` Docker image, run `mvn sonar:sonar` directly, do NOT use `sonar-scanner-cli` image
- **Gradle project** → `scanner_approach: gradle` — use `gradle` Docker image, run `./gradlew sonar` directly, do NOT use `sonar-scanner-cli` image
- **.NET project** → `scanner_approach: dotnet` — use `mcr.microsoft.com/dotnet/sdk` image, run `dotnet sonarscanner` begin/build/end directly
- **All others (JavaScript/TypeScript/Python/PHP/Go/Ruby...)** → `scanner_approach: docker-image` — use `sonarsource/sonar-scanner-cli` Docker image

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

## Processing Steps

**Execute these steps in order before handing off to pipeline-creation:**

1. Determine `scanner_approach` from the project type (see Scanner Approach Determination above)
2. ⛔ STOP — Fetch the **Main Documentation** URL now:
   - If `scanner_approach` is `docker-image`: extract the latest `sonarsource/sonar-scanner-cli` image tag from the examples — this is the `tool_version` to report and use in the pipeline
   - If `scanner_approach` is `maven`, `gradle`, or `dotnet`: extract the corresponding job example from the documentation — use this as the reference template when creating the pipeline. No image version applies.
   Do NOT proceed until the documentation has been fetched.
3. Collect pipeline structure details (git depth, triggers, cache) per Platform-Specific Configuration section above
4. List required variables based on SonarQube type (Cloud vs Server)
5. Pass all collected values to pipeline-creation via the Output Contract below

## Output Contract

After processing this skill, provide the following to pipeline-creation:

- `scanner_approach`: one of `docker-image`, `maven`, `gradle`, `dotnet`
- `tool_version`: latest tag of `sonarsource/sonar-scanner-cli` image (only when `scanner_approach` is `docker-image`) — **must be fetched in Processing Steps above before reporting**
- `workflow_structure`:
  - Git depth: `GIT_DEPTH: "0"`
  - Trigger: branches + merge requests
  - Cache: `.sonar/cache`
- `required_secrets`:
  - `SONAR_TOKEN` (always, mark as Masked and Protected)
  - `SONAR_HOST_URL` (Server only, mark as Protected)
- `reference_docs`: documentation URLs fetched during processing — for use by pipeline-creation if additional detail is needed:
  - SonarQube Cloud: https://docs.sonarsource.com/sonarqube-cloud/advanced-setup/ci-based-analysis/gitlab-ci
  - SonarQube Server: https://docs.sonarsource.com/sonarqube-server/devops-platform-integration/gitlab-integration/adding-analysis-to-gitlab-ci-cd

## Usage Instructions

**For SonarArchitectGuide:**
- Include documentation links in responses
- Explain GitLab CI concepts when relevant

**For SonarArchitectLight:**
- Use a browser-capable fetch tool to check latest scanner versions in official documentation
- Update or create `.gitlab-ci.yml` with appropriate scanner
- Do NOT include links in responses
