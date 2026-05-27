# Repository Guidelines

## Project Structure & Module Organization

This repository is a compatible agent-team plugin with a Codex-first skill. `.codex-plugin/plugin.json` is the Codex manifest. `.claude-plugin/plugin.json` and `qwen-extension.json` are compatibility manifests. The active Codex skill lives in `skills/team-work/`; its `SKILL.md` stays concise while `references/` holds routing, dispatch, and handoff details. Legacy specialist profiles live in `agents/` and should remain valid Markdown with YAML front matter.

## Build, Test, and Development Commands

There is no compile step. Use these checks:

```bash
python3 /Users/yjydist/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .
```

Validates the Codex plugin manifest and skill metadata.

```bash
python3 /Users/yjydist/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/team-work
```

Validates the `team-work` skill front matter.

```bash
python3 skills/team-work/scripts/check-routing-evals.py skills/team-work/references/routing-evals.json
```

Validates complexity-aware routing scenarios and role constraints.

```bash
git diff --check
```

Checks whitespace and patch formatting.

For Claude compatibility, manually run `claude --plugin-dir /path/to/claude-agent-team`.

## Coding Style & Naming Conventions

Use concise Markdown and ASCII text unless an existing file requires otherwise. Skill names and agent names use kebab-case, for example `team-work` and `security-engineer`. Codex skill front matter should contain only `name` and `description`. Claude agent profiles in `agents/` keep their existing `name`, `description`, `model`, `color`, and optional `tools` fields.

## Testing Guidelines

Test prompt behavior manually after routing changes. Cover at least one simple direct task, one medium multi-domain task, and one complex phased task. Check that simple tasks avoid over-dispatch, complex tasks include enough planning and verification, and parallel work has clear ownership boundaries.

## Commit & Pull Request Guidelines

The historical commits are terse `update` entries, but new commits should use descriptive imperative subjects such as `Add Codex plugin manifest` or `Refine team dispatch protocol`. Pull requests should list changed manifests, skills, and references; describe manual validation; and call out any compatibility impact for Claude or Qwen users.

## Security & Configuration Tips

Do not add secrets, local credentials, API keys, or machine-specific paths to prompts, manifests, or examples. Keep `.codex-plugin/`, `.claude-plugin/`, `skills/`, and `agents/` together when distributing the repository so each runtime can discover its expected files.
