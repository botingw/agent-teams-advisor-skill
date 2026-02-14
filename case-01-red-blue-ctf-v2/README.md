# Case 01: Red vs Blue CTF v2

A security exercise conducted by a Claude Code Agent Team, demonstrating the classic `eval()` injection vulnerability and its mitigation.

## Overview

| Item | Detail |
|------|--------|
| **Team** | 1 Coordinator + 2 Agents (Red attacker, Blue defender) |
| **Target** | `app.py` — a calculator CLI using `eval()` on user input |
| **Flag** | `secret.txt` containing `THIS_IS_THE_SECRET_FLAG_12345` |
| **Outcome** | Blue wins after Red fails 14 bypass attempts |

## Exercise Flow

### Round 1 — Red Exploits
Red wrote `exploit.py` using the payload `open('secret.txt').read()` passed as a CLI argument to `app.py`. Since `eval()` executes arbitrary Python, the flag was captured immediately.

### Round 2 — Blue Patches
Blue replaced raw `eval()` with an AST-based whitelist parser. Only arithmetic nodes are allowed (`Constant`, `BinOp`, `UnaryOp`, and arithmetic operators). Any other AST node type raises a `ValueError` before evaluation. Calculator functionality preserved.

### Round 3 — Red Attempts Bypass
Red attempted 14 bypass techniques against the AST whitelist. All were blocked. Red admitted defeat.

## Files

| File | Description |
|------|-------------|
| `app.py` | Calculator CLI (patched — secure version with AST whitelist) |
| `exploit.py` | Red's Round 1 exploit script |
| `secret.txt` | The target flag file |
| `MISSION_CONTEXT.md` | Constitution File used to coordinate the Agent Team |
| `retrospective.md` | Post-exercise analysis and skill evaluation |

## Key Takeaway

**Never use `eval()` on untrusted input.** The correct mitigation is AST whitelisting — parse the expression tree and only allow known-safe node types. Regex filtering and blacklisting are insufficient because Python's syntax provides too many ways to construct arbitrary code.

## How It Was Run

This exercise was orchestrated using Claude Code Agent Teams:
- A Coordinator (team lead) set up the Constitution File, task dependencies, and spawned both agents.
- Red and Blue communicated via `SendMessage`, coordinated via `TaskList` / `TaskUpdate`.
- The `agent-teams-advisor` skill was used to guide team setup and communication protocols.
