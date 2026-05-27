#!/usr/bin/env python3
"""Validate team-work routing evaluation scenarios."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


COMPLEXITIES = {"simple", "medium", "complex"}
REQUIRED_CATEGORIES = {
    "direct_specialist",
    "multi_domain_parallel",
    "risk_gated",
    "platform_build",
}
REQUIRED_FIELDS = {
    "id",
    "category",
    "complexity",
    "prompt",
    "required_roles",
    "optional_roles",
    "forbidden_roles",
    "dependency_notes",
    "expected_process",
}
ROLE_FIELDS = ("required_roles", "optional_roles", "forbidden_roles")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "evals",
        nargs="?",
        default="skills/team-work/references/routing-evals.json",
        help="Path to routing-evals.json",
    )
    args = parser.parse_args()

    path = Path(args.evals)
    errors = validate_file(path)
    if errors:
        print("Routing eval validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Routing eval validation passed: {path}")
    return 0


def validate_file(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return [f"missing eval file: {path}"]
    except json.JSONDecodeError as exc:
        return [f"invalid JSON: {exc}"]

    if not isinstance(payload, dict):
        return ["root must be a JSON object"]

    roles = payload.get("roles")
    if not isinstance(roles, list) or not roles:
        errors.append("root.roles must be a non-empty list")
        known_roles: set[str] = set()
    else:
        known_roles = set()
        for index, role in enumerate(roles):
            if not isinstance(role, str) or not role:
                errors.append(f"roles[{index}] must be a non-empty string")
                continue
            if role in known_roles:
                errors.append(f"duplicate role: {role}")
            known_roles.add(role)

    scenarios = payload.get("scenarios")
    if not isinstance(scenarios, list) or not scenarios:
        errors.append("root.scenarios must be a non-empty list")
        return errors

    seen_ids: set[str] = set()
    complexities: set[str] = set()
    categories: set[str] = set()
    has_overdispatch_guard = False
    has_parallel_dependency = False
    has_aggregation_constraint = False

    for index, scenario in enumerate(scenarios):
        label = f"scenarios[{index}]"
        if not isinstance(scenario, dict):
            errors.append(f"{label} must be an object")
            continue

        missing = REQUIRED_FIELDS - set(scenario)
        if missing:
            errors.append(f"{label} missing fields: {', '.join(sorted(missing))}")
            continue

        scenario_id = scenario.get("id")
        if not isinstance(scenario_id, str) or not scenario_id:
            errors.append(f"{label}.id must be a non-empty string")
            scenario_id = label
        elif scenario_id in seen_ids:
            errors.append(f"duplicate scenario id: {scenario_id}")
        else:
            seen_ids.add(scenario_id)

        complexity = scenario.get("complexity")
        if complexity not in COMPLEXITIES:
            errors.append(f"{scenario_id}.complexity must be one of {sorted(COMPLEXITIES)}")
        else:
            complexities.add(complexity)

        category = scenario.get("category")
        if not isinstance(category, str) or not category:
            errors.append(f"{scenario_id}.category must be a non-empty string")
        else:
            categories.add(category)

        for field in ("prompt", "expected_process"):
            value = scenario.get(field)
            if not isinstance(value, str) or len(value.strip()) < 20:
                errors.append(f"{scenario_id}.{field} must be a descriptive string")

        validate_role_fields(scenario_id, scenario, known_roles, errors)
        validate_dependency_notes(scenario_id, scenario, known_roles, errors)
        validate_complexity_shape(scenario_id, scenario, errors)

        forbidden = set(scenario.get("forbidden_roles", []))
        required = set(scenario.get("required_roles", []))
        optional = set(scenario.get("optional_roles", []))
        notes = " ".join(scenario.get("dependency_notes", []))
        expected = scenario.get("expected_process", "")

        if complexity == "simple" and (
            "output-aggregator" in forbidden
            or "product-manager" in forbidden
            or "system-architect" in forbidden
        ):
            has_overdispatch_guard = True
        if "parallel" in notes.lower() or "parallel" in expected.lower():
            has_parallel_dependency = True
        if "output-aggregator" in optional or "output-aggregator" in forbidden:
            has_aggregation_constraint = True
        if required & forbidden or required & optional or optional & forbidden:
            errors.append(f"{scenario_id} has overlapping role constraints")

    missing_complexities = COMPLEXITIES - complexities
    if missing_complexities:
        errors.append(f"missing complexity coverage: {', '.join(sorted(missing_complexities))}")

    missing_categories = REQUIRED_CATEGORIES - categories
    if missing_categories:
        errors.append(f"missing category coverage: {', '.join(sorted(missing_categories))}")

    if not has_overdispatch_guard:
        errors.append("missing simple-task over-dispatch prevention scenario")
    if not has_parallel_dependency:
        errors.append("missing parallel dependency scenario")
    if not has_aggregation_constraint:
        errors.append("missing aggregation constraint coverage")

    return errors


def validate_role_fields(
    scenario_id: str,
    scenario: dict[str, Any],
    known_roles: set[str],
    errors: list[str],
) -> None:
    for field in ROLE_FIELDS:
        roles = scenario.get(field)
        if not isinstance(roles, list):
            errors.append(f"{scenario_id}.{field} must be a list")
            continue
        seen: set[str] = set()
        for index, role in enumerate(roles):
            if not isinstance(role, str) or not role:
                errors.append(f"{scenario_id}.{field}[{index}] must be a non-empty string")
                continue
            if role not in known_roles:
                errors.append(f"{scenario_id}.{field}[{index}] uses unknown role: {role}")
            if role in seen:
                errors.append(f"{scenario_id}.{field} contains duplicate role: {role}")
            seen.add(role)


def validate_dependency_notes(
    scenario_id: str,
    scenario: dict[str, Any],
    known_roles: set[str],
    errors: list[str],
) -> None:
    notes = scenario.get("dependency_notes")
    if not isinstance(notes, list):
        errors.append(f"{scenario_id}.dependency_notes must be a list")
        return
    for index, note in enumerate(notes):
        if not isinstance(note, str) or not note.strip():
            errors.append(f"{scenario_id}.dependency_notes[{index}] must be a non-empty string")
            continue
        for token in note.replace(",", " ").replace(".", " ").split():
            if token.endswith("-developer") or token.endswith("-engineer") or token in {
                "product-manager",
                "system-architect",
                "ui-ux-designer",
                "output-aggregator",
            }:
                if token not in known_roles:
                    errors.append(
                        f"{scenario_id}.dependency_notes[{index}] references unknown role: {token}"
                    )


def validate_complexity_shape(
    scenario_id: str,
    scenario: dict[str, Any],
    errors: list[str],
) -> None:
    complexity = scenario.get("complexity")
    required_count = len(scenario.get("required_roles", []))
    forbidden = set(scenario.get("forbidden_roles", []))

    if complexity == "simple":
        if required_count > 1:
            errors.append(f"{scenario_id} simple scenarios should require at most one role")
        if "output-aggregator" not in forbidden:
            errors.append(f"{scenario_id} simple scenarios should forbid output-aggregator")
    elif complexity == "medium":
        if required_count < 2 or required_count > 4:
            errors.append(f"{scenario_id} medium scenarios should require 2-4 roles")
    elif complexity == "complex":
        if required_count < 5:
            errors.append(f"{scenario_id} complex scenarios should require at least five roles")


if __name__ == "__main__":
    sys.exit(main())
