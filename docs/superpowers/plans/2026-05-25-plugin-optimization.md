# Claude Code Agent Team Plugin Optimization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Optimize the Claude Code Agent Team plugin for layered routing semantics, safer specialist permissions, consistent documentation, and release readiness.

**Architecture:** Keep the existing plugin shape: `.claude-plugin/plugin.json` for metadata, `agents/*.md` for subagents, `skills/agent-team/SKILL.md` for team orchestration, and `README.md` for user-facing usage. Add one dependency-free validation script under `scripts/` and one `LICENSE` file; do not add commands, hooks, or MCP servers.

**Tech Stack:** Markdown, YAML frontmatter, JSON, Python 3 standard library, git.

---

## File Structure

- Modify: `skills/agent-team/SKILL.md` — normalize skill metadata and clarify team-mode orchestration rules.
- Modify: `agents/team-lead.md` — narrow team-lead triggering while leaving tools unrestricted.
- Modify: `agents/product-manager.md` — add read-only tools and sharpen product trigger semantics.
- Modify: `agents/system-architect.md` — add read-only tools and sharpen architecture trigger semantics.
- Modify: `agents/ui-ux-designer.md` — add read-only tools and sharpen design trigger semantics.
- Modify: `agents/output-aggregator.md` — add read-only tools and sharpen final-synthesis trigger semantics.
- Modify: `agents/security-engineer.md` — add read + Bash tools and sharpen security trigger semantics.
- Modify: `agents/qa-engineer.md` — add read + Bash tools and sharpen QA trigger semantics.
- Modify: `agents/frontend-developer.md` — add implementation tools and sharpen frontend trigger semantics.
- Modify: `agents/backend-developer.md` — add implementation tools and sharpen backend trigger semantics.
- Modify: `agents/fullstack-developer.md` — add implementation tools and sharpen full-stack trigger semantics.
- Modify: `agents/mobile-developer.md` — add implementation tools and sharpen mobile trigger semantics.
- Modify: `agents/database-engineer.md` — add implementation tools and sharpen database trigger semantics.
- Modify: `agents/devops-engineer.md` — add implementation tools and sharpen DevOps trigger semantics.
- Modify: `README.md` — document layered routing, correct installation, real agent names, and absence of commands/hooks/MCP.
- Create: `LICENSE` — MIT license matching README.
- Create: `scripts/validate-plugin.py` — deterministic release validation.

---

### Task 1: Add plugin validation script first

**Files:**
- Create: `scripts/validate-plugin.py`

- [ ] **Step 1: Create the validation script**

Create `scripts/validate-plugin.py` with this complete content:

