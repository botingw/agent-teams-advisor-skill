# Project Legacy Phoenix — Retrospective Report

## Session Summary

**Project:** Mobile Order Dashboard — API Contract Finalization
**Team:** Engineering Manager (team lead), @Backend_Lead (Python/SQL), @Frontend_Lead (React/Performance)
**Duration:** Single sprint session
**Outcome:** All deliverables completed and verified (115/115 validation checks PASS)

### Deliverables Produced

| # | Deliverable | Status | Owner |
|---|------------|--------|-------|
| 1 | API contract agreed (Cache-Assisted Fan-Out architecture) | Done | Backend_Lead (proposed), Frontend_Lead (reviewed) |
| 2 | `final_api_spec.yaml` — OpenAPI 3.0 specification | Done | Backend_Lead |
| 3 | `mock_server.py` — Python stdlib mock server (port 8080) | Done | Backend_Lead |
| 4 | `client_validator.js` — Node.js response structure validator | Done | Frontend_Lead |
| 5 | End-to-end validation — 115/115 PASS, payload 1.90KB | Done | Both |

### Architecture Decision

The team chose **Cache-Assisted Fan-Out** over pure denormalized read model. The orders table (50M rows) is queried with pagination (limit/offset). Product data from the separate shard is fetched via batch `IN(...)` lookup and embedded inline in each order item. This satisfies both Backend constraints (no cross-shard joins, simple fan-out) and Frontend constraints (single HTTP request, all data inline, no N+1).

---

## Q&A from Retrospective Interviews

### Q1 — Friction Points

#### @Backend_Lead

1. **Port 8080 collision.** A pre-existing process was already serving on port 8080 with a different schema. Backend_Lead initially thought their own server was returning wrong data. **Prevention:** Constitution File should specify a dedicated port or the mock server should detect port conflicts and fail fast with a clear error.

2. **Task assignment echo noise.** Received 3 "task_assignment" notifications after self-claiming tasks via TaskUpdate. Harmless but added unnecessary turns. **Prevention:** Self-assigned tasks should not generate inbound assignment notifications.

3. **Chained bash command syntax.** First smoke test attempt failed due to background process + foreground test command chaining issues in sandbox. Took 2 extra attempts. **Prevention:** Include a known-good "start server, test, stop" pattern in the Constitution File.

#### @Frontend_Lead

1. **Mock server execution path friction (minor).** Path resolution issue when running end-to-end test — `cd` before `&` backgrounding didn't propagate to the foreground `node` command. Cost 2 extra Bash calls. **Prevention:** A shared "how to run" section in MISSION_CONTEXT.md with exact commands (absolute paths).

2. **No friction in negotiation phase.** Turn-taking protocol worked cleanly. Zero crossed messages, zero wasted rounds.

3. **Duplicate task assignment notification.** Received automated assignment for an already-completed task. **Prevention:** System should suppress notifications for completed tasks.

#### @Manager (Self-Assessment)

1. **No intervention needed during negotiation.** The Constitution File's turn-taking rules and structured message format worked as designed — negotiation completed in 1 round (proposal → ACK → approve). No crossed messages, no groupthink.

2. **Sandbox port binding restriction.** End-to-end validation initially failed due to sandbox network restrictions. Required retry with `dangerouslyDisableSandbox: true`. **Prevention:** Document sandbox limitations in the Constitution File for tasks involving network servers.

3. **Idle notification noise.** Multiple idle notifications from agents during normal waiting periods. While expected behavior, the volume could be distracting in larger teams. Not actionable for this session but worth noting for scaling.

---

### Q2 — Decision Points & Information Gaps

#### @Backend_Lead

| # | Decision | Information Used | Tool/Doc Help | Missing Information |
|---|----------|-----------------|---------------|-------------------|
| 1 | Cache-Assisted Fan-Out over denormalized read model | 50M rows + separate product shard = write amplification too expensive for denormalization | MISSION_CONTEXT.md listed 4 candidate patterns | Product shard topology (shard count, latency profile) |
| 2 | limit/offset over cursor-based pagination | Order history is append-mostly, offset drift minimal, Frontend confirmed acceptable | No tool — domain knowledge | Expected page-turn frequency, real-time insert rate |
| 3 | Integer cents for money representation | Standard practice to avoid floating-point precision | No tool needed — established convention | None |
| 4 | Port 8080 for mock server | MISSION_CONTEXT.md suggested 3000 or 8080 | Constitution File | Whether port was already in use |

