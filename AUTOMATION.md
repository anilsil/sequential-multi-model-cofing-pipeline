# Automation Guide - with Claude Code CLI

This guide shows how to automate the agentic-code pipeline using **Claude Code CLI** (no API keys needed).

## Why Automate with Claude Code CLI?

| Feature | Manual Mode | API Mode | Claude CLI Auto |
|---------|-------------|----------|-----------------|
| **Cost** | $0 | $$$$ | **$0** |
| **API Keys** | None | Required | **None** |
| **Speed** | Slow (manual) | Fast | **Fast** |
| **Jumping Windows** | Yes (annoying) | No | **No** |
| **Audit Trail** | Complete | Complete | **Complete** |

## Prerequisites

1. **Claude Code CLI** installed:
   ```bash
   # Install from https://claude.com/code
   # Or use your package manager
   ```

2. **Verify installation**:
   ```bash
   claude --version
   ```

3. **Install agentic-code**:
   ```bash
   cd agentic-code
   pip install -e .
   ```

## Quick Start - Fully Automated

Run the entire pipeline with one command:

```bash
# Full automation with Claude Code CLI
python scripts/fully_automated.py examples/simple-function.md --skip-verification
```

That's it! No window switching, no copy-paste.

## How It Works

The automation script:

1. **Reads generated prompts** from the pipeline
2. **Calls Claude Code CLI** programmatically: `claude chat --no-stream < prompt.md`
3. **Captures responses** automatically
4. **Saves to correct files** for audit trail
5. **Progresses through all stages** without manual intervention

### Architecture

```
┌─────────────────────────────────────────────────────┐
│  AUTOMATED PIPELINE                                  │
├─────────────────────────────────────────────────────┤
│                                                      │
│  1. Repository Analysis                             │
│     ├─ Generate prompt                              │
│     ├─ Call: claude chat < prompt.md               │
│     └─ Save response automatically                  │
│                                                      │
│  2. Task Planning                                   │
│     ├─ Generate prompt                              │
│     ├─ Call: claude chat < prompt.md               │
│     └─ Save YAML automatically                      │
│                                                      │
│  3. Code Generation                                 │
│     ├─ Generate prompt                              │
│     └─ YOU implement in your IDE (manual step)      │
│                                                      │
│  4. Verification [Optional]                         │
│     ├─ Generate prompt                              │
│     └─ Paste into Gemini web OR skip                │
│                                                      │
│  5. Integration Decision                            │
│     ├─ Generate prompt                              │
│     ├─ Call: claude chat < prompt.md               │
│     └─ Save decision automatically                  │
│                                                      │
└─────────────────────────────────────────────────────┘
```

### What's Still Manual?

Only **Stage 3: Code Generation** requires manual work:
- You still need to write code in your IDE (Cursor, VSCode, etc.)
- This is intentional - the tool is for **governance**, not replacing you

Optionally manual:
- **Stage 4: Verification** - Can skip or use Gemini web

## Usage Examples

### Basic Automation

```bash
# Automate with Claude CLI (stages 1, 2, 5 automated)
python scripts/fully_automated.py examples/simple-function.md
```

### Skip Verification

```bash
# Skip verification step for faster execution
python scripts/fully_automated.py examples/simple-function.md --skip-verification
```

### What Happens

```
🚀 FULLY AUTOMATED AGENTIC CODE
Task: examples/simple-function.md
Mode: Claude Code CLI
Automation: Fully automated (no manual steps)

Run directory: output/2025-12-15_224530_simple-function

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏳ Stage 1: Repository Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤖 Calling Claude Code CLI...
✓ Received response (1,234 characters)
✓ Stage 1: Repository Analysis

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏳ Stage 2: Task Planning
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤖 Calling Claude Code CLI...
✓ Received response (892 characters)
✓ Stage 2: Task Planning

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏸  Stage 3: Code Generation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏸  MANUAL STEP REQUIRED
Please implement the code as specified in:
output/2025-12-15_224530_simple-function/codex_implementation_prompt.md
Save generated code to: output/.../generated_code/

Press Enter when code is ready...
```

## Advanced: Shell Script Automation

For maximum control, use the bash script:

```bash
# Make executable
chmod +x automate.sh

# Run
./automate.sh examples/simple-function.md --skip-verification
```

The shell script shows how to:
- Call `claude chat` from bash
- Capture output
- Handle errors
- Process responses

## Troubleshooting

### "Claude CLI not found"

