#!/usr/bin/env bash

# run-scenario.sh - Execute a single test scenario
# Usage: ./run-scenario.sh <scenario-file> --model <model-name> [--verbose]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TESTS_DIR="$(dirname "$SCRIPT_DIR")"
WORKSPACE_ROOT="$(dirname "$TESTS_DIR")"

# Default values
MODEL="${MODEL:-claude-sonnet-4}"
VERBOSE=false
SCENARIO_FILE=""
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Constants
TIME_FORMAT='%H:%M:%S'
SEPARATOR='━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --model)
      MODEL="$2"
      shift 2
      ;;
    --verbose|-v)
      VERBOSE=true
      shift
      ;;
    --help|-h)
      echo "Usage: $0 <scenario-file> --model <model-name> [--verbose]"
      echo ""
      echo "Arguments:"
      echo "  scenario-file    Path to scenario YAML file (relative to tests/scenarios/)"
      echo "  --model          LLM model to use (default: claude-sonnet-4)"
      echo "  --verbose        Enable verbose output"
      echo ""
      echo "Example:"
      echo "  $0 maven/github-actions-cloud.yaml --model claude-sonnet-4"
      exit 0
      ;;
    *)
      if [[ -z "$SCENARIO_FILE" ]]; then
        SCENARIO_FILE="$1"
      fi
      shift
      ;;
  esac
done

# Validate scenario file
if [[ -z "$SCENARIO_FILE" ]]; then
  echo -e "${RED}Error: No scenario file specified${NC}" >&2
  echo "Usage: $0 <scenario-file> --model <model-name>"
  exit 1
fi

