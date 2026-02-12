# Documentation Fetch Tracking - Example Output

This file shows example output when documentation fetch tracking is enabled.

## Example 1: Successful Validation with Documentation Tracking

### When Running Validation

```bash
$ python scripts/validate-result.py \
    --scenario scenarios/maven/github-actions-cloud.yaml \
    --result results/claude-sonnet-4/maven-github-actions-cloud.json
```

### Console Output

```
Validating Test Results

[Checkpoint] Validating skill invocation...
  ✓ All expected skills invoked

[Checkpoint] Validating scanner selection...
  ✓ Correct scanner selected

[Checkpoint] Validating file creation...
  ✓ File .github/workflows/sonarqube.yml validated

[Checkpoint] Validating security compliance...
  ✓ No security violations found

[Checkpoint] Validating version currency...
  ✓ Version currency: 3/3 current

[Checkpoint] Validating documentation fetches...
  📄 Total documentation fetches: 5
  🌐 Domains accessed: docs.sonarsource.com, github.com
  ✓ Appropriate number of fetches (5)
  ✓ Fetched from docs.sonarsource.com
  ✓ Fetched from github.com
  ✓ Fetched: Maven scanner documentation
  ✓ Fetched: GitHub Actions checkout documentation
  ✓ Fetched: GitHub Actions setup-java documentation

  📚 Documentation pages fetched:
     1. https://docs.sonarsource.com/sonarqube/latest/analyzing-source-code/scanners/sonarscanner-for-maven/
     2. https://github.com/actions/checkout - actions/checkout
     3. https://github.com/actions/setup-java - actions/setup-java
     4. https://docs.sonarsource.com/sonarcloud/getting-started/github/
     5. https://docs.sonarsource.com/sonarcloud/advanced-setup/languages/java/

============================================
TEST PASSED ✓
============================================
Score: 98/100
  Accuracy:   40/40
  Security:   20/20
  Efficiency: 13/15
  Currency:   15/15
  Usability:  10/10
============================================
```

## Example 2: Warning - Too Few Documentation Fetches

```
[Checkpoint] Validating documentation fetches...
  📄 Total documentation fetches: 1
  🌐 Domains accessed: github.com
  ✗ Too few fetches (1 < 2)
  ! No fetches from docs.sonarsource.com
  ✓ Fetched from github.com
  ! Missing: Maven scanner documentation
  ✓ Fetched: GitHub Actions checkout documentation

  📚 Documentation pages fetched:
     1. https://github.com/actions/checkout

============================================
TEST FAILED ✗
============================================
Score: 78/100
  Accuracy:   35/40
  Security:   20/20
  Efficiency: 8/15  (-5 for missing documentation fetches)
  Currency:   15/15
  Usability:  10/10
============================================

Failures:
- Too few documentation fetches: 1 < 2
- Agent may not be using web/fetch for SonarQube documentation
```

## Example 3: Summary Report with Documentation Metrics

```bash
$ python scripts/generate-summary.py --model claude-sonnet-4
```

### Console Output

```
═══════════════════════════════════════════════════════════════════════════════
Test Suite Summary Report
═══════════════════════════════════════════════════════════════════════════════

Model: claude-sonnet-4
Date: 2026-02-12 15:45:00
Total Scenarios: 5
Passed: 5 (100.0%)
Failed: 0 (0.0%)
Avg Documentation Fetches: 4.8 pages/scenario

═══════════════════════════════════════════════════════════════════════════════
Results by Category
═══════════════════════════════════════════════════════════════════════════════

Maven            5/ 5   ✓ 100.0%
Gradle           0/ 0   ✓ 0.0%
Dotnet           0/ 0   ✓ 0.0%
JavaScript       0/ 0   ✓ 0.0%
Python           0/ 0   ✓ 0.0%

═══════════════════════════════════════════════════════════════════════════════

✓ Summary report generated: tests/results/claude-sonnet-4/summary.md
```

### Generated Markdown Report

