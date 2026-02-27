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
- Access pipeline examples from documentation, adapt scanner configuration from scanner skills

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

**IMPORTANT - SonarQube documentation pages require JavaScript rendering:**
SonarQube documentation pages are dynamically rendered. A raw HTTP request (curl, wget) will NOT return the actual page content.

Use your environment's browser-capable fetch tool to access these URLs (including pipe repository pages):
- ❌ Do NOT use curl or wget for docs.sonarsource.com pages
- ✅ USE whichever tool in your environment can render JavaScript pages (e.g., web/fetch, WebFetch, url_context, or equivalent)

**Fallback Approach:**
- If working with SonarQube Cloud, first fetch from the Cloud documentation URL
- If the Cloud documentation lacks complete pipeline examples, also fetch from the Server documentation URL as a fallback
- If working with SonarQube Server, first fetch from the Server documentation URL
- If the Server documentation lacks complete pipeline examples, also fetch from the Cloud documentation URL as a fallback
- Adapt any server-specific or cloud-specific details when using fallback documentation

## Bitbucket Pipelines Implementation

### Scanner Approach Determination

Based on the project type identified in prerequisites-gathering, determine the scanner approach **before** invoking pipeline-creation:

- **Maven project** → `scanner_approach: maven` — run `mvn sonar:sonar` directly in a step, do NOT use pipes
- **Gradle project** → `scanner_approach: gradle` — run `./gradlew sonar` directly in a step, do NOT use pipes
- **.NET project** → `scanner_approach: dotnet` — run `dotnet sonarscanner` begin/build/end directly in a step, do NOT use pipes
- **All others (JavaScript/TypeScript/Python/PHP/Go/Ruby...)** → `scanner_approach: pipe` — use official SonarCloud/SonarQube scan pipe

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
2. **Check pipe versions**: Use a browser-capable fetch tool to verify latest pipe versions in official documentation
3. **Secure variables**: Always mark sensitive variables as Secured
4. **Full clone**: Use `depth: full` for accurate blame information
5. **Cache appropriately**: Cache `.sonar/cache` and build dependencies
6. **Quality gate step**: Add separate step for quality gate check

## Processing Steps

**Execute these steps in order before handing off to pipeline-creation:**

1. Determine `scanner_approach` from the project type (see Scanner Approach Determination above)
2. ⛔ STOP — Fetch the **Main Documentation** URL now:
   - If `scanner_approach` is `pipe`: also fetch the appropriate **Scan Pipe Repository** URL and extract the latest pipe version — this is the `tool_version` to report and use in the pipeline
   - If `scanner_approach` is `maven`, `gradle`, or `dotnet`: extract the corresponding step example from the documentation — use this as the reference template when creating the pipeline. No pipe version applies.
   Do NOT proceed until the documentation has been fetched.
3. Collect pipeline structure details (clone depth, branch config, cache) per Platform-Specific Configuration section above
4. List required repository variables based on SonarQube type (Cloud vs Server)
5. Pass all collected values to pipeline-creation via the Output Contract below

## Output Contract

After processing this skill, provide the following to pipeline-creation:

- `scanner_approach`: one of `pipe`, `maven`, `gradle`, `dotnet`
- `tool_version`: latest version of the scan pipe (only when `scanner_approach` is `pipe`) — **must be fetched in Processing Steps above before reporting**:
  - SonarQube Cloud: `sonarsource/sonarcloud-scan` version — fetch from Scan Pipe Repository
  - SonarQube Server: `sonarsource/sonarqube-scan` version — fetch from Scan Pipe Repository
- `workflow_structure`:
  - Clone depth: `full`
  - Branch and PR pipeline config
  - Cache: `.sonar/cache`
- `required_secrets`:
  - `SONAR_TOKEN` (always, mark as Secured)
  - `SONAR_HOST_URL` (Server only, mark as Secured)
- `reference_docs`: documentation URLs fetched during processing — for use by pipeline-creation if additional detail is needed:
  - SonarQube Cloud: https://docs.sonarsource.com/sonarqube-cloud/advanced-setup/ci-based-analysis/bitbucket-pipelines-for-sonarcloud
  - SonarQube Server: https://docs.sonarsource.com/sonarqube-server/devops-platform-integration/bitbucket-integration/bitbucket-cloud-integration/bitbucket-pipelines

## Usage Instructions

**For SonarArchitectGuide:**
- Include documentation links in responses
- Explain Bitbucket Pipelines concepts when relevant
- Mention pipes vs direct scanner options

**For SonarArchitectLight:**
- Use a browser-capable fetch tool to check latest pipe versions in official documentation
- Create or update `bitbucket-pipelines.yml` with appropriate scanner
- Prefer pipes for CLI scanner projects
- Do NOT include links in responses