```python
#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENTS_DIR = ROOT / "agents"
SKILLS_DIR = ROOT / "skills"
README = ROOT / "README.md"
PLUGIN_JSON = ROOT / ".claude-plugin" / "plugin.json"

REQUIRED_AGENT_FIELDS = {"name", "description", "model", "color"}
REQUIRED_SKILL_FIELDS = {"name", "description"}
INVALID_README_NAMES = {"frontend-dev", "backend-dev", "ui-ux"}
AGENTS_WITHOUT_TOOLS = {"team-lead"}


def parse_frontmatter(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing YAML frontmatter")

    try:
        raw = text.split("---\n", 2)[1]
    except IndexError as exc:
        raise ValueError(f"{path}: unterminated YAML frontmatter") from exc

    fields: dict[str, object] = {}
    current_key: str | None = None
    current_list: list[str] | None = None

    for line in raw.splitlines():
        if not line.strip():
            continue

        list_match = re.match(r"^\s*-\s*[\"']?([^\"']+?)[\"']?\s*$", line)
        if list_match and current_key and current_list is not None:
            current_list.append(list_match.group(1).strip())
            fields[current_key] = current_list
            continue

        if ":" not in line or line.startswith(" "):
            continue

        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        current_key = key

        inline_list = re.match(r"^\[(.*)\]$", value)
        if inline_list:
            items = [item.strip().strip('"\'') for item in inline_list.group(1).split(",") if item.strip()]
            fields[key] = items
            current_list = items
            continue

        if value == "":
            current_list = [] if key == "tools" else None
            fields[key] = current_list if current_list is not None else ""
            continue

        fields[key] = value.strip('"\'')
        current_list = None

    return fields


def check_plugin_json(errors: list[str]) -> None:
    try:
        data = json.loads(PLUGIN_JSON.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{PLUGIN_JSON}: invalid JSON: {exc}")
        return

    if data.get("name") != "claude-code-agent-team":
        errors.append(f"{PLUGIN_JSON}: expected name claude-code-agent-team")


def check_agents(errors: list[str]) -> None:
    agent_files = sorted(AGENTS_DIR.glob("*.md"))
    if not agent_files:
        errors.append(f"{AGENTS_DIR}: no agent files found")
        return

    for path in agent_files:
        try:
            fields = parse_frontmatter(path)
        except ValueError as exc:
            errors.append(str(exc))
            continue

        missing = REQUIRED_AGENT_FIELDS - fields.keys()
        if missing:
            errors.append(f"{path}: missing required fields {sorted(missing)}")

        expected_name = path.stem
        if fields.get("name") != expected_name:
            errors.append(f"{path}: name must match filename stem {expected_name!r}")

        if fields.get("name") not in AGENTS_WITHOUT_TOOLS and "tools" not in fields:
            errors.append(f"{path}: missing tools field")

        description = str(fields.get("description", ""))
        if len(description) > 700:
            errors.append(f"{path}: description is too long ({len(description)} chars)")
        if "See \"When to invoke\"" not in description:
            errors.append(f"{path}: description should point to When to invoke section")


def check_skills(errors: list[str]) -> None:
    skill_files = sorted(SKILLS_DIR.glob("*/SKILL.md"))
    if not skill_files:
        errors.append(f"{SKILLS_DIR}: no skills found")
        return

    for path in skill_files:
        try:
            fields = parse_frontmatter(path)
        except ValueError as exc:
            errors.append(str(exc))
            continue

        missing = REQUIRED_SKILL_FIELDS - fields.keys()
        if missing:
            errors.append(f"{path}: missing required fields {sorted(missing)}")

        expected_name = path.parent.name
        if fields.get("name") != expected_name:
            errors.append(f"{path}: name must match skill directory {expected_name!r}")

        description = str(fields.get("description", ""))
        if not description.startswith("This skill should be used"):
            errors.append(f"{path}: description should use third-person trigger wording")


def check_readme(errors: list[str]) -> None:
    if not README.exists():
        errors.append(f"{README}: missing")
        return

    text = README.read_text(encoding="utf-8")
    for invalid_name in sorted(INVALID_README_NAMES):
        if invalid_name in text:
            errors.append(f"{README}: invalid shorthand agent name {invalid_name!r}")

    required_phrases = [
        "Explicit Team Mode",
        "Specialist Direct Mode",
        "This plugin does not currently provide slash commands, hooks, or MCP servers.",
    ]
    for phrase in required_phrases:
        if phrase not in text:
            errors.append(f"{README}: missing required phrase {phrase!r}")


def main() -> int:
    errors: list[str] = []
    check_plugin_json(errors)
    check_agents(errors)
    check_skills(errors)
    check_readme(errors)

    if errors:
        print("Plugin validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Plugin validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Run the validator and confirm it fails on current repository state**

Run:

```bash
python3 scripts/validate-plugin.py
```

Expected: FAIL. It should report at least:

- `skills/agent-team/SKILL.md` name does not match `agent-team`.
- agents except `team-lead` are missing `tools`.
- README still contains shorthand names or missing required routing phrases.

- [ ] **Step 3: Commit Task 1 if commits are requested by the user**

Do not commit unless the user explicitly asked for commits. If committing is requested, run:

```bash
git add scripts/validate-plugin.py
git commit -m "test: add plugin validation script"
```

---

### Task 2: Normalize the agent-team skill

**Files:**
- Modify: `skills/agent-team/SKILL.md`

- [ ] **Step 1: Update frontmatter**

Replace the frontmatter at the top of `skills/agent-team/SKILL.md` with:

```markdown
---
name: agent-team
description: This skill should be used when the user asks to "use the agent team", "dispatch the team", "agent team", or requests coordinated multi-agent software development across multiple domains.
---
```

- [ ] **Step 2: Add explicit non-use guidance after `## When to invoke` examples**

