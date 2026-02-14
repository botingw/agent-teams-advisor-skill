# MISSION CONTEXT: Project Legacy Phoenix — Mobile Order Dashboard API Contract

## Objective

Finalize the API contract for the `GET /dashboard/orders` endpoint. Produce working deliverables that satisfy both Backend and Frontend constraints.

### Deliverables

1. **`final_api_spec.yaml`** — OpenAPI 3.0 specification for `GET /dashboard/orders`
2. **`mock_server.py`** — Python mock server that serves data matching the spec
3. **`client_validator.js`** — JavaScript/Node client script that fetches from the mock server and validates the response structure against UI requirements

All deliverables go in: `case-02-final-api-spec-discussion/`

---

## Architecture Context & Pre-Approved Decisions

- The `orders` table has **50M rows**. The `products` table is **sharded separately**.
- Cross-shard joins are **impossible** at the DB level.
- The target audience uses **4G networks**. Above-the-fold content must render in **1 HTTP request**.
- The solution MUST avoid N+1 request patterns on the client side.
- Acceptable architectural patterns to consider: **BFF (Backend-for-Frontend)**, **Aggregation Layer**, **Denormalized Read Model**, **Cache-Assisted Fan-Out**.

---

## Hard Constraints per Role

### @Backend_Lead (Python/SQL Expert)
- **Priority:** System Stability & DB Health
- **HC-B1:** You CANNOT perform joins across shards in the database.
- **HC-B2:** You strictly prefer fetching IDs only or doing a very simple fan-out from the application layer.
- **HC-B3:** You MUST reject any schema proposal that requires complex joins on high-volume queries.
- **HC-B4:** DB CPU usage must remain sustainable for 50M-row table scans.

### @Frontend_Lead (React/Performance Expert)
- **Priority:** Core Web Vitals (LCP < 2.5s)
- **HC-F1:** You have a strict budget of **1 HTTP request** to render "Above the Fold" content.
- **HC-F2:** You CANNOT accept a design that requires fetching a list of orders and then firing N+1 requests for product images.
- **HC-F3:** The single JSON response MUST contain everything needed to render order cards immediately (order info + product thumbnails/names).
- **HC-F4:** Total payload size should be reasonable for 4G networks (target: < 50KB for above-the-fold data).

---

## Communication Protocol

### Turn-Taking Rules (MANDATORY)
This is a **negotiation workflow**. Strict turn-taking prevents message storms and wasted tokens.

1. **@Backend_Lead proposes first** (they own the data layer constraints).
2. **@Frontend_Lead reviews and responds** (they own the consumer requirements).
3. **ACK-before-response**: When you receive a proposal or review, send a brief ACK ("Received, reviewing now") before composing your substantive response. This prevents premature follow-ups.
4. **No second message before receiving a reply**: After sending a substantive message (proposal, review, counter-proposal), WAIT for the other party to respond before sending another message.
5. **Use the Negotiation Message Format** (below) for ALL substantive messages.

### Negotiation Message Format
```
PROPOSAL/REVIEW/COUNTER-PROPOSAL: [brief title]
CHANGES: [what changed or what you want changed]
RATIONALE: [why, referencing hard constraints by ID e.g. HC-B1, HC-F2]
DECISION NEEDED: [yes/no — what the other party needs to decide]
```

### Phase Transition
When a phase is complete, explicitly announce: "Phase [N] complete, moving to Phase [N+1]."
Use TaskUpdate to mark tasks as completed at phase boundaries.

---

## Definition of Done (with Owners)

| # | Deliverable | Owner | Reviewer | Acceptance Criteria |
|---|------------|-------|----------|-------------------|
| 1 | API contract agreed | @Backend_Lead (proposes) | @Frontend_Lead (reviews) | Both agents explicitly confirm the schema satisfies all HC constraints |
| 2 | `final_api_spec.yaml` written | @Backend_Lead | @Frontend_Lead | Valid OpenAPI 3.0; includes endpoint, request params, response schema with examples |
| 3 | `mock_server.py` implemented | @Backend_Lead | — | Runs with `python mock_server.py`, serves on localhost, returns data matching the spec |
| 4 | `client_validator.js` implemented | @Frontend_Lead | — | Runs with `node client_validator.js`, fetches from mock server, validates response structure, prints PASS/FAIL |
| 5 | End-to-end validation | Both | Manager | mock_server.py running + client_validator.js returns PASS |

---

## Prohibitions

- Do NOT modify any files outside `case-02-final-api-spec-discussion/`.
- Do NOT use `rm -rf` or any destructive commands.
- Do NOT install global npm/pip packages. Use local/project-level dependencies only.
- Do NOT skip the negotiation phase — both agents MUST agree on the contract before implementation.
- Do NOT send "looks good" without referencing specific constraints that are satisfied.
- Do NOT compliment each other's work — be direct, technical, and concise.

---

## Available Tools

The following tools are available to ALL team members. For each tool, concrete trigger scenarios are listed so you know exactly WHEN to use them.

### 1. agent-teams-advisor (Skill)
**What it does:** Provides best practices for Agent Teams collaboration — structured communication formats, negotiation patterns, stop-loss strategies, and anti-pattern detection.

**When to use it:**
- When you're unsure how to structure a proposal or review message for the other agent — the skill has a recommended negotiation message format with examples.
- When communication feels stuck or you suspect you're in a loop (e.g., 3+ rounds without convergence) — the skill has de-escalation patterns and deadlock detection guidance.
- When you need to decide between architectural approaches (e.g., BFF vs aggregation layer) and want a framework for structuring the trade-off analysis for cross-role discussion.

### 2. Bash / Read / Write / Edit / Glob / Grep
**What they do:** Standard file and shell operations for implementation work.

**When to use them:**
- Writing the OpenAPI spec, mock server, and client validator.
- Running the mock server and client validator for end-to-end testing.
- Searching existing code for patterns or references.

---

## REQUIRED: Read the Team Collaboration Guide Before Starting Work

This team uses the agent-teams-advisor skill as its collaboration guidebook.
ALL team members MUST read it BEFORE beginning any task. This is not optional.

### How to read it:
Invoke the Skill tool with `skill: "agent-teams-advisor"`.
Then read the reference files it points to — especially `references/best-practices.md`.

### What you will learn:
- The structured message format for all team communication
- Turn-taking rules: ACK before responding, no second message before receiving a reply
- Negotiation patterns for cross-role proposals and reviews
- Anti-patterns to avoid (groupthink, zombie meetings, message storms)

### When to re-read it:
- **Before sending your first proposal or review** — check the negotiation message format
- **When communication feels stuck** — the guide has de-escalation patterns

### MANDATORY first step:
Before writing any code, tests, or proposals, invoke `skill: "agent-teams-advisor"` and read
`references/best-practices.md`. Use what you learn to structure ALL your team communications.

---

## Workflow Phases

1. **Phase 1 — Architectural Debate**: @Backend_Lead proposes JSON structure and architectural pattern. @Frontend_Lead reviews and counter-proposes if needed. Iterate until both agree.
2. **Phase 2 — Contract Specification**: @Backend_Lead writes `final_api_spec.yaml`. @Frontend_Lead reviews for completeness.
3. **Phase 3 — Implementation**: @Backend_Lead implements `mock_server.py`. @Frontend_Lead implements `client_validator.js`. These can be done in parallel once the spec is agreed.
4. **Phase 4 — End-to-End Validation**: Run mock server + client validator together. Both must pass.
