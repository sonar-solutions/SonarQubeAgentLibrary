# Quick Start Guide - Running Your First Test

This guide walks you through running your first SonarArchitectLight test scenario.

## Prerequisites

- Python 3.7+ installed
- Bash shell (macOS/Linux or Git Bash on Windows)
- Access to the SonarArchitectLight agent

## Step 1: Verify Setup

Check that all test files are in place:

```bash
cd tests
ls -la scenarios/maven/
ls -la fixtures/projects/maven-simple/
ls -la assertions/
ls -la scripts/
```

You should see:
- 5 scenario YAML files across different language directories
- Project fixtures for each language
- 5 assertion JSON files
- 5 script files

## Step 2: Make Scripts Executable

```bash
chmod +x scripts/*.sh
```

## Step 3: Run a Single Scenario (Dry Run)

The current implementation is a framework skeleton. To test the structure:

```bash
cd scripts
./run-scenario.sh maven/github-actions-cloud.yaml --model claude-sonnet-4
```

Expected output:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SonarArchitectLight Test Execution
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Scenario: github-actions-cloud
Language: maven
Model: claude-sonnet-4
Timestamp: 2026-02-12_15-45-00

[15:45:00] Starting test scenario...
[15:45:00] Preparing test environment...
[15:45:00] Loading scenario definition...
[15:45:00] Creating project fixture...
[15:45:00] Initializing agent session...
[15:45:00] Running validation checks...

✓ Test framework ready
Result file: ../results/claude-sonnet-4/maven-github-actions-cloud.json
```

## Step 4: View the Result File

```bash
cat ../results/claude-sonnet-4/maven-github-actions-cloud.json
```

This creates a template JSON structure showing what the result will look like.

## Step 5: Run All Scenarios

```bash
./run-all-scenarios.sh --model claude-sonnet-4
```

This runs all 5 priority scenarios and shows a summary.

## Step 6: Generate Summary Report

```bash
python generate-summary.py --model claude-sonnet-4
```

View the generated markdown report:

```bash
cat ../results/claude-sonnet-4/summary.md
```

## Step 7: Validate a Result (Manual)

Test the validation script with a scenario and result:

```bash
python validate-result.py \
  --scenario ../scenarios/maven/github-actions-cloud.yaml \
  --result ../results/claude-sonnet-4/maven-github-actions-cloud.json
```

This will show detailed validation including documentation fetch tracking.

## Documentation Fetch Tracking

The framework tracks which documentation pages the agent fetches during execution:

```json
{
  "documentation_fetches": {
    "total_count": 5,
    "pages": [
      {"url": "https://docs.sonarsource.com/...", "title": "Maven scanner"},
      {"url": "https://github.com/actions/checkout", "title": "checkout"}
    ],
    "domains": ["docs.sonarsource.com", "github.com"]
  }
}
```

**Why this matters:**
- Validates agent uses current documentation (not outdated training data)
- Ensures efficiency (not over-fetching)
- Confirms correct sources are consulted

See [DOCUMENTATION_TRACKING.md](DOCUMENTATION_TRACKING.md) for implementation details.

## What's Next?

### To Complete the Implementation

The framework is ready, but needs agent integration:

1. **Implement Agent Invocation**
   - Modify `run-scenario.sh` to actually invoke the SonarArchitectLight agent
   - Capture agent responses and created files
   - Extract skill invocation logs

2. **Capture Real Results**
   - Save files created by the agent
   - Record skill usage
   - Track token metrics
   - **Track documentation fetches** (which pages accessed)

3. **Full Validation**
   - Run `validate-result.py` on actual agent outputs
   - Verify scoring logic
   - Fine-tune assertion rules

### Example Integration Pattern

```bash
# In run-scenario.sh, replace the TODO section with:

# Create temporary workspace
TEMP_WORKSPACE=$(mktemp -d)
cp -r fixtures/projects/maven-simple/* $TEMP_WORKSPACE/

# Invoke agent (pseudo-code)
agent_invoke \
  --workspace $TEMP_WORKSPACE \
  --prompt "Set up SonarQube for my project" \
  --responses "Yes", "Cloud, my-project, my-org, US" \
  > $LOG_FILE 2>&1

# Collect created files
FILES_CREATED=$(find $TEMP_WORKSPACE -name "*.yml" -newer $TEMP_WORKSPACE)

# Extract skills from log
SKILLS_INVOKED=$(grep "skill:" $LOG_FILE | cut -d: -f2)

# Build result JSON
# ... populate result file with actual data ...

# Validate
python validate-result.py --scenario $SCENARIO_FILE --result $RESULT_FILE
```

## Testing the Framework Itself

You can test individual components:

### Test Scenario Loading
```bash
python -c "
import yaml
with open('../scenarios/maven/github-actions-cloud.yaml') as f:
    scenario = yaml.safe_load(f)
    print(f'Scenario: {scenario[\"name\"]}')
    print(f'Language: {scenario[\"language\"]}')
    print(f'Expected files: {len(scenario[\"expected\"][\"files_created\"])}')
"
```

### Test Assertion Loading
```bash
python -c "
import json
with open('../assertions/security-compliance.json') as f:
    assertions = json.load(f)
    print(f'Rules: {len(assertions[\"rules\"])}')
    for rule in assertions['rules']:
        print(f'  - {rule[\"id\"]}: {rule[\"name\"]}')
"
```

### Test Result Structure
```bash
python -c "
import json
with open('../results/claude-sonnet-4/maven-github-actions-cloud.json') as f:
    result = json.load(f)
    print(f'Scenario: {result[\"scenario\"]}')
    print(f'Status: {result[\"status\"]}')
    print(f'Total Score: {result[\"scores\"][\"total\"]}')
"
```

## Troubleshooting

### Script Permission Denied
```bash
chmod +x scripts/*.sh
```

### Python Module Not Found
```bash
pip install pyyaml  # for YAML parsing
```

### Empty Results Directory
This is expected - results are created when you run scenarios.

## Summary

You now have:
- ✅ Complete test framework structure
- ✅ 5 priority test scenarios defined
- ✅ Validation rules configured
- ✅ Automation scripts ready
- ✅ Result collection prepared
- ✅ Summary & comparison reports ready

**Next:** Integrate the actual SonarArchitectLight agent execution into `run-scenario.sh`

---
:
- [README.md](README.md) - Complete framework documentation
- [TESTING_STRATEGY.md](TESTING_STRATEGY.md) - Testing strategy
- [DOCUMENTATION_TRACKING.md](DOCUMENTATION_TRACKING.md) - How to track documentation fetches
For more details, see [README.md](README.md) and [TESTING_STRATEGY.md](TESTING_STRATEGY.md)
