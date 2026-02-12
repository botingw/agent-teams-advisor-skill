# Agent Teams: Best Practices Handbook

## Table of Contents
1. [Commander's Rules: Human / Leader Best Practices](#commanders-rules)
2. [Role Assignment and Collaboration](#role-assignment-and-collaboration)
3. [Environment Setup](#environment-setup)
4. [Stop-Loss Strategies](#stop-loss-strategies)
5. [Core Principle](#core-principle)

---

## Commander's Rules

### 1. Create a "Constitution File"
- Create a `MISSION_CONTEXT.md` (or `AGENTS_README.md`) in the project root
- Contents: project architecture, coding style, absolute prohibitions (e.g., "do not modify `config.yaml`"), and the current mission objective
- When launching the Team, force every Agent to read this file as their first step
- **Why**: Each Agent's Context is independent. Verbal instructions only reach the Agent that heard them. The Constitution File is the single Source of Truth — when Agents disagree, they refer back to this file to settle disputes.

### 2. Define a "Definition of Done" (DoD)
- Don't say: "Refactor the code"
- Say: "Refactor `auth.py` until `pytest tests/test_auth.py` passes completely, Pylint score > 9.0, and no new global variables are introduced"
- **Why**: Without a clear stop signal, Agents will endlessly tweak variable names, add comments, and burn through the Token budget. A concrete DoD is the only braking mechanism.

### 3. Use the Manager-Worker Pattern
- Designate one Agent as the Project Manager — it **does not write code**
- PM's job: read your instructions → decompose into tickets → assign to Worker Agents → review deliverables → report back to you
- **Why**: Coding Agents get tunnel vision (e.g., fixing a single bracket). A dedicated PM maintains the big picture and keeps everyone on track.

---

## Role Assignment and Collaboration

### Role Specialization
Never make all Agents generic "Developers." Heterogeneity is the key to effectiveness. Recommended roles:

| Role | Responsibility | Notes |
|------|---------------|-------|
| **Architect** | Read-only; reviews structure and API design | |
| **Coder** | Implementation; highest Context consumption | |
| **Critic / QA** | Extremely nitpicky; hunts for bugs and flaws | **The most important role** |
| **Librarian** | Maintains documentation; records all changes | |

### Structured Communication Protocol
Force Agents to use structured formats when communicating with each other:

```
Bad:  "Hey, I'm done, take a look."
Good: { "status": "review_ready", "changed_files": ["api/login.ts"], "test_results": "passed", "note": "Updated regex for email validation" }
```

**Why**: Natural language is full of ambiguity. Structured data lets the receiving Agent parse the task accurately, reducing round-trips caused by misunderstanding — saving both money and time.

---

## Environment Setup

### 1. Use tmux or Zellij
- Split the terminal: top-left pane for your commands, other panes tail each Agent's log in real time
- **Why**: "Zombie Agents" can get stuck on `npm install` or waiting for an API response. Without visibility into their output, you'll assume they're thinking when they've actually been hung for 10 minutes. Visualization is the key to saving money.

### 2. Sandbox Isolation
- Run Agent Teams inside Docker containers
- **Why**: Agent Teams have broad permissions. There have been incidents where an Agent accidentally ran `rm -rf` on the wrong directory. Treat them like a group of unsupervised interns — don't let them touch your host filesystem directly.

### 3. Shared Memory via Scratchpad
- Set up a `.claude/scratchpad/` directory that all Agents can read and write to
- Agent A writes code to `scratchpad/draft_v1.py`, then notifies Agent B to read it
- **Why**: Don't paste entire code blocks into the conversation (it wastes Tokens). Passing data through files can reduce Context consumption by over 60%.

---

## Stop-Loss Strategies

### Loop Detection
- If Agent A and Agent B are sending each other similar messages like "Please fix the lint error" more than 3 times → **kill the process immediately**
- Reason: They've entered a deadlock. The AI sometimes cannot resolve a specific lint error and will keep attempting ineffective fixes. A human must intervene, fix the line manually, and restart.

### Cost Monitoring
- Set `claude cost --limit $20` (or an appropriate amount)
- Agent Teams' Token consumption scales exponentially; an unmonitored run can result in massive bills.

### Groupthink Detection
- If Agents are complimenting each other but not writing code → **intervene and stop them**
- Add to the System Prompt: "Be concise. No pleasantries. Code only."

---

## Core Principle

> The essence of Agent Teams is **trading communication cost for reasoning depth**.
>
> Every setup measure (DoD, Constitution File, structured communication) exists to **reduce communication noise**, ensuring that every Agent interaction has a high signal-to-noise ratio.

**When to upgrade**: Start with Subagents. If you find an Agent frequently needing to "ask you" about information in other files, that's the signal to switch to Agent Teams.