```bash
# Install Claude Code CLI from:
# https://claude.com/code

# Verify:
claude --version
```

### "Empty response from Claude CLI"

Check if Claude CLI is authenticated:
```bash
# Try running Claude CLI manually first:
claude chat

# If prompted, authenticate
```

### "Timeout expired"

Increase timeout for complex prompts:
```python
# In scripts/fully_automated.py, line with call_claude_cli:
task_spec = call_claude_cli(planning_prompt, timeout=300)  # 5 minutes
```

## Comparison: Manual vs Automated

### Manual Mode (Original)

```bash
# Start pipeline
agentic-code run task.md

# Switch to Claude Code CLI window
# Copy prompt from output/*/claude_analysis_prompt.md
# Paste into Claude CLI
# Copy response
# Switch back
# Paste into output/*/claude_analysis_response.txt
# Confirm 'y'

# Repeat for every stage... 😓
```

### Automated Mode (New!)

```bash
# One command
python scripts/fully_automated.py task.md

# Only stop for code implementation
# Everything else automated ✨
```

## Cost Comparison

| Approach | Cost per Task | Cost per 100 Tasks |
|----------|---------------|---------------------|
| **Manual (prompt mode)** | $0 | **$0** |
| **Automated (Claude CLI)** | $0 | **$0** |
| **API mode (Anthropic)** | ~$0.15 | **~$15** |
| **API mode (OpenAI GPT-4)** | ~$0.30 | **~$30** |

**Winner**: Automated with Claude CLI - **Fast with subscription-based pricing** (no pay-per-use)! 🎉

## Customization

### Custom Claude CLI Arguments

Edit `scripts/fully_automated.py`, function `call_claude_cli()`:

```python
result = subprocess.run(
    [
        "claude", "chat",
        "--no-stream",           # Don't stream output
        "--model", "opus",       # Use specific model
        "--max-tokens", "8192"   # Longer responses
    ],
    input=prompt,
    capture_output=True,
    text=True,
    timeout=timeout,
    check=True
)
```

### Add Logging

```python
# Add after each call_claude_cli():
with open(run_dir / "automation.log", "a") as log:
    log.write(f"[{datetime.now()}] Stage completed\n")
```

### Parallel Execution

For multiple tasks:

```bash
# Run multiple tasks in parallel
python scripts/fully_automated.py task1.md --skip-verification &
python scripts/fully_automated.py task2.md --skip-verification &
python scripts/fully_automated.py task3.md --skip-verification &
wait
```

## Integration with CI/CD

```yaml
# .github/workflows/agentic-code.yml
name: Agentic Code Review

on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Install Claude Code CLI
        run: |
          # Install Claude CLI
          curl -sSL https://claude.com/install.sh | sh

      - name: Install agentic-code
        run: pip install -e .

      - name: Run automated review
        run: |
          python scripts/fully_automated.py \
            .github/tasks/pr-review.md \
            --skip-verification

      - name: Upload artifacts
        uses: actions/upload-artifact@v2
        with:
          name: agentic-code-review
          path: output/
```

## Best Practices

1. **Still review the artifacts** - Automation doesn't mean blind trust
2. **Keep audit trail** - All prompts and responses are saved
3. **Use --skip-verification for speed** - Verification is optional for simple tasks
4. **Manual code implementation** - This step should stay manual for quality
5. **Check decisions** - Review `integration_decision.yaml` before merging

## FAQ

**Q: Does this require API keys?**
A: No! Claude Code CLI requires no API keys, and we're just calling it programmatically.

**Q: How is this different from Cursor?**
A: This is for **governance** and **multi-model workflows with separation of duties**, not just code generation.

**Q: Can I use API keys instead?**
A: Yes, but it costs per task ($0.15-0.30). Claude CLI uses subscription pricing (Claude Pro $20/mo)!

**Q: What about Codex/GPT for stage 3?**
A: Stage 3 is still manual - you implement in your IDE with Cursor/Copilot/etc.

**Q: Can I automate stage 3 too?**
A: You could, but then you lose the human review. The point is governance!

## Summary

✅ **Subscription-based** - Uses Claude Code CLI (Claude Pro subscription required)
✅ **Fast** - No manual copy-paste
✅ **Automated** - One command runs entire pipeline
✅ **Auditable** - Complete artifact trail preserved
✅ **Governed** - Still enforces separation of duties

**Best of both worlds**: Speed of automation + Subscription pricing (no pay-per-use)! 🚀
