# Example sonar-project.properties Files

The `sonar-project.properties` file is used to configure SonarQube analysis for projects that don't use Maven or Gradle.

## Basic Configuration

### Node.js/TypeScript Project

```properties
# Unique identifier for your project
sonar.projectKey=my-nodejs-project

# Display name in SonarQube UI
sonar.projectName=My Node.js Project

# Version (optional, can be set dynamically in CI/CD)
sonar.projectVersion=1.0.0

# Path to source code (comma-separated paths)
sonar.sources=src

# Path to test files
sonar.tests=tests

# Encoding of source files
sonar.sourceEncoding=UTF-8

# Language
sonar.language=js

# JavaScript/TypeScript specific
sonar.javascript.lcov.reportPaths=coverage/lcov.info

# Exclusions (paths to ignore)
sonar.exclusions=**/node_modules/**,**/*.test.js,**/*.spec.ts

# Test exclusions
sonar.test.exclusions=**/*.test.js,**/*.spec.ts
```

### Python Project

```properties
sonar.projectKey=my-python-project
sonar.projectName=My Python Project
sonar.projectVersion=1.0.0

# Source directory
sonar.sources=src

# Test directory
sonar.tests=tests

sonar.sourceEncoding=UTF-8
sonar.language=py

# Python specific - coverage report
sonar.python.coverage.reportPaths=coverage.xml

# Exclusions
sonar.exclusions=**/venv/**,**/__pycache__/**,**/*.pyc
sonar.test.exclusions=**/test_*.py,**/*_test.py
```

### Multi-Language Project

```properties
sonar.projectKey=my-fullstack-project
sonar.projectName=My Full-Stack Project
sonar.projectVersion=1.0.0

# Multiple source directories
sonar.sources=frontend/src,backend/src

# Test directories
sonar.tests=frontend/tests,backend/tests

sonar.sourceEncoding=UTF-8

# Coverage reports (comma-separated)
sonar.javascript.lcov.reportPaths=frontend/coverage/lcov.info
sonar.python.coverage.reportPaths=backend/coverage.xml

# Exclusions
sonar.exclusions=**/node_modules/**,**/venv/**,**/dist/**,**/build/**
```

## Advanced Configuration

### With Quality Gate

```properties
sonar.projectKey=my-project
sonar.projectName=My Project

sonar.sources=src
sonar.tests=tests

# Quality gate (optional - usually set in SonarQube UI)
sonar.qualitygate.wait=true

# Branch analysis (for CI/CD)
# Note: These are often set dynamically in CI/CD pipelines
# sonar.branch.name=${BRANCH_NAME}
# sonar.pullrequest.key=${PR_NUMBER}
# sonar.pullrequest.branch=${PR_BRANCH}
# sonar.pullrequest.base=${PR_BASE_BRANCH}
```

### With Specific Rules

```properties
sonar.projectKey=my-project
sonar.projectName=My Project

sonar.sources=src

# Issue exclusions (ignore specific rules in certain files)
# Format: sonar.issue.ignore.multicriteria=e1,e2
# e1.ruleKey=javascript:S1192
# e1.resourceKey=**/*.test.js
```

## Important Notes

### DO NOT Include Sensitive Information

❌ **NEVER** include credentials in sonar-project.properties:

```properties
# WRONG - DO NOT DO THIS
sonar.login=admin
sonar.password=password123
sonar.token=squ_abc123def456
```

✅ **CORRECT** - Use environment variables or CI/CD secrets:

```properties
# These should be set via environment variables or CI/CD secrets
# SONAR_TOKEN and SONAR_HOST_URL
```

## Dynamic Properties in CI/CD

Many properties can be set dynamically in your CI/CD pipeline:

### GitHub Actions Example

```yaml
- name: SonarQube Scan
  uses: sonarsource/sonarqube-scan-action@master
  env:
    SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
    SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}
  with:
    args: >
      -Dsonar.projectVersion=${{ github.run_number }}
      -Dsonar.branch.name=${{ github.ref_name }}
```

## Official Documentation

For comprehensive configuration options:
- **Analysis Parameters**: https://docs.sonarsource.com/sonarqube/latest/analyzing-source-code/analysis-parameters/
- **Language-Specific Properties**: https://docs.sonarsource.com/sonarqube/latest/analyzing-source-code/languages/overview/

## Need Help?

Use the SonarArchitect agent in VS Code:
```
@sonarqube-helper Review my SonarQube configuration
```
