# Documentation Fetch Tracking Guide

This guide explains how to capture and track which documentation pages the SonarArchitectLight agent fetches during test execution.

## Why Track Documentation Fetches?

Tracking documentation fetches validates that the agent:
1. **Uses current documentation** - Not relying on outdated training data
2. **Fetches appropriate sources** - Gets information from official documentation
3. **Fetches efficiently** - Not over-fetching or under-fetching
4. **Accesses relevant pages** - Reads documentation specific to the scenario

**This is now a first-class assertion** in the testing framework, treated identically to security compliance, version currency, and other validation categories.

## Assertion Definition

Documentation fetch validation is defined in `tests/assertions/documentation-fetches.json`:

- **Scoring**: 15 points maximum (Efficiency: 7pts, Accuracy: 6pts, Quality: 2pts)
- **Rules**: minimum-fetches, maximum-fetches, official-sources, relevant-pages, fetch-timing, no-duplicate-fetches
- **Configuration**: Platform-specific expectations (GitHub Actions, GitLab CI, Azure DevOps, Bitbucket)

## Integration in Test Scenarios

Test scenarios reference documentation tracking in their validation section:

```yaml
validation:
  - type: "documentation_fetches"
    rules: ["minimum-fetches", "official-sources", "relevant-pages"]
```

This ensures documentation fetch validation runs automatically during test execution.

## Documentation Fetch Data Structure

### In Result JSON

Each test result includes a `documentation_fetches` object:

```json
{
  "scenario": "github-actions-cloud",
  "model": "claude-sonnet-4",
  "documentation_fetches": {
    "total_count": 5,
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
      },
      {
        "url": "https://github.com/actions/setup-java",
        "title": "actions/setup-java",
        "timestamp": "2026-02-12T14:30:10Z",
        "fetch_duration_ms": 198
      }
    ],
    "domains": [
      "docs.sonarsource.com",
      "github.com"
    ],
    "unique_pages": 5,
    "cache_hits": 0
  }
}
```

### In Scenario YAML

Define expected documentation fetches:

```yaml
expected:
  documentation_fetches:
    expected_domains:
      - "docs.sonarsource.com"
      - "github.com"
    expected_pages:
      - pattern: "docs.sonarsource.com.*maven"
        description: "Maven scanner documentation"
      - pattern: "github.com/actions.*checkout"
        description: "GitHub Actions checkout documentation"
      - pattern: "github.com/actions.*setup-java"
        description: "GitHub Actions setup-java documentation"
    min_fetches: 2
    max_fetches: 10
```

## Capturing Documentation Fetches

### Method 1: Agent Log Parsing

If your agent logs web/fetch calls:

```bash
# In run-scenario.sh, parse agent logs
grep "web/fetch" $LOG_FILE | while read line; do
  # Extract URL from log line
  URL=$(echo "$line" | sed -n 's/.*fetch: \(.*\)/\1/p')
  
  # Add to tracking array
  DOC_FETCHES+=("{\"url\": \"$URL\", \"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}")
done

# Build JSON array
DOC_FETCHES_JSON=$(printf '%s\n' "${DOC_FETCHES[@]}" | jq -s '.')
```

### Method 2: Network Monitoring

Monitor network requests during agent execution:

```python
# Python implementation
import json
from datetime import datetime

class DocumentationFetchTracker:
    def __init__(self):
        self.fetches = []
    
    def track_fetch(self, url, title=None, duration_ms=None):
        """Track a documentation fetch"""
        self.fetches.append({
            'url': url,
            'title': title or '',
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'fetch_duration_ms': duration_ms
        })
    
    def get_summary(self):
        """Get fetch summary"""
        domains = list(set(
            url.split('/')[2] for url in 
            [f['url'] for f in self.fetches]
        ))
        
        return {
            'total_count': len(self.fetches),
            'pages': self.fetches,
            'domains': domains,
            'unique_pages': len(set(f['url'] for f in self.fetches))
        }
```

### Method 3: Wrapper Function

Wrap the agent's web/fetch function:

```javascript
// JavaScript/TypeScript example
const originalFetch = agent.webFetch;
const documentationFetches = [];

agent.webFetch = async function(url, options) {
  const startTime = Date.now();
  const result = await originalFetch.call(this, url, options);
  const duration = Date.now() - startTime;
  
  documentationFetches.push({
    url: url,
    title: extractTitle(result),
    timestamp: new Date().toISOString(),
    fetch_duration_ms: duration
  });
  
  return result;
};

// After execution
const summary = {
  total_count: documentationFetches.length,
  pages: documentationFetches,
  domains: [...new Set(documentationFetches.map(f => new URL(f.url).hostname))],
  unique_pages: new Set(documentationFetches.map(f => f.url)).size
};
```

## Validation & Scoring

The validation script checks:

### 1. Fetch Count
```python
min_fetches = expected_doc_fetch.get('min_fetches', 0)
max_fetches = expected_doc_fetch.get('max_fetches', 100)

if total_fetches < min_fetches:
    # Too few fetches - agent might not be using web/fetch
    score -= 5
elif total_fetches > max_fetches:
    # Too many fetches - inefficient
    score -= 2
else:
    # Appropriate usage
    score += 3
```

### 2. Expected Domains
```python
expected_domains = ['docs.sonarsource.com', 'github.com']

for domain in expected_domains:
    if domain in fetched_domains:
        print(f"✓ Fetched from {domain}")
        score += 2
    else:
        print(f"! Missing fetches from {domain}")
```

