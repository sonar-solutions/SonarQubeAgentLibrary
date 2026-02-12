# SonarArchitectLight Automated Test Framework

This is a combined **Option B (Automated Test Suite)** and **Option C (Model Comparison)** testing framework for the SonarArchitectLight agent.

## 📁 Directory Structure

```
tests/
├── scenarios/              # Test scenario definitions (YAML)
│   ├── maven/
│   │   └── github-actions-cloud.yaml
│   ├── gradle/
│   │   └── gitlab-ci-server.yaml
│   ├── dotnet/
│   │   └── azure-devops-cloud.yaml
│   ├── javascript/
│   │   └── bitbucket-cloud.yaml
│   └── python/
│       └── github-actions-server.yaml
│
├── fixtures/               # Test data and project samples
│   ├── projects/           # Sample project structures
│   │   ├── maven-simple/
│   │   ├── gradle-kotlin/
│   │   ├── dotnet-webapp/
│   │   ├── javascript-react/
│   │   └── python-flask/
│   └── existing-pipelines/ # Sample existing CI/CD files
│
├── assertions/             # Validation rules (JSON)
│   ├── security-compliance.json
│   ├── scanner-selection.json
│   ├── version-currency.json
│   ├── file-creation.json
│   └── skill-invocation.json
│
├── scripts/                # Automation scripts
│   ├── run-scenario.sh          # Run single scenario
│   ├── run-all-scenarios.sh     # Run all/filtered scenarios
│   ├── validate-result.py       # Validate & score results
│   ├── generate-summary.py      # Generate summary reports
│   └── compare-models.py        # Compare multiple models
│
└── results/                # Test execution results
    ├── claude-sonnet-4/
    │   ├── maven-github-actions-cloud.json
    │   └── summary.md
    ├── gpt-4-turbo/
    └── model-comparison.md
```

## 🚀 Quick Start

### 1. Run a Single Scenario

```bash
cd tests/scripts
./run-scenario.sh maven/github-actions-cloud.yaml --model claude-sonnet-4
```

### 2. Run All Scenarios

```bash
./run-all-scenarios.sh --model claude-sonnet-4
```

### 3. Run Filtered Scenarios

```bash
# By language
./run-all-scenarios.sh --language maven --model claude-sonnet-4

# By platform
./run-all-scenarios.sh --platform github --model gpt-4-turbo

# Combined
./run-all-scenarios.sh --language javascript --platform bitbucket --model claude-sonnet-4
```

### 4. Generate Summary Report

```bash
python generate-summary.py --model claude-sonnet-4
```

### 5. Compare Multiple Models

```bash
python compare-models.py --models claude-sonnet-4,gpt-4-turbo,gemini-pro-2
```

## 📊 Understanding Results

### Result File Structure

Each test execution creates a JSON result file:

```json
{
  "scenario": "github-actions-cloud",
  "language": "maven",
  "model": "claude-sonnet-4",
  "timestamp": "2026-02-12_14-30-00",
  "status": "passed",
  "execution": {
    "start_time": "2026-02-12 14:30:00",
    "end_time": "2026-02-12 14:30:23",
    "duration_seconds": 23,
    "total_tokens": 3247
  },
  "scores": {
    "total": 98,
    "accuracy": 40,
    "security": 20,
    "efficiency": 13,
    "currency": 15,
    "usability": 10
  },
  "checkpoints": [...],
  "files_created": [...],
  "documentation_fetches": {
    "total_count": 5,
    "pages": [
      {"url": "https://docs.sonarsource.com/...", "title": "..."},
      {"url": "https://github.com/actions/checkout", "title": "..."}
    ],
    "domains": ["docs.sonarsource.com", "github.com"]
  },
  "validation_results": {...}
}
```

### Scoring Rubric

| Category | Max Points | Validates |
|----------|------------|-----------|
| **Accuracy** | 40 | Skill invocation, scanner selection, file creation |
| **Security** | 20 | No hardcoded credentials, proper secret usage |
| **Efficiency** | 15 | Batched questions, web fetch usage, documentation fetches |
| **Currency** | 15 | Latest action/task/image versions |
| **Usability** | 10 | Clear instructions, complete setup guide |
| **Total** | **100** | |

**Documentation Tracking:** The framework also tracks which documentation pages are fetched during execution, helping validate that agents use current information rather than outdated training data. See [DOCUMENTATION_TRACKING.md](DOCUMENTATION_TRACKING.md) for details.

### Summary Report Example

After running tests, generate a summary:

```
══════════════════════════════════════════════════════════════════════════════
Avg Documentation Fetches: 4.8 pages/scenario
Test Suite Summary Report
══════════════════════════════════════════════════════════════════════════════

Model: claude-sonnet-4
Date: 2026-02-12 15:45:00
Total Scenarios: 5
Passed: 5 (100.0%)
Failed: 0 (0.0%)

══════════════════════════════════════════════════════════════════════════════
Results by Category
══════════════════════════════════════════════════════════════════════════════

Maven            5/ 5   ✓ 100.0%
Gradle           0/ 0   ✓ 0.0%
Dotnet           0/ 0   ✓ 0.0%
JavaScript       0/ 0   ✓ 0.0%
Python           0/ 0   ✓ 0.0%

══════════════════════════════════════════════════════════════════════════════
```

## 🎯 Test Scenarios

### Priority Scenarios (Included)

1. **Maven + GitHub Actions + SonarQube Cloud**
   - Tests: Maven integration, GitHub Actions workflow, Cloud configuration
   - Expected: Use `mvn sonar:sonar`, not scan action

2. **Gradle + GitLab CI + SonarQube Server**
   - Tests: Gradle integration, GitLab CI, Server URL handling
   - Expected: Use `gradle sonar`, CI/CD variables

