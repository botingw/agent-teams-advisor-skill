# Agent Teams: Best Practices Handbook

## Quick-Start Checklist (Do These Before Your First Message)

1. Read your role's hard constraints in the Constitution File. Note their IDs if provided.
2. Identify your role: Are you the **proposer** or the **reviewer**? Check the Constitution File for turn-taking rules.
3. Use the **Negotiation Message Format** defined in the Constitution File for ALL substantive messages.
4. Always **ACK before responding** — send "Received, reviewing now" before composing a substantive reply.
5. **Never send a second message** before receiving a response to your first.
6. When you encounter an uncertain situation not covered by this checklist, **read the full sections below** — especially [Runtime Guidance](#runtime-guidance-during-execution) and [Stop-Loss Strategies](#stop-loss-strategies).

---

## Table of Contents
1. [Commander's Rules: Human / Leader Best Practices](#commanders-rules)
2. [Role Assignment and Collaboration](#role-assignment-and-collaboration)
3. [Environment Setup](#environment-setup)
4. [Stop-Loss Strategies](#stop-loss-strategies)
5. [Runtime Guidance (During Execution)](#runtime-guidance-during-execution)
6. [Post-Sprint Retrospective](#post-sprint-retrospective)
7. [Core Principle](#core-principle)

---

## Commander's Rules

### 1. Create a "Constitution File"
- Create a `MISSION_CONTEXT.md` (or `AGENTS_README.md`) in the project root
- When launching the Team, force every Agent to read this file as their first step
- **Why**: Each Agent's Context is independent. Verbal instructions only reach the Agent that heard them. The Constitution File is the single Source of Truth — when Agents disagree, they refer back to this file to settle disputes.

**A good Constitution File should include:**

| Section | Description | Example |
|---------|-------------|---------|
| **Objective** | What the team must deliver | "Finalize API spec + implement mock server and client validator" |
| **Architecture / Context** | Key technical decisions already made | "BFF pattern approved; no cross-shard joins" |
| **Hard Constraints per Role** | Each agent's non-negotiable rules | "@Backend_Lead: no cross-shard joins. @Frontend_Lead: max 1 HTTP request" |
| **Communication Protocol** | Turn-taking rules and message format | "In review/negotiation: one party proposes, the other responds. Send ACK before substantive replies. No second message before receiving a response to the first." |
| **Definition of Done (with owners)** | Measurable exit criteria, each assigned to an agent | "- [ ] `spec.yaml` written (@Backend) and reviewed (@Frontend)" |
| **Prohibitions** | Things agents must NOT do | "Do not modify `config.yaml`. Do not use `rm -rf`." |

**Ownership assignment pattern for negotiation workflows:**
**Applies to:** negotiation/debate workflows (API contracts, spec reviews, design critiques)
- Assign **proposal ownership** to the party with the strongest constraints on the artifact's shape (e.g., Backend proposes the API schema because they know data/DB constraints)
- Assign **review ownership** to the primary consumer (e.g., Frontend reviews because they know UI requirements)
- This avoids "two people editing the same draft" and ensures proposals respect structural constraints from the start

**Common mistakes to avoid:**
- Writing DoD items without assigning an owner — agents won't know who is responsible
- Specifying "use structured messages" without defining turn-taking — causes crossed messages in async P2P communication
- Omitting hard constraints — agents will make assumptions that violate unstated rules

### 2. Define a "Definition of Done" (DoD)
- Don't say: "Refactor the code"
- Say: "Refactor `auth.py` until `pytest tests/test_auth.py` passes completely, Pylint score > 9.0, and no new global variables are introduced"
- **Why**: Without a clear stop signal, Agents will endlessly tweak variable names, add comments, and burn through the Token budget. A concrete DoD is the only braking mechanism.
- **Include machine-verifiable checks**: Every DoD should include at least one automated acceptance test (a script, a test suite, a validator). Subjective "looks good" reviews are insufficient — agents may fall into groupthink and approve each other's flawed work. A script that exits 0/1 is unambiguous.

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

### Recommended Negotiation Message Format

**Applies to:** negotiation/debate workflows (API contracts, architecture debates, spec reviews)

For cross-role negotiations, mandate this message structure in the Constitution File:

```
PROPOSAL/REVIEW: [brief title]
CHANGES: [what changed or what you want changed]
RATIONALE: [why, referencing hard constraints by number]
DECISION NEEDED: [yes/no — what the other party needs to decide]
```

The mandatory `DECISION NEEDED` field forces every message to have a clear call-to-action, preventing ambiguous "FYI" messages that stall progress. In practice, this format has been shown to complete API contract negotiations in as few as 2 rounds.

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

## Runtime Guidance (During Execution)

The rules above cover **setup** (before the team starts). The following covers **runtime** — how to manage agents while they are actively working.

### 1. Avoid Over-Nudging (Leader Anti-Pattern)
- **Before sending a follow-up message to an agent, check TaskList status first.** If the task is `in_progress`, the agent is working — do not nudge unless they have been idle for an unusually long time.
- Do not send "do X now" messages for work the agent has already acknowledged or started. Redundant nudges waste tokens and create noise.
- Remember: agents going idle briefly between turns is **normal behavior**, not a sign of inaction. An agent sending a message and then going idle simply means they are waiting for a response.
- **Rule of thumb**: If you find yourself sending more than 2 messages to the same agent without receiving a substantive response, stop and check their task status instead of sending a third.

### 2. Message Crossing Prevention & Turn-Taking
- In async P2P communication, agents can send messages simultaneously without seeing each other's latest message. This creates "crossed messages" — duplicate or redundant exchanges that waste tokens.
- **ACK-before-response**: Instruct agents in the Constitution File to send a brief ACK ("Received, reviewing now") before composing a substantive response. This signals to the sender that their message was received, preventing premature follow-ups.
- **Explicit turn-taking**: For any workflow where agents exchange proposals, reviews, or feedback, define a clear protocol in the Constitution File:
  - One party sends a substantive message (proposal, review, deliverable)
  - The other party must ACK and respond before the first party sends another substantive message
  - No agent should send a second message before receiving a response to their first
- **Why this matters**: Without turn-taking rules, agents default to "fire and forget" — sending messages as fast as they can generate them. In a 2+ agent team, this creates message storms where everyone is talking and nobody is listening. Turn-taking is not just politeness; it's a token-saving mechanism.

### 3. Phase Transition Checkpointing
- For multi-phase tasks, instruct agents to explicitly announce phase transitions: "Phase 1 complete, moving to Phase 2."
- This helps the team lead and other agents know what's done and what's next, reducing redundant messages about completed work.
- Use TaskUpdate to mark tasks as completed at phase boundaries — this is the most reliable way to communicate progress, more reliable than chat messages.

### 4. Shared Readiness Gates for Converging Parallel Work
**Applies to:** parallel-then-converge workflows (e.g., multiple agents building components that must integrate)
- When multiple agents work in parallel and their outputs must converge (e.g., mock server + client validator both need to be ready before e2e testing), define a **shared readiness gate** in the Constitution File.
- Each agent marks their piece as "ready" (via TaskUpdate). The convergence phase only begins when ALL prerequisite tasks are completed.
- Without this, agents infer readiness from chat messages, which is fragile — a message may arrive out of order or be ambiguous.
- **Pattern**: Use task dependencies (`addBlockedBy`) to model convergence points. The downstream task auto-unblocks when all upstream tasks are complete.

---

## Post-Sprint Retrospective

Running retrospectives after each Agent Teams session is critical for continuously improving your team's working patterns. The insights feed back into your Constitution File, skill definitions, and protocol design.

### Retrospective Protocol
- **Do NOT announce the retrospective before or during execution.** Agents adjust behavior based on prompt content. If agents know they will be asked "did you use tool X?", they may force themselves to use it regardless of genuine need — producing biased usage data. Collect natural behavior first, then interview.
- **Ask after all deliverables are complete.** Only begin the retrospective once code is working and specs are finalized.

### Recommended Questions

These questions are designed to produce **actionable improvement signals**, not satisfaction scores:

**Q1 — Friction Points:**
> "In this session, at which points did you experience friction — wasted messages, unclear ownership, waiting without knowing why, or duplicated work? Describe each friction point and what would have prevented it."

**Q2 — Decision Points & Information Gaps:**
> "List every decision point where you had to choose between multiple approaches (architectural, communication, or implementation). For each, describe: (a) what you decided, (b) what information you used to decide, (c) whether any available tool or documentation helped, and (d) what information was missing that would have helped you decide faster."

**Q3 — Reusable Patterns:**
> "What did you learn in this session that would be useful for a DIFFERENT team working on a DIFFERENT task? Describe any communication patterns, decision frameworks, or workflow structures that you'd recommend generalizing."

**Q4 — Skill Self-Assessment:**

This question creates a feedback loop: each session's retrospective improves the agent-teams-advisor skill, which improves the next session. Ask each agent (and answer for yourself as leader):

> "The agent-teams-advisor skill was available to the team during this session.
>
> (a) Did you use it? If yes, describe when and what it returned.
>     If no, explain why — did you not need it, not notice it,
>     or not understand when to use it?
>
> (b) If you used it: was the advice actionable? Did it change
>     your decision or confirm what you already planned?
>
> (c) If you didn't use it: looking back at your decision points
>     from Q2, is there any point where it COULD have helped?
>     What would have triggered you to use it?
>
> (d) What would make this skill more useful to you?
>     (Better trigger scenarios in the docs? Different output
>     format? More specific advice for your role?)"

### Classifying Insights

When reviewing retrospective answers, label each insight with one of these categories:

- **[GENERIC]** — Applicable to any Agent Teams task, unconditionally.
  Example: "Machine-verifiable DoD prevents groupthink."
- **[SITUATION: \<context\>]** — Useful but only in specific workflow types. Clearly state the context.
  Examples: `[SITUATION: negotiation/debate workflows]`, `[SITUATION: parallel-then-converge workflows]`, `[SITUATION: cross-role API contract design]`
- **[DOMAIN-SPECIFIC]** — Only relevant to this exact project type.
  Example: "Include payload size budget for mobile API design."

This labeling ensures that when feeding insights back into skills or protocols, you know exactly when each piece of advice applies and do not over-generalize.

### Recommended Retrospective Output Structure

Compile retrospective results into two separate documents:

**1. Retrospective Record** (e.g., `PROJECT_RETROSPECTIVE.md`) — the full observational record:
- **Session Summary** — One paragraph: what the team built, how many agents, key outcomes
- **Friction Points** (from Q1) — Bullet list per agent, each with: what happened → root cause → suggested fix
- **Decision Log** (from Q2) — For each decision: chosen approach, info used, info missing
- **Reusable Patterns** (from Q3) — Each pattern with a `[GENERIC]` or `[SITUATION: X]` label
- **Skill Assessment** (from Q4) — Per-agent summary: did they use it, why/why not, what would improve it

**2. Skill Update Proposal** (separate document) — actionable improvements extracted from the retrospective:
- Only includes items that should change the agent-teams-advisor skill or the Constitution File template
- Each item tagged with its classification label
- `[GENERIC]` insights → add directly
- `[SITUATION: <context>]` insights → add with a clear "**Applies to:**" label so future readers know the scope
- `[DOMAIN-SPECIFIC]` insights → do NOT add to the skill

Separating the record from the proposal ensures the retrospective captures everything, while the proposal stays concise and reviewable.

### Feeding Results Back
- **[GENERIC] insights** (communication patterns, turn-taking rules, leader behaviors) → update this skill's best practices
- **[SITUATION] insights** (workflow-specific protocols) → update this skill with an explicit "**Applies to:**" label
- **[DOMAIN-SPECIFIC] insights** (API design patterns, DB optimization strategies) → update project-level documentation only; do NOT add to the skill
- **Protocol improvements** (better Constitution File structure, better DoD format) → update your team's Constitution File template

---

## Core Principle

> The essence of Agent Teams is **trading communication cost for reasoning depth**.
>
> Every setup measure (DoD, Constitution File, structured communication) exists to **reduce communication noise**, ensuring that every Agent interaction has a high signal-to-noise ratio.

**When to upgrade**: Start with Subagents. If you find an Agent frequently needing to "ask you" about information in other files, that's the signal to switch to Agent Teams.
