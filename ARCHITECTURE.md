# Architecture Overview

This document clarifies the architectural design of Agentic Code and its relationship to multi-agent systems theory.

## TL;DR

**Agentic Code is a sequential multi-model pipeline with governance, NOT a concurrent multi-agent system.**

While we use specialized "agents" (ClaudeAgent, CodexAgent, GeminiAgent) in our code, they represent different **model roles** in a sequential pipeline, not autonomous agents with emergent behavior.

---

## What This IS

✅ **Sequential Multi-Model Pipeline**
- Five distinct stages executed in order
- Each stage uses a different AI model for separation of duties
- Deterministic, predictable workflow

✅ **Governance Architecture**
- Human-in-the-loop approval at every stage
- No model reviews its own work
- Complete audit trail of all decisions

✅ **Prompt Orchestrator**
- Generates prompts for different AI tools
- User manually pastes prompts and responses
- Full transparency into all AI interactions

✅ **Separation of Duties**
- Claude (Analyst Role) - Repository analysis
- Claude (Planner Role) - Task planning
- Codex/Cursor (Implementation Role) - Code generation
- Gemini (Verification Role) - Security & quality verification
- Claude (Decision-Maker Role) - Integration approval

---

## What This is NOT

❌ **NOT a Concurrent Multi-Agent System**
- Stages run sequentially, not concurrently
- No parallel agent interactions
- No autonomous agent negotiations

