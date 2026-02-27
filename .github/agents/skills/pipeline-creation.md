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

### Version Information

**Use versions from the platform skill Output Contract. Only fetch if not already provided.**

- If the platform skill Output Contract includes `tool_version`: use that value directly — it was already fetched during platform skill processing
- If `tool_version` is missing or unknown: fetch it now using the `reference_docs` URLs provided in the Output Contract (use a browser-capable fetch tool for docs.sonarsource.com pages)
- For scanner-specific versions (Maven plugin, Gradle plugin, .NET scanner): use the `tool_version` from the scanner skill Output Contract, or fetch from the Scanner Version Information URL in the relevant scanner skill if missing
- DO NOT guess or use hardcoded versions — always use a confirmed value from either the Output Contract or a live fetch

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

### Input Contract

**pipeline-creation assembles files from decisions already made by platform and scanner skills. Before creating any files, verify the following have been determined:**

**From platform-* skill:**
- `scanner_approach`: Which execution method the platform uses (e.g. `sonarqube-scan-action`, `maven`, `gradle`, `dotnet`, `docker-image`, `pipe`)
- `tool_version`: Latest version of the platform action/task/image/pipe (if applicable)
- `workflow_structure`: Triggers, job/stage structure, checkout config, cache config
- `required_secrets`: List of secrets/variables the user must configure

**From scanner-* skill:**
- `build_commands`: Exact commands to run (including test/coverage steps)
- `scanner_parameters`: Key `sonar.*` properties or command-line parameters
- `required_files`: Any files to create or modify (e.g. `sonar-project.properties`, `pom.xml` changes)
- `working_directory`: Directory from which scanner commands must run
- `runtime_requirements`: JDK version, .NET SDK version, etc. (if applicable)

**If any of these are missing: invoke the appropriate platform or scanner skill first before proceeding.**

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
