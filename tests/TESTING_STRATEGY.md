# SonarArchitectLight Testing Strategy

This document outlines comprehensive testing approaches for validating the SonarArchitectLight agent across different scenarios, platforms, and LLM models.

## Why Testing Matters

The [WORKFLOW_EXAMPLE.md](../docs/WORKFLOW_EXAMPLE.md) naturally maps to a test specification because it defines:

1. **Clear inputs** (project type, platform, SonarQube type)
2. **Expected behaviors** (which skills, which decisions)
3. **Verifiable outputs** (files created, content structure)
4. **Decision points** (when to use scan action vs build commands)

## Testing Benefits

### 1. Scenario Coverage Matrix

Test all combinations of:
```
Languages:        Maven, Gradle, .NET, JavaScript/TypeScript, Python
Platforms:        GitHub Actions, GitLab CI, Azure DevOps, Bitbucket
SonarQube:        Cloud (US/EU), Server
Branches:         main, feature/*, develop
```

**Total Combinations**: 5 languages × 4 platforms × 3 SonarQube types = **60+ distinct test scenarios**

### 2. LLM Model Comparison

Using the workflow as a test spec, compare models on:
- **Accuracy**: Does each model invoke correct skills?
- **Decision quality**: Does it choose right scanner/action?
- **Security compliance**: Does it follow security-practices?
- **Consistency**: Same scenario = same result?
- **Version fetching**: Does it actually use web/fetch?
- **Efficiency**: How many interactions to complete?
- **Cost**: Token usage per scenario
- **Speed**: Time to completion

### 3. Regression Testing

When updating skills, verify:
- ✅ All test scenarios still pass
- ✅ No duplication reintroduced
- ✅ Security practices maintained
- ✅ Latest versions fetched
- ✅ No breaking changes in workflow

---

## Testing Options

### Option A: Test Scenarios Matrix Document

**File**: `tests/TEST_SCENARIOS.md`

**Content Structure**:
```markdown
# Test Scenarios Matrix

## Scenario Categories

### 1. Maven Projects
- Maven + GitHub Actions + SonarQube Cloud (US)
- Maven + GitHub Actions + SonarQube Cloud (EU)
- Maven + GitHub Actions + SonarQube Server
- Maven + GitLab CI + SonarQube Cloud
- Maven + GitLab CI + SonarQube Server
- Maven + Azure DevOps + SonarQube Cloud
- Maven + Azure DevOps + SonarQube Server
- Maven + Bitbucket + SonarQube Cloud
- Maven + Bitbucket + SonarQube Server

### 2. Gradle Projects
[Same matrix as Maven]

### 3. .NET Projects
[Same matrix as Maven]

### 4. JavaScript/TypeScript Projects (CLI Scanner)
[Same matrix as Maven]

### 5. Python Projects (CLI Scanner)
[Same matrix as Maven]

## Each Scenario Includes:

### Input Specification
- Project structure (files present)
- Current branch
- User responses

### Expected Behavior
- Skills invoked (in order)
- Decision points
- Files to be created/modified

### Verification Checkpoints
- Correct scanner selection
- Security compliance
- Version currency
- File syntax validity
- Complete configuration

### Pass/Fail Criteria
- All prerequisites gathered
- Correct files created
- No hardcoded credentials
- Latest versions used
- Appropriate secrets configuration instructions
```

**Benefits**:
- Exhaustive coverage
- Clear expected results
- Easy to validate manually or with automation
- Can be used as test cases

---

### Option B: Automated Test Suite Structure

