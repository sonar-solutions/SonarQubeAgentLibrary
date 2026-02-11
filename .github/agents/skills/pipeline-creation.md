---
name: pipeline-creation
description: Guidelines for creating and editing SonarQube configuration files. Use this to generate pipeline files, sonar-project.properties, and build configurations.
---

# Pipeline Creation Skill

This skill defines how to create and edit SonarQube configuration files.

## File Creation Guidelines

### Before Creating ANY Files

**PREREQUISITES CHECK:**
- ✅ All prerequisites from prerequisites-gathering skill are confirmed
- ✅ SonarQube type (Cloud/Server) is known
- ✅ CI/CD platform is identified
- ✅ Current branch is detected
- ✅ Project type/build system is identified
- ✅ Project key is provided

**If ANY prerequisite is missing: STOP and gather it first.**

### Fetch Latest Versions

Before creating pipeline configuration files:
1. Use `web/fetch` to retrieve official documentation
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
- Set trigger branches (include current branch if not main/master)
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

### Configuration Best Practices

**Always:**
- Add comments explaining configuration options
- Use environment variables/secrets for sensitive values
- Never hardcode tokens or URLs
- Preserve existing file structure when editing
- Include current branch in triggers if not main/master
- Validate YAML/properties syntax after creation

**Scanner Selection:**
- Maven project → Use Maven plugin
- Gradle project → Use Gradle plugin
- JavaScript/TypeScript/Python/Other → Use SonarScanner CLI

**Coverage Configuration:**
- JavaScript/TypeScript: Include `sonar.javascript.lcov.reportPaths`
- Python: Include `sonar.python.coverage.reportPaths`
- Java: Coverage handled by Maven/Gradle plugins

### Editing Workflow

1. Show user what will be created/changed
2. Explain key configuration options
3. Create or edit the file using `edit` tools
4. Validate syntax
5. Inform user about next steps (secrets configuration)
