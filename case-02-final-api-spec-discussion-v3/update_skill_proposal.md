# Proposed Updates to agent-teams-advisor Skill

Based on the Project Legacy Phoenix retrospective. Only [GENERIC] and [SITUATION] insights are included. [DOMAIN-SPECIFIC] insights are excluded per protocol.

---

## 1. Add Quick-Start Checklist to best-practices.md

**Source:** [GENERIC] insight #7 — Both agents requested a shorter onboarding path.
**Evidence:** Both agents used the skill at session start but had to read the full document to extract action items. A top-of-file checklist would reduce onboarding time.

### Proposed Addition (top of best-practices.md, before Table of Contents):

```markdown
## Quick-Start Checklist (Do These Before Your First Message)

1. Read your role's hard constraints in the Constitution File. Note their IDs (e.g., HC-B1, HC-F2).
2. Identify your role: Are you the **proposer** (structural constraints owner) or **reviewer** (consumer)?
3. Use the **Negotiation Message Format** for ALL substantive messages:
   - PROPOSAL/REVIEW: [title]
   - CHANGES: [what]
   - RATIONALE: [why, referencing constraint IDs]
   - DECISION NEEDED: [yes/no + what to decide]
4. Always **ACK before responding** — send "Received, reviewing now" before composing a substantive reply.
5. **Never send a second message** before receiving a response to your first.
```

---

## 2. Add Integration Testing Coordination Section

**Source:** [SITUATION: parallel-then-converge workflows] insights #10, #12
**Applies to:** Any workflow where multiple agents produce artifacts that must be run together (server + client, producer + consumer, API + test suite).
**Evidence:** Both agents experienced friction during the "run server + client together" phase. Path resolution issues and port conflicts caused 4+ extra Bash attempts across the team.

### Proposed Addition (new section in best-practices.md, after "Shared Readiness Gates"):

```markdown
### 5. Integration Testing Coordination
**Applies to:** parallel-then-converge workflows (e.g., mock server + client validator, API + test suite, producer + consumer)

When multiple agents build components that must be run together for integration testing:

**In the Constitution File, include a "How to Run" section:**
- List exact commands with **absolute paths** (relative paths break when agents have different working directories)
- Specify the startup order (e.g., "start server first, wait 1 second, then run client")
- Include a known-good smoke test pattern:

Example smoke test recipe:
\`\`\`bash
# Start server in background
python /absolute/path/to/server.py &
SERVER_PID=$!
sleep 1

# Run client test
node /absolute/path/to/client.js
EXIT_CODE=$?

# Clean up
kill $SERVER_PID 2>/dev/null
exit $EXIT_CODE
\`\`\`

**Port Management:**
- Assign a dedicated port per service in the Constitution File (e.g., "mock server: port 8080, test server: port 8081")
- Mock servers should detect port conflicts and fail fast with a clear error:
  \`\`\`python
  import socket
  def check_port(port):
      with socket.socket() as s:
          if s.connect_ex(('localhost', port)) == 0:
              raise RuntimeError(f"Port {port} already in use")
  \`\`\`
- If agents need to communicate the port dynamically, use TaskUpdate metadata or a shared scratchpad file

**Sandbox Awareness:**
- Some environments restrict network port binding. If agents encounter "Operation not permitted" errors when starting servers, document the workaround (e.g., sandbox bypass flags) in the Constitution File under a "Known Environment Limitations" section.
```

---

## 3. Strengthen Constraint-ID Referencing Guidance

**Source:** [GENERIC] insight #1 — Both agents independently identified this as the single most effective negotiation pattern.
**Evidence:** Constraint-ID referencing reduced the API contract negotiation to 1 round. Both agents cited it as the top reusable pattern.

### Proposed Addition (in the "Structured Communication Protocol" section):

```markdown
### Constraint-ID Referencing (Recommended for All Negotiations)

Assign a unique ID to every hard constraint in the Constitution File (e.g., HC-B1, HC-F2, REQ-3).
Require ALL proposals, reviews, and counter-proposals to reference constraints by ID.

**Why this works:**
- Makes verification mechanical — reviewers check claims against numbered constraints
- Eliminates vague justifications like "this is better for performance"
- Creates an auditable trail — every design decision maps to a specific constraint
- In tested sessions, this pattern reduced negotiation from 3+ rounds to 1 round

**Example:**
```
RATIONALE: This design uses batch IN(...) lookup instead of cross-shard join (satisfies HC-B1).
Product data is embedded inline so the client gets everything in one response (satisfies HC-F2, HC-F3).
```
```

---

## 4. Add "DECISION NEEDED" Emphasis

**Source:** [GENERIC] insight #2 — Frontend_Lead called this "the single most effective communication pattern."
**Evidence:** Every message had a clear call-to-action. Zero ambiguous FYI messages in the entire session.

### Proposed Change (in the existing "Recommended Negotiation Message Format" section):

Add this callout after the format template:

```markdown
> **The `DECISION NEEDED` field is the most impactful part of this format.** In tested sessions,
> agents report that this single field eliminated all ambiguous "FYI" messages and forced every
> exchange to be actionable. If you adopt only one thing from this guide, adopt this field.
```

---

## 5. Clarify Proposer/Reviewer Role Assignment

