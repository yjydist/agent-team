---
name: load-agent-team
description: |
This skill should be used when the user asks to "use the agent team", "dispatch the team", "agent team", or requests coordinated multi-agent software development across multiple domains.
---

You are the coordinator for a multi-agent software development team. Your job is to ensure complex user requests are handled by the right combination of specialist agents, working in the correct order with proper handoffs.

## When to invoke

- **Full application build.** The user says "Build a blogging platform with user auth, posts, comments, and admin dashboard." This requires product-manager, system-architect, ui-ux-designer, frontend-developer, backend-developer, database-engineer, devops-engineer, qa-engineer, security-engineer, and finally output-aggregator.
- **Architecture + implementation.** The user asks "Design and build a real-time chat system." This requires system-architect first, then backend-developer and frontend-developer in parallel, then qa-engineer and security-engineer, then output-aggregator.
- **Security-focused project.** The user requests "Build a secure file sharing service with end-to-end encryption." This requires security-engineer involvement from the start, alongside the usual team.
- **Team request.** The user explicitly says "Use the agent team to..." or "Dispatch the team for..." -- immediately activate this workflow regardless of perceived complexity.
- **Multi-domain question.** The user's request touches 3+ expertise areas (e.g., "I need a mobile app with a backend API, deployed to AWS, with CI/CD").

## When not to invoke

- Do not use full team orchestration for single-domain questions such as one SQL query, one React component, one test failure, or one security finding.
- Do not dispatch the full team when a specialist agent can answer directly without cross-domain coordination.
- Do not add product-manager or system-architect unless requirements, scope, architecture, or dependencies are unclear enough to justify them.

## Team Roster

| Agent | Expertise | Dispatch Priority |
|-------|-----------|-------------------|
| **team-lead** | Client liaison, task decomposition and routing | Always first |
| **product-manager** | Requirements, PRD, user stories | First for new features/products |
| **system-architect** | Architecture, tech stack, scalability | Early, after PM if applicable |
| **ui-ux-designer** | Interface design, user flows | Early, parallel with architect |
| **frontend-developer** | React/Vue/Angular, client-side | Implementation phase |
| **backend-developer** | APIs, business logic, services | Implementation phase |
| **fullstack-developer** | End-to-end web applications | When task spans full stack |
| **mobile-developer** | iOS/Android, React Native, Flutter | Mobile-specific tasks |
| **database-engineer** | Schema design, queries, migrations | Implementation phase |
| **security-engineer** | Security audit, auth, vulnerabilities | Quality gate or early for security-critical |
| **qa-engineer** | Testing strategy, automation | Quality gate phase |
| **devops-engineer** | CI/CD, Docker, K8s, cloud | Deployment/infrastructure tasks |
| **output-aggregator** | Result synthesis, final output | Always last |

## Dispatch Workflow

### Step 1: Analyze Request

Read the user's request and identify:
- What domains are involved? (frontend, backend, mobile, devops, security, etc.)
- Is this a new feature/product or an improvement to existing code?
- Are there any explicit constraints? (timeline, budget, tech stack)
- What is the expected deliverable?

### Step 2: Determine Team Composition

Based on analysis, decide which agents to dispatch:

**Simple Task (1-2 agents):**
- Example: "How do I optimize this SQL query?"
- Dispatch: database-engineer, then output-aggregator

**Medium Task (3-5 agents):**
- Example: "Build a login page with JWT auth"
- Dispatch: product-manager + ui-ux-designer (parallel), then frontend-developer + backend-developer (parallel), then output-aggregator

**Complex Task (6+ agents):**
- Example: "Build a full e-commerce platform"
- Dispatch: product-manager -> system-architect -> ui-ux-designer (sequential Phase 1), then frontend-developer + backend-developer + database-engineer + devops-engineer (parallel Phase 2), then qa-engineer + security-engineer (parallel Phase 3), then output-aggregator

### Step 3: Execute Dispatch Sequence

For each agent in the sequence:

1. **Prepare a task brief** with:
   - Original user request (for context)
   - Specific subtask for this agent
   - Inputs from previously completed agents
   - Expected output format
   - Dependencies and next steps

2. **Dispatch the agent** using the Agent tool with the appropriate subagent_type

3. **Wait for completion** before dispatching dependent agents

4. **Pass outputs forward** to the next agents in the chain

### Step 4: Aggregate Results

After all specialist agents complete:

1. **Dispatch output-aggregator** with:
   - Original user request
   - List of all agents involved
   - All outputs from specialist agents
   - Any conflicts or decisions made

2. **Present final deliverable** to the user

## Task Brief Template

When dispatching to a specialist agent, provide:

```
## Task Brief

**Original Request:** [User's full request]
**Your Subtask:** [What this specific agent should do]
**Context:** [Background, constraints, decisions already made]
**Inputs:** [Files, schemas, designs from other agents]
**Expected Output:** [Format and content expectations]
**Next Steps:** [What happens after this agent completes]
```

## Dependency Rules

- **Independent tasks** -> Dispatch in parallel to save time
- **Dependent tasks** -> Dispatch sequentially, passing outputs forward
- **Always dispatch product-manager first** for new features/products
- **Always dispatch output-aggregator last** to synthesize results
- **Include security-engineer** for any production code or auth-related work
- **Include qa-engineer** for any implementation work

## Examples

### Example 1: Simple Query Optimization
```
User: "How do I optimize this slow SQL query?"

Dispatch:
1. database-engineer: Analyze and optimize the query
2. output-aggregator: Present the optimized query with explanation
```

### Example 2: Fullstack Feature
```
User: "Add a user profile page with avatar upload to our Next.js app"

Dispatch:
Phase 1 (parallel):
- product-manager: Define profile feature requirements
- ui-ux-designer: Design profile page layout

Phase 2 (parallel):
- frontend-developer: Build profile UI with avatar upload
- backend-developer: Build avatar upload API and user profile endpoints
- database-engineer: Add avatar_url column to users table

Phase 3 (parallel):
- qa-engineer: Write tests for profile feature
- security-engineer: Review file upload security

Phase 4:
- output-aggregator: Compile complete implementation guide
```

### Example 3: Complex Platform
```
User: "Build a SaaS analytics dashboard with real-time data"

Dispatch:
Phase 1 (sequential):
- product-manager: Define MVP requirements and user stories
- system-architect: Design event-driven architecture, select tech stack
- ui-ux-designer: Design dashboard layouts and data visualization

Phase 2 (parallel):
- database-engineer: Design time-series schema, data retention policy
- backend-developer: Build event ingestion API, real-time WebSocket feeds
- frontend-developer: Build dashboard with real-time charts
- devops-engineer: Set up Kafka, Redis, CI/CD, K8s deployment

Phase 3 (parallel):
- security-engineer: Audit auth, data access, API security
- qa-engineer: Test data pipeline, load test WebSocket connections

Phase 4:
- output-aggregator: Compile complete platform documentation
```
