---
name: scanner-cli
description: SonarScanner CLI configuration for SonarQube. Use this for JavaScript, TypeScript, Python, Go, PHP, and other languages not using Maven/Gradle/.NET.
---

# SonarScanner CLI Skill

This skill provides SonarScanner CLI documentation and configuration guidance for languages like JavaScript, TypeScript, Python, Go, PHP, Ruby, and others.

## Official Documentation

### SonarQube Cloud
- https://docs.sonarsource.com/sonarqube-cloud/advanced-setup/ci-based-analysis/sonarscanner-cli

### SonarQube Server
- https://docs.sonarsource.com/sonarqube-server/analyzing-source-code/scanners/sonarscanner

## Scanner Overview

**Use `web/fetch` to get current installation methods and versions from official documentation.**

The SonarScanner CLI is a standalone scanner for JavaScript, TypeScript, Python, Go, PHP, Ruby, and other languages not using Maven, Gradle, or .NET.

**IMPORTANT: CLI Scanner projects REQUIRE CI/CD scan actions/tasks.**
- GitHub Actions: Use `sonarsource/sonarqube-scan-action`
- GitLab CI: Use `sonarsource/sonar-scanner-cli` Docker image
- Azure DevOps: Use SonarQubePrepare and SonarQubeAnalyze tasks
- Bitbucket: Use SonarQube or SonarCloud pipes
- These actions/tasks handle scanner installation and execution

### Key Concepts
- Language-agnostic scanner that works with any programming language
- Configuration via `sonar-project.properties` file (required)
- Can override properties via command line parameters
- Runs as standalone binary or Docker container
- Available as npm package for JavaScript/TypeScript projects
- Coverage must be generated before scanning (not during)

### Installation Options
- **Binary download**: Platform-specific executables from official site
- **Docker image**: `sonarsource/sonar-scanner-cli` for containerized environments
- **NPM package**: `sonarqube-scanner` for Node.js projects
- **Package managers**: Some platforms offer apt, brew, chocolatey packages

## Configuration File: sonar-project.properties

**Required for CLI scanner. Fetch current examples from official documentation.**

