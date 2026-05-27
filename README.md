# Agent Team

Agent Team is a compatible multi-agent software development plugin. It now provides a Codex-first `team-work` skill while keeping the existing Claude Code and Qwen metadata for users who still rely on those runtimes.

Use it when a request benefits from coordinated specialist reasoning: product scope, architecture, frontend, backend, database, DevOps, QA, security, mobile, and final synthesis.

## What Changed for Codex

- `.codex-plugin/plugin.json` is the Codex plugin manifest.
- `skills/team-work/SKILL.md` is the Codex entry point.
- `skills/team-work/references/` contains routing, dispatch, handoff, and evaluation details loaded only when needed.
- `agents/*.md` remain available as Claude-compatible specialist profiles and reference material.
- `.claude-plugin/plugin.json` and `qwen-extension.json` are preserved for compatibility.

## Repository Layout

```text
.
├── .codex-plugin/plugin.json      # Codex plugin manifest
├── .claude-plugin/plugin.json     # Claude Code compatibility manifest
├── qwen-extension.json            # Qwen compatibility manifest
├── skills/
│   └── team-work/
│       ├── SKILL.md               # Codex-first coordination skill
│       ├── agents/openai.yaml     # Codex skill UI metadata
│       ├── references/            # Routing, dispatch, handoff guidance
│       └── scripts/               # Offline routing eval validator
├── agents/                        # Legacy specialist agent profiles
├── AGENTS.md                      # Contributor guide
└── LICENSE
```

## Usage in Codex

Invoke the skill explicitly for coordinated work:

```text
Use $team-work to plan and implement this full-stack feature.
Use $team-work to coordinate parallel agents for this migration.
Use $team-work to review this multi-domain architecture change.
```

The skill is intentionally selective. It should not expand a simple one-file bug, single SQL query, or ordinary explanation into a full team workflow unless you ask for team mode. Medium tasks use a small coordinated team; complex tasks use phased planning, implementation, verification, and synthesis.

## Coordination Model

The `team-work` skill follows this flow:

1. Classify the request by goal, deliverable, domains, risk, and dependencies.
2. Classify complexity as simple, medium, or complex.
3. Select the smallest effective team using `references/routing-matrix.md`.
4. Build dependency batches before dispatching.
5. Parallelize only independent work with clear ownership boundaries.
6. Synthesize multiple outputs only when there are multiple specialists, conflicts, or final integration decisions.

Parallel work is favored when it does not create integration risk. The dispatch protocol explicitly prevents overlapping edits to the same files, unresolved API/schema conflicts, or implementation before required contracts exist. Routing scenarios in `references/routing-evals.json` keep simple, medium, and complex behavior from drifting.

## Specialist Roles

| Role | Primary Ownership |
| --- | --- |
| `product-manager` | Scope, user stories, acceptance criteria, prioritization |
| `system-architect` | Architecture, service boundaries, technology choices |
| `ui-ux-designer` | User flows, wireframes, usability, design systems |
| `frontend-developer` | Browser UI, components, state, layout, accessibility |
| `backend-developer` | APIs, services, auth services, jobs, integrations |
| `fullstack-developer` | Small end-to-end slices and prototypes |
| `mobile-developer` | iOS, Android, React Native, Flutter, device APIs |
| `database-engineer` | Schema, migrations, queries, indexes, data pipelines |
| `devops-engineer` | CI/CD, containers, cloud, observability, releases |
| `qa-engineer` | Test strategy, automation, quality gates |
| `security-engineer` | Auth, secrets, payment, public APIs, compliance |
| `output-aggregator` | Multi-output synthesis and conflict resolution |

## Development and Validation

There is no build step. Validate changes with:

```bash
python3 /Users/yjydist/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py /path/to/claude-agent-team
python3 /Users/yjydist/.codex/skills/.system/skill-creator/scripts/quick_validate.py /path/to/claude-agent-team/skills/team-work
python3 /path/to/claude-agent-team/skills/team-work/scripts/check-routing-evals.py /path/to/claude-agent-team/skills/team-work/references/routing-evals.json
git diff --check
```

For Claude Code compatibility, load the directory manually:

```bash
claude --plugin-dir /path/to/claude-agent-team
```

## Compatibility Notes

Codex discovers the plugin through `.codex-plugin/plugin.json` and the `team-work` skill. Codex does not automatically treat `agents/*.md` as native subagents; those files are retained for Claude Code compatibility and as source material for the routing references.