```markdown
# SonarArchitectLight Test Suite Summary

**Model:** claude-sonnet-4
**Date:** 2026-02-12 15:45:00
**Total Scenarios:** 5

## Overall Results

- ✅ **Passed:** 5 (100.0%)
- ❌ **Failed:** 0 (0.0%)
- 📊 **Average Score:** 96.4/100
- 📚 **Avg Documentation Fetches:** 4.8 pages/scenario

---

## Score Breakdown

| Scenario | Accuracy | Security | Efficiency | Currency | Usability | Total | Doc Fetches |
|----------|----------|----------|------------|----------|-----------|-------|-------------|
| maven/github-actions-cloud | 40/40 | 20/20 | 13/15 | 15/15 | 10/10 | 98/100 | 5 |
| gradle/gitlab-ci-server | 40/40 | 20/20 | 12/15 | 15/15 | 10/10 | 97/100 | 4 |
| dotnet/azure-devops-cloud | 38/40 | 20/20 | 13/15 | 15/15 | 10/10 | 96/100 | 5 |
| javascript/bitbucket-cloud | 40/40 | 20/20 | 11/15 | 15/15 | 10/10 | 96/100 | 6 |
| python/github-actions-server | 38/40 | 20/20 | 13/15 | 15/15 | 9/10 | 95/100 | 4 |
```

## Example 4: Model Comparison with Documentation Metrics

```bash
$ python scripts/compare-models.py --models claude-sonnet-4,gpt-4-turbo,gemini-pro-2
```

### Console Output

```
══════════════════════════════════════════════════════════════════════════════════════════════════════════════
LLM Model Comparison
══════════════════════════════════════════════════════════════════════════════════════════════════════════════

Models: claude-sonnet-4, gpt-4-turbo, gemini-pro-2

Model                Scenarios  Passed   Pass Rate    Avg Score   Doc Fetches
──────────────────────────────────────────────────────────────────────────────────────────────────────────────
claude-sonnet-4      5          5         100.0%       96.4/100      4.8
gpt-4-turbo          5          4          80.0%       88.6/100      3.2
gemini-pro-2         5          5         100.0%       93.2/100      6.1

🏆 Best Overall: claude-sonnet-4 (Score: 96.4/100)

══════════════════════════════════════════════════════════════════════════════════════════════════════════════

✓ Comparison report generated: tests/results/model-comparison.md
```

### Generated Comparison Report

```markdown
# LLM Model Comparison for SonarArchitectLight

**Date:** 2026-02-12 15:45:00
**Models Compared:** claude-sonnet-4, gpt-4-turbo, gemini-pro-2

## Overall Comparison

| Model | Scenarios | Passed | Failed | Pass Rate | Avg Score | Accuracy | Security | Efficiency | Currency | Usability | Avg Docs |
|-------|-----------|--------|--------|-----------|-----------|----------|----------|------------|----------|-----------|----------|
| claude-sonnet-4 | 5 | 5 | 0 | 100.0% | 96.4/100 | 39.2/40 | 20.0/20 | 12.4/15 | 15.0/15 | 9.8/10 | 4.8 |
| gpt-4-turbo | 5 | 4 | 1 | 80.0% | 88.6/100 | 35.0/40 | 20.0/20 | 9.6/15 | 15.0/15 | 9.0/10 | 3.2 |
| gemini-pro-2 | 5 | 5 | 0 | 100.0% | 93.2/100 | 37.0/40 | 20.0/20 | 11.2/15 | 15.0/15 | 10.0/10 | 6.1 |

---

## Best in Category

- 🏆 **Best Pass Rate:** claude-sonnet-4 (100.0%)
- 🏆 **Best Average Score:** claude-sonnet-4 (96.4/100)
- 🔒 **Best Security:** claude-sonnet-4, gpt-4-turbo, gemini-pro-2 (20.0/20)
- ⚡ **Best Efficiency:** claude-sonnet-4 (12.4/15)

---

## Detailed Performance Breakdown

### claude-sonnet-4

**Overall Performance:**
- Scenarios: 5
- Pass Rate: 100.0%
- Average Score: 96.4/100

**Score Breakdown:**
- Accuracy: 39.2/40
- Security: 20.0/20
- Efficiency: 12.4/15
- Currency: 15.0/15
- Usability: 9.8/10

**Documentation Usage:**
- Average Doc Fetches: 4.8 pages/scenario
- Total Doc Fetches: 24

**Analysis:** Optimal documentation usage - fetches the right amount of information without being excessive.

### gpt-4-turbo

**Overall Performance:**
- Scenarios: 5
- Pass Rate: 80.0%
- Average Score: 88.6/100

**Score Breakdown:**
- Accuracy: 35.0/40
- Security: 20.0/20
- Efficiency: 9.6/15
- Currency: 15.0/15
- Usability: 9.0/10

**Documentation Usage:**
- Average Doc Fetches: 3.2 pages/scenario
- Total Doc Fetches: 16

**Analysis:** Under-fetching documentation (3.2 avg) - may be relying on training data rather than current docs. This correlates with lower efficiency score.

⚠️ **Areas for Improvement:**
- Efficiency (batching & web fetch)
- Documentation fetching (too few fetches)

### gemini-pro-2

**Overall Performance:**
- Scenarios: 5
- Pass Rate: 100.0%
- Average Score: 93.2/100

**Score Breakdown:**
- Accuracy: 37.0/40
- Security: 20.0/20
- Efficiency: 11.2/15
- Currency: 15.0/15
- Usability: 10.0/10

**Documentation Usage:**
- Average Doc Fetches: 6.1 pages/scenario
- Total Doc Fetches: 31

**Analysis:** Over-fetching documentation (6.1 avg) - very thorough but less efficient. Still performs well overall.

---

## Recommendations

### Best Overall Model
**claude-sonnet-4**
- Average Score: 96.4/100
- Pass Rate: 100.0%
- Optimal documentation usage (4.8 fetches/scenario)
- Best balance of accuracy and efficiency
```