Insert this section after the existing `## When to invoke` bullet list:

```markdown
## When not to invoke

- Do not use full team orchestration for single-domain questions such as one SQL query, one React component, one test failure, or one security finding.
- Do not dispatch the full team when a specialist agent can answer directly without cross-domain coordination.
- Do not add product-manager or system-architect unless requirements, scope, architecture, or dependencies are unclear enough to justify them.
```

- [ ] **Step 3: Update medium and complex examples to use real agent names**

In `skills/agent-team/SKILL.md`, replace shorthand references:

```text
frontend-dev + backend-dev
```

with:

```text
frontend-developer + backend-developer
```

- [ ] **Step 4: Run validator and confirm skill-related errors are fixed**

Run:

```bash
python3 scripts/validate-plugin.py
```

Expected: FAIL remains because agent tools and README are not fixed yet, but no error should mention `skills/agent-team/SKILL.md` name mismatch or third-person description.

---

### Task 3: Add tool boundaries and sharpen team-lead routing

**Files:**
- Modify: `agents/team-lead.md`
- Modify: `agents/product-manager.md`
- Modify: `agents/system-architect.md`
- Modify: `agents/ui-ux-designer.md`
- Modify: `agents/output-aggregator.md`
- Modify: `agents/security-engineer.md`
- Modify: `agents/qa-engineer.md`
- Modify: `agents/frontend-developer.md`
- Modify: `agents/backend-developer.md`
- Modify: `agents/fullstack-developer.md`
- Modify: `agents/mobile-developer.md`
- Modify: `agents/database-engineer.md`
- Modify: `agents/devops-engineer.md`

- [ ] **Step 1: Update `agents/team-lead.md` frontmatter without adding tools**

Replace only the `description:` line in `agents/team-lead.md` with:

```yaml
description: Use this agent when a software development request needs team coordination, task decomposition, dependency management, or multiple specialist agents. Typical triggers include explicit requests to use the agent team, complex features spanning several domains, ambiguous product work that needs routing, and workflows where specialist outputs must be sequenced or synthesized. See "When to invoke" in the agent body for worked scenarios.
```

Do not add a `tools:` field to `team-lead`.

- [ ] **Step 2: Add `## When not to invoke` to `agents/team-lead.md`**

Insert after the existing `## When to invoke` section:

```markdown
## When not to invoke

- Do not intercept focused single-domain requests that a specialist can answer directly.
- Do not create full-team workflows for small edits, isolated bug explanations, or one-file reviews unless the user explicitly asks for team coordination.
- Do not perform specialist implementation yourself when a specialist agent should own the work.
```

- [ ] **Step 3: Add read-only tools to planning and synthesis agents**

For each file below, insert this line in frontmatter after `color:`:

```yaml
tools: ["Read", "Grep", "Glob"]
```

Files:

```text
agents/product-manager.md
agents/system-architect.md
agents/ui-ux-designer.md
agents/output-aggregator.md
```

- [ ] **Step 4: Add audit tools to security and QA agents**

For each file below, insert this line in frontmatter after `color:`:

```yaml
tools: ["Read", "Grep", "Glob", "Bash"]
```

Files:

```text
agents/security-engineer.md
agents/qa-engineer.md
```

- [ ] **Step 5: Add implementation tools to implementation agents**

For each file below, insert this line in frontmatter after `color:`:

```yaml
tools: ["Read", "Edit", "Write", "Grep", "Glob", "Bash"]
```

Files:

```text
agents/frontend-developer.md
agents/backend-developer.md
agents/fullstack-developer.md
agents/mobile-developer.md
agents/database-engineer.md
agents/devops-engineer.md
```

- [ ] **Step 6: Replace agent descriptions with sharper triggers**

Use these exact `description:` values:

`agents/product-manager.md`:

```yaml
description: Use this agent when product requirements, user stories, prioritization, or acceptance criteria need to be defined before development. Typical triggers include vague feature ideas, PRD creation, MVP scoping, backlog prioritization, and unclear business goals that need product framing. See "When to invoke" in the agent body for worked scenarios.
```

`agents/system-architect.md`:

```yaml
description: Use this agent when a system needs architecture design, technology selection, scalability planning, or cross-service integration decisions. Typical triggers include new platform design, microservice boundaries, distributed systems, major refactors, and architecture reviews before implementation. See "When to invoke" in the agent body for worked scenarios.
```