# Construct full path to scenario
if [[ ! "$SCENARIO_FILE" = /* ]]; then
  SCENARIO_FILE="$TESTS_DIR/scenarios/$SCENARIO_FILE"
fi

if [[ ! -f "$SCENARIO_FILE" ]]; then
  echo -e "${RED}Error: Scenario file not found: $SCENARIO_FILE${NC}" >&2
  exit 1
fi

# Extract scenario name
SCENARIO_NAME=$(basename "$SCENARIO_FILE" .yaml)
LANGUAGE=$(basename "$(dirname "$SCENARIO_FILE")")

# Create results directory
RESULTS_DIR="$TESTS_DIR/results/$MODEL"
mkdir -p "$RESULTS_DIR"

RESULT_FILE="$RESULTS_DIR/${LANGUAGE}-${SCENARIO_NAME}.json"
LOG_FILE="$RESULTS_DIR/${LANGUAGE}-${SCENARIO_NAME}.log"

# Print header
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}SonarArchitectLight Test Execution${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${BLUE}Scenario:${NC} $SCENARIO_NAME"
echo -e "${BLUE}Language:${NC} $LANGUAGE"
echo -e "${BLUE}Model:${NC} $MODEL"
echo -e "${BLUE}Timestamp:${NC} $TIMESTAMP"
echo ""

# Start test execution
START_TIME=$(date +%s)
echo -e "${YELLOW}[$(date +"$TIME_FORMAT")]${NC} Starting test scenario..."

# Parse scenario file to build prompt
echo -e "${YELLOW}[$(date +"$TIME_FORMAT")]${NC} Loading scenario definition..."

# Extract key information from YAML
PLATFORM=$(grep "^platform:" "$SCENARIO_FILE" | awk '{print $2}' | tr -d '"')
SONARQUBE_TYPE=$(grep "^sonarqube:" "$SCENARIO_FILE" | awk '{print $2}' | tr -d '"')
DESCRIPTION=$(grep "^description:" "$SCENARIO_FILE" | cut -d':' -f2- | sed 's/^ *//' | tr -d '"')

if [[ -z "$PLATFORM" || -z "$SONARQUBE_TYPE" ]]; then
    echo -e "${RED}Error: Failed to parse scenario file${NC}" >&2
    echo "Platform: $PLATFORM, SonarQube: $SONARQUBE_TYPE"
    exit 1
fi

# Create temporary workspace for test
TEST_WORKSPACE="$RESULTS_DIR/.workspace-${SCENARIO_NAME}-$$"
mkdir -p "$TEST_WORKSPACE"
echo -e "${YELLOW}[$(date +"$TIME_FORMAT")]${NC} Created test workspace: $TEST_WORKSPACE"

# Copy project fixture if it exists
FIXTURE_DIR="$TESTS_DIR/fixtures/projects/${LANGUAGE}-simple"
if [[ -d "$FIXTURE_DIR" ]]; then
    cp -r "$FIXTURE_DIR"/* "$TEST_WORKSPACE/"
    echo -e "${YELLOW}[$(date +"$TIME_FORMAT")]${NC} Copied project fixture for $LANGUAGE"
fi

# Build prompt for agent - include expected responses directly
AGENT_PROMPT="Setup SonarQube analysis for a $LANGUAGE project using $PLATFORM. "
AGENT_PROMPT+="Target: $SONARQUBE_TYPE. "
AGENT_PROMPT+="$DESCRIPTION "

# Parse user_responses from scenario and include in prompt
echo -e "${YELLOW}[$(date +"$TIME_FORMAT")]${NC} Preparing test configuration..."
USER_RESPONSES=$(grep -A 100 "user_responses:" "$SCENARIO_FILE" | grep "answer:" | sed 's/.*answer: *//' | tr -d '"')
RESPONSE_COUNT=$(echo "$USER_RESPONSES" | grep -c . || echo "0")

if [[ "$RESPONSE_COUNT" -gt 0 ]]; then
    # Extract key information from responses
    PROJECT_KEY=""
    ORG_KEY=""
    SERVER_URL=""
    REGION=""
    
    if echo "$USER_RESPONSES" | grep -qi "cloud"; then
        # Parse Cloud response: "Cloud, project-key, org-key, US/EU"
        CLOUD_INFO=$(echo "$USER_RESPONSES" | grep -i "cloud")
        PROJECT_KEY=$(echo "$CLOUD_INFO" | cut -d',' -f2 | tr -d ' ')
        ORG_KEY=$(echo "$CLOUD_INFO" | cut -d',' -f3 | tr -d ' ')
        REGION=$(echo "$CLOUD_INFO" | cut -d',' -f4 | tr -d ' ')
        
        AGENT_PROMPT+="Use SonarQube Cloud with project key '$PROJECT_KEY' and organization '$ORG_KEY' in the $REGION region. "
    elif echo "$USER_RESPONSES" | grep -qi "server"; then
        # Parse Server response: "Server, https://url, project-key"
        SERVER_INFO=$(echo "$USER_RESPONSES" | grep -i "server")
        SERVER_URL=$(echo "$SERVER_INFO" | cut -d',' -f2 | tr -d ' ')
        PROJECT_KEY=$(echo "$SERVER_INFO" | cut -d',' -f3 | tr -d ' ')
        
        AGENT_PROMPT+="Use SonarQube Server at '$SERVER_URL' with project key '$PROJECT_KEY'. "
    fi
    
    if [[ "$VERBOSE" == "true" ]]; then
        echo -e "${BLUE}Parsed responses:${NC}"
        [[ -n "$PROJECT_KEY" ]] && echo "  Project key: $PROJECT_KEY"
        [[ -n "$ORG_KEY" ]] && echo "  Organization: $ORG_KEY"
        [[ -n "$SERVER_URL" ]] && echo "  Server URL: $SERVER_URL"
        [[ -n "$REGION" ]] && echo "  Region: $REGION"
    fi
fi

AGENT_PROMPT+="Create all necessary CI/CD configuration files with proper structure and best practices. "
AGENT_PROMPT+="Do not ask for additional information - proceed with the setup using the provided details."

echo -e "${YELLOW}[$(date +"$TIME_FORMAT")]${NC} Invoking SonarArchitectLight agent..."
if [[ "$VERBOSE" == "true" ]]; then
    echo -e "${BLUE}Full prompt:${NC}"
    echo "  $AGENT_PROMPT" | fold -s -w 80 | sed 's/^/  /'
fi

# Invoke agent and capture output
AGENT_OUTPUT="$RESULTS_DIR/${LANGUAGE}-${SCENARIO_NAME}.agent-output.txt"
cd "$TEST_WORKSPACE"

# Use non-interactive mode with auto-approval
# --allow-all-tools: Allow tools to run without confirmation
if copilot --agent=SonarArchitectLight \
          --prompt "$AGENT_PROMPT" \
          --allow-all-tools \
          > "$AGENT_OUTPUT" 2>&1; then
    AGENT_STATUS="success"
    echo -e "${GREEN}✓${NC} Agent execution completed"
else
    AGENT_STATUS="failed"
    echo -e "${RED}✗${NC} Agent execution failed"
fi

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

# Return to original directory
cd "$WORKSPACE_ROOT"

# Capture created files
echo -e "${YELLOW}[$(date +"$TIME_FORMAT")]${NC} Capturing created files..."
FILES_CREATED=$(find "$TEST_WORKSPACE" -type f -newer "$RESULTS_DIR" 2>/dev/null || find "$TEST_WORKSPACE" -type f 2>/dev/null)

# Build files_created array for result JSON
FILES_JSON="[]"
if [[ -n "$FILES_CREATED" ]]; then
    FILES_JSON="["
    FIRST=true
    while IFS= read -r file; do
        if [[ -f "$file" ]]; then
            REL_PATH="${file#$TEST_WORKSPACE/}"
            CONTENT=$(cat "$file" | jq -Rs '.')
            
            if [[ "$FIRST" == "true" ]]; then
                FIRST=false
            else
                FILES_JSON+=","
            fi
            
            FILES_JSON+="{\"path\":\"$REL_PATH\",\"content\":$CONTENT}"
        fi
    done <<< "$FILES_CREATED"
    FILES_JSON+="]"
fi

# Extract documentation fetches from agent output (if logged)
# Look for patterns like "Fetched: https://docs.sonarsource.com/..."
DOC_FETCHES=$(grep -oE 'https?://[^ ]+' "$AGENT_OUTPUT" | grep -E '(docs\.sonarsource|github\.com|docs\.gitlab|learn\.microsoft|docs\.azure)' 2>/dev/null || true)
if [[ -z "$DOC_FETCHES" ]]; then
    DOC_COUNT="0"
else
    DOC_COUNT=$(echo "$DOC_FETCHES" | wc -l | tr -d ' ')
fi

# Build documentation_fetches JSON
DOC_JSON='{"total_count":'$DOC_COUNT',"pages":[],"domains":[]}'
if [[ "$DOC_COUNT" -gt 0 ]]; then
    DOC_PAGES="["
    DOC_DOMAINS="["
    FIRST=true
    while IFS= read -r url; do
        if [[ -n "$url" ]]; then
            DOMAIN=$(echo "$url" | awk -F[/:] '{print $4}')
            
            if [[ "$FIRST" == "true" ]]; then
                FIRST=false
            else
                DOC_PAGES+=","
                DOC_DOMAINS+=","
            fi
            
            DOC_PAGES+="{\"url\":\"$url\",\"timestamp\":\"$(date -u +"%Y-%m-%dT%H:%M:%SZ")\"}"
            DOC_DOMAINS+="\"$DOMAIN\""
        fi
    done <<< "$DOC_FETCHES"
    DOC_PAGES+="]"
    DOC_DOMAINS+="]"
    DOC_JSON='{"total_count":'$DOC_COUNT',"pages":'$DOC_PAGES',"domains":'$DOC_DOMAINS'}'
fi

# Create result file
cat > "$RESULT_FILE" <<EOF
{
  "scenario": "$SCENARIO_NAME",
  "language": "$LANGUAGE",
  "model": "$MODEL",
  "platform": "$PLATFORM",
  "sonarqube_type": "$SONARQUBE_TYPE",
  "timestamp": "$TIMESTAMP",
  "status": "$AGENT_STATUS",
  "execution": {
    "start_time": "$(date -r $START_TIME -u +"%Y-%m-%dT%H:%M:%SZ")",
    "end_time": "$(date -r $END_TIME -u +"%Y-%m-%dT%H:%M:%SZ")",
    "duration_seconds": $DURATION,
    "workspace": "$TEST_WORKSPACE",
    "agent_output": "$AGENT_OUTPUT"
  },
  "files_created": $FILES_JSON,
  "documentation_fetches": $DOC_JSON,
  "scores": {
    "total": 0,
    "accuracy": 0,
    "security": 0,
    "efficiency": 0,
    "currency": 0,
    "usability": 0
  },
  "checkpoints": []
}
EOF

echo -e "${GREEN}✓${NC} Result file created: $RESULT_FILE"
echo ""

# Run validation
echo "$SEPARATOR"
echo -e "${YELLOW}[$(date +"$TIME_FORMAT")]${NC} Running validation..."
echo "$SEPARATOR"
echo ""

if python3 "$SCRIPT_DIR/validate-result.py" --scenario "$SCENARIO_FILE" --result "$RESULT_FILE"; then
    echo ""
    echo -e "${GREEN}✓${NC} Validation completed"
else
    echo ""
    echo -e "${RED}✗${NC} Validation failed"
fi

echo ""
echo "$SEPARATOR"
echo -e "${BLUE}Test workspace:${NC} $TEST_WORKSPACE"
echo -e "${BLUE}Agent output:${NC} $AGENT_OUTPUT"
echo -e "${BLUE}Result file:${NC} $RESULT_FILE"
echo -e "${BLUE}Duration:${NC} ${DURATION}s"
echo "$SEPARATOR"
echo ""
