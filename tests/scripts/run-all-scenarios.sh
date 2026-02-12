#!/usr/bin/env bash

# run-all-scenarios.sh - Execute all test scenarios or filtered subset
# Usage: ./run-all-scenarios.sh [--model <model>] [--language <lang>] [--platform <platform>]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TESTS_DIR="$(dirname "$SCRIPT_DIR")"

# Default values
MODEL="${MODEL:-claude-sonnet-4}"
FILTER_LANGUAGE=""
FILTER_PLATFORM=""
PARALLEL=false

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --model)
      MODEL="$2"
      shift 2
      ;;
    --language)
      FILTER_LANGUAGE="$2"
      shift 2
      ;;
    --platform)
      FILTER_PLATFORM="$2"
      shift 2
      ;;
    --parallel)
      PARALLEL=true
      shift
      ;;
    --help|-h)
      echo "Usage: $0 [OPTIONS]"
      echo ""
      echo "Options:"
      echo "  --model <name>      LLM model to use (default: claude-sonnet-4)"
      echo "  --language <lang>   Filter by language (maven, gradle, dotnet, javascript, python)"
      echo "  --platform <plat>   Filter by platform string in filename"
      echo "  --parallel          Run scenarios in parallel (experimental)"
      echo ""
      echo "Examples:"
      echo "  $0 --model claude-sonnet-4"
      echo "  $0 --language maven --model gpt-4-turbo"
      echo "  $0 --language javascript --platform github"
      exit 0
      ;;
    *)
      echo -e "${RED}Unknown option: $1${NC}"
      exit 1
      ;;
  esac
done

# Find all scenario files
SCENARIOS_DIR="$TESTS_DIR/scenarios"
SCENARIO_FILES=()

if [[ -n "$FILTER_LANGUAGE" ]]; then
  # Filter by language
  SEARCH_DIR="$SCENARIOS_DIR/$FILTER_LANGUAGE"
  if [[ ! -d "$SEARCH_DIR" ]]; then
    echo -e "${RED}Error: Language directory not found: $SEARCH_DIR${NC}"
    exit 1
  fi
  while IFS= read -r -d '' file; do
    if [[ -z "$FILTER_PLATFORM" ]] || [[ "$file" == *"$FILTER_PLATFORM"* ]]; then
      SCENARIO_FILES+=("$file")
    fi
  done < <(find "$SEARCH_DIR" -name "*.yaml" -print0)
else
  # All languages
  while IFS= read -r -d '' file; do
    if [[ -z "$FILTER_PLATFORM" ]] || [[ "$file" == *"$FILTER_PLATFORM"* ]]; then
      SCENARIO_FILES+=("$file")
    fi
  done < <(find "$SCENARIOS_DIR" -name "*.yaml" -print0)
fi

TOTAL_SCENARIOS=${#SCENARIO_FILES[@]}

if [[ $TOTAL_SCENARIOS -eq 0 ]]; then
  echo -e "${RED}No scenarios found matching criteria${NC}"
  exit 1
fi

# Print header
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}SonarArchitectLight Test Suite${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${BLUE}Model:${NC} $MODEL"
echo -e "${BLUE}Total Scenarios:${NC} $TOTAL_SCENARIOS"
if [[ -n "$FILTER_LANGUAGE" ]]; then
  echo -e "${BLUE}Language Filter:${NC} $FILTER_LANGUAGE"
fi
if [[ -n "$FILTER_PLATFORM" ]]; then
  echo -e "${BLUE}Platform Filter:${NC} $FILTER_PLATFORM"
fi
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Run scenarios
PASSED=0
FAILED=0
CURRENT=0

for scenario in "${SCENARIO_FILES[@]}"; do
  CURRENT=$((CURRENT + 1))
  REL_PATH="${scenario#$SCENARIOS_DIR/}"
  
  echo -e "${YELLOW}[$CURRENT/$TOTAL_SCENARIOS]${NC} Running: $REL_PATH"
  
  if "$SCRIPT_DIR/run-scenario.sh" "$REL_PATH" --model "$MODEL" > /dev/null 2>&1; then
    echo -e "  ${GREEN}✓ PASSED${NC}"
    PASSED=$((PASSED + 1))
  else
    echo -e "  ${RED}✗ FAILED${NC}"
    FAILED=$((FAILED + 1))
  fi
  echo ""
done

# Summary
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}Test Suite Summary${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "Total Scenarios: $TOTAL_SCENARIOS"
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"

if [[ $FAILED -eq 0 ]]; then
  echo -e "\n${GREEN}✓ All tests passed!${NC}"
  echo ""
else
  echo -e "\n${RED}✗ Some tests failed${NC}"
  echo ""
  exit 1
fi

# Generate summary report
echo "Generating summary report..."
"$SCRIPT_DIR/generate-summary.py" --model "$MODEL"

echo ""
echo "Results saved to: $TESTS_DIR/results/$MODEL/"
echo ""