**Directory Structure**:
```
tests/
├── scenarios/
│   ├── maven/
│   │   ├── github-actions-cloud-us.yaml
│   │   ├── github-actions-cloud-eu.yaml
│   │   ├── github-actions-server.yaml
│   │   ├── gitlab-ci-cloud.yaml
│   │   ├── gitlab-ci-server.yaml
│   │   ├── azure-devops-cloud.yaml
│   │   ├── azure-devops-server.yaml
│   │   ├── bitbucket-cloud.yaml
│   │   └── bitbucket-server.yaml
│   ├── gradle/
│   │   └── [same as maven]
│   ├── dotnet/
│   │   └── [same as maven]
│   ├── javascript/
│   │   └── [same as maven]
│   └── python/
│       └── [same as maven]
├── fixtures/
│   ├── projects/
│   │   ├── maven-simple/
│   │   │   └── pom.xml
│   │   ├── gradle-kotlin/
│   │   │   ├── build.gradle.kts
│   │   │   └── settings.gradle.kts
│   │   ├── dotnet-webapp/
│   │   │   └── MyApp.csproj
│   │   ├── javascript-react/
│   │   │   └── package.json
│   │   └── python-flask/
│   │       └── requirements.txt
│   └── existing-pipelines/
│       ├── github-ci.yml
│       ├── gitlab-ci.yml
│       ├── azure-pipelines.yml
│       └── bitbucket-pipelines.yml
├── assertions/
│   ├── file-creation.json
│   ├── security-compliance.json
│   ├── skill-invocation.json
│   ├── version-currency.json
│   └── syntax-validation.json
├── results/
│   ├── gpt-4-turbo/
│   │   ├── maven-github-cloud.json
│   │   └── [other scenarios]
│   ├── claude-sonnet-4/
│   │   └── [all scenarios]
│   ├── gemini-pro-2/
│   │   └── [all scenarios]
│   └── comparison-report.md
└── scripts/
    ├── run-scenario.sh
    ├── validate-output.py
    ├── compare-models.py
    └── generate-report.py
```

**Scenario File Example** (`maven/github-actions-cloud-us.yaml`):
```yaml
name: maven-github-actions-cloud-us
description: Maven project with GitHub Actions targeting SonarQube Cloud US instance

input:
  project_structure:
    - pom.xml
    - .github/workflows/ci.yml
    - src/main/java/Main.java
  git_branch: feature/user-auth
  
  user_responses:
    - question: "CI/CD platform confirmation"
      answer: "That's correct"
    - question: "SonarQube information"
      answer: "Cloud, my-org_my-project, my-org, US"

expected:
  skills_invoked:
    - project-detection
    - prerequisites-gathering
    - platform-github-actions
    - scanner-maven
    - pipeline-creation
    - security-practices
    - devops-setup-instructions
  
  decisions:
    - checkpoint: "Scanner selection"
      expected: "Use mvn sonar:sonar command (NO scan action)"
      reason: "Maven build tool integration"
    
    - checkpoint: "Branch trigger"
      expected: "Include feature/user-auth"
      reason: "Current branch not main/master"
    
    - checkpoint: "SonarQube URL"
      expected: "https://sonarqube.us"
      reason: "US instance specified"
  
  files_created:
    - path: ".github/workflows/sonarqube.yml"
      must_contain:
        - "actions/checkout@v4"
        - "fetch-depth: 0"
        - "actions/setup-java@v4"
        - "${{ secrets.SONAR_TOKEN }}"
        - "mvn -B verify sonar:sonar"
        - "-Dsonar.projectKey=my-org_my-project"
        - "-Dsonar.organization=my-org"
        - "-Dsonar.host.url=https://sonarqube.us"
        - "feature/user-auth"
      must_not_contain:
        - "sonarqube-scan-action"
        - "squ_"  # hardcoded token
        - "actions/checkout@v3"  # outdated version
  
  validation:
    - type: "yaml_syntax"
      file: ".github/workflows/sonarqube.yml"
    - type: "no_hardcoded_credentials"
      files: ["**/*.yml", "**/*.yaml"]
    - type: "version_currency"
      check: "GitHub Actions versions"
    - type: "security_compliance"
      rules: ["security-practices"]

assertions:
  - "All prerequisites gathered before file creation"
  - "web/fetch used to get latest versions"
  - "Correct scanner selection (command vs action)"
  - "Security practices applied (secrets, not hardcoded)"
  - "Current branch included in triggers"
  - "Secrets setup instructions provided"
```

**Benefits**:
- Machine-readable test definitions
- Automated execution possible
- Reproducible results
- Easy to add new scenarios
- Can track regressions

---

### Option C: LLM Testing Scorecard

**File**: `tests/LLM_COMPARISON.md`