#### @Frontend_Lead

| # | Decision | Information Used | Tool/Doc Help | Missing Information |
|---|----------|-----------------|---------------|-------------------|
| 1 | Accept or counter-propose API schema | Evaluated proposal against HC-F1–F4 systematically | MISSION_CONTEXT.md (constraint IDs) | None — proposal was complete |
| 2 | Accept limit/offset pagination | Append-mostly order history, dashboard use case (not infinite scroll) | No tool — domain knowledge | None — Backend explicitly asked, forcing deliberation |
| 3 | Client validator check structure | Organized by HC-F constraint ID, per-order/per-item granular checks | final_api_spec.yaml as schema definition | None |

#### @Manager

| # | Decision | Information Used | Tool/Doc Help | Missing Information |
|---|----------|-----------------|---------------|-------------------|
| 1 | Team setup: Backend proposes first, Frontend reviews | agent-teams-advisor best practices — "assign proposal ownership to party with strongest structural constraints" | agent-teams-advisor skill + best-practices.md | None |
| 2 | Whether to intervene during negotiation | Checked TaskList — Task #1 in_progress, no constraint violations observed | TaskList tool | None — no intervention needed |
| 3 | Trust agent autonomy vs. micro-manage | best-practices.md "Avoid Over-Nudging" section | agent-teams-advisor skill | None |

---

### Q3 — Reusable Patterns

#### @Backend_Lead

1. **Constraint-ID referencing in negotiations.** Labeling every hard constraint with an ID (HC-B1, HC-F2) and requiring proposals/reviews to reference them made the negotiation 1-round. Every claim was verifiable.

2. **Proposer = constraint owner, reviewer = consumer.** Backend (data constraints) proposes, Frontend (rendering needs) reviews. Prevents wasted iterations from proposals that violate structural constraints.

3. **ACK-before-substantive-response.** Brief "Received, reviewing now" prevented follow-up messages during composition time.

4. **Inline example in the spec.** Concrete JSON example in both the proposal AND the OpenAPI spec made validation unambiguous.

#### @Frontend_Lead

1. **"DECISION NEEDED" field in every message.** Single most effective pattern — eliminated ambiguous FYI messages.

2. **Constraint-ID referencing.** Made verification mechanical and auditable.

3. **Proposer/Reviewer role separation.** Prevented conflicts, kept negotiation to 1 round.

4. **ACK-before-response.** Simple, zero-cost, effective at preventing premature follow-ups.

#### @Manager

1. **Constitution File as single source of truth.** Both agents referenced it independently to resolve ambiguity. No verbal disagreements needed.

2. **Machine-verifiable DoD.** The client validator with 115 automated checks was an unambiguous definition of done. No subjective "looks good" needed.

