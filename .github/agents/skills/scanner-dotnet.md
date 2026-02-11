---
name: scanner-dotnet
description: .NET scanner configuration for SonarQube. Use this for C#, VB.NET, and F# projects.
---

# .NET Scanner Skill

This skill provides .NET-specific scanner documentation and configuration guidance.

## Official Documentation

### SonarQube Server
- https://docs.sonarsource.com/sonarqube-server/analyzing-source-code/scanners/dotnet/using

### SonarQube Cloud
- SonarQube Cloud uses the same .NET scanner as Server

## Scanner Overview

**Use `web/fetch` to get current examples and versions from official documentation.**

The .NET scanner is a command-line tool that integrates SonarQube analysis for C#, VB.NET, and F# projects.

### Key Concepts
- Three-step process: begin analysis → build project → end analysis
- Must be installed as .NET global or local tool
- Works with .NET Core, .NET Framework, and .NET 5+
- Supports solution files with multiple projects
- Integrates with coverlet or VSTest for code coverage
- Wraps MSBuild to collect analysis data during compilation

### Installation Options
- **Global tool**: Installed system-wide, accessible from any directory
- **Local tool**: Installed per project using tool manifest (recommended for CI/CD)

### Configuration Options
- **Command-line parameters**: Pass configuration via `/k:`, `/d:` parameters
- **Begin step**: Configure project key, host URL, organization, coverage paths
- **End step**: Upload results to SonarQube server

## Scanner Usage

**Fetch current command examples from official documentation.**

### Three-Step Process

1. **Begin Analysis**: Initialize scanner with project configuration
   - Specify project key (`/k:`)
   - Set host URL and token (`/d:sonar.host.url`, `/d:sonar.token`)
   - Configure organization for Cloud (`/o:`)
   - Set coverage report paths

2. **Build Project**: Compile with dotnet build
   - Scanner intercepts build to collect analysis data
   - Must run between begin and end steps

3. **End Analysis**: Upload results to SonarQube
   - Pass token again for authentication
   - Results uploaded to server for processing

## Code Coverage

### Coverage Tools
- **coverlet**: Popular cross-platform coverage tool for .NET
- **VSTest**: Built-in Visual Studio test coverage

### Coverlet Integration
- Install coverlet.msbuild package
- Collect coverage during test execution
- Configure OpenCover or Cobertura format
- Specify coverage report path in begin step using `/d:sonar.cs.opencover.reportsPaths`

### VSTest Integration
- Use `--collect:"XPlat Code Coverage"` with dotnet test
- Configure coverage XML report paths in begin step

**Fetch coverage configuration examples from official documentation.**

## Common Configuration Parameters

**Fetch current parameter examples from official documentation.**

### Key Parameters:
- **Project identification**: `/k:"project-key"`, `/n:"Project Name"`, `/v:"1.0"`
- **Organization** (Cloud only): `/o:"organization-key"`
- **Host and auth**: `/d:sonar.host.url`, `/d:sonar.token`
- **Coverage reports**: `/d:sonar.cs.opencover.reportsPaths`, `/d:sonar.cs.vscoveragexml.reportsPaths`
- **Exclusions**: `/d:sonar.exclusions`, `/d:sonar.test.exclusions`
- **Roslyn**: `/d:sonar.cs.roslyn.ignoreIssues`

## Solution with Multiple Projects

- Scanner automatically detects all projects in a solution
- Run analysis on .sln file for multi-project solutions
- Each project analyzed as part of the solution
- Single quality gate for entire solution
- Use same three-step process (begin → build solution → end)

## Common Issues

### Issue: Scanner not found
**Solution:** Install globally or use local tool manifest

### Issue: No coverage reported
**Solution:** Ensure coverage format is correct and path matches

### Issue: Build output not found
**Solution:** Must run `dotnet build` between begin/end

## Best Practices

1. **Use local tool manifest**: Better for reproducible builds in CI/CD environments
2. **Collect coverage**: Always include code coverage with coverlet or VSTest
3. **Token security**: Use environment variables for tokens, never hardcode
4. **Build before end**: Always run `dotnet build` between begin and end steps
5. **Specify coverage paths**: Use explicit coverage report paths with wildcards
6. **Update regularly**: Keep scanner tool updated with `dotnet tool update`
7. **Exclude generated code**: Exclude bin/, obj/, and auto-generated files
8. **Solution-level analysis**: Analyze entire solution for multi-project setups
9. **Test before analysis**: Run tests with coverage collection before end step
10. **Check scanner version**: Use `web/fetch` to verify compatible scanner versions

## Platform Integration

See platform-specific skills for CI/CD integration:
- **platform-github-actions**: GitHub Actions with .NET
- **platform-gitlab-ci**: GitLab CI with .NET
- **platform-azure-devops**: Azure Pipelines with .NET
- **platform-bitbucket**: Bitbucket Pipelines with .NET

## Configuration Workflow

**CRITICAL: Follow this workflow when setting up .NET projects:**

1. **Locate solution/project files**: Use `search` to find `.sln`, `.csproj`, or `.vbproj` files
2. **Note file location**: Scanner commands must run from directory containing solution/project file
   - Example: If MySolution.sln is in `src/`, all three commands run from `src/`
3. **Check for tool manifest**: Look for `.config/dotnet-tools.json` (indicates local tool setup)
4. **Verify scanner version**: 
   - If tool manifest exists: Use `web/fetch` to get latest version, update if outdated
   - If no manifest: Commands will use globally installed scanner or need installation
5. **Detect test projects**: Look for `*Test.csproj`, `*.Tests.csproj` files to enable coverage
6. **Working directory in CI/CD**: Set to directory containing .sln file
   - All three steps (begin/build/end) must run from same directory

## Environment Variables

**Required:**
- `SONAR_TOKEN`: Authentication token

**Optional:**
- `SONAR_HOST_URL`: Can be passed as parameter instead
- `SONAR_ORGANIZATION`: Can be passed as parameter instead

## Usage Instructions

**For SonarArchitectGuide:**
- Include documentation link in responses
- Explain .NET scanner three-step process
- Mention code coverage setup

**For SonarArchitectLight:**
- **Step 1**: Search for .sln, .csproj files to locate solution/project
- **Step 2**: Note directory containing solution file (working directory for commands)
- **Step 3**: Check for .config/dotnet-tools.json
- **Step 4**: Use `web/fetch` to get latest scanner version
- **Step 5**: Search for test projects (*Test.csproj, *.Tests.csproj)
- **Step 6**: Create CI/CD with begin/build/end pattern, all from same working directory
- **Step 7**: Include coverage collection if test projects found