**Content Structure**:
```markdown
# LLM Model Comparison for SonarArchitectLight

## Testing Methodology

Each LLM model is evaluated across multiple test scenarios using the same:
- Input project structures
- User responses
- Expected outcomes
- Evaluation criteria

## Scoring Rubric (Per Scenario)

### 1. Accuracy (40 points)
- **Skill Invocation** (10 pts): Correct skills in correct order
- **Scanner Selection** (10 pts): Appropriate scanner for project type
- **Platform Implementation** (10 pts): Correct platform-specific syntax
- **Configuration Completeness** (10 pts): All required properties present

### 2. Security (20 points)
- **No Hardcoded Credentials** (10 pts): Uses secrets/variables
- **Security Practices Applied** (10 pts): Follows security-practices skill

### 3. Efficiency (15 points)
- **Prerequisite Gathering** (5 pts): Batches questions appropriately
- **Token Usage** (5 pts): Reasonable token consumption
- **Interaction Count** (5 pts): Minimal back-and-forth

### 4. Version Currency (15 points)
- **Web Fetch Usage** (5 pts): Actually fetches documentation
- **Latest Actions/Tasks** (5 pts): Uses current versions
- **Latest Plugins** (5 pts): Current scanner versions

### 5. Usability (10 points)
- **Clear Communication** (5 pts): Concise, actionable responses
- **Setup Instructions** (5 pts): Complete DevOps setup guidance

**Total: 100 points per scenario**

## Model Comparison Table

| Model | Avg Score | Accuracy | Security | Efficiency | Currency | Usability | Token/Scenario | Time/Scenario |
|-------|-----------|----------|----------|------------|----------|-----------|----------------|---------------|
| GPT-4 Turbo | - | - | - | - | - | - | - | - |
| Claude Sonnet 4 | - | - | - | - | - | - | - | - |
| Gemini Pro 2.0 | - | - | - | - | - | - | - | - |
| GPT-4o | - | - | - | - | - | - | - | - |
| Claude Opus | - | - | - | - | - | - | - | - |

## Detailed Results by Scenario

### Scenario: Maven + GitHub Actions + SonarQube Cloud

#### GPT-4 Turbo
**Score: __/100**

Strengths:
- [List]

Weaknesses:
- [List]

Notable Behaviors:
- [Observations]

#### Claude Sonnet 4
**Score: __/100**

[Same structure]

#### Gemini Pro 2.0
**Score: __/100**

[Same structure]

---

### Scenario: Gradle + GitLab CI + SonarQube Server

[Same structure for each model]

---

## Common Failure Patterns by Model

### GPT-4 Turbo
- [Pattern 1]
- [Pattern 2]

### Claude Sonnet 4
- [Pattern 1]
- [Pattern 2]

### Gemini Pro 2.0
- [Pattern 1]
- [Pattern 2]

## Recommendations

### Best Overall Model
**Recommendation**: [Model Name]

**Reasoning**:
- [Point 1]
- [Point 2]

### Best for Specific Use Cases

**High Security Requirements**: [Model]
**Cost Optimization**: [Model]
**Complex Scenarios**: [Model]
**Speed Priority**: [Model]

## Cost Analysis

| Model | Avg Tokens/Scenario | Input Token Cost | Output Token Cost | Total Cost/Scenario |
|-------|---------------------|------------------|-------------------|---------------------|
| GPT-4 Turbo | - | - | - | - |
| Claude Sonnet 4 | - | - | - | - |
| Gemini Pro 2.0 | - | - | - | - |

**Cost for Full Test Suite (60 scenarios)**:
- GPT-4 Turbo: $__
- Claude Sonnet 4: $__
- Gemini Pro 2.0: $__
```

**Benefits**:
- Objective comparison framework
- Identifies model strengths/weaknesses
- Supports model selection decisions
- Tracks improvements over time

---

## Key Testing Criteria

Based on [WORKFLOW_EXAMPLE.md](../docs/WORKFLOW_EXAMPLE.md), each test should verify:

| Checkpoint | Verification | Skill Reference |
|------------|--------------|-----------------|
| **Skills Invoked** | Correct sequence: detection → prerequisites → platform → scanner → creation | All skills |
| **Prerequisites Complete** | All gathered before file creation | `prerequisites-gathering` |
| **Web Fetch** | Actually fetches docs.sonarsource.com (not guessing versions) | `pipeline-creation`, platform skills |
| **Scanner Selection** | Correct choice (scan action vs build command) | `pipeline-creation` |
| **Scanner Decision Logic** | Maven/Gradle/.NET use commands; JS/TS/Python use actions | `scanner-*` skills |
| **Security Compliance** | Uses secrets, never hardcodes credentials | `security-practices` |
| **Files Created** | Correct path, valid syntax, complete content | `pipeline-creation` |
| **Version Currency** | Uses latest versions from documentation | Platform & scanner skills |
| **Branch Handling** | Includes current branch if not main/master | `prerequisites-gathering`, `pipeline-creation` |
| **Platform Syntax** | Correct secret/variable syntax for platform | Platform-specific skills |
| **Setup Instructions** | Complete, actionable DevOps configuration steps | `devops-setup-instructions` |
| **No Duplication** | Doesn't repeat scanner logic or security syntax | All skills (post-consolidation) |

