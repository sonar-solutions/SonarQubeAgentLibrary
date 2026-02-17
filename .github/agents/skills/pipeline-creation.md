---
name: pipeline-creation
description: Guidelines for creating and editing SonarQube configuration files. Use this to generate pipeline files, sonar-project.properties, and build configurations.
---

# Pipeline Creation Skill

This skill defines how to create and edit SonarQube configuration files.

## File Creation Guidelines

### File Location Rules

**CRITICAL - Project Workspace Boundaries:**
- ✅ Create files within the project workspace only
- ✅ Use relative paths appropriate for each platform (see platform-specific skills)
- ❌ DO NOT create files in parent directories outside the project
- ❌ DO NOT use absolute paths that escape the project workspace

**Platform-specific file locations are defined in the platform skills** (e.g., GitHub Actions uses `.github/workflows/`, GitLab uses root)

### Before Creating ANY Files

**PREREQUISITES CHECK:**
- ✅ All prerequisites from prerequisites-gathering skill are confirmed
- ✅ SonarQube type (Cloud/Server) is known
- ✅ CI/CD platform is identified
- ✅ Project type/build system is identified
- ✅ Project key is provided

**If ANY prerequisite is missing: STOP and gather it first.**

### Retrieve Latest Versions

**How to retrieve version information:**
- Use HTTP GET requests (curl, wget, or similar) to access official SonarQube documentation and scanner version URLs
- For scanner versions, use the Scanner Version Information URLs provided in the scanner skills
- For platform-specific actions/tasks, check the official SonarQube documentation

Before creating pipeline configuration files:
1. Retrieve latest version information from official SonarQube documentation (docs.sonarsource.com) or Scanner Version Information URLs
2. Check for latest action/task versions:
   - GitHub Actions: Check version in examples (e.g., `@v7`)
   - Azure DevOps: Check task versions
   - GitLab/Bitbucket: Check image versions
3. DO NOT guess or use outdated versions

### Files You Can Create/Edit

#### Base Configuration Files

**sonar-project.properties**
- Required for: CLI scanner projects (JavaScript/TypeScript/Python)
- Not required for: Maven/Gradle projects (they use their own config)
- Include:
  - `sonar.projectKey`
  - `sonar.organization` (Cloud only)
  - `sonar.sources`
  - `sonar.tests` (if applicable)
  - `sonar.exclusions` (node_modules, build directories)
  - Coverage report paths (if applicable)

#### CI/CD Pipeline Files

**GitHub Actions: `.github/workflows/sonarqube.yml`**
- Set trigger branches to `main`, `master`, `develop/*`, `feature/*` for comprehensive coverage
- Checkout with `fetch-depth: 0` for full git history
- Configure appropriate scanner based on project type
- Use secrets for `SONAR_TOKEN` and `SONAR_HOST_URL`
- Add caching for SonarQube packages
- Include test coverage steps if applicable

**GitLab CI: `.gitlab-ci.yml` (add SonarQube stage)**
- Create or update with SonarQube job
- Set `GIT_DEPTH: "0"` for full git history
- Configure caching
- Use CI/CD variables for secrets
- Include test coverage in script

**Azure DevOps: `azure-pipelines.yml`**
- Add SonarQube tasks (prepare, run, publish)
- Configure service connection
- Use pipeline variables for secrets
- Include coverage tasks if applicable

**Bitbucket: `bitbucket-pipelines.yml`**
- Add SonarQube scan pipe
- Configure repository variables
- Set clone depth
- Include quality gate step if needed

#### Build Configuration Files

**Maven: `pom.xml`**
- Add SonarQube Maven plugin to `<build><plugins>`
- No need for separate sonar-project.properties
- Properties can be set in pom.xml or passed via command line

**Gradle: `build.gradle` or `build.gradle.kts`**
- Add SonarQube Gradle plugin
- Configure sonarqube block with properties
- No need for separate sonar-project.properties

### Scanner Selection Rules

**By Build System/Project Type:**

1. **Maven Projects**
   - Use Maven SonarQube plugin
   - Run `mvn sonar:sonar` command
   - Configuration in `pom.xml` or command line parameters
   - No separate `sonar-project.properties` needed
   - See: scanner-maven skill

2. **Gradle Projects**
   - Use Gradle SonarQube plugin
   - Run `./gradlew sonar` command
   - Configuration in `build.gradle` or `build.gradle.kts`
   - No separate `sonar-project.properties` needed
   - See: scanner-gradle skill

3. **.NET Projects**
   - Use SonarScanner for .NET
   - Run begin/build/end pattern
   - Configuration via command line parameters
   - See: scanner-dotnet skill

4. **CLI Scanner Projects** (JavaScript/TypeScript/Python/PHP/Go/Ruby/Other)
   - Use SonarScanner CLI
   - Requires `sonar-project.properties` file
   - Platform-specific execution:
     - GitHub Actions: Use `sonarsource/sonarqube-scan-action`
     - GitLab CI: Use `sonarsource/sonar-scanner-cli` Docker image
     - Azure DevOps: Use SonarQube extension tasks
     - Bitbucket: Use SonarCloud/SonarQube pipes
   - See: scanner-cli skill

**Platform Implementation Details:**
- Each platform has specific ways to execute scanners
- Maven/Gradle/.NET: Run build tool commands directly in pipeline
- CLI Scanner: Use platform-specific actions/images/tasks/pipes
- See platform-specific skills for implementation

### Configuration Best Practices

**Always:**
- Add comments explaining configuration options
- Use environment variables/secrets for sensitive values (see: security-practices skill)
- Never hardcode tokens or URLs
- Preserve existing file structure when editing
- Include standard branch patterns in triggers: `main`, `master`, `develop/*`, `feature/*`
- Fetch full git history for accurate blame information
- Validate YAML/properties syntax after creation

**Coverage Configuration:**
- JavaScript/TypeScript: Include `sonar.javascript.lcov.reportPaths`
- Python: Include `sonar.python.coverage.reportPaths`
- Java: Coverage handled by Maven/Gradle plugins automatically

### Editing Workflow

1. Show user what will be created/changed
2. Explain key configuration options
3. Create or edit the file using `edit` tools
4. Validate syntax
5. Inform user about next steps (secrets configuration)
