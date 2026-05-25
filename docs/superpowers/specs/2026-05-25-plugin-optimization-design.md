# Claude Code Agent Team Plugin Optimization Design

## Summary

Optimize the `claude-code-agent-team` plugin for clearer routing semantics, safer agent permissions, consistent documentation, and release readiness. The plugin will keep its current product identity as a virtual software development team, but its dispatch model will become layered instead of forcing every software task through the team lead.

## Goals

- Clarify when to use full team orchestration versus direct specialist agents.
- Reduce over-triggering from broad agent descriptions.
- Add least-privilege tool boundaries for specialist agents.
- Fix plugin metadata and documentation inconsistencies.
- Add lightweight validation for publish-time confidence.

## Non-Goals

- Add slash commands.
- Add hooks.
- Add MCP servers.
- Change the number of specialist agents.
- Implement actual application features outside the plugin metadata and documentation.

## Current State

The repository currently contains:

- `.claude-plugin/plugin.json`
- `README.md`
- `.gitignore`
- 13 agent files under `agents/`
- 1 skill under `skills/agent-team/SKILL.md`

There are no `commands/`, `hooks/`, or `.mcp.json` components. That is acceptable for this plugin, but the README should make this explicit.

## Routing Model

Adopt a two-layer routing model.

### Explicit Team Mode

Use the `agent-team` skill and `team-lead` agent when the user explicitly asks for team coordination or requests work spanning multiple domains.

Trigger examples:

- “Use the agent team to build a real-time chat app.”
- “Dispatch the team for this project.”
- “I need frontend, backend, database, and deployment planning.”
- “Coordinate multiple agents to design and implement this feature.”

### Specialist Direct Mode

Allow specialist agents to trigger directly for single-domain requests.

Examples:

- SQL tuning routes to `database-engineer`.
- Auth threat modeling routes to `security-engineer`.
- Test strategy routes to `qa-engineer`.
- React component implementation routes to `frontend-developer`.
- API design routes to `backend-developer`.

## Skill Changes

Update `skills/agent-team/SKILL.md`.

Required changes:

- Change frontmatter `name` from `Agent Team Orchestration` to `agent-team`.
- Rewrite `description` in third person with concrete trigger phrases.
- Add explicit “When not to use” guidance for single-domain tasks.
- Keep the core dispatch workflow but reduce repeated examples.
- Preserve the team roster and dependency rules.

Proposed description:

```yaml
description: This skill should be used when the user asks to "use the agent team", "dispatch the team", "agent team", or requests coordinated multi-agent software development across multiple domains.
```

## Agent Changes

Update all files in `agents/*.md`.

### Description Strategy

Each agent frontmatter description should:

- Start with “Use this agent when...”
- Include 2-4 concrete trigger scenarios.
- Point to the body’s “When to invoke” section.
- Be shorter and more specific than the current descriptions.

Each agent body should add a short `## When not to use` section where helpful, especially for agents with broad domains.

### Team Lead

`team-lead` remains unrestricted by `tools:` to preserve maximum orchestration ability.

Its description should be narrowed from “all software development requests” to:

- explicit team requests,
- multi-domain work,
- dependency coordination,
- ambiguous requests that likely require multiple specialists.

### Specialist Agents

Specialists should be directly discoverable for focused work in their domains. Their descriptions should avoid implying that the team lead must always dispatch them first.

## Tool Permission Boundaries

Add `tools:` frontmatter to all agents except `team-lead`.

### Read-only planning and synthesis agents

Agents:

- `product-manager`
- `system-architect`
- `ui-ux-designer`
- `output-aggregator`

Tools:

```yaml
tools: ["Read", "Grep", "Glob"]
```

### Audit and validation agents

Agents:

- `security-engineer`
- `qa-engineer`

Tools:

```yaml
tools: ["Read", "Grep", "Glob", "Bash"]
```

### Implementation agents

Agents:

- `frontend-developer`
- `backend-developer`
- `fullstack-developer`
- `mobile-developer`
- `database-engineer`
- `devops-engineer`

Tools:

```yaml
tools: ["Read", "Edit", "Write", "Grep", "Glob", "Bash"]
```

## README Changes

Update `README.md` to:

- Explain explicit team mode and specialist direct mode.
- Fix installation instructions so hidden `.claude-plugin/plugin.json` is not skipped.
- Avoid instructing users to copy plugin contents into a nested `.claude-plugin/` directory incorrectly.
- Replace shorthand names such as `frontend-dev`, `backend-dev`, and `ui-ux` with real agent names.
- State that the plugin currently provides agents and one skill only; no commands, hooks, or MCP servers are included.
- Keep the plugin structure diagram aligned with actual files.

## Manifest and License Changes

Keep `.claude-plugin/plugin.json` mostly unchanged.

Add a `LICENSE` file with the MIT license because the README already declares MIT licensing.

Do not remove `keywords` unless validation shows it breaks plugin loading. It is useful metadata and should be harmless unless a strict marketplace validator rejects unknown fields.

## Validation Script

Add `scripts/validate-plugin.py` as a local release-check helper.

The script should verify:

- `.claude-plugin/plugin.json` is valid JSON.
- All `agents/*.md` files have required frontmatter fields: `name`, `description`, `model`, `color`.
- Agent file names match frontmatter `name`.
- All agents except `team-lead` have `tools:`.
- All `skills/*/SKILL.md` files have frontmatter `name` and `description`.
- Skill directory names match frontmatter `name`.
- README does not reference known invalid shorthand agent names.

The script should be deterministic, dependency-free, and runnable with Python 3.

## Verification Plan

Run these checks after implementation:

```bash
python3 -m json.tool .claude-plugin/plugin.json
python3 scripts/validate-plugin.py
git diff --check
git status --short
```

Review the final diff manually for:

- trigger description clarity,
- permission boundary correctness,
- README consistency,
- accidental scope creep.

## Risks and Mitigations

### Risk: Team lead triggers less often than before

Mitigation: Keep explicit team phrases strong in both the skill and `team-lead` description.

### Risk: Specialist agents trigger too often

Mitigation: Add “When not to use” sections and keep descriptions domain-specific.

### Risk: Tool restrictions block useful specialist behavior

Mitigation: Implementation agents retain write-capable tools. Planning and synthesis agents are intentionally read-only. `team-lead` remains unrestricted.

### Risk: README suggests unsupported plugin features

Mitigation: Explicitly document that commands, hooks, and MCP servers are not part of this plugin.

## Implementation Scope

Files expected to change:

- `.claude-plugin/plugin.json` only if metadata cleanup is needed.
- `README.md`
- `skills/agent-team/SKILL.md`
- all `agents/*.md`
- new `LICENSE`
- new `scripts/validate-plugin.py`

No other files should be changed unless validation reveals a directly related issue.
