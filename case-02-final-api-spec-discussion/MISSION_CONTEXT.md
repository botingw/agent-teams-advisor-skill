# MISSION_CONTEXT.md — Project Legacy Phoenix
# Single Source of Truth for All Team Members
# READ THIS FILE FIRST BEFORE ANY OTHER ACTION

---

## Objective

Finalize the API contract for `GET /dashboard/orders` and deliver working implementations:

1. **`final_api_spec.yaml`** — OpenAPI 3.0 specification agreed upon by both Backend and Frontend
2. **Mock Server** — Python server generating data matching the spec
3. **Client Validator** — Script that fetches from the mock server and validates the response structure against UI needs

All deliverables go in: `/Users/wangbo-ting/git/agent-war-room-2/case-02-final-api-spec-discussion/`

---

## Architecture Context & Pre-Approved Decisions

- The `orders` table has **50 million rows**. The `products` table is **sharded separately**.
- Cross-shard joins are impossible at the DB level.
- Target audience is on **4G networks**. Core Web Vitals target: **LCP < 2.5s**.
- The frontend has a strict budget of **1 HTTP request** for above-the-fold content.
- A **BFF (Backend-for-Frontend) aggregation layer** is the pre-approved architectural pattern. The BFF sits between the frontend and the microservices/DB, performing fan-out internally.

---

## Team Roles & Hard Constraints

### @Backend_Lead
- **Domain**: Python, SQL, system stability, DB health
- **Hard Rules (NON-NEGOTIABLE)**:
  1. NO cross-shard joins in the database layer
  2. NO complex joins on high-volume queries (50M row table)
  3. The BFF may perform simple fan-out (fetch order IDs, then batch-fetch product data), but the DB query itself must be simple
  4. Response pagination is required for large result sets
- **Owns**: `final_api_spec.yaml` (initial draft), mock server implementation

### @Frontend_Lead
- **Domain**: React, performance, Core Web Vitals
- **Hard Rules (NON-NEGOTIABLE)**:
  1. The single API response MUST contain all data needed to render above-the-fold order cards (no N+1 requests)
  2. Product images must be URLs in the response (not separate fetches)
  3. LCP < 2.5s on 4G — response payload must be optimized (no unnecessary fields)
- **Owns**: Client validator implementation, UI field requirements review

---

## Communication Protocol

### Turn-Taking Rules (MANDATORY)
1. **Proposal Phase**: @Backend_Lead proposes the initial API schema first (since they own the data constraints)
2. **Review Phase**: @Frontend_Lead reviews and responds with requested changes
3. **ACK-before-response**: Before writing a substantive reply, send a brief ACK ("Received, reviewing now")
4. **No double-sending**: Do NOT send a second message before receiving a response to your first
5. **Disagreements**: Reference this MISSION_CONTEXT.md to resolve disputes. If still unresolved, escalate to the Engineering Manager.

### Message Format
When sending proposals or reviews, use this structure:
```
PROPOSAL/REVIEW: [brief title]
CHANGES: [what changed or what you want changed]
RATIONALE: [why, referencing hard constraints]
DECISION NEEDED: [yes/no — what the other party needs to decide]
```

### Phase Transitions
Announce phase transitions explicitly:
- "Phase 1 (Debate) complete, moving to Phase 2 (Spec Writing)"
- "Phase 2 (Spec) complete, moving to Phase 3 (Implementation)"

---

## Definition of Done (with Owners)

| # | Deliverable | Owner | Reviewer | Criteria |
|---|------------|-------|----------|----------|
| 1 | API schema debate concluded | Both | Manager | Both leads explicitly agree on the JSON structure |
| 2 | `final_api_spec.yaml` written | @Backend_Lead | @Frontend_Lead | Valid OpenAPI 3.0, includes all agreed fields |
| 3 | `final_api_spec.yaml` approved | @Frontend_Lead | @Backend_Lead | Frontend confirms all UI-required fields are present |
| 4 | Mock server (`mock_server.py`) | @Backend_Lead | — | Runs on localhost, serves data matching the spec |
| 5 | Client validator (`client_validator.py`) | @Frontend_Lead | — | Fetches from mock server, validates response structure, prints pass/fail |
| 6 | End-to-end verification | Both | Manager | Client validator successfully validates mock server response |

---

## Prohibitions

1. Do NOT modify any files outside the `case-02-final-api-spec-discussion/` directory
2. Do NOT use `rm -rf` or any destructive commands
3. Do NOT install system-level packages (pip install to local/virtual env only if needed)
4. Do NOT skip the debate phase — both parties must explicitly agree before writing the spec
5. Do NOT send more than 2 messages without receiving a response — if stuck, escalate to Manager
6. Do NOT use pleasantries or filler — be concise, technical, and direct

---

## Workflow Summary

```
Phase 1: DEBATE
  @Backend_Lead proposes initial JSON schema
  @Frontend_Lead reviews and negotiates
  Iterate until both explicitly agree

Phase 2: SPEC
  @Backend_Lead writes final_api_spec.yaml
  @Frontend_Lead reviews and approves

Phase 3: IMPLEMENTATION (parallel)
  @Backend_Lead → mock_server.py
  @Frontend_Lead → client_validator.py

Phase 4: VERIFICATION
  Run client_validator.py against mock_server.py
  Both confirm success → Mission Complete
```