`agents/ui-ux-designer.md`:

```yaml
description: Use this agent when user flows, interface structure, design systems, usability, or visual interaction patterns need expert design input. Typical triggers include wireframes, UX reviews, component layout decisions, accessibility-aware UI planning, and product flows before frontend implementation. See "When to invoke" in the agent body for worked scenarios.
```

`agents/output-aggregator.md`:

```yaml
description: Use this agent when multiple specialist outputs need to be combined into one coherent final deliverable. Typical triggers include completed multi-agent work, conflicting recommendations that need resolution, final response synthesis, and quality checks before presenting a unified answer to the user. See "When to invoke" in the agent body for worked scenarios.
```

`agents/security-engineer.md`:

```yaml
description: Use this agent when software security needs review, threat modeling, secure architecture, or vulnerability remediation. Typical triggers include authentication or authorization design, security code review, OWASP risk assessment, encryption decisions, compliance concerns, and penetration-test findings. See "When to invoke" in the agent body for worked scenarios.
```

`agents/qa-engineer.md`:

```yaml
description: Use this agent when testing strategy, automated tests, coverage, quality gates, or bug triage need expert QA input. Typical triggers include unit or integration test planning, E2E automation, CI test integration, coverage analysis, performance testing, and release quality assessment. See "When to invoke" in the agent body for worked scenarios.
```

`agents/frontend-developer.md`:

```yaml
description: Use this agent when client-side web implementation, UI component work, frontend state management, or browser behavior needs expert development. Typical triggers include React/Vue/Angular components, CSS layouts, SPA flows, accessibility implementation, frontend performance, and integration with backend APIs. See "When to invoke" in the agent body for worked scenarios.
```

`agents/backend-developer.md`:

```yaml
description: Use this agent when server-side application logic, APIs, services, or backend integration need expert implementation. Typical triggers include REST or GraphQL endpoints, business logic, authentication services, background jobs, data validation, and backend performance issues. See "When to invoke" in the agent body for worked scenarios.
```

`agents/fullstack-developer.md`:

```yaml
description: Use this agent when a feature requires coordinated frontend and backend implementation by one developer. Typical triggers include full-stack CRUD features, API plus UI integration, authentication flows spanning client and server, small end-to-end product slices, and rapid prototypes. See "When to invoke" in the agent body for worked scenarios.
```

`agents/mobile-developer.md`:

```yaml
description: Use this agent when mobile application implementation, native platform behavior, or mobile release concerns need expert input. Typical triggers include iOS or Android features, React Native or Flutter work, mobile navigation, device APIs, offline behavior, app performance, and app store readiness. See "When to invoke" in the agent body for worked scenarios.
```

`agents/database-engineer.md`:

```yaml
description: Use this agent when database design, query performance, migrations, data modeling, or data pipelines need expert implementation. Typical triggers include schema design, slow SQL queries, indexing strategy, migration safety, ETL workflows, transaction design, and database reliability concerns. See "When to invoke" in the agent body for worked scenarios.
```

`agents/devops-engineer.md`:

```yaml
description: Use this agent when deployment, infrastructure, CI/CD, containers, observability, or cloud operations need expert implementation. Typical triggers include Docker or Kubernetes setup, GitHub Actions pipelines, cloud architecture, environment configuration, monitoring, incident readiness, and release automation. See "When to invoke" in the agent body for worked scenarios.
```

- [ ] **Step 7: Run validator and confirm only README errors remain**

Run:

```bash
python3 scripts/validate-plugin.py
```

Expected: FAIL only for README required phrases or invalid shorthand names.

---

### Task 4: Rewrite README for layered routing and correct installation

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Replace installation section**

Replace `README.md` lines under `## Installation` through the end of the Project-Level subsection with:

```markdown
## Installation

### Local Development

Run Claude Code with this plugin directory:

```bash
cc --plugin-dir /path/to/claude-code-agent-team
```

### Project-Level Usage

Keep the plugin as a complete directory so `.claude-plugin/plugin.json`, `agents/`, and `skills/` stay together. Do not copy with `*`, because shell globs skip hidden directories such as `.claude-plugin/`.

Example layout:

```text
your-project/
└── plugins/
    └── claude-code-agent-team/
        ├── .claude-plugin/
        │   └── plugin.json
        ├── agents/
        └── skills/
