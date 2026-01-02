#!/bin/bash
# Automation script for agentic-code using Claude Code CLI (100% FREE)
#
# This script automates the prompt orchestrator by:
# 1. Reading generated prompts
# 2. Passing them to Claude Code CLI (free)
# 3. Saving responses automatically
# 4. Progressing through all stages
#
# Requirements:
# - Claude Code CLI installed (https://claude.com/code)
# - Task file path as argument
#
# Usage:
#   ./automate.sh examples/simple-function.md
#   ./automate.sh examples/simple-function.md --skip-verification

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Check if Claude Code CLI is available
if ! command -v claude &> /dev/null; then
    echo -e "${RED}Error: Claude Code CLI not found${NC}"
    echo "Install from: https://claude.com/code"
    exit 1
fi

# Check arguments
if [ $# -lt 1 ]; then
    echo "Usage: $0 <task-file> [--skip-verification]"
    echo "Example: $0 examples/simple-function.md --skip-verification"
    exit 1
fi

TASK_FILE="$1"
SKIP_VERIFICATION="${2:-}"

echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}🚀 Automated Agentic Code (FREE)${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""
echo -e "${BLUE}Task: $TASK_FILE${NC}"
echo -e "${BLUE}Mode: Claude Code CLI (100% FREE)${NC}"
echo ""

# Step 1: Start the pipeline (will generate first prompt and wait)
echo -e "${YELLOW}Starting pipeline...${NC}"

# Run in background, capture output directory
if [ "$SKIP_VERIFICATION" = "--skip-verification" ]; then
    OUTPUT=$(agentic-code run "$TASK_FILE" --skip-verification 2>&1 | tee /dev/tty)
else
    OUTPUT=$(agentic-code run "$TASK_FILE" 2>&1 | tee /dev/tty)
fi

# Extract run directory from output
RUN_DIR=$(echo "$OUTPUT" | grep "Run directory:" | awk '{print $3}')

if [ -z "$RUN_DIR" ]; then
    echo -e "${RED}Could not determine run directory${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Run directory: $RUN_DIR${NC}"

# Function to call Claude CLI with a prompt file and save response
call_claude() {
    local prompt_file="$1"
    local response_file="$2"
    local stage_name="$3"

    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}🤖 Stage: $stage_name${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

    if [ ! -f "$prompt_file" ]; then
        echo -e "${RED}Prompt file not found: $prompt_file${NC}"
        return 1
    fi

    echo -e "${CYAN}Reading prompt: $prompt_file${NC}"

    # Call Claude Code CLI with the prompt content
    # Using 'claude chat' in non-interactive mode with prompt from file
    echo -e "${YELLOW}Calling Claude CLI...${NC}"

    # Read prompt and pass to claude
    PROMPT_CONTENT=$(cat "$prompt_file")

    # Call claude in batch mode (you may need to adjust based on your Claude CLI version)
    # Option 1: Using echo and pipe
    echo "$PROMPT_CONTENT" | claude chat --no-stream > "$response_file" 2>&1

    # Alternative Option 2: Using heredoc
    # claude chat --no-stream <<EOF > "$response_file"
    # $PROMPT_CONTENT
    # EOF

    if [ $? -eq 0 ] && [ -s "$response_file" ]; then
        RESPONSE_SIZE=$(wc -c < "$response_file")
        echo -e "${GREEN}✓ Response saved: $response_file ($RESPONSE_SIZE bytes)${NC}"
        return 0
    else
        echo -e "${RED}Failed to get response from Claude CLI${NC}"
        return 1
    fi
}

# Wait for pipeline to create prompt files
sleep 2

# Stage 1: Repository Analysis
echo ""
echo -e "${CYAN}Stage 1: Repository Analysis${NC}"
ANALYSIS_PROMPT="$RUN_DIR/claude_analysis_prompt.md"
ANALYSIS_RESPONSE="$RUN_DIR/claude_analysis_response.txt"

if [ -f "$ANALYSIS_PROMPT" ]; then
    call_claude "$ANALYSIS_PROMPT" "$ANALYSIS_RESPONSE" "Repository Analysis"
else
    echo -e "${YELLOW}Waiting for analysis prompt to be generated...${NC}"
    # Could add retry logic here
fi

# Signal to pipeline that response is ready (press 'y' automatically)
# This part would need integration with the Python pipeline

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}Automation script structure complete${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${YELLOW}Note: This is a template. For full automation, you need to:${NC}"
echo -e "1. Run the pipeline in background"
echo -e "2. Monitor for prompt file creation"
echo -e "3. Call Claude CLI automatically"
echo -e "4. Save responses"
echo -e "5. Signal pipeline to continue"
echo ""
echo -e "${CYAN}See: scripts/fully_automated.py for Python implementation${NC}"