❌ **NOT Emergent Intelligence** (e.g., Minsky's Society of Mind)
- Behavior is pre-programmed, not emergent
- Central orchestrator (`AgenticPipeline` class) controls flow
- No lateral communication between "agents"

❌ **NOT Autonomous Agents**
- Models don't make independent decisions
- Human approval required at each stage
- No agent-to-agent coordination

---

## Relationship to Multi-Agent Systems Theory

### Minsky's Society of Mind

Marvin Minsky's "Society of Mind" theory proposes that:
- Intelligence emerges from interactions of simple specialized agents
- No central controller—behavior emerges from agent interactions
- Agents operate concurrently and negotiate solutions
- K-Lines (memory patterns) reactivate sets of agents
- Conflict resolution happens through agent competition

### How Agentic Code Differs

| Principle | Society of Mind | Agentic Code |
|-----------|-----------------|--------------|
| **Execution** | Concurrent agent interactions | Sequential stage execution |
| **Control** | No central controller | Central `AgenticPipeline` orchestrator |
| **Behavior** | Emergent from interactions | Pre-programmed workflow |
| **Communication** | Lateral agent-to-agent | Unidirectional data flow (stage to stage) |
| **Decision-Making** | Agent negotiation/competition | Human approval gates |
| **Intelligence** | Emerges from simple agents | Leverages existing LLM capabilities |
| **Goal** | Theoretical model of mind | Practical governed workflows |

---

## Why This Design?

We prioritize **governance, auditability, and human oversight** over theoretical multi-agent architectures:

### 1. **Auditability**
Sequential workflows are easier to audit than concurrent agent interactions. Every stage has clear inputs, outputs, and decision points.

### 2. **Human Control**
Human approval gates ensure that no code is generated, verified, or integrated without explicit developer consent.

### 3. **Separation of Duties**
Different models handle different roles to prevent bias. No model reviews its own work.

### 4. **Transparency**
Every prompt and response is saved to disk. Users can see exactly what each model was asked and how it responded.

### 5. **Compliance & Security**
Enterprise environments require clear accountability. Our architecture creates a complete audit trail for compliance.

### 6. **Simplicity**
Sequential pipelines are easier to understand, debug, and maintain than emergent multi-agent systems.

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────┐
│  SEQUENTIAL MULTI-MODEL PIPELINE                    │
│  (Governance Architecture)                          │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │  STAGE 1: Repository Analysis                │  │
│  │  Model: Claude (Analyst Role)                │  │
│  │  Input: Task description, repo files         │  │
│  │  Output: Codebase analysis                   │  │
│  │  Human Gate: Review analysis ✓               │  │
│  └──────────────────────────────────────────────┘  │
│                      ↓                               │
│  ┌──────────────────────────────────────────────┐  │
│  │  STAGE 2: Task Planning                      │  │
│  │  Model: Claude (Planner Role)                │  │
│  │  Input: Task + Analysis                      │  │
│  │  Output: YAML implementation spec            │  │
│  │  Human Gate: Review plan ✓                   │  │
│  └──────────────────────────────────────────────┘  │
│                      ↓                               │
│  ┌──────────────────────────────────────────────┐  │
│  │  STAGE 3: Code Implementation                │  │
│  │  Model: Codex/Cursor (Implementation Role)   │  │
│  │  Input: YAML spec + Analysis                 │  │
│  │  Output: Generated code files                │  │
│  │  Human Gate: Review code ✓                   │  │
│  └──────────────────────────────────────────────┘  │
│                      ↓                               │
│  ┌──────────────────────────────────────────────┐  │
│  │  STAGE 4: Verification [OPTIONAL]            │  │
│  │  Model: Gemini (Verification Role)           │  │
│  │  Input: Generated code                       │  │
│  │  Output: Security & quality findings         │  │
│  │  Human Gate: Review findings ✓               │  │
│  └──────────────────────────────────────────────┘  │
│                      ↓                               │
│  ┌──────────────────────────────────────────────┐  │
│  │  STAGE 5: Integration Decision               │  │
│  │  Model: Claude (Decision-Maker Role)         │  │
│  │  Input: Code + Findings + Spec               │  │
│  │  Output: APPROVE or REJECT + Rationale       │  │
│  │  Human Gate: Final approval ✓                │  │
│  └──────────────────────────────────────────────┘  │
│                                                      │
└─────────────────────────────────────────────────────┘

Key Characteristics:
- Unidirectional flow (top to bottom)
- No feedback loops between stages
- Human approval required at each stage
- Central orchestrator controls execution
```

---

## Key Design Principles

### 1. Sequential Execution
Stages execute one at a time in a fixed order. This is **not** concurrent multi-agent collaboration.

### 2. Model Specialization
Different models handle different roles based on their strengths:
- **Claude**: Strong reasoning for analysis, planning, and decisions
- **Codex/Cursor**: Optimized for code generation
- **Gemini**: Additional verification perspective

### 3. Separation of Duties
Critical governance principle: No model reviews its own work.
- Claude plans → Codex implements → Gemini verifies → Claude decides
- The planner doesn't implement
- The implementer doesn't verify
- The verifier doesn't make the final decision

### 4. Human-in-the-Loop
Every stage requires explicit human approval:
- Review generated prompts before using them
- Review model responses before accepting them
- Edit prompts if needed
- Skip stages if appropriate
- Veto power at every step

### 5. Complete Auditability
Every run creates a timestamped directory with:
- All prompts generated
- All responses received
- Complete file manifest
- Final decision with rationale
- Human approval records

---

## Comparison with Other Architectures

### vs. Traditional Single-Model Tools (e.g., Copilot, Cursor)
- **Single Model**: One AI does everything (no separation of duties)
- **Agentic Code**: Different models for different roles (governance through specialization)

### vs. API-Based Multi-Agent Frameworks (e.g., AutoGPT, BabyAGI)
- **API Frameworks**: Autonomous agents with emergent behavior
- **Agentic Code**: Human-supervised sequential pipeline

### vs. Society of Mind Implementations
- **Society of Mind**: Concurrent agents, emergent intelligence, no central control
- **Agentic Code**: Sequential stages, pre-programmed workflow, central orchestrator

---

## Future Evolution

While the current architecture prioritizes practical governance, future versions could explore:

### Potential Enhancements
- **Parallel verification**: Run multiple verifiers concurrently (Gemini + GPT-4 + custom tools)
- **Feedback loops**: Allow verifier to send feedback to implementer for corrections
- **Dynamic routing**: Choose different models based on task characteristics
- **Agent negotiation**: Allow models to "negotiate" solutions under human supervision

### Constraints
Any evolution must maintain:
- ✅ Complete human oversight
- ✅ Full auditability
- ✅ Separation of duties
- ✅ Transparency

---

## Terminology Clarification

### Why we use "Agent" in code

The classes `ClaudeAgent`, `CodexAgent`, and `GeminiAgent` use "agent" terminology because:
- Common in software engineering (e.g., "user agent", "build agent")
- Represents an entity that performs actions on behalf of the user
- Convenient abstraction for different model interfaces

### Important Distinction

**Code terminology** (ClaudeAgent) ≠ **Theoretical multi-agent systems** (Minsky's Society of Mind)

Our "agents" are:
- Wrappers around different AI model APIs
- Responsible for specific stages in a pipeline
- Not autonomous entities with emergent behavior

---

## Summary

Agentic Code implements a **sequential multi-model pipeline with governance**, not a theoretical multi-agent system.

**Design Focus**:
- ✅ Practical governance for enterprise environments
- ✅ Complete transparency and auditability
- ✅ Human oversight at every decision point
- ✅ Separation of duties between different models

**Not Focused On**:
- ❌ Emergent intelligence from agent interactions
- ❌ Autonomous agent negotiations
- ❌ Theoretical multi-agent architectures
- ❌ Replacing human judgment with agent collaboration

**Philosophy**: We believe the best AI coding tools **augment human developers** through transparent, governed workflows—not replace them with autonomous agent systems.

---

## References

- **Minsky, M. (1986)**. *The Society of Mind*. Simon & Schuster. - Theoretical foundation for multi-agent systems.
- **Wooldridge, M. (2009)**. *An Introduction to MultiAgent Systems*. Wiley. - Comprehensive overview of multi-agent architectures.

For questions or suggestions, please open an issue or contribute to the project.
