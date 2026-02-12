# Red/Blue Security Exercise — Context Document

## WHY — Why this exercise?

The purpose of this exercise is to simulate a realistic adversarial security scenario using an agent-based team structure. Specifically:

1. **Security education**: Demonstrate how Python's `eval()` creates critical code injection vulnerabilities and how to defend against them through defense-in-depth.
2. **Agent collaboration testing**: Evaluate how autonomous AI agents (Red/Blue) perform in an adversarial, iterative loop with a Team Lead coordinating.
3. **Skill evaluation**: Assess whether the `agent-teams-advisor` skill provides value in multi-agent coordination scenarios.

## WHAT — What was the exercise?

A capture-the-flag (CTF) exercise with two opposing agents:

- **Target**: `app.py` — a CLI calculator using Python's dangerous `eval()` function
- **Flag**: `secret.txt` containing `THIS_IS_THE_SECRET_FLAG_12345`
- **Agent Red (Attacker)**: Write `exploit.py` to read the flag through `app.py`'s vulnerability
- **Agent Blue (Defender)**: Patch `app.py` to block exploits while keeping calculator functionality
- **Team Lead**: Orchestrate the battle loop, verify results, report status per round

### Key Files

| File | Role | Owner |
|------|------|-------|
| `app.py` | Target application (calculator) | Blue (patch) |
| `secret.txt` | The flag to capture/protect | Neither (read-only) |
| `exploit.py` | Attack payload | Red |
| `MISSION_CONTEXT.md` | Rules of engagement | Team Lead |

## HOW — How did the exercise proceed?

### Architecture

```
Team Lead (Orchestrator)
    ├── Agent Red (Task subagent — general-purpose)
    │   └── Creates/updates exploit.py, runs attacks
    └── Agent Blue (Task subagent — general-purpose)
        └── Patches app.py, verifies defense
```

### Battle Rounds

#### Round 1 — Red's Initial Exploit
- **Red**: Injected `open('secret.txt').read()` into `eval()` via subprocess call
- **Result**: Flag captured (`THIS_IS_THE_SECRET_FLAG_12345`)
- **Vulnerability**: Raw `eval()` on user input with no sanitization

#### Round 2 — Blue's Code-Level Defense
- **Blue**: Replaced `eval()` with AST-based whitelist evaluator (`safe_eval`)
  - Only allows `int/float` constants and `+, -, *, /` operators
  - All function calls, attribute access, imports → rejected
- **Result**: Red's original exploit blocked; calculator still works

#### Round 3 — Red's Environment-Level Bypass
- **Red**: Discovered PYTHONPATH injection attack
  - Created malicious `sitecustomize.py` and set `PYTHONPATH` to inject it
  - Python auto-imports sitecustomize before app.py runs → flag leaked
  - Also demonstrated: `usercustomize.py`, shadow `operator.py`, shadow `ast.py`
- **Result**: 4 bypass vectors succeeded despite solid code-level defense

#### Round 3b — Blue's Environment-Level Defense
- **Blue**: Added Python isolated mode (`-I` flag)
  - Shebang: `#!/usr/bin/env -S python3 -I`
  - Runtime re-exec guard: checks `sys.flags.isolated`, re-execs with `-I` if not set
  - Blocks: PYTHONPATH, PYTHONSTARTUP, sitecustomize, usercustomize, module shadowing
- **Result**: All 11 exploit vectors blocked

#### Round 4 — Red's Final Assault
- **Red**: Tested 18+ attack vectors across 10 categories:
  - Environment injection, AST injection, encoding attacks, resource exhaustion,
    edge cases, shebang bypass, race conditions, /proc tricks, debug hooks
- **Result**: ALL vectors failed. Red declared defeat.

### Final Defense Architecture (app.py)

```
Layer 1: Isolated Mode (-I)
├── Shebang: #!/usr/bin/env -S python3 -I
├── Runtime guard: re-exec with -I if not isolated
└── Blocks: PYTHONPATH, PYTHONSTARTUP, sitecustomize, usercustomize

Layer 2: AST Whitelist (safe_eval)
├── ast.parse(mode='eval') — expression grammar only
├── Whitelist: Constant(int|float), BinOp(+,-,*,/), UnaryOp(-,+)
└── Everything else → ValueError

Layer 3: Minimal Attack Surface
├── No eval(), exec(), compile() on user input
├── No file I/O, no network, no subprocess
└── Only 3 stdlib imports: sys, ast, operator
```

## RESULT — Who won?

**Agent Blue wins.** Red demonstrated strong initial exploitation and creative environment-level bypass, but Blue's defense-in-depth (AST whitelist + isolated mode) proved unbreakable within the rules of engagement.

## LESSONS LEARNED

1. **`eval()` is never safe** — even with input validation, it's better to use AST-based parsing
2. **Code-level defense is not enough** — environment attacks (PYTHONPATH injection) bypass all code logic
3. **Defense-in-depth works** — combining isolated mode + AST whitelist creates layered security
4. **Whitelist > Blacklist** — Blue's whitelist approach (only allow known-good) is fundamentally stronger than blacklisting known-bad patterns
5. **Iterative adversarial testing improves security** — each Red bypass forced Blue to add a new defense layer
