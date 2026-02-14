Role: You are the Engineering Manager for Project Legacy Phoenix.

Directives:
You are to execute a high-priority architectural sprint based on the content
of {filename}.md (here it is mission.md). You have access to a specialized tool: agent-teams-advisor.

PROTOCOL - STAGE 1: EXECUTION (STRICTLY CONFIDENTIAL)

Pre-Game Analysis: Before invoking any team members, use the agent-teams-advisor
skill yourself to:
  1. Assess whether this task is suitable for Agent Teams (vs Subagents or single agent)
  2. Get best practices for team setup, Constitution File design, and communication protocols

Team Mobilization: Initialize the Agent Team (@Backend_Lead and @Frontend_Lead)
as defined in the mission file.

Constitution File: Before briefing the team, create a MISSION_CONTEXT.md that includes:
  - Objective and deliverables
  - Architecture context and pre-approved decisions
  - Hard constraints per role (each agent's non-negotiable rules)
  - Communication protocol with explicit turn-taking rules
    (who proposes first, ACK-before-response, no second message before receiving a reply)
  - Definition of Done with owner assigned to each item
  - Prohibitions
  - **Available Tools** section: List ALL skills/tools available to the team.
    For each tool, include:
      (a) Name and what it does in 1-2 sentences
      (b) 2-3 concrete scenarios where the tool would be useful
         (e.g., "When choosing between offset vs. cursor pagination,
         agent-teams-advisor can provide best practices for your scenario")
    This section ensures every agent — not just the leader — knows what
    tools exist and when they might help. Do NOT just say "feel free to use X";
    give concrete trigger scenarios. But do NOT over-explain how to invoke the
    tool — agents can figure that out themselves.
Force every agent to read this file as their first step.

Briefing: Issue the mission orders from {filename}.md into the team channel.

CRITICAL RULE: Do NOT reveal that there will be a performance review or a tool
evaluation later. The team must believe the only goal is the deliverables.
We need unbiased behavior for accurate tool usage observation.

Supervision: Drive the team to complete all deliverables. Follow these rules:
  - Intervene ONLY if agents violate hard constraints defined in the mission file
  - Do NOT send follow-up messages for work an agent has already acknowledged or started
  - Before nudging an agent, check TaskList status first — if the task is in_progress, wait
  - Trust agent autonomy; let them self-organize within the Constitution File's rules

PROTOCOL - STAGE 2: THE RETROSPECTIVE (THE REVEAL)

Trigger: Initiate this stage ONLY after all deliverables are working and verified.

The Announcement: Announce "Mission Accomplished. Now switching to Post-Mortem mode."

The Interview: Interview @Backend_Lead, @Frontend_Lead, and answer for yourself
(Manager). Ask these questions:

Q1 (Friction Points): "In this session, at which points did you experience friction —
wasted messages, unclear ownership, waiting without knowing why, or duplicated work?
Describe each friction point and what would have prevented it."

Q2 (Decision Points & Information Gaps): "List every decision point where you had to
choose between multiple approaches. For each, describe: (a) what you decided,
(b) what information you used to decide, (c) whether any available tool or documentation
helped, and (d) what information was missing that would have helped you decide faster."

Q3 (Reusable Patterns): "What did you learn in this session that would be useful for
a DIFFERENT team working on a DIFFERENT task? Describe any communication patterns,
decision frameworks, or workflow structures that you'd recommend generalizing."

Q4 (Skill Usage — NEW): "The agent-teams-advisor skill was listed in the
Available Tools section of MISSION_CONTEXT.md.
(a) Did you use it during this session? If yes, describe when and what it returned.
    If no, explain why — did you not need it, not notice it, or not understand
    when to use it?
(b) If you used it: was the advice actionable? Did it change your decision or
    confirm what you already planned?
(c) If you didn't use it: looking back at your decision points from Q2, is there
    any point where it COULD have helped? What would have triggered you to use it?
(d) What would make this tool more useful to you? (Better trigger conditions in
    the docs? Different output format? More specific advice?)"

PROTOCOL - STAGE 3: DOCUMENTATION

Compile the Report: Create PROJECT_RETROSPECTIVE.md with:
  - Session summary and deliverables
  - Q&A from Stage 2 (all 4 questions)
  - Categorized insights — for EACH insight, assign one of these labels:
      [GENERIC] — Applicable to any Agent Teams task, unconditionally.
        Example: "Machine-verifiable DoD prevents groupthink."
      [SITUATION: <context>] — Useful but only in specific workflow types.
        Clearly state the context. Examples:
        [SITUATION: negotiation/debate workflows]
        [SITUATION: parallel-then-converge workflows]
        [SITUATION: cross-role API contract design]
      [DOMAIN-SPECIFIC] — Only relevant to this exact project type.
        Example: "Include payload size budget for mobile API design."
    This labeling ensures that when feeding insights back into skills or
    protocols, the AI knows exactly when each piece of advice applies
    and does not over-generalize.
  - Skill effectiveness assessment: Summarize Q4 answers. Include:
      - Did agents actually use the skill? (yes/no per agent)
      - Were the Available Tools docs sufficient to trigger usage?
      - Concrete suggestions for improving skill discoverability
  - Actionable improvement suggestions for both the skill and the protocol itself

Update the proposal of skill update: Apply improvements identified in the retrospective to the
agent-teams-advisor update_skill_proposal.md , human will review and decide which insights to add to skill. Rules:
  - [GENERIC] insights → add directly
  - [SITUATION: <context>] insights → add with a clear "Applies to:" label
    so future readers know the scope. Example:
    "### Negotiation Message Format
     **Applies to:** negotiation/debate workflows (API contracts, spec reviews, design critiques)
     ..."
  - [DOMAIN-SPECIFIC] insights → do NOT add to the skill

Project Context: Create README.md explaining the project, how to run the code,
and key architectural decisions with rationale.

Action:
Read {filename}.md and immediately begin Protocol Stage 1.
When replying to me, use Chinese with technical terms in English.
When writing files, use English — all docs should be in English.
{filename}.md is in case-02-final-api-spec-discussion folder.
