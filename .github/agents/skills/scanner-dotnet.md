---
name: scanner-dotnet
description: .NET scanner configuration for SonarQube. Use this for C#, VB.NET, and F# projects. Fetches current scanner version and produces an Output Contract.
---

# .NET Scanner Skill

## Purpose

Configure SonarQube integration for .NET projects. This skill locates the solution or project file, fetches the latest scanner version, verifies or creates configuration, and produces an Output Contract for the platform skill and pipeline-creation.

## Official Documentation

| SonarQube Type | Documentation URL |
|---|---|
| Server | `https://docs.sonarsource.com/sonarqube-server/analyzing-source-code/scanners/dotnet/using` |
| Cloud | Same .NET scanner documentation applies for both Cloud and Server |

**Version JSON:**
`https://downloads.sonarsource.com/sonarqube/update/scannermsbuild.json`

## Documentation Fetching Strategy

| URL pattern | Required tool |
|---|---|
| `docs.sonarsource.com` | Use your environment's **browser-capable fetch tool** (e.g., web/fetch, WebFetch, url_context, or equivalent). **NOT curl.** |
| `downloads.sonarsource.com/sonarqube/update/scannermsbuild.json` | **curl or wget is acceptable** |

## Processing Steps

Execute these steps in order. Do not skip any step.

**Step 1:** Locate the solution or project file using file search tools.
- Look for `.sln` files first (preferred for multi-project solutions)
- If no `.sln`, look for `.csproj`, `.vbproj`, or `.fsproj`
- Note the directory containing the solution/project file — all three steps (begin/build/end) must run from this directory

**Step 2:** Check for existing configuration:
- Look for `.config/dotnet-tools.json` — indicates local tool installation
- If tool manifest exists, note the current scanner version

**Step 3:** ⛔ STOP — Fetch the latest scanner version NOW.

Run: `curl -s https://downloads.sonarsource.com/sonarqube/update/scannermsbuild.json`

Extract the latest version from the JSON response.

**Completion condition:** Do not proceed to Step 4 until you have the exact version string from the JSON. If the curl command fails, use the browser-capable fetch tool on the Server documentation URL as fallback.

**Step 4:** Detect test projects for coverage configuration:
- Look for `*Test.csproj`, `*.Tests.csproj`, or `*Spec.csproj` files
- If test projects found, include coverage collection in the build command

**Step 5:** Populate the Output Contract below.

## Build Commands — Three-Step Pattern

All .NET SonarQube analysis follows this mandatory three-step sequence, all executed from the same working directory:

```bash
# Step 1: Begin analysis
dotnet sonarscanner begin \
  /k:"PROJECT_KEY" \
  /o:"ORG_KEY" \        # Cloud only
  /d:sonar.token="$SONAR_TOKEN" \
  /d:sonar.host.url="$SONAR_HOST_URL" \
  /d:sonar.cs.opencover.reportsPaths="**/coverage.opencover.xml"

# Step 2: Build
dotnet build --no-incremental

# Step 3: Run tests with coverage (if test projects exist)
dotnet test --collect:"XPlat Code Coverage" --results-directory ./TestResults

# Step 4: End analysis
dotnet sonarscanner end /d:sonar.token="$SONAR_TOKEN"
```

**Note:** `begin` and `end` steps must reference the same `sonar.token`.

## Installation

The scanner must be installed before use. For CI/CD, local tool installation is recommended:

```bash
# Install as local tool (add to .config/dotnet-tools.json)
dotnet tool install dotnet-sonarscanner

# Or install globally
dotnet tool install --global dotnet-sonarscanner --version X.Y.Z
```

## Coverage Configuration

| Coverage tool | Property | Report format |
|---|---|---|
| Coverlet | `/d:sonar.cs.opencover.reportsPaths="**/coverage.opencover.xml"` | OpenCover XML |
| VSTest | `/d:sonar.cs.vscoveragexml.reportsPaths="**/*.coveragexml"` | VSCoverage XML |

Add to `dotnet test`:
```bash
dotnet test --collect:"XPlat Code Coverage" -- DataCollectionRunSettings.DataCollectors.DataCollector.Configuration.Format=opencover
```

## Runtime Requirements

| Field | Value |
|---|---|
| .NET SDK | The version used by the project (detected from `global.json` or `.csproj` `<TargetFramework>`) |
| Scanner version | Fetched in Step 3 |

## Output Contract

This contract must be fully populated before pipeline-creation runs. No field may contain "TODO", "fetch from docs", or a placeholder.

```
scanner: dotnet
tool_version: [exact version from Step 3, e.g., "9.0.0"]        ← resolved in Step 3
build_commands:
  - "dotnet sonarscanner begin /k:\"PROJECT_KEY\" ..."
  - "dotnet build --no-incremental"
  - "dotnet test ..."      # if test projects found
  - "dotnet sonarscanner end /d:sonar.token=\"$SONAR_TOKEN\""
solution_file: [path to .sln or .csproj, e.g., "src/MySolution.sln"]
working_directory: [directory containing .sln or .csproj]
dotnet_sdk_version: [version required by project, e.g., "8.0"]
test_projects_found: [yes | no]
coverage_format: [opencover | vscoverage | none]
sonar_project_key: [value from prerequisites]
sonar_organization: [value from prerequisites, or "N/A" for Server]
required_files: [list of files modified or created]
```

## Usage Instructions

**For SonarArchitectGuide:** Include documentation links and explain the three-step .NET scanner process when relevant.

**For SonarArchitectLight:** Execute all Processing Steps silently. Produce the Output Contract. Do not include links or explanations in responses.
