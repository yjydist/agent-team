# Handoff Contracts

Use these concise templates when briefing specialists or synthesizing results.

## Specialist Brief

```markdown
## Task Brief

Original request: <user request>
Role: <specialist role>
Objective: <specific outcome>
Ownership: <files/modules/contracts/deliverables owned by this role>
Context: <decisions, constraints, existing code, prior outputs>
Inputs: <links, schemas, API contracts, designs, diffs>
Do not touch: <parallel conflict boundaries, if any>
Expected output: <patch, plan, review findings, test strategy, etc.>
Handoff: <what the next role needs from this output>
```

## Aggregation Brief

```markdown
## Aggregation Brief

Original request: <user request>
Participants: <roles involved>
Outputs: <summaries or links to each output>
Conflicts to resolve: <known disagreements or gaps>
Required final shape: <implementation summary, plan, PR notes, review, etc.>
Quality bar: <tests, risks, acceptance criteria>
```

## Final Synthesis Checklist

- Answer the user's original request directly.
- Identify the chosen approach and why it fits the constraints.
- Merge duplicate recommendations.
- Resolve naming, API, schema, and ownership inconsistencies.
- Call out remaining risks and verification status.
- Keep final output concise unless the user requested a full design or plan.