### Key Configuration Properties
- **Project identification**: `sonar.projectKey`, `sonar.projectName`, `sonar.projectVersion`
- **Organization** (Cloud only): `sonar.organization`
- **Host URL**: `sonar.host.url` (e.g., https://sonarcloud.io)
- **Source paths**: `sonar.sources` (comma-separated directories)
- **Test paths**: `sonar.tests` (comma-separated test directories)
- **Exclusions**: `sonar.exclusions`, `sonar.test.exclusions`
- **Coverage paths**: Language-specific properties
- **Encoding**: `sonar.sourceEncoding` (usually UTF-8)

### File Structure
- Create in project root directory
- Standard Java properties format
- Comments use `#` character
- Multi-line values use backslash continuation

## Language-Specific Configuration

**Fetch language-specific examples from official documentation.**

### JavaScript/TypeScript
- **Source patterns**: Common paths like `src`, `lib`
- **Test patterns**: Files matching `*.test.js`, `*.spec.ts`, etc.
- **Exclusions**: `node_modules`, `dist`, `build`, `coverage`
- **Coverage format**: LCOV (`sonar.javascript.lcov.reportPaths`)
- **Test runner**: Jest, Mocha, Jasmine (generate coverage first)
- **ESLint integration**: Optional external report import

### Python
- **Source patterns**: Typically `src`, package directories
- **Test patterns**: `tests`, `test`
- **Exclusions**: `venv`, `__pycache__`, `.pyc` files
- **Coverage format**: XML from coverage.py or pytest-cov
- **Coverage property**: `sonar.python.coverage.reportPaths`
- **Python version**: `sonar.python.version` for compatibility

### Go
- **Source patterns**: Usually `.` (root) or specific packages
- **Test patterns**: Files matching `*_test.go`
- **Exclusions**: `vendor` directory
- **Coverage format**: Go coverage profile
- **Coverage property**: `sonar.go.coverage.reportPaths`
- **Test command**: `go test` with `-coverprofile` flag

### PHP
- **Source patterns**: `src`, application directories
- **Test patterns**: `tests`, PHPUnit directories
- **Exclusions**: `vendor`, `cache`
- **Coverage format**: Clover XML or PHPUnit coverage
- **Coverage property**: `sonar.php.coverage.reportPaths`
- **PHP version**: `sonar.php.version` for rule compatibility

### Ruby
- **Source patterns**: `lib`, `app` for Rails/Sinatra
- **Test patterns**: `spec`, `test`
- **Exclusions**: `vendor`, `tmp`
- **Coverage format**: SimpleCov resultset JSON
- **Coverage property**: `sonar.ruby.coverage.reportPaths`

## Command Line Usage

**Fetch current command syntax from official documentation.**

### Execution Methods

1. **With properties file**: If `sonar-project.properties` exists, scanner reads configuration automatically
   - Pass token via command line parameter
   - Override specific properties if needed

2. **Command line only**: All configuration via `-D` parameters
   - Must specify project key, sources, host URL
   - Useful for dynamic configurations

3. **Debug mode**: Enable verbose logging for troubleshooting
   - Use `-X` flag
   - Shows detailed analysis steps

## Code Coverage Setup

**Coverage must be generated BEFORE running scanner.**

### Coverage Workflow
1. Run tests with coverage collection enabled
2. Generate coverage report in supported format
3. Configure coverage path in sonar-project.properties
4. Run sonar-scanner (uploads coverage with analysis)

### Language-Specific Tools
- **JavaScript/TypeScript**: Jest, Istanbul, nyc (LCOV format)
- **Python**: coverage.py, pytest-cov (XML format)
- **Go**: Built-in coverage with `-coverprofile` (coverage.out format)
- **PHP**: PHPUnit with code coverage (Clover XML)
- **Ruby**: SimpleCov (JSON resultset format)

**Fetch coverage commands and formats from official documentation.**

## Best Practices

1. **Always create sonar-project.properties**: Required for CLI scanner, defines project structure
2. **Generate coverage first**: Run tests with coverage before scanning
3. **Exclude dependencies**: node_modules, vendor, venv should always be excluded
4. **Use environment variables**: Store SONAR_TOKEN in CI/CD secrets, never commit
5. **Specify source paths explicitly**: Clear sonar.sources configuration avoids ambiguity
6. **Define test patterns**: Use sonar.test.inclusions for accurate test detection
7. **Set encoding**: Explicitly set sonar.sourceEncoding if not UTF-8
8. **Version the scanner**: Pin scanner version in CI/CD for reproducibility
9. **Check scanner version**: Use `web/fetch` to verify compatible scanner versions
10. **Enable debug for troubleshooting**: Use -X flag when investigating issues
11. **Validate coverage paths**: Ensure coverage files exist before scanning
12. **Use platform-specific actions**: Prefer official CI/CD integrations when available

## Platform Integration

Most CI/CD platforms provide official actions/pipes for CLI scanner:

- **platform-github-actions**: Use `sonarsource/sonarqube-scan-action`
- **platform-gitlab-ci**: Use `sonarsource/sonar-scanner-cli` Docker image
- **platform-azure-devops**: Use SonarQube CLI task
- **platform-bitbucket**: Use SonarCloud/SonarQube scan pipes

See platform-specific skills for integration details.

## Environment Variables

**Required:**
- `SONAR_TOKEN`: Authentication token

**Optional:**
- `SONAR_HOST_URL`: Can be in properties file instead
- `SONAR_ORGANIZATION`: Can be in properties file instead

## Troubleshooting

### Scanner not finding sources
- Check `sonar.sources` path is correct
- Verify path is relative to project root

### Coverage not reported
- Ensure coverage file exists and path matches property
- Check coverage report format is correct for language

### Encoding issues
- Set `sonar.sourceEncoding=UTF-8` explicitly

## Configuration Workflow

**CRITICAL: Follow this workflow when setting up CLI scanner projects:**

1. **Check for existing sonar-project.properties**: Use `search` to find if file exists
2. **Read properties file if exists**: Use `read` to view complete content
3. **Check existing configuration**: Note what properties are already configured
4. **Verify scanner version**: 
   - Use `web/fetch` to get latest scanner version recommendation
   - Note version for CI/CD setup
5. **Update, don't duplicate**: 
   - If properties exist: Only add missing properties
   - If properties missing: Create complete configuration
6. **Note properties file location**: Scanner must run from directory containing sonar-project.properties
   - Example: If sonar-project.properties is in `frontend/`, CI/CD must use `working-directory: frontend`
7. **Verify coverage setup**: Check if test runner and coverage tools are configured

## Usage Instructions

**For SonarArchitectGuide:**
- Include documentation link in responses
- Explain sonar-project.properties structure
- Mention coverage setup for specific language

**For SonarArchitectLight:**
- **Step 1**: Search for existing sonar-project.properties file
- **Step 2**: If exists, read complete file to check configuration
- **Step 3**: Use `web/fetch` to get latest scanner version and configuration examples
- **Step 4**: Note directory containing sonar-project.properties (working directory)
- **Step 5**: Create or update properties file (don't duplicate existing properties)
- **Step 6**: Include language-specific coverage configuration
- **Step 7**: Configure CI/CD to run tests before scan, from correct working directory
