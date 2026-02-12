# Agent Teams: Scenario Guide

## Table of Contents
1. [Best-Fit Scenarios](#best-fit-scenarios)
2. [Scenarios to Avoid](#scenarios-to-avoid)
3. [Advanced / High-Potential Applications](#advanced--high-potential-applications)
4. [Benchmarks and Cost References](#benchmarks-and-cost-references)

---

## Best-Fit Scenarios

### #1 Strict TDD (Test-Driven Development)
- **Setup**: Agent A (Test-Writer) only writes tests; Agent B (Implementer) writes the implementation
- **Effect**: A acts as a relentless QA gatekeeper — it refuses to accept anything until all tests pass, forcing B to fix code until the suite is green
- **Real-world feedback**: Slower, but the resulting code quality is extremely high with virtually no regressions
- **Why it works**: Solves the common problem of AI "cutting corners" on tests. Two independent sessions keep each other honest.

### #2 Competitive Debugging
- **Scenario**: An intermittent bug with no obvious root cause
- **Setup**: Spin up 3 Agents, each investigating a different hypothesis (e.g., DB deadlock / React race condition / network timeout)
- **Effect**: As soon as one Agent finds evidence, it broadcasts via the Inbox so others can stand down
- **Why it works**: Divide-and-conquer drastically reduces debugging time

### #3 Full-Stack Vertical Slice
- **Scenario**: Simultaneously modifying DB schema, backend API, and frontend UI
- **Setup**: Backend Agent defines the API and mocks data → notifies Frontend Agent to start UI → Backend continues real implementation
- **Why it works**: Front and back ends develop in parallel; API changes are communicated via Inbox in real time, reducing errors compared to a single Agent switching between files

### Other Proven Scenarios
- **Multi-perspective Code Review**: Security Expert + Performance Hawk + Product Manager review the same code from different angles
- **Documentation Swarm**: Multiple Agents each update docs for an assigned folder; an Editor Agent reviews for style consistency
- **Legacy Code Migration**: An Interface Keeper defines type definitions while multiple Workers convert files in parallel

---

## Scenarios to Avoid

### Linearly Dependent Tasks
"Read file A first, then modify B based on A" — the order is fixed and no inter-agent communication is needed. A single Subagent is sufficient.

### Simple CRUD
Don't use a sledgehammer to crack a nut. The Team initialization overhead (scanning project structure, allocating tasks) can take longer than just writing the code directly.

### Large Refactors Without Test Coverage
Without tests, Agents easily "break each other silently." Agent A changes a library, Agent B references the old version, and with no test failures to flag the problem, both hallucinate that everything is fine. The result: merge conflicts everywhere.

### Rule of Thumb
> Start with Subagents. If you find an Agent repeatedly needing to "ask you" about information in other files, that's the signal to upgrade to Agent Teams.

---

## Advanced / High-Potential Applications

### Red/Blue Teaming (Security Audit)
- Blue Agent fixes vulnerabilities; Red Agent's sole job is to attack Blue's code (SQL injection, XSS, permission bypass)
- Because the two Agents have independent memory, Red doesn't know what Blue just fixed, enabling objective attacks
- Simulates real offensive/defensive security — far more effective than simply asking AI to "check for vulnerabilities"

### The Hiring Committee (Simulated Code Review)
- Multiple personas (Google Interviewer / Startup CTO / Junior Dev) each review the same code
- They debate among themselves, then deliver a combined score

---

## Benchmarks and Cost References

### Official Stress Test: The C Compiler (Nicholas Carlini)
- **Task**: Write a C compiler from scratch capable of compiling the Linux kernel
- **Scale**: 16 Agents in parallel, ~2,000 total sessions
- **Result**: Successfully produced ~100,000 lines of code (supporting x86, ARM, RISC-V)
- **Cost**: ~$20,000 USD

### Community Counter-Example: The Gemini Review
- A complex feature built by Agent Teams was submitted to Google Gemini 3 Pro for code review
- Gemini flagged **19 critical issues**
- **Lesson**: Agent Teams can fall into "groupthink." Without strict acceptance criteria, Agents may praise each other's flawed code and close the task prematurely.

### Cost Expectations
- 5 Agents "meeting" for 15 minutes can burn ~$50 USD
- Token consumption scales exponentially; an unmonitored overnight run can result in massive bills