## Example 5: Using the Helper Script

### Track Documentation Fetches During Execution

```bash
# Initialize tracking file
python scripts/track-doc-fetch.py add \
  --url "https://docs.sonarsource.com/sonarqube/latest/analyzing-source-code/scanners/sonarscanner-for-maven/" \
  --title "SonarScanner for Maven" \
  --duration 342 \
  --file /tmp/doc-tracking.json

✓ Tracked fetch: https://docs.sonarsource.com/...

# Add more fetches
python scripts/track-doc-fetch.py add \
  --url "https://github.com/actions/checkout" \
  --title "actions/checkout" \
  --duration 215 \
  --file /tmp/doc-tracking.json

✓ Tracked fetch: https://github.com/actions/checkout

# View summary
python scripts/track-doc-fetch.py summary --file /tmp/doc-tracking.json

📚 Documentation Fetch Summary
==================================================
Total Fetches: 2
Unique Pages: 2
Domains: docs.sonarsource.com, github.com
==================================================

Pages Fetched:
 1. https://docs.sonarsource.com/sonarqube/latest/analyzing-source-code/scanners/sonarscanner-for-maven/
    Title: SonarScanner for Maven
    Time: 2026-02-12T14:30:05Z

 2. https://github.com/actions/checkout
    Title: actions/checkout
    Time: 2026-02-12T14:30:08Z

# Export to result file format
python scripts/track-doc-fetch.py export \
  --file /tmp/doc-tracking.json \
  --output /tmp/doc-summary.json

✓ Summary exported to: /tmp/doc-summary.json
```

### Exported Summary JSON

```json
{
  "total_count": 2,
  "pages": [
    {
      "url": "https://docs.sonarsource.com/sonarqube/latest/analyzing-source-code/scanners/sonarscanner-for-maven/",
      "title": "SonarScanner for Maven",
      "timestamp": "2026-02-12T14:30:05Z",
      "fetch_duration_ms": 342
    },
    {
      "url": "https://github.com/actions/checkout",
      "title": "actions/checkout",
      "timestamp": "2026-02-12T14:30:08Z",
      "fetch_duration_ms": 215
    }
  ],
  "domains": [
    "docs.sonarsource.com",
    "github.com"
  ],
  "unique_pages": 2
}
```

## Key Insights from Examples

### What Good Documentation Fetching Looks Like

**Claude Sonnet 4 (4.8 avg fetches):**
- ✅ Fetches from official sources (docs.sonarsource.com)
- ✅ Gets platform-specific docs (GitHub Actions)
- ✅ Not excessive (4-5 pages is optimal)
- ✅ High efficiency score (12.4/15)

### Warning Signs

**GPT-4 Turbo (3.2 avg fetches):**
- ⚠️ Under-fetching (< 3 pages)
- ⚠️ May rely on training data
- ⚠️ Lower efficiency score (9.6/15)
- ⚠️ Some scenarios fail

**Gemini Pro 2 (6.1 avg fetches):**
- ⚠️ Over-fetching (> 6 pages)
- ⚠️ Less efficient but thorough
- ✓ Still passes all scenarios
- ⚠️ Slightly lower efficiency (11.2/15)

### Correlations

Documentation fetch count correlates with:
- **Efficiency Score:** Optimal range (4-5 fetches) = higher efficiency
- **Pass Rate:** Too few fetches = higher failure rate
- **Version Currency:** Fetching docs = using latest versions
