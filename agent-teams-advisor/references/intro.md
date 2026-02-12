# Agent Teams Architecture Overview

## What Are Agent Teams?

An experimental feature in Claude Code that allows multiple Agents to form a team and collaborate. Core characteristics:

- **Team Lead**: The main Terminal session acts as the commander — responsible for decomposing tasks, assigning work, and accepting deliverables
- **Mesh Communication (P2P)**: Teammates can send messages directly to each other without routing through the Team Lead
- **Independent Context Windows**: Each Agent is a fully independent Claude session, so they never crowd out each other's context
- **Shared Task Board**: Agents share state and can coordinate progress in real time

## Agent Teams vs. Subagents

| Feature | Subagents (Legacy) | Agent Teams (New) |
| :--- | :--- | :--- |
| **Communication topology** | Hub-and-Spoke — can only report up to the parent | Mesh — teammates can message each other directly |
| **Collaboration model** | Sequential/independent — A has no idea what B did | Parallel/dynamic — real-time notification via Inbox |
| **Context** | Shared or branched from the main thread; prone to interference | Each Agent has an independent Context, no mutual impact |
| **Best suited for** | Single, well-defined tasks | Complex projects with multi-role parallel development |

## How It Works Under the Hood

- **Shared State**: The system creates shared communication and task files under `.claude/teams/`
- **Inbox mechanism**: Every Agent has its own Inbox; other Agents can write messages into it
- **Visualization (tmux)**: Split Panes can be opened to monitor multiple Agents' work simultaneously
- **Feature Flag**: Typically requires setting `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` to enable

## Pros and Cons at a Glance

**Pros:**
- Agents can communicate to resolve conflicts in real time instead of discovering breakage at integration time
- Parallel processing is faster than sequential, especially for full-stack changes
- Multi-Agent debate produces more accurate results than a single Agent guessing
- Each Agent's independent Context prevents the main thread from overflowing

**Cons:**
- Cost scales multiplicatively (N Agents = at least N× the cost)
- Agents can fall into pointless "zombie meetings" or mutual waiting
- Experimental in nature; less stable than a single Agent
- Requires environment setup (tmux, etc.), which raises the barrier to entry
