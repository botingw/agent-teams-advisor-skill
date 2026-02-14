# docs: Raw Research Sources for Agent Teams

This directory stores the raw discussion files collected during research on `Claude Code Agent Teams`.
It acts as the upstream source library used to extract insights, consolidate best practices, and generate/update the related skill.

## Purpose

- Preserve raw conversations and exploratory findings (theory + field experience)
- Provide source material for `agent-teams-advisor`
- Keep reasoning traceability instead of preserving only final conclusions

## File Index

| File | Focus |
|---|---|
| `agent-teams-intro.md` | Agent Teams fundamentals: architecture, Team Lead, and differences from Subagents |
| `agent-teams-best-practice-usage.md` | Operational best practices: prompting, role design, environment setup, and stop-loss rules |
| `agent-teams-best-usage-scenario.md` | Suitable/unsuitable task types, usage cases, benchmarks, and cost observations |

## Recommended Workflow

1. Read `agent-teams-intro.md` to establish shared terminology and the base mental model
2. Read `agent-teams-best-practice-usage.md` to extract actionable operating rules
3. Read `agent-teams-best-usage-scenario.md` to evaluate task fit and cost/risk tradeoffs
4. Distill stable, repeatable rules into the `agent-teams-advisor/` skill

## Maintenance Rules

- Keep `docs/` for raw discussion and exploration, not final operating manuals
- Move finalized, executable guidance into `agent-teams-advisor/SKILL.md` and `agent-teams-advisor/references/`
- Use clear topic-based names for new files (for example: `agent-teams-<topic>.md`)
- If a document includes external viewpoints, add sources when possible for later verification
