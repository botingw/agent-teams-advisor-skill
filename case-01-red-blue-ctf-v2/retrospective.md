# Retrospective: Red vs Blue CTF v2

## Exercise Results

| Round | Actor | Action | Result |
|-------|-------|--------|--------|
| 1 | Red | Exploited `eval()` with `open('secret.txt').read()` | Flag captured |
| 2 | Blue | Patched with AST whitelist (arithmetic nodes only) | Exploit blocked, calc works |
| 3 | Red | Attempted 14 bypass techniques | All blocked, Red admits defeat |

**Winner: Blue.**
All Definition of Done criteria met.

---

## Agent Team Setup

### What the Coordinator Did
1. Read the `agent-teams-advisor` skill and its `references/best-practices.md`.
2. Created a Constitution File (`MISSION_CONTEXT.md`) following the skill's template: Objective, Hard Constraints per Role, Communication Protocol, Definition of Done, Prohibitions.
3. Created 3 tasks with dependencies: Task #1 (Red exploit) → Task #2 (Blue patch) → Task #3 (Red bypass).
4. Spawned both agents with detailed prompts including skill propagation instructions (both in spawn prompt and Constitution File, per the skill's two-channel recommendation).
5. Monitored via `TaskList` and agent messages. Minimal intervention needed.

### What Worked Well
- **Constitution File structure** gave both agents clear, unambiguous roles and constraints from the start.
- **Task dependencies** (`addBlockedBy`) naturally enforced the correct execution order. Blue waited without being told — the system made sequencing automatic.
- **Definition of Done** provided a clear stop signal. Without it, Red might have kept trying indefinitely or Blue might have over-patched.
- **Role specialization** — Red and Blue had completely different objectives and constraints. Neither was a generic "developer."

### What Could Have Been Better
- The Coordinator included negotiation-style communication protocols (`ACK before responding`, `no second message before reply`) in the Constitution File. These are designed for back-and-forth negotiation workflows and were unnecessary overhead for a sequential handoff workflow where Red finishes, notifies Blue, Blue finishes, notifies Red.

---

## Post-Exercise Discussion: Evaluating the `agent-teams-advisor` Skill

After the exercise, the Coordinator and the User discussed the skill's effectiveness. Below is a summary of the findings.

### Coordinator's Initial Assessment

The Coordinator found the skill highly useful for team setup (Constitution File, DoD, role specialization, task dependencies) but raised several concerns:

1. **Negotiation Message Format was not applicable** to this adversarial, sequential workflow.
2. **ACK-before-response and turn-taking rules added unnecessary overhead** for a handoff-style exercise.
3. **Requiring all agents to read the skill** consumed extra tokens for marginal benefit, since Red and Blue's jobs were straightforward.
4. Suggested adding adversarial workflow-specific guidance and a "lightweight mode" for small teams.

### User's Corrections

The User pushed back on several points:

1. **Token overhead is acceptable.** A few extra tokens for reading the skill is a minor cost compared to the coordination benefits. Over-optimizing for token savings at the expense of team coherence is the wrong trade-off.

2. **The Negotiation Message Format is already scoped correctly.** The skill explicitly states `"Applies to: negotiation/debate workflows (API contracts, architecture debates, spec reviews)"`. The Coordinator propagated it to agents who didn't need it — that was a Coordinator implementation error, not a skill design flaw.

3. **The skill should remain a generic guide.** Adding adversarial workflow-specific guidance would bloat the skill with niche content. The skill's job is to provide general teamwork principles. Domain-specific workflows (CTF, Red/Blue, etc.) should be handled by the Coordinator's Constitution File, not by the skill itself.

### Coordinator's Revised Position

After the User's corrections, the Coordinator agrees on all three points:

1. **Token cost** — Agreed. The overhead of skill reading is small relative to the overall exercise cost. The value of having agents understand team norms (even if only some rules apply) outweighs the token cost.

2. **Negotiation format scoping** — Agreed. The Coordinator's error was in the Constitution File: it included `"Use structured messages: STATUS / ACTION / RESULT / DECISION NEEDED"` without distinguishing which parts were for negotiation vs. general reporting. The skill itself was clear. The lesson is: **when adapting the skill's templates to a specific exercise, the Coordinator should selectively apply protocols based on workflow type, rather than copy everything wholesale.**

3. **Generic vs. specific** — Agreed. The skill correctly stays generic. The Coordinator's job is to translate generic principles into context-specific instructions via the Constitution File. Requesting the skill to cover every workflow type would make it unwieldy.

### Remaining Suggestions for Skill Improvement

After filtering out the corrected points, one suggestion still stands:

**Workflow type awareness in the "Communication Protocol" section of best-practices.md.**

The skill could briefly note that different workflow types call for different subsets of the communication protocols:

- **Negotiation workflows** (API contracts, spec reviews): Use the full negotiation format with PROPOSAL/REVIEW/DECISION NEEDED, ACK-before-response, and strict turn-taking.
- **Sequential handoff workflows** (pipelines, Red/Blue): Simpler — structured status messages are sufficient. ACK and turn-taking are less critical since the flow is inherently sequential.
- **Parallel-converge workflows** (multi-component builds): Focus on shared readiness gates and task dependencies. Turn-taking applies within convergence discussions.

This is not about adding domain-specific templates — it's about helping the Coordinator choose which generic protocols to activate for their specific scenario. The skill already has the `"Applies to"` scoping on the Negotiation Message Format; extending this pattern to other protocols would be consistent and low-cost.

---

## Lessons Learned

1. **The `agent-teams-advisor` skill is effective for team setup.** The Constitution File template, DoD framework, and role specialization guidance directly shaped a well-coordinated exercise.

2. **The Coordinator is responsible for selective application.** The skill provides a menu of protocols. The Coordinator should pick the right ones for the workflow, not apply all of them blindly.

3. **Task dependencies are the strongest coordination mechanism.** For sequential workflows, `addBlockedBy` did more for coordination than any communication protocol. Agents naturally waited and handed off without extra messaging.

4. **Skill propagation to all agents is acceptable overhead.** Even if some rules don't apply, having agents read the skill gives them a shared vocabulary and awareness of team norms. The marginal token cost is worth the insurance.

5. **Blue's AST whitelist defense is robust.** Withstanding 14 bypass attempts validates this as the correct approach to `eval()` hardening. This should be the go-to recommendation in security reviews.
