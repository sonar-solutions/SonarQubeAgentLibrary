# SonarArchitectLight — Agent Redesign Brief

This document describes the current agent structure, its intended design, known limitations, and the constraints to enforce in a redesigned version.

---

## What the Agent Does

SonarArchitectLight is a DevOps automation agent that sets up SonarQube CI/CD pipeline analysis for a user's project. Given a project repository and a few user inputs, it:

1. Detects the project type and build system
2. Gathers required configuration inputs from the user
3. Fetches latest versions and workflow examples from official SonarQube documentation
4. Creates the pipeline configuration file(s) and any supporting files
5. Tells the user what secrets/variables to configure in their DevOps platform

The agent is action-oriented and concise — it creates files directly rather than explaining how to do it.

---

## Skill Chain (Intended Execution Order)

```
project-detection
      ↓
prerequisites-gathering
      ↓
platform-{github-actions | gitlab-ci | azure-devops | bitbucket}
      ↓
scanner-{maven | gradle | dotnet | cli}
      ↓
pipeline-creation
      ↓
devops-setup-instructions
```

Each skill has a defined responsibility and is meant to hand off structured outputs to the next skill.

---

## Skill Responsibilities

### `project-detection`
- Scans the project for build system files (`pom.xml`, `build.gradle`, `package.json`, `.csproj`, etc.)
- Detects the CI/CD platform from existing workflow files
- Returns: project type, build system, CI/CD platform, existing SonarQube config presence
- Does NOT ask the user anything — autonomous detection only

### `prerequisites-gathering`
- Validates or collects all required inputs before any files are created
- Required inputs: SonarQube type (Cloud/Server), CI/CD platform, project key, organization key (Cloud only), Cloud instance (US: sonarqube.us or EU: sonarcloud.io)
- MUST run every time — even if inputs are provided upfront (validation mode)
- Blocks progress until all prerequisites are confirmed

### `platform-{name}`
**This is where scanner approach selection and version fetching must happen.**

Responsibilities:
- Determine `scanner_approach` based on project type:
  - Maven → `maven` (run `mvn sonar:sonar` directly)
  - Gradle → `gradle` (run `./gradlew sonar` directly)
  - .NET → `dotnet` (run `dotnet sonarscanner` begin/build/end)
  - Everything else → platform-specific action/image/pipe (e.g. `sonarqube-scan-action` on GitHub Actions)
- **Fetch official documentation** to get:
  - The latest action/image/pipe version (when `scanner_approach` is the platform-specific tool)
  - The workflow example for build tool approaches (Maven/Gradle/.NET) to use as reference template
- Produce an **Output Contract** for `pipeline-creation` containing: `scanner_approach`, `tool_version` (if applicable), `workflow_structure`, `required_secrets`, `reference_docs`

### `scanner-{name}`
**This is where scanner-specific configuration is determined.**

Responsibilities:
- Determine what build commands to run (including test/coverage steps before scanning)
- Identify what files need to be created or modified (`sonar-project.properties`, `pom.xml`, `build.gradle`)
- Specify key scanner parameters or properties needed
- Produce an **Output Contract** for `pipeline-creation` containing: `build_commands`, `scanner_parameters`, `required_files`, `working_directory`, `runtime_requirements`, `tool_version` (plugin/scanner version from official version JSON endpoint)

### `pipeline-creation`
**Assembly only — no decisions.**

Responsibilities:
- Receive the Output Contract from the platform skill and scanner skill
- Use `tool_version` from the Output Contract directly if provided; only fetch if it is missing (using `reference_docs` URLs from the Output Contract)
- Create the CI/CD pipeline file and any supporting files
- Apply security practices (secrets, never hardcode credentials)
- Does NOT make scanner selection decisions — those come from the platform skill

### `devops-setup-instructions`
- Tells the user what secrets/variables to configure and where
- Platform-specific instructions (e.g. GitHub Actions Secrets, GitLab CI Variables, Azure DevOps service connection)
- Brief and actionable — no "push and run" instructions

---

## Output Contract Pattern

The Output Contract is the key mechanism for structured handoff between skills. Each platform and scanner skill must produce one before `pipeline-creation` runs.

### Platform skill Output Contract fields:
- `scanner_approach` — which execution method to use
- `tool_version` — version of the platform action/image/pipe (if applicable, must be fetched during platform skill execution)
- `workflow_structure` — triggers, checkout config, cache config
- `required_secrets` — secrets the user must configure
- `reference_docs` — documentation URLs already fetched, passed to `pipeline-creation` as fallback

### Scanner skill Output Contract fields:
- `build_commands` — exact commands to run (test + scan)
- `scanner_parameters` — key `sonar.*` properties
- `required_files` — files to create/modify with content
- `working_directory` — where commands must run from
- `runtime_requirements` — JDK, .NET SDK version (if applicable)
- `tool_version` — scanner plugin version (fetched from official JSON endpoint)

