# Agentic Code - Prompt Orchestrator

**Local-first, governed multi-model coding pipeline**

A CLI tool that orchestrates governed, multi-model coding workflows with **separation of duties** using **prompt generation** instead of API calls. Subscription-based tools, maximum control.

---

## 🎯 What Makes This Different

### **Traditional AI Coding Tools:**
- ❌ Single AI model does everything (plan, code, verify)
- ❌ Black-box execution (can't see prompts)
- ❌ API costs ($0.10-0.50 per task)
- ❌ No separation of duties
- ❌ Limited governance

### **Agentic Code (Prompt Orchestrator):**
- ✅ **Separation of duties** - Different AI models for different roles (multi-model architecture)
- ✅ **100% transparent** - See and edit every prompt
- ✅ **Subscription-based** - Uses tools like Claude Code CLI, Cursor, Gemini (no pay-per-use API charges)
- ✅ **Human-in-the-loop** - Review and approve every step
- ✅ **Complete audit trail** - Every decision documented
- ✅ **No API keys required** - Works with tools you already have

**Note**: This is a sequential multi-model pipeline with governance, not a concurrent multi-agent system with emergent behavior.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│  MULTI-MODEL SEQUENTIAL PIPELINE                        │
│  (Separation of Duties Architecture)                    │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  STAGE 1: Repository Analysis                           │
│  Model: Claude (Analyst Role) - via Claude Code CLI     │
│     ├─ Generate repo analysis prompt                    │
│     ├─ You paste into Claude Code CLI                   │
│     └─ You save response                                │
│                                                          │
│  STAGE 2: Task Planning                                 │
│  Model: Claude (Planner Role) - via Claude Code CLI     │
│     ├─ Generate task planning prompt                    │
│     ├─ You paste into Claude Code CLI                   │
│     └─ You save YAML spec                               │
│                                                          │
│  STAGE 3: Code Implementation                           │
│  Model: Codex/Cursor (Implementation Role)              │
│     ├─ Generate implementation prompt                   │
│     ├─ You paste into your AI IDE                       │
│     └─ You implement & save code                        │
│                                                          │
│  STAGE 4: Verification [OPTIONAL]                       │
│  Model: Gemini (Verification Role) - via web            │
│     ├─ Generate verification prompt                     │
│     ├─ You paste into Gemini web                        │
│     └─ You save JSON findings                           │
│                                                          │
│  STAGE 5: Integration Decision                          │
│  Model: Claude (Decision-Maker Role) - via Claude CLI   │
│     ├─ Generate integration decision prompt             │
│     ├─ You paste into Claude Code CLI                   │
│     └─ You save APPROVE/REJECT decision                 │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## ⚡ Execution Modes

This tool offers three distinct execution modes to fit your workflow, from fully manual to fully automated.

---

### **1. Prompt-Based (Manual)**

This is the default mode. It gives you maximum control by generating prompts for you to use in your existing AI tools (like the Claude Code CLI or Gemini's web interface).

**Usage:**
```bash
agentic-code run examples/simple-function.md
```
- **Cost:** Subscription-based tools (Claude Pro, Cursor, etc.) - no pay-per-use charges
- **Control:** Full human-in-the-loop at every stage.
- **Requirements:** Manual copy-pasting between tools.

---

### **2. Fully Automated (API-Based)**

This mode uses APIs directly for a truly hands-off experience. It's the fastest way to run the pipeline but requires you to have API keys. By default, it uses the Gemini API for code generation.

**Usage:**
```bash
# Ensure GEMINI_API_KEY and ANTHROPIC_API_KEY are set
python scripts/truly_automated_pipeline.py examples/simple-function.md
```
- **Cost:** Requires API credits for Gemini and Claude.
- **Control:** Automated execution with optional human review checkpoints.
- **Requirements:** `GEMINI_API_KEY` and `ANTHROPIC_API_KEY` environment variables.
- **Note:** You can override the code generation step to use a local CLI tool (like a `codex` CLI) by setting the `implementation_cli_command` in the configuration. See `agentic_code/config.py`.

---

### **3. CLI Orchestrator (Hybrid)**

This mode automates the calls to the Claude Code CLI but still requires manual steps for code implementation and the optional Gemini verification. It's a good balance between automation and cost.

**Usage:**
```bash
python scripts/hybrid_pipeline.py examples/simple-function.md
```
- **Cost:** Subscription-based (Claude Pro) - no pay-per-use charges
- **Control:** Partially automated, with manual steps for coding and verification.
- **Requirements:** Claude Code CLI installed (requires Claude Pro subscription).

---

## 🚀 Quick Start

### Installation

```bash
# Clone or navigate to the agentic-code directory
cd agentic-code

# Install
pip install -e .
```

### Run Your First Pipeline (Prompt-Based)

This is the recommended way to start, as it helps you understand each step of the process.

```bash
# Run with an example task
agentic-code run examples/simple-function.md

# The tool will:
# 1. Generate prompts in an `output/` directory.
# 2. Pause at each stage for you to provide responses.
# 3. Create a complete audit trail of the entire process.
```

The tool will guide you through each stage, telling you which prompts to use and where to save the responses.

---

## 📋 How It Works

### **Stage 1: Repository Analysis (Claude)**

**Tool generates:**
```markdown
# Repository Analysis Task
Analyze this repository and provide:
1. Primary Language(s)
2. Project Type
3. Key Frameworks
...
```

**You do:**
1. Open `output/.../claude_analysis_prompt.md`
2. Paste into **Claude Code CLI** (new conversation)
3. Copy Claude's response
4. Save to `output/.../claude_analysis_response.txt`
5. Confirm in tool (press `y`)

---

### **Stage 2: Task Planning (Claude)**

**Tool generates:**
```markdown
# Task Planning - Create Implementation Specification
Context: [repo analysis]
Task: [your task description]

Create YAML specification with:
- requirements
- files to modify
- implementation steps
...
```

**You do:**
1. Open `output/.../claude_planning_prompt.md`
2. Paste into **Claude Code CLI**
3. Copy Claude's YAML response
4. Save to `output/.../claude_planning_response.yaml`
5. Confirm in tool

---

### **Stage 3: Code Generation (Codex/Cursor)**

**Tool generates:**
```markdown
# Implementation Task for Codex
Follow this specification:
[task spec in YAML]

Output CODE ONLY to: output/.../generated_code/
```

**You do:**
1. Open `output/.../codex_implementation_prompt.md`
2. Paste into **Cursor, Copilot, or your AI IDE**
3. Implement the code
4. Save files to `output/.../generated_code/`
5. Confirm in tool

---

### **Stage 4: Verification (Gemini) [OPTIONAL]**

**Tool generates:**
```markdown
# Code Verification Task
Check this code for:
- Security issues
- Logic errors
- Race conditions
...

Output findings as JSON array.
```

**You do:**
1. Open `output/.../gemini_verification_prompt.md`
2. Paste into **https://gemini.google.com**
3. Copy JSON response
4. Save to `output/.../gemini_verification_response.json`
5. Confirm in tool (or skip this step)

---

### **Stage 5: Integration Decision (Claude)**

**Tool generates:**
```markdown
# Integration Decision - Review and Approve/Reject
Task: [spec]
Verification Findings: [issues found]

Decide: APPROVE / REJECT / APPROVE_WITH_NOTES
```

**You do:**
1. Open `output/.../claude_decision_prompt.md`
2. Paste into **Claude Code CLI**
3. Copy Claude's YAML decision
4. Save to `output/.../claude_decision_response.yaml`
5. Confirm in tool

---

## 🎓 Complete Example

```bash
# Terminal
$ cd /path/to/your/project
$ agentic-code run tasks/add-email-validation.md --skip-verification

============================================================
🚀 AGENTIC CODE PIPELINE (Prompt Orchestrator)
============================================================

⏳ Stage 1: Repository Analysis (Claude)
📝 Claude: Generating repository analysis prompt...
→ Prompt generated: output/2025-12-14_143022_add-email-validation/claude_analysis_prompt.md

⏸  HUMAN ACTION REQUIRED: Repository Analysis
STEPS:
1. Open Claude Code CLI (the tool you're using right now)
2. Paste the contents of: output/.../claude_analysis_prompt.md
3. Copy Claude's response
4. Save it to: output/.../claude_analysis_response.txt
5. Return here and confirm

Have you saved Claude's response to claude_analysis_response.txt? [y/n] (n): y

✓ Response loaded (1,234 characters)

⏳ Stage 2: Task Planning (Claude)
[... continues through all stages ...]

============================================================
⚖️  INTEGRATION DECISION
============================================================

Decision: APPROVE

rationale: |
  Code meets all requirements. Email validation logic is sound,
  edge cases are handled, and comprehensive tests are included.
  No security issues or performance concerns identified.

✓ Pipeline completed - Code approved for integration

============================================================
📊 PIPELINE SUMMARY
============================================================

Status: completed
Task: add-email-validation
Duration: 8m 23s
Decision: APPROVE

📦 Artifacts Created:
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━┓
┃ File                               ┃   Size ┃ Modified ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━┩
│ claude_analysis_prompt.md          │ 1.0 KB │ 14:30:22 │
│ claude_analysis_response.txt       │ 1.2 KB │ 14:31:45 │
│ claude_planning_prompt.md          │ 1.5 KB │ 14:32:01 │
│ claude_planning_response.yaml      │ 892 B  │ 14:33:12 │
│ task_spec.yaml                     │ 892 B  │ 14:33:12 │
│ codex_implementation_prompt.md     │ 2.1 KB │ 14:33:15 │
│ generated_code/utils/email.py      │ 1.8 KB │ 14:35:42 │
│ generated_code/tests/test_email.py │ 2.3 KB │ 14:35:42 │
│ claude_decision_prompt.md          │ 1.4 KB │ 14:36:01 │
│ claude_decision_response.yaml      │ 456 B  │ 14:38:22 │
│ integration_decision.yaml          │ 456 B  │ 14:38:22 │
└────────────────────────────────────┴────────┴──────────┘

Run directory: output/2025-12-14_143022_add-email-validation
```

---

## 📖 Usage

### Basic Command

```bash
agentic-code run <task-file>
```

### With Options

```bash
# Skip verification (faster, 4 stages instead of 5)
agentic-code run task.md --skip-verification

# Custom output directory
agentic-code run task.md --output /tmp/agentic-runs

# Both
agentic-code run task.md --skip-verification --output ./my-output
```

### Task File Formats

**Markdown (.md):**
```markdown
# Add Email Validation

Create a utility function to validate email addresses.

Requirements:
- Validate format using regex
- Handle edge cases
- Add tests
```

**YAML (.yaml):**
```yaml
name: add-email-validation
objective: Create email validation utility
requirements:
  - Regex-based validation
  - Edge case handling
  - Comprehensive tests
constraints:
  - No external dependencies
  - Follow existing utils pattern
```

**JSON (.json):**
```json
{
  "name": "add-email-validation",
  "objective": "Create email validation utility",
  "requirements": ["Regex validation", "Tests"]
}
```

---

## 🎯 Core Principles

### 1. **Separation of Duties**

No agent reviews its own work:

| Role | Plan | Implement | Verify | Decide |
|------|------|-----------|--------|--------|
| Claude | ✓ | ✗ | ✗ | ✓ |
| Codex | ✗ | ✓ | ✗ | ✗ |
| Gemini | ✗ | ✗ | ✓ | ✗ |
| **You** | Review | Required | Review | **Final Authority** |

### 2. **Human-in-the-Loop**

Every stage requires your approval:
- Review prompts before using them
- Review responses before saving them
- Edit prompts if needed
- Skip stages if appropriate
- **You have veto power at every step**

### 3. **Complete Auditability**

Every run creates:
- All prompts used
- All responses received
- Timestamp for each action
- Final decision with rationale
- Complete file manifest

### 4. **Subscription-Based Model**

Works with subscription-based tools (no pay-per-use API charges):
- **Claude Code CLI** - Requires Claude Pro subscription ($20/month)
- **Cursor** - Subscription-based tiers available
- **Gemini** - Free tier available with limits

---

## 🆚 Comparison

| Feature | API-Based Tools | Agentic Code (Prompt Orchestrator) |
|---------|-----------------|-------------------------------------|
| **Cost** | $0.10-0.50/task (pay-per-use) | **Subscription-based** (Claude Pro $20/mo) |
| **API Keys** | Required (3+) | **None required** |
| **Transparency** | Black box | **See every prompt** |
| **Control** | Auto-execution | **Human approval required** |
| **Auditability** | Limited logs | **Complete artifact trail** |
| **Security** | API key risks | **No keys to leak** |
| **Flexibility** | Fixed prompts | **Edit prompts anytime** |
| **Learning** | Hidden process | **Understand each step** |

---

## 💡 Best Practices

### **When to Use Agentic Code**

✅ **Great for:**
- Enterprise codebases requiring governance
- Security-critical implementations
- Learning how agentic systems work
- Building audit trails for compliance
- Complex refactoring tasks
- Team environments with review requirements

❌ **Not ideal for:**
- Quick one-line fixes
- Rapid prototyping iterations
- When you just want speed over governance

### **Tips for Success**

1. **Review prompts before pasting** - Make sure they make sense for your context
2. **Edit prompts if needed** - You can customize them before using
3. **Save responses accurately** - Don't skip or summarize AI responses
4. **Use descriptive task names** - Makes finding artifacts easier
5. **Skip verification for simple tasks** - Use `--skip-verification` flag
6. **Keep conversations focused** - Start fresh Claude conversation for each prompt

---

## 🛠️ Advanced Usage

### Custom Prompts

Edit generated prompts before using them:

```bash
# Tool generates prompt
→ output/.../claude_planning_prompt.md

# You can edit it before pasting:
nano output/.../claude_planning_prompt.md

# Then paste the edited version into Claude
```

### Reusing Responses

If you already have analysis or planning from previous runs:

```bash
# Copy existing response files to new run directory
cp old-run/claude_analysis_response.txt new-run/

# Tool will read it when you confirm
```

### Batch Processing

For multiple similar tasks:

```bash
# Create task files
for task in task1 task2 task3; do
  agentic-code run tasks/$task.md --skip-verification
done
```

---

## 📊 Artifact Structure

Every run creates a timestamped directory:

```
output/
└── 2025-12-14_143022_task-name/
    ├── claude_analysis_prompt.md          # Prompt: Repo analysis
    ├── claude_analysis_response.txt       # Response: What you pasted
    ├── claude_planning_prompt.md          # Prompt: Task planning
    ├── claude_planning_response.yaml      # Response: Implementation spec
    ├── task_spec.yaml                     # Extracted task specification
    ├── codex_implementation_prompt.md     # Prompt: Implementation
    ├── generated_code/                    # Your implemented code
    │   ├── src/feature.py
    │   ├── tests/test_feature.py
    │   └── summary.md
    ├── gemini_verification_prompt.md      # Prompt: Verification [if not skipped]
    ├── gemini_verification_response.json  # Response: Findings [if not skipped]
    ├── verification_findings.json         # Parsed findings
    ├── claude_decision_prompt.md          # Prompt: Integration decision
    ├── claude_decision_response.yaml      # Response: APPROVE/REJECT
    └── integration_decision.yaml          # Final decision
```

**Every artifact is:**
- ✅ Timestamped
- ✅ Human-readable
- ✅ Version-controllable (plain text)
- ✅ Auditable
- ✅ Reproducible

---

## 🔍 Troubleshooting

### "Response file is empty"

Make sure you:
1. Actually pasted content from AI tool
2. Saved the file (not just created it)
3. Saved to the exact filename specified

### "Response file not found"

Check:
1. File is in the correct directory (`output/...`)
2. Filename matches exactly (case-sensitive)
3. File extension is correct (`.txt`, `.yaml`, `.json`)

### "Could not parse decision YAML"

Ensure:
1. Claude output valid YAML (no markdown code blocks)
2. You copied the complete response
3. No extra text before/after the YAML

### Pipeline interrupted

This is normal! You can:
- Stop anytime with Ctrl+C
- Restart from beginning
- Review artifacts created so far

---

## 🤝 Contributing

This tool embodies **governance-first AI development**. Contributions welcome:

1. **Better prompts** - Improve prompt templates
2. **More agents** - Add support for other AI models
3. **Integrations** - IDE plugins, Git hooks
4. **Documentation** - Examples, tutorials, guides

---

## 📄 License

MIT License - See LICENSE file

---

## 🙏 Credits

Built with:
- **Typer** - Modern CLI framework
- **Rich** - Beautiful terminal formatting
- **PyYAML** - YAML parsing
- **Pydantic** - Data validation

Designed for teams who value:
- **Transparency** over magic
- **Control** over automation
- **Governance** over speed
- **Learning** over black boxes

---

## 💬 Philosophy

> "The best AI coding tools don't replace human judgment—they enhance it."

Agentic Code is built on the principle that **AI should augment, not replace, human developers**. Our architecture emphasizes **governance through separation of duties** rather than emergent multi-agent behavior.

**Key Design Principles:**
- **Sequential multi-model pipeline** - Different models handle different roles
- **Human-in-the-loop governance** - Not autonomous agent interactions
- **Transparency over emergence** - Predictable, auditable workflows
- **Separation of duties** - No model reviews its own work

By making every step transparent and requiring human approval, we:

- ✅ Build trust in AI-generated code
- ✅ Catch issues before they become problems
- ✅ Learn how AI thinks about code
- ✅ Maintain full control and accountability
- ✅ Create audit trails for compliance
- ✅ **Do it all with subscription-based tools** (no pay-per-use charges)

**Note**: While inspired by multi-agent concepts, this implementation prioritizes practical governance over theoretical multi-agent architectures (e.g., Minsky's Society of Mind). See [ARCHITECTURE.md](ARCHITECTURE.md) for details.

---

## 🚀 Get Started

```bash
# Install
pip install -e .

# Run
agentic-code run examples/simple-function.md --skip-verification

# Learn
# Each prompt teaches you what that model/stage does
# Each response shows you how AI thinks
# Complete transparency, subscription-based model
```

**Welcome to governed AI coding!** 🎉
