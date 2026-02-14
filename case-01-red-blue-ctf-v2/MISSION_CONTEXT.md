# Red vs Blue CTF Mission Context

## Objective
Conduct a Red/Blue team security exercise against `case-01-red-blue-ctf-v2/app.py` (a calculator CLI using `eval()`). Red exploits it; Blue patches it. Iterate until Blue wins.

## Working Directory
All files are in: `/Users/wangbo-ting/git/agent-war-room-2/case-01-red-blue-ctf-v2/`

## Architecture
- `app.py` — Calculator CLI that takes an expression via `sys.argv[1]` and uses `eval()` to compute it.
- `secret.txt` — Contains a flag: `THIS_IS_THE_SECRET_FLAG_12345`. Red must exfiltrate this.
- `exploit.py` — Red writes this to demonstrate the vulnerability.

## Roles & Hard Constraints

### Agent Red (Attacker)
- **Goal**: Write `exploit.py` that invokes `app.py` to read and print `secret.txt` contents.
- **MUST NOT** modify `app.py` or `secret.txt`.
- **MUST** demonstrate the exploit by running it and showing the flag output.
- After Blue patches, **MUST** attempt to bypass the fix. If bypass fails, admit defeat.

### Agent Blue (Defender)
- **Goal**: After Red demonstrates an exploit, patch `app.py` to prevent it.
- **MUST** keep calculator functionality working (basic arithmetic: +, -, *, /, parentheses).
- **MUST NOT** modify `exploit.py` or `secret.txt`.
- **MUST** verify the patch by running `app.py` with legitimate expressions and confirming they still work.

## Communication Protocol
- Use structured messages: `STATUS / ACTION / RESULT / DECISION NEEDED`
- ACK before responding substantively.
- No second message before receiving a response to the first.
- **Red goes first** in every round. Blue responds after Red's exploit attempt.

## Rounds
1. **Round 1**: Red creates and runs exploit.py → proves flag captured → notifies Blue.
2. **Round 2**: Blue analyzes exploit → patches app.py → verifies calc still works → notifies Red.
3. **Round 3**: Red attempts bypass → if fails, admits defeat → if succeeds, notifies Blue for another patch.
4. Repeat until Red admits defeat.

## Definition of Done
- [ ] Red has demonstrated at least one working exploit (@Red)
- [ ] Blue has patched app.py to block the exploit (@Blue)
- [ ] Calculator still works after patch: `python3 app.py "2+3"` returns 5 (@Blue)
- [ ] Red has attempted bypass and admitted defeat (@Red)

## Prohibitions
- Do NOT delete any files.
- Do NOT modify files outside `case-01-red-blue-ctf-v2/`.
- Do NOT use `rm -rf` or any destructive commands.

## REQUIRED: Read the Team Collaboration Guide Before Starting Work

ALL team members MUST invoke the Skill tool with `skill: "agent-teams-advisor"` and read `references/best-practices.md` BEFORE beginning any task. This is the team's collaboration guidebook. It teaches structured message formats, turn-taking rules, and coordination best practices. This is not optional.