---

## Documentation Fetching Rules

SonarQube documentation pages at `docs.sonarsource.com` require JavaScript rendering and **cannot** be fetched with `curl` or `wget`. The agent must use a browser-capable fetch tool.

Scanner version JSON endpoints at `downloads.sonarsource.com` are static files and **can** be fetched with `curl`.

| Source | Tool |
|--------|------|
| `docs.sonarsource.com` | Browser-capable fetch (web/fetch, WebFetch, url_context, or equivalent) |
| `downloads.sonarsource.com` (JSON) | `curl` or `wget` OK |

### Version fetch responsibility by skill:
- **Platform skill** → fetches action/image/pipe version from `docs.sonarsource.com` (browser tool required)
- **Scanner skill** → fetches plugin/scanner version from `downloads.sonarsource.com` (curl OK)
- **pipeline-creation** → uses versions from Output Contract; only fetches if version is missing

---

## Scanner Approach by Platform

| Project Type | GitHub Actions | GitLab CI | Azure DevOps | Bitbucket |
|---|---|---|---|---|
| Maven | `mvn sonar:sonar` | `mvn sonar:sonar` | SonarQubePrepare (Maven mode) | `mvn sonar:sonar` |
| Gradle | `./gradlew sonar` | `./gradlew sonar` | SonarQubePrepare (Gradle mode) | `./gradlew sonar` |
| .NET | `dotnet sonarscanner` begin/build/end | `dotnet sonarscanner` begin/build/end | SonarQubePrepare (MSBuild mode) | `dotnet sonarscanner` begin/build/end |
| JS/TS/Python/other | `sonarsource/sonarqube-scan-action` | `sonarsource/sonar-scanner-cli` image | SonarQubePrepare (CLI mode) | `sonarsource/sonarcloud-scan` or `sonarqube-scan` pipe |

Azure DevOps is a special case — extension tasks are used for ALL project types, just with different modes. Every approach still requires fetching the task version.

---

## Known Limitations to Fix in Redesign

### 1. Version fetching happens too late
**Problem:** The agent reads the platform skill but does not actually **stop and fetch** the version during that skill. It defers to `pipeline-creation`, which was still instructing the agent to fetch versions at file-creation time. By then, the platform skill's intent is lost.

**Fix:** The platform skill must contain an explicit, imperative processing step (e.g. "⛔ STOP — fetch this URL now") that cannot be deferred. `pipeline-creation` should trust the Output Contract and only fetch as a fallback.

### 2. Scanner selection was duplicated
**Problem:** Scanner selection logic existed in both the platform skills and `pipeline-creation`. The agent could skip platform skills entirely and still get a result from `pipeline-creation`.

**Fix:** Remove scanner selection from `pipeline-creation` entirely. Platform skills own this decision.

### 3. Platform skills were passive, not imperative
**Problem:** Platform skills described what to do ("fetch from docs") as informational statements rather than required actions. The agent treated them as reference material, not instructions.

**Fix:** Use imperative language and hard stops (`⛔ STOP`) within the platform skill processing steps, not just in the Output Contract description.

### 4. No separation between "what to fetch" vs "what to report"
**Problem:** The Output Contract listed `tool_version: fetch from Main Documentation` — this reads like a description of the field, not a mandatory action. The agent reported it as "will fetch later."

**Fix:** Separate the fetch action (in Processing Steps with a ⛔ STOP) from the reporting format (in the Output Contract). The Output Contract should say "must be fetched in Processing Steps above before reporting."

---

## Design Constraints for New Agent

1. **Skills are executed sequentially and completely** — each skill must finish its responsibilities (including any doc fetches) before the next skill starts
2. **Output Contract is mandatory** — no skill can hand off to `pipeline-creation` without producing a complete Output Contract
3. **`pipeline-creation` makes zero decisions** — it receives and assembles; all scanner selection and version fetching happens upstream
4. **Version fetching is always live** — never use hardcoded or guessed versions
5. **Documentation fetching uses the right tool** — `docs.sonarsource.com` always requires browser-capable tool; this must be stated wherever a URL appears
6. **Prerequisites are always validated** — `prerequisites-gathering` runs every time without exception
7. **No duplicate logic across skills** — if a decision is in a platform skill, it must not also appear in `pipeline-creation`

---

## Files in Scope

```
.github/agents/
  SonarArchitectLight.agent.md       # Main agent definition
  skills/
    project-detection.md
    prerequisites-gathering.md
    platform-github-actions.md
    platform-gitlab-ci.md
    platform-azure-devops.md
    platform-bitbucket.md
    scanner-maven.md
    scanner-gradle.md
    scanner-dotnet.md
    scanner-cli.md
    pipeline-creation.md
    security-practices.md
    devops-setup-instructions.md
```
