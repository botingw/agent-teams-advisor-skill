# Agent Teams Advisor Skill

A [Claude Code Skill](https://docs.anthropic.com/en/docs/claude-code/skills) that helps you evaluate, configure, and operate **Claude Code Agent Teams** effectively.

When you ask questions like *"Is this task suitable for Agent Teams?"* or *"How should I set up my team?"*, this skill provides structured guidance — including task assessment, team composition, communication protocols, cost control, and stop-loss strategies.

## Repository Structure

```
.
├── agent-teams-advisor/          # The skill itself (installable)
│   ├── SKILL.md                  # Core skill definition and workflow
│   └── references/               # Reference documents loaded by the skill
│       ├── intro.md              # Agent Teams architecture & Subagents comparison
│       ├── best-practices.md     # Operational handbook (roles, comms, stop-loss)
│       ├── best-scenarios.md     # Best-fit scenarios, anti-patterns, cost data
│       └── skill-propagation-templates.md  # Constitution & spawn prompt templates
├── agent-teams-advisor.skill     # Pre-packaged skill archive
├── docs/                         # Raw research sources (upstream of the skill)
├── case-01-red-blue-ctf/         # Demo: Red/Blue CTF security exercise
├── case-01-red-blue-ctf-v2/      # Demo: Red/Blue CTF v2
├── case-02-final-api-spec-discussion/    # Demo: API spec discussion
├── case-02-final-api-spec-discussion-v2/ # Demo: API spec discussion v2
├── case-02-final-api-spec-discussion-v3/ # Demo: API spec discussion v3
└── case-03-dice-roller/          # Demo: Dice roller
```

## Installation

### Option 1: Install from the `.skill` file (Recommended)

Use the Claude Code `/install-skill` slash command and point it to the `.skill` file:

```
/install-skill /path/to/agent-teams-advisor.skill
```

Or if you cloned this repo:

```
/install-skill ./agent-teams-advisor.skill
```

### Option 2: Copy the skill folder manually

1. Create the skills directory if it doesn't exist:

```bash
mkdir -p ~/.claude/skills
```

2. Copy the entire `agent-teams-advisor/` folder into it:

```bash
cp -r agent-teams-advisor ~/.claude/skills/agent-teams-advisor
```

3. Restart Claude Code. The skill will be auto-detected from `SKILL.md`.

### Option 3: Project-level installation

If you only want the skill available in a specific project, copy it into that project's `.claude/skills/` directory:

```bash
mkdir -p /path/to/your-project/.claude/skills
cp -r agent-teams-advisor /path/to/your-project/.claude/skills/agent-teams-advisor
```

## Usage

Once installed, the skill triggers automatically when you ask Claude Code about Agent Teams. Examples:

- *"Is this task suitable for Agent Teams?"*
- *"How should I configure a team for a full-stack feature?"*
- *"Should I use Agent Teams or Subagents for this?"*
- *"What are the best practices for running Agent Teams?"*
- *"How do I control costs with Agent Teams?"*

You can also invoke it explicitly:

```
/agent-teams-advisor
```

## What the Skill Does

1. **Assesses your task** — decides between single agent, subagents, or agent teams using a structured decision tree
2. **Recommends team composition** — suggests proven configurations (TDD pair, full-stack trio, debug squad, red/blue team, etc.)
3. **Provides operational guidance** — constitution file structure, Definition of Done, communication protocols, monitoring, and stop-loss rules
4. **Enforces skill propagation** — ensures every teammate reads the collaboration guidelines before starting work (this is mandatory because each agent has an independent context window)

## Demo Cases

This repo includes several real-world demo cases that were used to test and refine the skill:

| Case | Description |
|------|-------------|
| `case-01-red-blue-ctf` | Red/Blue CTF security exercise — attacker vs defender over a vulnerable Python app |
| `case-02-final-api-spec-discussion` | Multi-agent API specification review and discussion |
| `case-03-dice-roller` | Collaborative dice roller implementation |

## Contributing

1. Capture new insights in `docs/` first (preserve raw context)
2. Distill them into actionable guidance in `agent-teams-advisor/references/`
3. Update `agent-teams-advisor/SKILL.md` trigger logic and workflow as needed
4. Test with real cases before finalizing changes