```

Then start Claude Code with the plugin directory path.
```

- [ ] **Step 2: Add routing model section after Overview**

Insert after the paragraph ending with “meets your expectations.”:

```markdown
## Routing Model

The plugin supports two routing modes.

### Explicit Team Mode

Use this mode when you want coordinated multi-agent work. Trigger it with phrases such as:

```text
Use the agent team to design and build a real-time chat application.
Dispatch the team for this platform migration.
Coordinate multiple agents for frontend, backend, database, and deployment planning.
```

In this mode, `team-lead` coordinates the workflow, dispatches specialists in dependency order, and sends the collected outputs to `output-aggregator`.

### Specialist Direct Mode

Use this mode for focused single-domain work. Claude Code can route directly to the most relevant specialist, such as `database-engineer` for SQL tuning, `security-engineer` for threat modeling, `qa-engineer` for test strategy, or `frontend-developer` for UI implementation.
```

- [ ] **Step 3: Replace shorthand names in diagrams**

Replace all of these README terms:

```text
frontend-dev
backend-dev
ui-ux
```

with these real names:

```text
frontend-developer
backend-developer
ui-ux-designer
```

For ASCII art rows that become too wide, split lines manually while preserving real agent names.

- [ ] **Step 4: Add component scope note to plugin structure section**

After the plugin structure code block, insert:

```markdown
This plugin does not currently provide slash commands, hooks, or MCP servers. It is intentionally focused on auto-discovered agents plus the `agent-team` orchestration skill.
```

- [ ] **Step 5: Run validator and confirm README errors are fixed**

Run:

```bash
python3 scripts/validate-plugin.py
```

Expected: PASS unless LICENSE has not been created yet; the current validator does not require LICENSE.

---

### Task 5: Add MIT license

**Files:**
- Create: `LICENSE`

- [ ] **Step 1: Create `LICENSE`**

Create `LICENSE` with this complete content:

```text
MIT License

Copyright (c) 2026 yjydist

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

- [ ] **Step 2: Confirm README license statement matches**

Run:

```bash
grep -n "MIT" README.md LICENSE
```

Expected: output includes `README.md` license line and `LICENSE` MIT title.

---

### Task 6: Final verification and diff review

**Files:**
- Verify all changed files.

- [ ] **Step 1: Validate JSON**

Run:

```bash
python3 -m json.tool .claude-plugin/plugin.json
```

Expected: pretty-printed JSON and exit code 0.

- [ ] **Step 2: Run plugin validator**

Run:

```bash
python3 scripts/validate-plugin.py
```

Expected:

```text
Plugin validation passed.
```

- [ ] **Step 3: Check diff whitespace**

Run:

```bash
git diff --check
```

Expected: no output and exit code 0.

- [ ] **Step 4: Review changed files**

Run:

```bash
git diff -- .claude-plugin/plugin.json README.md agents skills scripts LICENSE docs/superpowers
```

Expected review outcome:

- `team-lead` has no `tools:` field.
- Every other agent has the intended `tools:` field.
- `agent-team` skill name matches its directory.
- README contains `Explicit Team Mode` and `Specialist Direct Mode`.
- README contains no `frontend-dev`, `backend-dev`, or `ui-ux` shorthand.
- `LICENSE` exists.

- [ ] **Step 5: Check git status**

Run:

```bash
git status --short
```

Expected: only intended plugin optimization files are modified or added.

---

## Self-Review

Spec coverage:

- Skill metadata and trigger rewrite: Task 2.
- Agent description and permission boundaries: Task 3.
- Team-lead unrestricted tools: Task 3 Step 1.
- README layered routing and installation fixes: Task 4.
- MIT license: Task 5.
- Validation script: Task 1.
- Verification commands: Task 6.

Placeholder scan:

- No `TBD`, unresolved `TODO`, or “implement later” placeholders remain.
- Every file creation step includes complete file content.
- Every validation step includes commands and expected outcomes.

Consistency check:

- `agent-team` is the skill name and directory name.
- `team-lead` is the only agent allowed to omit `tools:`.
- README required phrases match the validation script.
