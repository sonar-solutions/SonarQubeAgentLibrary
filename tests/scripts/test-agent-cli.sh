#!/usr/bin/env bash

# test-agent-cli.sh - Test agent CLI access capabilities
# This script tests different methods of invoking the SonarArchitectLight agent from command line

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}Agent CLI Access Test${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Test 1: Check if VS Code CLI is available
echo -e "${YELLOW}[Test 1]${NC} Checking VS Code CLI access..."
if command -v code &> /dev/null; then
    CODE_VERSION=$(code --version | head -n1)
    echo -e "${GREEN}✓${NC} VS Code CLI found: $CODE_VERSION"
else
    echo -e "${RED}✗${NC} VS Code CLI not found"
    echo -e "  ${YELLOW}→${NC} Install with: ln -s '/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code' /usr/local/bin/code"
    echo ""
    exit 1
fi

# Test 2: List installed extensions
echo ""
echo -e "${YELLOW}[Test 2]${NC} Checking installed extensions..."
echo -e "${BLUE}Extensions matching 'sonar':${NC}"
code --list-extensions | grep -i sonar || echo -e "${YELLOW}  No extensions matching 'sonar' found${NC}"

echo ""
echo -e "${BLUE}All installed extensions:${NC}"
code --list-extensions | head -n 10
TOTAL_EXTENSIONS=$(code --list-extensions | wc -l | tr -d ' ')
if [[ $TOTAL_EXTENSIONS -gt 10 ]]; then
    echo "  ... and $((TOTAL_EXTENSIONS - 10)) more"
fi

# Test 3: Test command execution via URI
echo ""
echo -e "${YELLOW}[Test 3]${NC} Testing VS Code command execution..."
echo -e "${BLUE}Available methods:${NC}"
echo "  1. code --open-url 'vscode://command/workbench.action.showCommands'"
echo "  2. code --list-extensions (already working ✓)"
echo "  3. code --extensionDevelopmentPath <path>"

# Test 4: Check if agent extension exposes CLI commands
echo ""
echo -e "${YELLOW}[Test 4]${NC} Checking for GitHub Copilot CLI..."
if command -v gh &> /dev/null; then
    echo -e "${GREEN}✓${NC} GitHub CLI found"
    
    # Check if gh copilot is available (built-in or extension)
    if gh copilot -- --version &> /dev/null; then
        COPILOT_VERSION=$(gh copilot -- --version 2>&1 | head -n1)
        echo -e "${GREEN}✓${NC} GitHub Copilot CLI available: $COPILOT_VERSION"
        echo ""
        echo -e "${BLUE}Test commands:${NC}"
        echo "  gh copilot suggest 'Setup SonarQube analysis for Maven project'"
        echo "  gh copilot explain 'what does this pom.xml do'"
    else
        echo -e "${YELLOW}!${NC} GitHub Copilot CLI not available"
        echo -e "  ${BLUE}Note:${NC} Run 'gh copilot' to download it"
    fi
else
    echo -e "${YELLOW}!${NC} GitHub CLI not found"
    echo -e "  ${BLUE}Install with:${NC} brew install gh"
fi

# Test 5: Check for custom agent CLI
echo ""
echo -e "${YELLOW}[Test 5]${NC} Checking for custom agent CLI tools..."
CUSTOM_COMMANDS=("sonar-architect" "sonararchitect" "sonar-agent" "sonaragent")
FOUND_CUSTOM=false

for cmd in "${CUSTOM_COMMANDS[@]}"; do
    if command -v "$cmd" &> /dev/null; then
        echo -e "${GREEN}✓${NC} Found: $cmd"
        FOUND_CUSTOM=true
    fi
done

if [[ "$FOUND_CUSTOM" == "false" ]]; then
    echo -e "${YELLOW}!${NC} No custom agent CLI found"
fi

# Summary
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}Recommendations:${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "For VS Code extension invocation, you can:"
echo ""
echo "Option A: Use GitHub Copilot CLI (if extension is Copilot-based)"
echo "  ${BLUE}→${NC} gh copilot suggest '<your-prompt>'"
echo ""
echo "Option B: Create a VS Code task/command wrapper"
echo "  ${BLUE}→${NC} code --new-window <project-path>"
echo "  ${BLUE}→${NC} Use VS Code API to invoke extension commands"
echo ""
echo "Option C: Build a custom CLI wrapper around your extension"
echo "  ${BLUE}→${NC} node cli-wrapper.js --extension <ext-id> --command <cmd>"
echo ""
echo "Option D: Use VS Code automation (puppeteer-like)"
echo "  ${BLUE}→${NC} Automate VS Code UI interactions programmatically"
echo ""
echo -e "${YELLOW}Next Step:${NC}"
echo "  Tell me your extension ID or how you currently invoke it in VS Code,"
echo "  and I'll create the appropriate wrapper for run-scenario.sh"
echo ""