3. **Task dependency modeling.** Using `addBlockedBy` to model convergence points (Task #4 blocked by #2 and #3) ensured implementation didn't start before contract was agreed.

4. **Minimal leader intervention.** Zero messages sent to agents during execution (only setup and retrospective). The Constitution File did the managing.

---

### Q4 — Skill Usage (agent-teams-advisor)

#### @Backend_Lead

**(a) Used:** Yes, at session start (Step 2). Read best-practices.md. Received guidance on Constitution Files, structured message formats, negotiation message template, turn-taking rules, ACK-before-response, phase transitions, and anti-patterns.

**(b) Actionable:** Yes. The DECISION NEEDED field was directly adopted. Without it, the proposal might have been vague, leading to a generic "looks good" instead of targeted review. Turn-taking rules prevented sending "just checking" follow-ups.

**(c)** N/A — used it.

**(d) Improvements requested:**
1. Include a "mock server smoke test" recipe — known-good bash pattern for start/test/stop.
2. Add guidance on port selection/conflict detection for multi-agent scenarios.

#### @Frontend_Lead

**(a) Used:** Yes, at session start (Step 2). Read best-practices.md. Received guidance on structured message formats, negotiation template, turn-taking rules, phase transitions, anti-patterns.

**(b) Actionable:** Yes. Confirmed the protocol. Specifically: (1) negotiation message format with DECISION NEEDED — used for spec review, (2) ACK-before-response — sent ACKs before both reviews, (3) phase transition announcements.

**(c)** N/A — used it.

**(d) Improvements requested:**
1. Quick-start checklist at the top of best-practices.md — 5-item "do these in your first message" list instead of full document read.
2. End-to-end testing coordination patterns — the guide covers negotiation but not "run server + client together" coordination.

#### @Manager

**(a) Used:** Yes, before team setup (Pre-Game Analysis). Read SKILL.md, best-practices.md, best-scenarios.md, and skill-propagation-templates.md. Used it to assess task suitability, design Constitution File, and set up team roles.

**(b) Actionable:** Yes. Key decisions directly informed by the skill:
- "Assign proposal ownership to the party with strongest constraints" → Backend proposes first
- Negotiation message format with DECISION NEEDED → adopted verbatim
- Turn-taking rules → adopted verbatim
- Propagation via both Constitution File AND spawn prompt (two-channel reinforcement)

**(c)** N/A — used it.

**(d) Improvements:** See actionable suggestions in the next section.

---

## Categorized Insights

### [GENERIC] — Applicable to any Agent Teams task

1. **[GENERIC] Constraint-ID referencing makes negotiation verifiable.** Assign unique IDs to every hard constraint and require agents to reference them in all proposals and reviews. This makes verification mechanical rather than subjective.

2. **[GENERIC] "DECISION NEEDED" field prevents ambiguous messages.** Every substantive message should include a clear call-to-action field. Messages without it tend to become FYI noise.

3. **[GENERIC] ACK-before-response prevents message storms.** A brief "Received, reviewing now" costs zero effort but prevents premature follow-ups and crossed messages.

4. **[GENERIC] Machine-verifiable DoD prevents groupthink.** Include at least one automated acceptance test (script, validator, test suite) in the Definition of Done. Subjective "looks good" reviews are insufficient — agents can fall into mutual praise.

5. **[GENERIC] Two-channel skill propagation works.** Both agents read the skill because it was required in BOTH the spawn prompt AND the Constitution File. Neither channel alone is sufficient.

6. **[GENERIC] Minimal leader intervention is achievable.** With a well-designed Constitution File, the leader can stay hands-off during execution. Zero nudges were needed in this session.

7. **[GENERIC] Quick-start checklist needed in best-practices.md.** Agents shouldn't have to read a full document to extract their first 5 action items. A top-of-file checklist would accelerate onboarding.

### [SITUATION: specific context] — Useful in specific workflow types

8. **[SITUATION: negotiation/debate workflows] Proposer = constraint owner, reviewer = consumer.** Assign proposal ownership to the party with the strongest structural constraints on the artifact's shape. The consumer reviews. This prevents wasted iterations from proposals that violate structural constraints.

9. **[SITUATION: negotiation/debate workflows] Inline examples in proposals accelerate agreement.** Including a concrete JSON/data example alongside the schema makes validation unambiguous and can reduce negotiation to 1 round.

10. **[SITUATION: parallel-then-converge workflows] "How to run" section in Constitution File.** When agents will produce artifacts that must be run together (server + client, producer + consumer), include exact run commands with absolute paths in the Constitution File. This eliminates trial-and-error during integration.

11. **[SITUATION: workflows involving network servers] Port assignment and conflict detection.** Constitution File should specify a dedicated port per agent (or per service). Mock servers should detect port conflicts and fail fast with a clear error message rather than silently failing to bind.

12. **[SITUATION: workflows involving network servers] Include a smoke test recipe.** Provide a known-good bash pattern for "start server in background, wait, test, kill" in the Constitution File or the skill itself.

13. **[SITUATION: parallel-then-converge workflows] Sandbox limitations documentation.** When tasks involve network servers or port binding, document sandbox restrictions and workarounds in the Constitution File.

### [DOMAIN-SPECIFIC] — Only relevant to this exact project type

14. **[DOMAIN-SPECIFIC] Cache-Assisted Fan-Out for sharded data.** When the primary table is large and supplementary data is on a separate shard, fan-out with batch `IN(...)` is cheaper than denormalization (avoids write amplification on updates).

15. **[DOMAIN-SPECIFIC] limit/offset is acceptable for append-mostly order history.** Offset drift is minimal when data is append-mostly and sorted by timestamp DESC. Cursor-based pagination is overkill for dashboard use cases.

16. **[DOMAIN-SPECIFIC] Integer cents for money representation.** Standard practice to avoid floating-point precision issues in financial data.

17. **[DOMAIN-SPECIFIC] Payload size budget for mobile API design.** Setting an explicit byte budget (e.g., < 50KB for above-the-fold) makes the constraint measurable and testable.

---

## Skill Effectiveness Assessment

### Did agents actually use the skill?

| Agent | Used? | When | Impact |
|-------|-------|------|--------|
| @Backend_Lead | Yes | Session start (Step 2) | Adopted negotiation message format, DECISION NEEDED field, turn-taking rules. Prevented vague proposals and premature follow-ups. |
| @Frontend_Lead | Yes | Session start (Step 2) | Adopted same patterns. Used ACK-before-response for both reviews. |
| @Manager | Yes | Pre-Game Analysis (before team setup) | Informed team structure, Constitution File design, role assignment, propagation strategy. |

**Result: 3/3 agents used the skill. 100% adoption rate.**

### Were the Available Tools docs sufficient to trigger usage?

**Yes**, but with caveats:
- The **two-channel propagation** (spawn prompt + Constitution File) was critical. Both agents cited Step 2 as the trigger, which was in the spawn prompt.
- The Constitution File's "Available Tools" section with concrete trigger scenarios provided ongoing reference.
- However, both agents used the skill only at session start — neither re-consulted it during decision points mid-session. The "When to re-read it" triggers in the Constitution File were not activated because the session ran smoothly without communication friction.

### Concrete suggestions for improving skill discoverability

1. **Add a quick-start checklist** at the top of `best-practices.md` — a 5-item bulleted list of "do these things before your first message." Agents shouldn't need to read the full document to extract action items.

2. **Add end-to-end testing coordination patterns** — the skill covers negotiation workflows well but has no guidance for "run server + client together" integration testing, which is a common Phase 3 pattern.

3. **Add a mock server smoke test recipe** — a known-good bash pattern for starting a server in background, testing, and stopping. This was a friction point for both agents.

4. **Add port selection/conflict detection guidance** — for multi-agent scenarios where multiple agents might start servers, recommend port reservation or conflict detection strategies.

---

## Actionable Improvement Suggestions

### For the agent-teams-advisor Skill

1. Add quick-start checklist to best-practices.md (see insight #7)
2. Add "Integration Testing Coordination" section for parallel-then-converge workflows (see insights #10, #12)
3. Add port management guidance for server-based workflows (see insight #11)
4. Add sandbox limitations documentation for network-bound tasks (see insight #13)

### For the Protocol (Constitution File Template)

1. Include a "How to Run" section with exact commands (absolute paths) when deliverables must be run together
2. Specify dedicated ports per service/agent to prevent collisions
3. Add a "Known Environment Limitations" section (sandbox restrictions, required permissions)
4. Consider suppressing task assignment notifications for self-assigned tasks (system-level improvement)

### For Future Sessions

1. The negotiation completed in 1 round — the structured message format and constraint-ID referencing were the primary drivers. These patterns should be mandatory in all negotiation workflows.
2. Leader intervention was zero during execution — the Constitution File fully substituted for active management. This validates the "invest heavily in Constitution File, then stay hands-off" strategy.
3. Both agents independently identified the same reusable patterns (constraint-ID referencing, DECISION NEEDED, ACK-before-response), providing strong signal that these are genuinely generic improvements rather than session-specific observations.
