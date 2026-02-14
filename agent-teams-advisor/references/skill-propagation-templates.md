# Skill Propagation Templates

Ready-to-use templates for implementing Step 4 of the Core Workflow.
The core instruction is in SKILL.md. This file provides copy-paste templates and rationale.

---

## Template: Constitution File Section

Copy this into your Constitution File (MISSION_CONTEXT.md). You may adapt wording to fit your project, but keep the REQUIRED/MANDATORY language and the specific invocation instruction.

```markdown
## REQUIRED: Read the Team Collaboration Guide Before Starting Work

This team uses the agent-teams-advisor skill as its collaboration guidebook.
ALL team members MUST read it BEFORE beginning any task. This is not optional.

### How to read it:
Invoke the Skill tool with `skill: "agent-teams-advisor"`.
Then read the reference files it points to — especially `references/best-practices.md`.

### What you will learn:
- The structured message format for all team communication
  (STATUS / CHANGED_FILES / TEST_RESULTS / DECISION NEEDED)
- Turn-taking rules: ACK before responding, no second message before receiving a reply
- Negotiation patterns for cross-role proposals and reviews
- How to report test results and handoff deliverables
- Anti-patterns to avoid (groupthink, zombie meetings, message storms)

### When to re-read it:
- **Before sending your first proposal or review** — check the negotiation message format
- **When communication feels stuck** — the guide has de-escalation patterns

### MANDATORY first step:
Before writing any code, tests, or proposals, invoke `skill: "agent-teams-advisor"` and read
`references/best-practices.md`. Use what you learn to structure ALL your team communications.
```

---

## Template: Spawn Prompt Snippet

Include this as an early numbered step in every teammate's spawn prompt (Step 1 or Step 2, immediately after reading the Constitution File):

```
**STEP [N] (REQUIRED — BEFORE STARTING WORK):** This team uses a collaboration guidebook.
Invoke the Skill tool with `skill: "agent-teams-advisor"` and read its reference file
`references/best-practices.md`. This teaches you:
- Structured message format for all team communications
- Turn-taking and ACK rules to prevent wasted messages
- Negotiation, handoff, and test reporting best practices
You MUST read this before writing any code or tests. Use what you learn to structure
ALL messages you send to teammates. This is mandatory.
```

---

## Why Both Templates Are Needed

| Channel | Purpose | Risk if missing |
|---------|---------|----------------|
| **Constitution File** | Persistent reference — agents can re-read anytime during the session | Agents may forget the skill exists mid-session when they actually need it |
| **Spawn Prompt** | Immediate action — forces reading as the very first step | Agents may skim the Constitution File and skip the tools section |

Testing has shown that using only one channel is insufficient. Agents given only a Constitution File mention often skim or deprioritize the "Available Tools" section. Agents given only a spawn prompt instruction may forget the skill exists later when they encounter a decision point.

Both together create two-layer reinforcement:
1. Spawn prompt → forces immediate reading at session start
2. Constitution File → provides ongoing reference with re-read triggers for decision points

---

## Verification (Optional)

After teammates complete their work, you may verify skill adoption:
> "Did you invoke the agent-teams-advisor skill during this session? What did you learn and how did it affect your communication?"
