---
name: agent-teams-advisor
description: "Agent Teams Advisor: Evaluate whether a task is suitable for Claude Code Agent Teams and provide operational guidance. Trigger this skill when the user asks about: (1) whether a specific task suits Agent Teams, (2) how to set up and configure Agent Teams, (3) role assignment and collaboration strategies for Agent Teams, (4) choosing between Agent Teams vs Subagents, (5) best practices, cost control, and stop-loss strategies for Agent Teams, (6) any questions about the Claude Code Agent Teams feature. Use this skill when the user asks about agent teams, multi-agent collaboration, whether a task suits agent teams, or how to organize and operate agent teams effectively."
---

# Agent Teams Advisor

Evaluate whether a task suits Agent Teams, recommend configurations, and provide operational guidance.

## Core Workflow

### Step 1: Assess the Task

When a user describes a task, evaluate it against these criteria to determine if Agent Teams is appropriate:

**Use Agent Teams when ALL of these are true:**
- Task involves 2+ independent but interconnected workstreams
- Agents would benefit from peer-to-peer communication (not just top-down delegation)
- Task is complex enough that a single Agent's Context would be strained
- The codebase has reasonable test coverage (to prevent agents from silently breaking each other's work)

**Use Subagents (not Agent Teams) when:**
- Tasks are linearly dependent (A must finish before B starts)
- Simple CRUD or single-file changes
- No inter-agent communication needed

**Use a single Agent when:**
- Task is straightforward and fits in one context window
- No parallelism benefit

### Step 2: Recommend Configuration

Based on the task type, recommend a team composition. For detailed scenario examples and proven configurations, read [references/best-scenarios.md](references/best-scenarios.md).

Common patterns:
- **TDD pair**: Test-Writer + Implementer
- **Full-stack trio**: Backend + Frontend + Tester
- **Debug squad**: 2-3 Agents with different hypotheses
- **Red/Blue team**: Defender + Attacker for security audits
- **Review panel**: Multiple perspectives (Security / Performance / Readability)

### Step 3: Provide Operational Guidance

For detailed best practices on running Agent Teams effectively, read [references/best-practices.md](references/best-practices.md). Key points to always mention:

1. **Create a Constitution File** (`MISSION_CONTEXT.md`) as single source of truth
2. **Define clear DoD** (Definition of Done) with measurable exit criteria
3. **Assign specialized roles** — never make all agents generic "developers"
4. **Monitor for anti-patterns**: zombie meetings, groupthink, deadlocks
5. **Set cost limits** before starting

## Quick Decision Tree

```
Is the task a simple, single-file change?
  → YES: Use single Agent
  → NO: Does it need multiple parallel workstreams?
      → NO: Use Subagent
      → YES: Do the workstreams need to communicate with each other?
          → NO: Use multiple Subagents in parallel
          → YES: Do you have test coverage for the affected code?
              → NO: Add tests first, then consider Agent Teams
              → YES: Use Agent Teams ✓
```

## Reference Files

- **[references/intro.md](references/intro.md)**: Agent Teams architecture, how it works, comparison with Subagents. Read when the user needs to understand what Agent Teams is.
- **[references/best-scenarios.md](references/best-scenarios.md)**: Proven use cases, anti-patterns, benchmark data, and cost references. Read when evaluating whether a specific task fits Agent Teams.
- **[references/best-practices.md](references/best-practices.md)**: Operational handbook — role assignment, communication protocols, environment setup, stop-loss strategies. Read when the user needs guidance on how to run Agent Teams effectively.