---

## Recommended Testing Approach

### Phase 1: Core Scenarios (Priority)
Test one representative scenario per combination:
1. **Maven + GitHub Actions + SonarQube Cloud**
2. **Gradle + GitLab CI + SonarQube Server**
3. **.NET + Azure DevOps + SonarQube Cloud**
4. **JavaScript + Bitbucket + SonarQube Cloud**
5. **Python + GitHub Actions + SonarQube Server**

**Total**: 5 scenarios covering all languages and platforms

### Phase 2: Platform Variations
Expand to test all platform combinations for each language:
- Maven across all 4 platforms (GitHub, GitLab, Azure, Bitbucket)
- Same for Gradle, .NET, JavaScript, Python

**Total**: 20 scenarios (5 languages × 4 platforms)

### Phase 3: SonarQube Instance Variations
Test Cloud (US vs EU) and Server variations:
- For critical combinations

**Total**: Additional 10-15 scenarios

### Phase 4: Edge Cases
- Projects with existing incomplete configurations
- Multi-module projects
- Monorepos with multiple languages
- Non-standard branch names
- Projects with existing SonarQube config (migration scenarios)

**Total**: 10-15 scenarios

### Phase 5: Regression Suite
Run full test matrix after any skill changes:
- All 60+ scenarios
- Compare against baseline results
- Flag any deviations

---

## Testing Workflow

### 1. Prepare Test Environment
```bash
# Set up test fixtures
tests/fixtures/projects/maven-simple/
tests/fixtures/projects/gradle-kotlin/
# etc.

# Prepare scenario definitions
tests/scenarios/maven/github-actions-cloud.yaml
# etc.
```

### 2. Execute Test Run
```bash
# Run single scenario
./tests/scripts/run-scenario.sh maven/github-actions-cloud.yaml --model claude-sonnet-4

# Run all scenarios for a model
./tests/scripts/run-all-scenarios.sh --model claude-sonnet-4

# Run all scenarios for all models (comparison)
./tests/scripts/compare-models.sh
```

### 3. Validate Results
```bash
# Validate output files
./tests/scripts/validate-output.py results/claude-sonnet-4/maven-github-cloud.json

# Check assertions
./tests/scripts/check-assertions.py \
  --scenario scenarios/maven/github-actions-cloud.yaml \
  --result results/claude-sonnet-4/maven-github-cloud.json
```

### 4. Generate Reports
```bash
# Generate comparison report
./tests/scripts/generate-report.py \
  --input results/ \
  --output results/comparison-report.md

# Generate scorecard
./tests/scripts/generate-scorecard.py \
  --input results/ \
  --output tests/LLM_COMPARISON.md
```

### 5. Review & Iterate
- Review comparison report
- Identify common failures
- Update skills to address issues
- Re-run regression suite
- Document findings

---

## Success Metrics

### Test Pass Criteria (Per Scenario)
- ✅ All prerequisites gathered
- ✅ Correct skills invoked in proper sequence
- ✅ Correct scanner selection
- ✅ All required files created
- ✅ No hardcoded credentials
- ✅ Valid YAML/properties syntax
- ✅ Latest versions used
- ✅ Secrets setup instructions provided
- ✅ Platform-specific syntax correct
- ✅ Current branch included (if applicable)

### Overall Suite Success
- **95%+ scenarios pass** across all checkpoints
- **100% security compliance** (no hardcoded credentials ever)
- **90%+ version currency** (uses latest from docs)
- **Consistent results** (same input = same output)

### Model Comparison Success
- **Clear winner identified** for overall use case
- **Use-case specific recommendations** documented
- **Cost/performance tradeoffs** understood
- **Failure patterns** documented for improvement

---

## Next Steps

1. **Choose initial approach**: Start with Option A (Test Scenarios Matrix) for comprehensive documentation
2. **Build core scenarios**: Create 5 priority test scenarios first
3. **Manual validation**: Run scenarios manually with primary LLM model
4. **Document results**: Record outcomes in structured format
5. **Expand coverage**: Add platform and instance variations
6. **Implement automation**: Build to Option B (Automated Suite) if needed
7. **Compare models**: Use Option C (Scorecard) for model evaluation
8. **Iterate & improve**: Use findings to refine skills

