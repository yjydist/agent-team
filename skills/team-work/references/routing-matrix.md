# Routing Matrix

Use this matrix after classifying complexity. Choose the smallest effective team and prefer narrow ownership over broad labels.

## Complexity First

| Complexity | Default Process | Team Size |
| --- | --- | --- |
| Simple | Local answer or one direct specialist; no aggregation | 0-1 roles |
| Medium | Small coordinated batch with explicit contracts | 2-4 roles |
| Complex | Phased product, architecture/design, implementation, verification, and synthesis | 5+ roles |

If a simple task names the agent team explicitly, still keep the process small unless the prompt adds cross-domain risk.

| Role | Strong Triggers | Avoid When |
| --- | --- | --- |
| `product-manager` | Vague product idea, MVP scope, user stories, acceptance criteria, prioritization | Requirements are already explicit and implementation is straightforward |
| `system-architect` | New system, major refactor, distributed design, service boundaries, tech selection, scaling plan | Work is a small feature inside an established architecture |
| `ui-ux-designer` | User flows, information architecture, wireframes, design systems, usability and accessibility planning | UI implementation details are already specified |
| `frontend-developer` | Browser UI, components, routing, client state, CSS/layout, accessibility implementation, frontend performance | The task is only API, schema, or infrastructure |
| `backend-developer` | APIs, services, business logic, auth services, jobs, integrations, backend performance | Only frontend rendering or database-only optimization is needed |
| `fullstack-developer` | Small end-to-end feature slice, prototype, single full-stack framework change | Large systems where frontend/backend/database owners should split work |
| `mobile-developer` | iOS, Android, React Native, Flutter, mobile navigation, device APIs, app release | Browser-only responsive work |
| `database-engineer` | Schema, migrations, SQL/query tuning, indexes, transactions, ETL/warehouse modeling | Data access code only, without schema/query concerns |
| `devops-engineer` | CI/CD, Docker, Kubernetes, cloud infrastructure, runtime config, observability, release automation | App code changes with no deployment or operational impact |
| `qa-engineer` | Test strategy, test automation, E2E, coverage gates, release risk, bug triage | Implementer can add small local tests directly |
| `security-engineer` | Authz/authn, secrets, payment, encryption, compliance, public API, sensitive data, vulnerability remediation | Low-risk internal UI or docs changes |
| `output-aggregator` | Multiple specialist outputs, conflicts, final architecture/implementation synthesis | Single-agent direct answer |

## Common Compositions

- Login or account feature: product-manager if scope is unclear, then backend-developer and frontend-developer; add security-engineer for auth review.
- Data-heavy feature: product-manager if needed, database-engineer for schema/query contract, backend-developer for API, frontend-developer for UI.
- Platform build: product-manager, system-architect, ui-ux-designer, then implementation specialists by ownership, then targeted QA/security.
- CI or deployment work: devops-engineer, plus qa-engineer only if quality gates are part of the request.
- Small full-stack CRUD: fullstack-developer alone unless separate ownership or risk justifies specialists.

## Regression Scenarios

Use [routing-evals.json](routing-evals.json) as the routing behavior corpus. It encodes simple, medium, and complex examples with required, optional, and forbidden roles so routing can remain flexible without losing guardrails.
