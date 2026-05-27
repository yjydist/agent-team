# Routing Eval Guide

Use `routing-evals.json` when changing routing, complexity, dispatch, or role-boundary behavior. The scenarios are constraints, not exact answer keys: they preserve flexibility while preventing over-dispatch and under-dispatch.

## Run the Static Check

```bash
python3 skills/team-work/scripts/check-routing-evals.py skills/team-work/references/routing-evals.json
```

This validates scenario shape, known roles, complexity coverage, required/optional/forbidden conflicts, dependency notes, and coverage for simple, medium, complex, parallel, risk-gated, and aggregation behavior.

## Manual Forward-Test Pattern

For a behavior check, prompt a fresh agent with only the skill and one scenario prompt. Do not include required, optional, or forbidden roles in the prompt.

```text
Use $team-work at /path/to/skills/team-work to handle:
<scenario prompt>
```

Then compare the response against the scenario constraints:

- Required roles should appear or be clearly represented by local direct work.
- Forbidden roles should not appear.
- Optional roles should appear only when justified by ambiguity or risk.
- Simple scenarios should not create multi-phase workflows.
- Medium scenarios should use a small team with clear contracts.
- Complex scenarios should include phased planning, implementation, verification, and synthesis.

If the response only passes by seeing the expected roles, the eval is contaminated. Re-run with a clean prompt.
