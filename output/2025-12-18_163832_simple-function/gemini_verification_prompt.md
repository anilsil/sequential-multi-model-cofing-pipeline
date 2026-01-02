# Code Verification Task

You are a code verification specialist. Your ONLY job is to find issues - NOT to fix them or rewrite code.

## Task Specification
```yaml
Simulated Claude response in test mode.
```

## Code to Verify
```
# File: src/dummy_module.py
def dummy_function():
    return 'Hello from dummy!'


# File: summary.md
### Implementation Summary
- Files Created: `src/dummy_module.py`
- Key Decisions: Simulated decision.
- How to Run: N/A


```

## Verification Checklist

### 1. Logical Correctness
- Does the code meet the task requirements?
- Are there logic errors or edge cases not handled?
- Are algorithms implemented correctly?
- Off-by-one errors?

### 2. Security Issues
- SQL injection vulnerabilities?
- XSS (Cross-Site Scripting) vulnerabilities?
- Insecure data handling?
- Authentication/authorization bypasses?
- Sensitive data exposure in logs?
- Unsafe deserialization?
- Path traversal vulnerabilities?

### 3. Concurrency & Race Conditions
- Thread safety issues?
- Resource locking problems?
- Race conditions in async code?
- Deadlock potential?

### 4. Error Handling
- Are exceptions properly caught?
- Are error messages informative (but not leaking sensitive info)?
- Are resources cleaned up in finally blocks?
- Are edge cases handled (null, empty, invalid input)?

### 5. Performance Risks
- N+1 query problems?
- Inefficient algorithms (O(n^2) where O(n) possible)?
- Memory leaks?
- Unnecessary database calls?
- Missing indices or caching?

## Output Format

Return a JSON array of findings. Each finding MUST have:
```json
[
  {
    "severity": "HIGH" | "MEDIUM" | "LOW",
    "category": "Security" | "Logic" | "Concurrency" | "ErrorHandling" | "Performance",
    "message": "Clear description of the issue",
    "location": "File and line/function where issue occurs",
    "suggestion": "How to fix (plain language, NO CODE)"
  }
]
```

**CRITICAL RULES:**
1. Output ONLY valid JSON (no markdown code blocks)
2. If no issues found, return empty array: `[]`
3. Do NOT include code snippets in suggestions
4. Do NOT rewrite or implement fixes
5. Focus on genuine issues, not style preferences

**Begin verification - output JSON only:**