---

## Maintenance

### When to Run Tests
- **Before releasing skill changes**: Full regression suite
- **After skill updates**: Affected scenarios
- **Monthly**: Version currency check (are we still fetching latest?)
- **When evaluating new LLM models**: Full comparison scorecard

### Updating Tests
- Add new scenarios when supporting new platforms
- Update expectations when official documentation changes
- Add edge cases discovered in production use
- Refresh fixtures to match current best practices

### Test Result Retention
- Keep baseline results for comparison
- Archive model comparison reports
- Track improvements/regressions over time
- Document learnings and pattern changes

---

## Resources

- [WORKFLOW_EXAMPLE.md](../docs/WORKFLOW_EXAMPLE.md) - Detailed workflow reference
- [Skills Directory](../.github/agents/skills/) - All skill definitions
- [Agent Definition](../.github/agents/SonarArchitectLight.agent.md) - Agent behavior spec

---

## Appendix: Sample Test Execution Log

```
$ ./tests/scripts/run-scenario.sh maven/github-actions-cloud.yaml --model claude-sonnet-4

[2026-02-11 10:15:23] Starting scenario: maven-github-actions-cloud
[2026-02-11 10:15:23] Model: claude-sonnet-4
[2026-02-11 10:15:23] Preparing test environment...
[2026-02-11 10:15:24] Loading scenario definition...
[2026-02-11 10:15:24] Creating project fixture...
[2026-02-11 10:15:25] Initializing agent session...
[2026-02-11 10:15:26] 
[2026-02-11 10:15:26] → User: "Set up SonarQube for my project"
[2026-02-11 10:15:28] ← Agent: Uses project-detection skill
[2026-02-11 10:15:29] ← Agent: "I detected a Maven project with GitHub Actions..."
[2026-02-11 10:15:29] ✓ Checkpoint: Correct detection
[2026-02-11 10:15:30] 
[2026-02-11 10:15:30] → User: "That's correct"
[2026-02-11 10:15:32] ← Agent: Uses prerequisites-gathering skill
[2026-02-11 10:15:33] ← Agent: "I need some information..."
[2026-02-11 10:15:33] ✓ Checkpoint: Batched questions
[2026-02-11 10:15:34] 
[2026-02-11 10:15:34] → User: "Cloud, my-org_my-project, my-org, US"
[2026-02-11 10:15:37] ← Agent: Uses web/fetch for GitHub Actions docs
[2026-02-11 10:15:38] ← Agent: Uses web/fetch for Maven scanner docs
[2026-02-11 10:15:39] ✓ Checkpoint: Fetched documentation
[2026-02-11 10:15:40] ← Agent: Creates .github/workflows/sonarqube.yml
[2026-02-11 10:15:41] ✓ Checkpoint: File created
[2026-02-11 10:15:42] ← Agent: Provides secrets setup instructions
[2026-02-11 10:15:42] ✓ Checkpoint: Instructions provided
[2026-02-11 10:15:43] 
[2026-02-11 10:15:43] Running validation checks...
[2026-02-11 10:15:44] ✓ YAML syntax valid
[2026-02-11 10:15:44] ✓ No hardcoded credentials
[2026-02-11 10:15:45] ✓ Latest action versions used
[2026-02-11 10:15:45] ✓ Correct scanner selection (mvn sonar:sonar)
[2026-02-11 10:15:45] ✓ Current branch included
[2026-02-11 10:15:45] ✓ Security practices applied
[2026-02-11 10:15:46] 
[2026-02-11 10:15:46] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[2026-02-11 10:15:46] TEST PASSED ✓
[2026-02-11 10:15:46] Score: 98/100
[2026-02-11 10:15:46]   Accuracy: 40/40
[2026-02-11 10:15:46]   Security: 20/20
[2026-02-11 10:15:46]   Efficiency: 13/15 (-2 for token usage)
[2026-02-11 10:15:46]   Currency: 15/15
[2026-02-11 10:15:46]   Usability: 10/10
[2026-02-11 10:15:46] Tokens: 3,247 (input: 2,103, output: 1,144)
[2026-02-11 10:15:46] Duration: 23 seconds
[2026-02-11 10:15:46] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