3. **.NET + Azure DevOps + SonarQube Cloud**
   - Tests: .NET scanner, Azure Pipelines, Cloud EU instance
   - Expected: Use `dotnet sonarscanner`, pipeline variables

4. **JavaScript + Bitbucket + SonarQube Cloud**
   - Tests: CLI scanner, Bitbucket Pipelines, properties file
   - Expected: Use `sonar-scanner-cli`, create `sonar-project.properties`

5. **Python + GitHub Actions + SonarQube Server**
   - Tests: CLI scanner, Server URL as secret, properties file
   - Expected: Use scan action or CLI, `SONAR_HOST_URL` secret

### Adding New Scenarios

Create a new YAML file in `tests/scenarios/<language>/`:

```yaml
name: my-new-scenario
description: Description of what this tests
category: priority
language: maven
platform: github-actions
sonarqube: cloud-us

input:
  project_structure:
    - pom.xml
    - .github/workflows/ci.yml
  git_branch: main
  
  user_responses:
    - question: "CI/CD platform confirmation"
      answer: "Yes"
    - question: "SonarQube information"
      answer: "Cloud, my-project, my-org, US"

expected:
  skills_invoked:
    - project-detection
    - prerequisites-gathering
    # ... more skills
  
  decisions:
    - checkpoint: "Scanner selection"
      expected: "Use mvn sonar:sonar"
      reason: "Maven integration"
  
  files_created:
    - path: ".github/workflows/sonarqube.yml"
      must_contain:
        - "actions/checkout@v4"
        - "${{ secrets.SONAR_TOKEN }}"
      must_not_contain:
        - "squ_"

  validation:
    - type: "yaml_syntax"
      file: ".github/workflows/sonarqube.yml"
    - type: "security_compliance"
```

## 🔬 Validation Rules

Validation is driven by JSON assertion files in `tests/assertions/`:

### Security Compliance (`security-compliance.json`)
- No hardcoded SonarQube tokens (squ_, sqp_)
- Proper use of secrets/variables per platform
- No credentials in properties files

### Scanner Selection (`scanner-selection.json`)
- Maven/Gradle/.NET: Use build tool integration
- JavaScript/Python: Use CLI scanner
- No incorrect scanner for project type

### Version Currency (`version-currency.json`)
- GitHub Actions: v4 for checkout/setup actions
- GitLab CI: Latest images
- Azure DevOps: Current task versions

### File Creation (`file-creation.json`)
- Correct file paths per platform
- Required content elements present
- Branch handling (include current branch if not main)

## 📈 Model Comparison

Compare multiple models side-by-side:

```bash
python scripts/compare-models.py --models claude-sonnet-4,gpt-4-turbo,gemini-pro-2
```

Generates `results/model-comparison.md`:

| Model | Scenarios | Passed | Pass Rate | Avg Score | Accuracy | Security | Efficiency |
|-------|-----------|--------|-----------|-----------|----------|----------|------------|
| claude-sonnet-4 | 5 | 5 | 100.0% | 96.4/100 | 38.2/40 | 20.0/20 | 13.2/15 |
| gpt-4-turbo | 5 | 4 | 80.0% | 88.6/100 | 35.0/40 | 20.0/20 | 11.6/15 |
| gemini-pro-2 | 5 | 5 | 100.0% | 93.2/100 | 37.0/40 | 20.0/20 | 12.2/15 |

## 🛠️ Extending the Framework

### Add New Validation Rules

1. Create/edit assertion JSON in `tests/assertions/`
2. Update `validate-result.py` to implement new checks
3. Test with existing scenarios

### Add New Project Fixtures

1. Create project structure in `tests/fixtures/projects/<language>/`
2. Include minimal but representative files
3. Reference in scenario YAML files

### Customize Scoring

Edit scoring weights in assertion JSON files:

```json
{
  "scoring": {
    "critical_failure": -20,
    "medium_failure": -10,
    "success": 10
  }
}
```

## 📝 Next Steps

### Immediate
1. ✅ Framework structure created
2. ✅ 5 priority scenarios defined
3. ✅ Validation rules configured
4. ✅ Scripts ready

### To Implement
1. **Agent Invocation Logic**
   - Integrate actual agent execution in `run-scenario.sh`
   - Capture agent output and files created
   - Parse skill invocations from agent logs

2. **Result Collection**
   - Save agent-created files
   - Log skill usage
   - Track token/cost metrics

3. **Expand Scenarios**
   - Add remaining 55+ scenario combinations
   - Edge cases (existing configs, monorepos, etc.)

### Usage Pattern

```bash
# 1. Run tests
./run-all-scenarios.sh --model claude-sonnet-4

# 2. Review summary
cat ../results/claude-sonnet-4/summary.md

# 3. Investigate failures (if any)
cat ../results/claude-sonnet-4/gradle-gitlab-ci-server.json

# 4. Compare models (when you have multiple)
python compare-models.py --models claude-sonnet-4,gpt-4-turbo
```

## 🤝 Contributing

WheDOCUMENTATION_TRACKING.md](DOCUMENTATION_TRACKING.md) - Guide to tracking documentation fetches
- [n adding scenarios:
1. Follow existing YAML structure
2. Add corresponding fixtures if needed
3. Test scenario file validity
4. Document any new patterns

## 📚 References

- [TESTING_STRATEGY.md](TESTING_STRATEGY.md) - Full testing strategy document
- [WORKFLOW_EXAMPLE.md](../docs/WORKFLOW_EXAMPLE.md) - Agent workflow reference
- Skills Directory: `../.github/agents/skills/` - All skill definitions

---

**Ready to test!** 🚀

The framework is set up and ready. The next step is implementing the actual agent invocation logic in `run-scenario.sh` to execute the SonarArchitectLight agent with the test scenarios and capture results.
