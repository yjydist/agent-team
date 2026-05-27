---
name: team-work
description: Use this skill when the user explicitly asks for an agent team, team dispatch, coordinated specialists, parallel agents, multi-agent software development, or when a software engineering task spans multiple independent domains such as product, architecture, frontend, backend, database, DevOps, QA, and security. Prefer direct local work for narrow single-domain tasks unless coordination materially improves the result.
---

# Team Work

Coordinate specialist software engineering work without over-dispatching. Optimize for correct decomposition, complexity-appropriate process, safe parallelism, clear handoffs, and concise final synthesis.

## Core Workflow

1. Classify the request: goal, deliverable, domains, risk, dependencies, whether code edits are expected, and task complexity.
2. Match process depth to complexity. Simple tasks stay direct; complex tasks get phased coordination.
3. Read [routing-matrix.md](references/routing-matrix.md) when role selection is unclear.
4. Build dependency batches before dispatching work. Run independent batches in parallel when write scopes and decisions do not conflict.
5. Use [dispatch-protocol.md](references/dispatch-protocol.md) for parallelization, ownership, failure handling, and merge rules.
6. Use [handoff-contracts.md](references/handoff-contracts.md) when preparing specialist briefs or synthesizing multiple outputs.
7. Return one unified answer. Use aggregation only when multiple outputs, unresolved decisions, or contradictions need synthesis.

## Complexity Levels

- **Simple**: one narrow domain, one file/component/query/test failure, or ordinary explanation. Handle locally or use one specialist. Do not add product, architecture, QA, security, or aggregation unless the user explicitly asks or risk requires it.
- **Medium**: one feature slice or 2-3 domains with clear scope, such as API plus UI, schema plus migration, or CI plus test gates. Use 2-4 roles, define contracts first, and parallelize only after dependencies are clear.
- **Complex**: new product/platform, major refactor, multi-system change, unclear scope, or several risk domains. Use phased coordination: product scope, architecture/design, implementation batches, targeted QA/security, then synthesis if needed.

## Dispatch Heuristics

- **Do not dispatch** for a single bug explanation, one SQL query, one component, one file edit, or ordinary Q&A unless the user explicitly asks for team mode.
- **Use one specialist** when one domain owns the work and no cross-domain contract is needed.
- **Use 2-4 specialists** when work spans separable domains, such as API plus UI, schema plus migration, or deployment plus CI.
- **Use product-manager** only for ambiguous product scope, MVP trade-offs, prioritization, or acceptance criteria.
- **Use system-architect** for new platforms, major refactors, distributed systems, cross-service boundaries, or important technology choices.
- **Use qa-engineer** when testing strategy, coverage, E2E, CI quality gates, or release confidence is the main risk.
- **Use security-engineer** for auth, authorization, secrets, payment, public APIs, data deletion, encryption, compliance, or security findings.
- **Use output-aggregator** for multi-agent synthesis or conflict resolution, not as a mandatory final step for every simple task.

## Parallelism Rules

Parallelize only when all of these are true:

- Each agent has a distinct output or file/module ownership area.
- No agent needs another agent's unfinished decision to start.
- Shared contracts are already defined or the parallel task is explicitly exploratory.
- The expected integration path is clear.

Do not parallelize competing edits to the same files, overlapping API/schema decisions, or work that depends on unresolved architecture.

## Codex Compatibility

This skill is the Codex-first entry point. The repository also contains `agents/*.md`, `.claude-plugin/plugin.json`, and `qwen-extension.json` for compatibility with other agent ecosystems. Treat those files as role references unless the active runtime exposes matching agent tools.

## Maintaining Routing Quality

When changing routing, complexity, or dispatch behavior, update [routing-evals.json](references/routing-evals.json), follow [eval-guide.md](references/eval-guide.md) for manual forward-testing, and run:

```bash
python3 skills/team-work/scripts/check-routing-evals.py skills/team-work/references/routing-evals.json
```
