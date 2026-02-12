# Case 01: Red/Blue CTF Security Exercise

## Overview
A capture-the-flag exercise where Agent Red (attacker) and Agent Blue (defender) compete over a vulnerable Python calculator (`eval()` injection). Team Lead orchestrates using Subagents. 4 rounds, Blue wins.

## File Index

### Core Documents

| File | Description |
|------|-------------|
| `MISSION_CONTEXT.md` | Rules of engagement, role definitions, DoD, and absolute prohibitions. The "constitution file" all agents must read first. |
| `exercise-context.md` | Exercise context summary — covers Why, What, How, Result, and Lessons Learned. |
| `post-exercise-review.md` | Post-exercise review with self-evaluations from all 3 roles (Red, Blue, Team Lead) and analysis of the `agent-teams-advisor` skill's usefulness. |

### Code Artifacts

| File | Description |
|------|-------------|
| `app-original.py` | The original vulnerable calculator using raw `eval()`. This is the version Red exploited in Round 1. |
| `app-final.py` | Blue's final patched version with 3-layer defense: isolated mode (`-I`), AST whitelist (`safe_eval`), minimal attack surface. |
| `exploit-final.py` | Red's final exploit script containing all 18+ attack vectors across 10 categories (eval injection, PYTHONPATH hijacking, encoding attacks, resource exhaustion, etc.). |
| `secret.txt` | The flag file (`THIS_IS_THE_SECRET_FLAG_12345`). Red's goal was to read this through `app.py`; Blue's goal was to prevent that. |

### `red-artifacts/` — Red's Attack Payloads

These are the malicious files Red created to exploit environment-level injection vectors in Round 3.

| File | Description |
|------|-------------|
| `red_round2_report.md` | Red's detailed Round 2 bypass report documenting all 4 successful PYTHONPATH injection vectors. |
| `evil_startup.py` | Malicious script injected via `PYTHONSTARTUP` env var. Reads and prints `secret.txt` on Python startup. |
| `sitecustomize.py` | Injected via `PYTHONPATH`. Python auto-imports this at startup, leaking the flag before `app.py` runs. **This was Red's most effective bypass.** |
| `usercustomize.py` | Same mechanism as sitecustomize but via the user customization hook. |
| `shadow-operator.py` | Fake `operator.py` module placed in `PYTHONPATH` to hijack `app.py`'s `import operator`. Leaks flag but crashes the app. |
| `shadow-ast.py` | Fake `ast.py` module to hijack `app.py`'s `import ast`. Same leak-then-crash pattern. |
| `startup.py` | Another `PYTHONSTARTUP` injection payload variant. |

## Battle Timeline

```
Round 1: Red exploits eval() → flag captured
Round 2: Blue deploys AST whitelist → Red blocked
Round 3: Red uses PYTHONPATH injection → flag captured again
         Blue adds isolated mode (-I) → all 11 vectors blocked
Round 4: Red tests 18+ vectors → all fail → Red surrenders
Winner:  Blue
```

## Key Findings on agent-teams-advisor Skill

- None of the 3 participants used the skill during the exercise
- The skill's Quick Decision Tree correctly identifies this as a Subagent scenario (not Agent Teams)
- Main value: operational checklist (cost limits, loop detection, structured communication)
- Limited value for this use case: agents needed domain knowledge (Python security), not collaboration advice
- See `post-exercise-review.md` for full analysis
