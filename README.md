# Claude Code Agent Team

A multi-agent software development team plugin for Claude Code that simulates real-world team workflows.

## Overview

This plugin creates a virtual software development team inside Claude Code. You act as the **client (甲方)**, and the plugin orchestrates a team of specialist agents to deliver complete solutions.

```
You (Client)
    |
    v
[team-lead] -- listens, clarifies, decides team composition
    |
    v
[product-manager] -- requirements & PRD (when needed)
    |
    v
[system-architect] + [ui-ux-designer] -- architecture & design
    |
    v
[frontend-developer] + [backend-developer] + [database-engineer] + [devops-engineer]
    |-- implementation (parallel, based on dependencies)
    |
    v
[qa-engineer] + [security-engineer] -- quality gates
    |
    v
[output-aggregator] -- synthesizes final deliverable
    |
    v
Complete solution delivered to you
```

The **team-lead** agent is your single point of contact. It understands your request, asks clarifying questions if needed, determines which specialists are required, coordinates their execution (parallel or sequential), and ensures the final output meets your expectations.

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

## Prerequisites

- [Claude Code](https://claude.ai/code) CLI installed
- Claude Code version that supports plugins

## Installation

### Local Development

Run Claude Code with this plugin directory:

```bash
claude --plugin-dir /path/to/claude-code-agent-team
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

## The Team

| Agent | Role | When Dispatched |
|-------|------|-----------------|
| **team-lead** | Client liaison & team coordinator | **Always first** -- your single point of contact |
| **product-manager** | Requirements analyst & PRD author | New features, unclear requirements, product scoping |
| **system-architect** | Architecture design & tech decisions | Complex systems, new platforms, scaling concerns |
| **ui-ux-designer** | Interface design & user experience | UI mockups, design systems, usability review |
| **frontend-developer** | Client-side implementation | React/Vue/Angular components, SPAs, PWA |
| **backend-developer** | Server-side implementation | APIs, business logic, microservices |
| **fullstack-developer** | End-to-end implementation | Full-stack apps, frontend+backend integration |
| **mobile-developer** | Mobile application development | iOS/Android, React Native, Flutter |
| **database-engineer** | Data design & optimization | Schemas, migrations, query tuning, ETL |
| **security-engineer** | Security audit & hardening | Code review, auth design, vulnerability assessment |
| **qa-engineer** | Testing strategy & automation | Test plans, coverage, CI integration |
| **devops-engineer** | CI/CD & infrastructure | Deployment pipelines, Docker, K8s, cloud |
| **output-aggregator** | Result synthesis & final output | **Always last** -- compiles all deliverables |

## Usage

Simply describe your software development need in natural language. The **team-lead** agent will analyze your request, determine the appropriate team composition, and coordinate the workflow automatically.

### How It Works

1. **You describe the need** -- "Build a blogging platform with user auth and comments"
2. **team-lead assesses** -- decides complexity, asks clarifying questions if needed
3. **team-lead assembles the team** -- dispatches the right specialists in the right order
4. **Agents work** -- parallel or sequential, passing outputs forward
5. **output-aggregator synthesizes** -- compiles all outputs into a coherent deliverable
6. **team-lead presents** -- delivers the final result to you

## Workflows

The team-lead automatically determines task complexity and selects the appropriate workflow.

### Simple Task Workflow (1-2 agents)

For single-domain questions with clear scope. No PRD or architecture needed.

**Example:** "How do I optimize this SQL query?"

```
You
 |
 v
team-lead -- analyzes: single-domain, straightforward
 |
 v
database-engineer -- query analysis & optimization
 |
 v
output-aggregator -- presents optimized query with explanation
 |
 v
You -- receive answer
```

**When triggered:** Pure questions, single-file changes, query optimization, error explanation, code review of one component.

**Team size:** 1 specialist + output-aggregator.

---

### Medium Task Workflow (3-5 agents)

For features spanning 2-3 domains with clear requirements. No dedicated PRD phase.

**Example:** "Build a login page with JWT authentication"

```
You
 |
 v
team-lead -- analyzes: multi-domain feature, requirements are clear
 |
 +----------------+-----------------+------------------+
 v                v                 v
ui-ux-designer  backend-developer  frontend-developer
 |                |                 |
 login            JWT               React
 design           API               component
 |                |                 |
 +----------------+-----------------+
 |
 v
security-engineer -- audits auth flow
 |
 v
output-aggregator -- compiles implementation guide
 |
 v
You -- receive deliverable
```

**When triggered:** Feature implementations, API + frontend integration, component libraries, deployment setup.

**Team size:** 3-4 specialists + security/QA (if production) + output-aggregator.

---

### Complex Task Workflow (6-12 agents)

For new products or platforms requiring full SDLC. Dedicated requirements and architecture phases.

**Example:** "Build a full e-commerce platform with payment integration"

```
You
 |
 v
team-lead -- analyzes: new product, requires full SDLC
 |
 v
+==========================+
| Phase 1: Requirements    |
+==========================+
 |
 +-- product-manager --> PRD & user stories
 |
 v
+==========================+
| Phase 2: Architecture    |
+==========================+
 |
 +-- system-architect --> tech stack & system design
 +-- ui-ux-designer --> user flows & wireframes (parallel)
 |
 v
+==========================+
| Phase 3: Implementation  |
+==========================+
 |
 +-- database-engineer --> schema & migrations
 +-- backend-developer --> order management API
 +-- frontend-developer --> product catalog UI
 +-- devops-engineer --> CI/CD & infrastructure
     (all parallel after Phase 2 completes)
 |
 v
+==========================+
| Phase 4: Quality Gates   |
+==========================+
 |
 +-- security-engineer --> security audit
 +-- qa-engineer --> test plan & automation
     (parallel)
 |
 v
+==========================+
| Phase 5: Delivery        |
+==========================+
 |
 +-- output-aggregator --> final platform documentation
 |
 v
You -- receive complete deliverable
```

**When triggered:** New product builds, platform migrations, microservices architecture, full-stack applications from scratch.

**Team size:** Full team (10+ agents across 5 phases).

## Task Complexity Guide

The team-lead automatically determines complexity and adjusts the team size:

| Complexity | Agents | Example |
|------------|--------|---------|
| **Simple** | 1-2 | "Optimize this SQL query", "Explain this error" |
| **Medium** | 3-5 | "Build a login page", "Add Stripe payments" |
| **Complex** | 6-12 | "Build an e-commerce platform", "Design a microservices architecture" |

## Agent Team Skill

This plugin also provides an `agent-team` skill that activates when you explicitly request team coordination:

```
Use the agent team to build a real-time chat application
```

The skill provides detailed orchestration logic for complex multi-agent workflows.

## Plugin Structure

```
claude-code-agent-team/
├── .claude-plugin/
│   └── plugin.json              # Plugin manifest
├── agents/                       # Agent definitions (13 agents)
│   ├── team-lead.md             # Client liaison & coordinator
│   ├── product-manager.md       # Requirements & PRD
│   ├── system-architect.md      # Architecture design
│   ├── ui-ux-designer.md        # Interface design
│   ├── frontend-developer.md    # Client-side dev
│   ├── backend-developer.md     # Server-side dev
│   ├── fullstack-developer.md   # End-to-end dev
│   ├── mobile-developer.md      # Mobile dev
│   ├── database-engineer.md     # Data design
│   ├── security-engineer.md     # Security audit
│   ├── qa-engineer.md           # Testing strategy
│   ├── devops-engineer.md       # CI/CD & infra
│   └── output-aggregator.md     # Result synthesis
├── skills/
│   └── agent-team/
│       └── SKILL.md             # Team orchestration skill
├── README.md
└── .gitignore
```

This plugin does not currently provide slash commands, hooks, or MCP servers. It is intentionally focused on auto-discovered agents plus the `agent-team` orchestration skill.

## Tips for Best Results

1. **Be specific** -- The more context you provide, the better the team-lead can match specialists
2. **Mention constraints** -- Budget, timeline, tech stack preferences help the team-lead make better decisions
3. **Simple questions are fine** -- The team-lead recognizes when only 1 specialist is needed and won't spin up the whole team
4. **Iterate** -- After receiving deliverables, you can ask follow-ups; the team-lead will dispatch the right agent to refine

## License

MIT