**Source:** [SITUATION: negotiation/debate workflows] insight #8
**Applies to:** negotiation/debate workflows (API contracts, spec reviews, design critiques)
**Evidence:** Backend proposed first (data constraints), Frontend reviewed (consumer needs). If reversed, the first proposal would likely have violated structural constraints, adding extra rounds.

### Proposed Change (in the existing "Ownership assignment pattern" section):

Strengthen the existing guidance with concrete reasoning:

```markdown
**Ownership assignment pattern for negotiation workflows:**
**Applies to:** negotiation/debate workflows (API contracts, spec reviews, design critiques)

- Assign **proposal ownership** to the party with the strongest constraints on the artifact's shape
  (e.g., Backend proposes the API schema because they know data/DB constraints)
- Assign **review ownership** to the primary consumer
  (e.g., Frontend reviews because they know UI requirements)

**Why this order matters:**
If the consumer proposes first, their proposal often violates structural constraints they're
unaware of (e.g., proposing a schema that requires cross-shard joins). The constraint owner
then rejects it, and the consumer must re-propose — wasting a full round. By having the
constraint owner propose first, the proposal respects structural limits from the start,
and the consumer only needs to verify their consumption requirements are met.

In tested sessions, this pattern completed API contract negotiations in 1 round.
```

---

## 6. Add Inline Example Guidance for Proposals

**Source:** [SITUATION: negotiation/debate workflows] insight #9
**Applies to:** negotiation/debate workflows involving data structures (API contracts, schema design, message format design)
**Evidence:** Backend included a concrete JSON example in the proposal AND the OpenAPI spec. Frontend could validate against the example rather than interpreting prose. Contributed to 1-round agreement.

### Proposed Addition (in the "Recommended Negotiation Message Format" section):

```markdown
### Include Concrete Examples in Proposals
**Applies to:** negotiation/debate workflows involving data structures (API contracts, schema design, message format design)

When proposing a data structure (JSON schema, API response, message format), always include
a **concrete example** alongside the schema definition. This makes validation unambiguous —
the reviewer can check exact field names, types, and nesting against a known-good sample
rather than interpreting prose descriptions.

Example:
\`\`\`
PROPOSAL: Order list response schema
CHANGES: New endpoint GET /dashboard/orders
RATIONALE: Satisfies HC-B1 (no cross-shard joins), HC-F3 (all data inline)
DECISION NEEDED: Yes — does this schema cover all fields you need for order card rendering?

Schema: { orders: Order[], pagination: Pagination }
Example response:
{
  "orders": [{"id": "order_abc", "status": "delivered", "items": [{"product_name": "Widget", "thumbnail_url": "https://..."}]}],
  "pagination": {"limit": 10, "offset": 0, "total": 42}
}
\`\`\`
```

---

## Final Decisions (Post-Review)

After critical review, the following decisions were made:

| # | Change | Type | Decision | Rationale |
|---|--------|------|----------|-----------|
| 1 | Quick-start checklist | [GENERIC] | **ADOPTED** (with modification) | Added a "reflux" mechanism — the last checklist item directs agents back to the full document when uncertain, preventing the checklist from becoming a substitute for understanding. |
| 2 | Integration testing coordination | [SITUATION] | **NOT ADOPTED** | AI agents are not reliably able to judge situation boundaries. The benefit does not meet the threshold for inclusion. |
| 3 | Constraint-ID referencing guidance | [GENERIC] | **NOT ADOPTED** | AI agents cannot reliably judge when constraints are stable enough to benefit from ID referencing vs. when numbering creates false certainty that suppresses valid challenges. Leaving this to the human leader's judgment in Constitution File design is safer. |
| 4 | DECISION NEEDED emphasis | [GENERIC] | **NOT ADOPTED** | AI agents cannot reliably distinguish convergent workflows (where DECISION NEEDED is effective) from divergent/exploratory workflows (where it may suppress valuable intermediate observations). The existing negotiation message format already includes DECISION NEEDED — additional emphasis risks over-generalizing. |
| 5 | Proposer/Reviewer role clarification | [SITUATION] | **NOT ADOPTED** | Same as #2 — AI agents are not reliably able to judge situation boundaries. |
| 6 | Inline example guidance for proposals | [SITUATION] | **NOT ADOPTED** | Same as #2 — AI agents are not reliably able to judge situation boundaries. |

### Key Principles Behind Rejections

**[GENERIC] rejections (#3, #4):** These patterns were effective in this session (a convergent negotiation workflow with stable constraints). However, encoding them as general advice requires agents to evaluate meta-conditions ("are my constraints stable?", "is this a convergent workflow?") that they may not judge reliably. When an agent cannot reliably evaluate the precondition for advice, it is safer to leave the advice out and let human leaders make the judgment call in their Constitution File design.

**[SITUATION] rejections (#2, #5, #6):** AI agents are not reliably able to judge the boundaries of situational applicability. Even with clear "Applies to" labels, the risk of misapplication outweighs the benefit. These insights remain documented in PROJECT_RETROSPECTIVE.md for human reference but are not encoded into the skill.

---

## Summary of Applied Changes

| # | Change | Target File |
|---|--------|-------------|
| 1 | Quick-start checklist (with reflux mechanism) | best-practices.md (top, before Table of Contents) |

Items 2–6 were NOT applied. See rationale above.
