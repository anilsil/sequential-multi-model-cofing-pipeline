# How to Test Login Workflow with Agentic-Code

This guide shows you how to use agentic-code to create comprehensive tests for your login workflow.

## 🎯 What Agentic-Code Does

**Important**: Agentic-code is NOT a testing framework. It's a **code generation orchestrator** that helps you:
- Generate well-structured test code
- Follow best practices for testing
- Get AI agents to plan, implement, and verify your tests
- Maintain governance and auditability

## 📋 Quick Start

### Step 1: Prepare Your Task File

I've created a sample task file for you:

```bash
# The task file is already created at:
examples/test-login-workflow.md
```

### Step 2: Run Agentic-Code (Choose Your Mode)

**Option A: Manual Mode (learning-focused)**
```bash
cd /Users/anilsharma/webkins/trustlink-aigardian-main/agentic-code

# Run the pipeline
agentic-code run examples/test-login-workflow.md --skip-verification

# This will generate prompts that you paste into:
# - Claude Code CLI (for analysis, planning, decision)
# - Cursor/Copilot (for implementation)
```

**Option B: Automated Mode (faster)**
```bash
cd /Users/anilsharma/webkins/trustlink-aigardian-main/agentic-code

# Run fully automated with Claude CLI
python scripts/fully_automated.py examples/test-login-workflow.md --skip-verification

# This automatically calls Claude CLI and only pauses for you to implement code
```

## 🔄 What Happens in the Pipeline

### **Stage 1: Repository Analysis** (Claude analyzes your codebase)

**What Claude does:**
- Scans your TrustLink AI Guardian project
- Identifies existing test patterns
- Finds your authentication code (likely in `src/hooks/useAuth.tsx`)
- Determines test framework (probably Jest + React Testing Library)
- Notes existing test structure

**Output:** Analysis of your codebase patterns

### **Stage 2: Task Planning** (Claude creates implementation plan)

**What Claude does:**
- Creates a YAML specification for the test implementation
- Lists specific test files to create:
  ```yaml
  new_files:
    - src/__tests__/auth/login.test.tsx
    - src/__tests__/auth/loginValidation.test.ts
    - src/__tests__/fixtures/authFixtures.ts
  ```
- Defines test cases to implement
- Specifies mocking strategy (Supabase auth, etc.)

**Output:** Detailed YAML specification

### **Stage 3: Code Implementation** (YOU write the tests)

**What YOU do:**
1. Open the implementation prompt in Cursor or your IDE
2. Use AI assistance to write the tests based on the spec
3. Save test files to `generated_code/` directory

**Example test structure you'd create:**

```typescript
// generated_code/src/__tests__/auth/login.test.tsx
import { renderHook } from '@testing-library/react';
import { useAuth } from '@/hooks/useAuth';
import { supabase } from '@/integrations/supabase/client';

jest.mock('@/integrations/supabase/client');

describe('Login Workflow', () => {
  describe('Happy Path', () => {
    it('should login with valid credentials', async () => {
      // Test implementation
    });

    it('should create session after successful login', async () => {
      // Test implementation
    });
  });

  describe('Error Handling', () => {
    it('should show error for invalid email format', async () => {
      // Test implementation
    });

    it('should show error for wrong password', async () => {
      // Test implementation
    });
  });

  describe('Security', () => {
    it('should not expose password in error messages', async () => {
      // Test implementation
    });
  });
});
```

### **Stage 4: Verification** (Optional - Gemini checks for issues)

**What Gemini does:**
- Reviews test code for security issues
- Checks for incomplete test coverage
- Identifies missing edge cases
- Validates mocking strategy

**You can skip this**: Use `--skip-verification` flag

### **Stage 5: Integration Decision** (Claude approves/rejects)

**What Claude does:**
- Reviews the complete test suite
- Checks if all requirements are met
- Verifies tests follow best practices
- Decides: APPROVE / REJECT / APPROVE_WITH_NOTES

**Output:** Final decision with rationale

## 📂 Where Your Tests End Up

After running the pipeline, you'll have:

```
output/2025-12-23_HHMMSS_test-login-workflow/
├── claude_analysis_prompt.md          # What was analyzed
├── claude_analysis_response.txt       # Analysis results
├── claude_planning_prompt.md
├── task_spec.yaml                     # Implementation spec
├── codex_implementation_prompt.md     # Instructions for implementation
├── generated_code/                    # YOUR TEST CODE HERE
│   ├── src/__tests__/auth/
│   │   ├── login.test.tsx            # Main login tests
│   │   ├── loginValidation.test.ts   # Validation logic tests
│   │   └── loginSecurity.test.tsx    # Security tests
│   ├── src/__tests__/fixtures/
│   │   └── authFixtures.ts           # Test data/mocks
│   └── README.md                      # How to run tests
├── claude_decision_prompt.md
└── integration_decision.yaml          # APPROVE/REJECT decision
```

## 🚀 Running the Tests (After Generation)

