# Design Notes

This document records the design rationale behind the agent-teams-advisor skill. It is intended for skill maintainers, not for AI agents consuming the skill at runtime.

---

## Retrospective Questions Design

### Q1 — Friction Points

Replaces "rate your performance 1-10". A numeric score tells you nothing actionable. Specific friction points (wasted messages, unclear ownership, waiting, duplicated work) can be directly converted into protocol improvements.

### Q2 — Decision Points & Information Gaps

Replaces "did you use tool X?". Asking about tool usage directly biases agents toward or against specific tools. Instead, Q2 captures information gaps indirectly — sub-question (c) "whether any available tool or documentation helped" reveals tool usage organically without leading the witness.

### Q3 — Reusable Patterns

Replaces "how to improve the tool?". The key phrase is "for a DIFFERENT team working on a DIFFERENT task" — this forces agents to distinguish domain-specific insights from generic ones. Without this framing, agents tend to give project-specific suggestions that don't generalize.

### Q4 — Skill Self-Assessment

This is the self-improvement loop — the most important long-term mechanism in the skill. Design decisions:

- **Sub-question (a) distinguishes three kinds of "didn't use"**: "didn't need it", "didn't notice it", and "didn't know when to use it" are three completely different problems requiring three different fixes (scope adjustment, better Available Tools docs, better trigger scenarios).
- **Sub-question (b) distinguishes "changed decision" vs "confirmed plan"**: Both have value, but if the skill only ever confirms, it may be too generic and not providing new information. If it frequently changes decisions, it's filling genuine knowledge gaps. This signal tells you whether the skill's content is at the right specificity level.
- **Sub-question (c) anchors to Q2**: This is critical. Q2 already made the agent list all decision points. (c) forces them to go back and cross-reference, rather than answering from vague memory. Without this anchor, agents tend to say "maybe it could have helped somewhere" — useless feedback.
- **Sub-question (d) gives three concrete dimensions in parentheses**: (trigger scenarios / output format / role-specific advice) prevents agents from giving "make it better" style feedback that can't be acted on.

### Why Q4 exists alongside Q2

Q2 captures tool usage indirectly and without bias — this is important for observing natural behavior. Q4 then asks directly about agent-teams-advisor specifically. The two questions serve different purposes: Q2 is the unbiased observation, Q4 is the targeted self-improvement probe. Q4 must come after Q2 so that agents have already reflected on their decision points before being asked about the skill specifically.

---

## Insight Classification System

### Why three tiers instead of two

The original skill only had two categories: generic vs domain-specific. In practice (observed in case-01 and case-02 retrospectives), many insights fall in between — they're not universally applicable, but they're not unique to one project either. For example:

- "Use PROPOSAL/COUNTER/ACCEPT format for API contract negotiation" — not generic (not all teams negotiate), not domain-specific (applies to any negotiation, not just APIs)

The `[SITUATION: <context>]` tier captures these. Without it, maintainers either over-generalize (add situation-specific advice as if it's universal) or under-generalize (discard useful advice because it's "not generic enough").

### How labels map to skill updates

- `[GENERIC]` → add directly to best-practices.md
- `[SITUATION: <context>]` → add with an explicit "**Applies to:**" label so readers know the scope
- `[DOMAIN-SPECIFIC]` → do NOT add to the skill; stays in project docs only

---

## Retrospective Output Structure

### Why two separate documents

The retrospective record (e.g., `PROJECT_RETROSPECTIVE.md`) and the skill update proposal are separated because they serve different audiences and review workflows:

- The **retrospective record** is long, detailed, and captures everything — it's the raw observational data. You read it when you want full context.
- The **skill update proposal** is short and actionable — it's what the human maintainer reviews to decide what changes to make. It should be reviewable in under 5 minutes.

If combined into one document, the maintainer has to dig through pages of Q&A to find the 3-5 actionable items. Separating them keeps the review cycle fast.

### Why not prescribe file names

The skill recommends the structure but does not mandate specific file names. Different repos have different conventions. What matters is the separation of record vs proposal, not what they're called.

---

## "Why" explanations are excluded from the skill

The skill itself (best-practices.md) contains only execution instructions — what to do and how. Design rationale is deliberately excluded because:

1. The skill's reader is an AI agent executing a task, not a skill designer. Adding "why" increases token consumption without improving execution quality.
2. Agents follow concrete sub-questions faithfully. Understanding the design rationale does not make them ask better questions — the question structure itself does that.
3. Design rationale is for the human maintainer who needs to decide whether to modify the skill. That's this document.