### 3. Expected Pages
```python
expected_pages = [
    {'pattern': 'docs.sonarsource.com.*maven', 'description': 'Maven docs'}
]

for expected in expected_pages:
    if any(re.search(expected['pattern'], page['url']) for page in pages):
        print(f"✓ Fetched: {expected['description']}")
    else:
        print(f"! Missing: {expected['description']}")
```

## Example Output

### During Validation

```
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
     2. https://github.com/actions/checkout
     3. https://github.com/actions/setup-java
     4. https://docs.sonarsource.com/sonarcloud/getting-started/github/
     5. https://docs.sonarsource.com/sonarcloud/advanced-setup/languages/java/
```

### In Summary Report

```markdown
## Overall Results

- ✅ Passed: 5 (100.0%)
- ❌ Failed: 0 (0.0%)
- 📊 Average Score: 96.4/100
- 📚 Avg Documentation Fetches: 4.8 pages/scenario

## Score Breakdown

| Scenario | Accuracy | Security | Efficiency | Currency | Usability | Total | Doc Fetches |
|----------|----------|----------|------------|----------|-----------|-------|-------------|
| maven/github-actions-cloud | 40/40 | 20/20 | 13/15 | 15/15 | 10/10 | 98/100 | 5 |
```

### In Model Comparison

```markdown
| Model | Scenarios | Passed | Pass Rate | Avg Score | Avg Docs |
|-------|-----------|--------|-----------|-----------|----------|
| claude-sonnet-4 | 5 | 5 | 100.0% | 96.4/100 | 4.8 |
| gpt-4-turbo | 5 | 4 | 80.0% | 88.6/100 | 3.2 |
| gemini-pro-2 | 5 | 5 | 100.0% | 93.2/100 | 6.1 |
```

**Analysis:** 
- Claude Sonnet 4: Good balance (4.8 fetches/scenario)
- GPT-4 Turbo: Under-fetching (3.2) - may rely on training data
- Gemini Pro 2: Over-fetching (6.1) - less efficient but thorough

## Integration Example

Complete example for `run-scenario.sh`:

```bash
# Track documentation fetches
DOC_FETCH_FILE="$TEMP_DIR/doc_fetches.json"

# Initialize tracker
echo '{"fetches": []}' > "$DOC_FETCH_FILE"

# Set up fetch hook (if agent supports)
export AGENT_FETCH_HOOK="python $SCRIPT_DIR/track-fetch.py $DOC_FETCH_FILE"

# Run agent
agent_execute ... > "$LOG_FILE" 2>&1

# Alternative: Parse from logs
grep "Fetched:" "$LOG_FILE" | while IFS= read -r line; do
  URL=$(echo "$line" | sed -n 's/.*Fetched: \(.*\)/\1/p')
  TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  
  # Append to tracking file
  jq ".fetches += [{\"url\": \"$URL\", \"timestamp\": \"$TIMESTAMP\"}]" \
    "$DOC_FETCH_FILE" > "$DOC_FETCH_FILE.tmp"
  mv "$DOC_FETCH_FILE.tmp" "$DOC_FETCH_FILE"
done

# Extract summary
TOTAL_FETCHES=$(jq '.fetches | length' "$DOC_FETCH_FILE")
DOMAINS=$(jq -r '[.fetches[].url | split("/")[2]] | unique | .[]' "$DOC_FETCH_FILE" | jq -R . | jq -s .)

# Add to result JSON
jq ".documentation_fetches = {
  \"total_count\": $TOTAL_FETCHES,
  \"pages\": $(jq '.fetches' "$DOC_FETCH_FILE"),
  \"domains\": $DOMAINS
}" "$RESULT_FILE" > "$RESULT_FILE.tmp"
mv "$RESULT_FILE.tmp" "$RESULT_FILE"
```

## Best Practices

### For Test Scenarios

1. **Set realistic bounds**
   ```yaml
   min_fetches: 2    # At least some documentation
   max_fetches: 10   # Not excessive
   ```

2. **Focus on critical pages**
   ```yaml
   expected_pages:
     - pattern: "docs.sonarsource.com.*scanner"  # Scanner docs
     - pattern: "platform-specific-docs"          # CI/CD platform docs
   ```

3. **Include all relevant domains**
   ```yaml
   expected_domains:
     - "docs.sonarsource.com"  # Official SonarQube docs
     - "github.com"             # GitHub Actions
     - "docs.gitlab.com"        # GitLab CI (if applicable)
   ```

### For Agent Implementation

1. **Log all fetches** - Even if cached
2. **Include timestamps** - Track when fetches occur
3. **Track failures** - Note if fetch fails
4. **Deduplicate** - Count unique pages

## Common Patterns

### Maven + GitHub Actions
Typical fetches (3-5 pages):
- Maven scanner documentation
- GitHub Actions checkout
- GitHub Actions setup-java
- SonarCloud getting started

### Gradle + GitLab CI
Typical fetches (3-5 pages):
- Gradle scanner documentation
- GitLab CI YAML reference
- SonarQube server setup
- Gradle plugin docs

### JavaScript + Bitbucket
Typical fetches (4-6 pages):
- CLI scanner documentation
- Bitbucket Pipelines reference
- Node.js setup
- sonar-project.properties guide

## Troubleshooting

### No Fetches Recorded
- Check if agent has web/fetch capability enabled
- Verify fetch tracking code is running
- Check log file for fetch events

### Too Many Fetches
- Agent might be inefficient
- Consider caching documentation
- Review fetch patterns

### Wrong Pages Fetched
- Agent might be confused about project type
- Check if correct skills are invoked
- Verify project detection

---

**Related:**
- [README.md](README.md) - Main test framework documentation
- [TESTING_STRATEGY.md](TESTING_STRATEGY.md) - Overall testing strategy
- [validate-result.py](scripts/validate-result.py) - Validation implementation