Once agentic-code generates your tests:

```bash
# Copy generated tests to your main project
cp -r output/*/generated_code/src/__tests__ ../src/

# Run the tests
cd ..  # Go to TrustLink AI Guardian root
npm test -- login.test.tsx
```

## 💡 Pro Tips

### 1. **Customize the Task File**

Edit `examples/test-login-workflow.md` to match your specific needs:
- Add specific test cases you want
- Specify security concerns unique to your app
- Reference specific files in your codebase

### 2. **Use Verification for Security-Critical Tests**

For login tests, verification is valuable:
```bash
# Don't skip verification for security tests
agentic-code run examples/test-login-workflow.md
```

Gemini will check for:
- Authentication bypass vulnerabilities
- Insecure token handling
- Missing security test cases

### 3. **Iterate on Failed Tests**

If Claude rejects the implementation:
1. Read the rejection rationale
2. Fix the issues in `generated_code/`
3. Re-run from Stage 4 (verification)

### 4. **Reuse the Spec**

The generated `task_spec.yaml` is reusable:
```bash
# Use it as a template for testing other workflows
cp output/*/task_spec.yaml examples/test-signup-workflow.yaml
# Edit and reuse
```

## 🎓 Example: Full Workflow

Here's a complete example run:

```bash
# 1. Navigate to agentic-code directory
cd /Users/anilsharma/webkins/trustlink-aigardian-main/agentic-code

# 2. Run automated mode (fastest)
python scripts/fully_automated.py examples/test-login-workflow.md --skip-verification

# 3. Wait for Stage 1 & 2 to auto-complete
# Output:
# ✓ Stage 1: Repository Analysis - COMPLETED
# ✓ Stage 2: Task Planning - COMPLETED

# 4. Implement the tests when prompted
# The script will show you:
# → Prompt file: output/.../codex_implementation_prompt.md
# → Save code to: output/.../generated_code/

# Open Cursor, paste the prompt, implement tests, save to generated_code/

# 5. Press Enter when done

# 6. Wait for Stage 5 (Decision)
# Output:
# ✓ Stage 5: Integration Decision - COMPLETED
# Decision: APPROVE
# Rationale: Tests cover all requirements...

# 7. Copy tests to your project
cp -r output/2025-12-23_*/generated_code/src/__tests__ \
      /Users/anilsharma/webkins/trustlink-aigardian-main/src/

# 8. Run the tests
cd /Users/anilsharma/webkins/trustlink-aigardian-main
npm test
```

## 🔍 What You'll Get

Agentic-code helps you create:

✅ **Structured tests** following your project's patterns
✅ **Comprehensive coverage** (happy path, errors, security, edge cases)
✅ **Proper mocking** for Supabase, API calls, etc.
✅ **Security validation** for auth flows
✅ **Documentation** on how to run and maintain tests
✅ **Best practices** enforced by multi-model review with separation of duties

## 🆚 Agentic-Code vs. Just Using Cursor

| Approach | Agentic-Code | Just Cursor |
|----------|--------------|-------------|
| **Planning** | Claude analyzes codebase first | You provide context manually |
| **Structure** | YAML spec ensures completeness | Ad-hoc implementation |
| **Verification** | Optional Gemini security check | You review yourself |
| **Audit Trail** | Complete record of decisions | No record |
| **Governance** | Multi-model separation of duties | Single AI does everything |
| **Learning** | See the reasoning process | Black box |

## ❓ FAQ

**Q: Can agentic-code RUN the tests?**
A: No. Agentic-code GENERATES test code. You run the tests with your normal test runner (npm test, pytest, etc.)

**Q: What if I already have some login tests?**
A: Agentic-code will analyze them and create ADDITIONAL tests that complement existing ones. The YAML spec will note which tests already exist.

**Q: Can I test the actual UI login form?**
A: Yes! Specify in the task file that you want E2E tests with Playwright or Cypress. Agentic-code will generate those.

**Q: How long does this take?**
A:
- Automated mode: ~5-10 minutes total
- Manual mode: ~10-15 minutes (more copy-paste)

**Q: What if the generated tests fail?**
A: That's normal! Tests often need tweaking for your specific setup. The governance process helps catch issues early.

## 🎯 Next Steps

1. **Run the example**:
   ```bash
   python scripts/fully_automated.py examples/test-login-workflow.md --skip-verification
   ```

2. **Review the generated tests** in `output/.../generated_code/`

3. **Copy to your project** and run them

4. **Iterate** if needed (fix failures, add more tests)

5. **Create task files** for other workflows (signup, password reset, etc.)

## 📚 Related Examples

Check out other example task files:
- `examples/simple-function.md` - Basic function testing
- `examples/url-validation.md` - Validation logic testing
- Create your own for: signup, logout, password reset, etc.

---

**Happy Testing!** 🧪

Remember: Agentic-code doesn't replace you—it augments your testing workflow with structure, governance, and AI assistance.
