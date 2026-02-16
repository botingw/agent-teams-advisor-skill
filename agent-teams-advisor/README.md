# agent-teams-advisor

`agent-teams-advisor` is a Claude Code skill for Team Leads. It is designed to:

- Evaluate whether a task is a good fit for Agent Teams
- Recommend team composition and collaboration strategy
- Provide operational guidance (communication, DoD, cost control, stop-loss)
- Prevent common failure modes (groupthink, zombie meetings, deadlocks)

## Directory Structure

| Path | Description |
|---|---|
| `SKILL.md` | Core skill definition: triggers, decision flow, and mandatory steps |
| `references/intro.md` | Agent Teams architecture and comparison with Subagents |
| `references/best-practices.md` | Operational handbook (roles, communication protocols, environment, stop-loss) |
| `references/best-scenarios.md` | Best-fit scenarios, anti-patterns, benchmark and cost references |
| `references/skill-propagation-templates.md` | Copy-paste templates for Constitution files and spawn prompts |
| `DESIGN_NOTES.md` | Design rationale behind skill decisions (for maintainers, not consumed by agents) |

## When to Trigger This Skill

Use this skill when requests include any of the following:

- "Is this task suitable for Agent Teams?"
- "How should Agent Teams be configured and organized?"
- "How do I choose between Agent Teams and Subagents?"
- "What are best practices, cost controls, and stop-loss rules?"
- Any operational or evaluation question about Claude Code Agent Teams

## Standard Output Flow (Team Lead)

1. **Assess task**: decide between single agent / subagents / agent teams
2. **Recommend configuration**: provide concrete role setup (for example TDD pair, full-stack trio)
3. **Operational guidance**: provide Constitution file structure, DoD, communication protocol, monitoring, and stop-loss rules
4. **Mandatory propagation**: require every teammate to read this skill before work starts (via Constitution file + spawn prompt)

> Step 4 is mandatory. Every agent has an independent context window, so collaboration rules must be explicitly propagated.

## Relationship with `docs/`

This skill is distilled from raw research files in `docs/`:

| Source file | Skill target |
|---|---|
| `docs/agent-teams-intro.md` | `references/intro.md` |
| `docs/agent-teams-best-practice-usage.md` | `references/best-practices.md` |
| `docs/agent-teams-best-usage-scenario.md` | `references/best-scenarios.md` |

`references/skill-propagation-templates.md` packages the "force-read-before-work" rule into reusable templates so Team Leads can apply it directly.

## Maintenance Recommendations

1. Capture new insights in `docs/` first (preserve raw context)
2. Distill them into actionable guidance in `references/`
3. Update `SKILL.md` trigger logic and workflow as needed
4. Re-test with real cases (token cost, deadlock rate, iteration count) before calling changes successful
