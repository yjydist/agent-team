#!/usr/bin/env python3
"""
Plugin validation script for claude-code-agent-team.

Validates plugin structure, agent definitions, skills, and README
before publishing. Uses only Python 3 standard library.
"""

import glob
import json
import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

errors = []


def error(msg: str) -> None:
    errors.append(msg)


def parse_frontmatter(text: str) -> tuple[dict, str] | tuple[None, None]:
    """Parse YAML frontmatter from markdown text.

    Returns (data_dict, body) on success, (None, None) on failure.
    Only handles simple key: value pairs and literal blocks (|).
    """
    if not text.startswith("---"):
        return None, None

    # Find the end of frontmatter
    end_match = re.search(r"\n---\s*(?:\n|$)", text, re.DOTALL)
    if not end_match:
        return None, None

    fm_text = text[3:end_match.start()]  # skip initial ---
    body = text[end_match.end():]

    data: dict[str, str] = {}
    current_key: str | None = None
    current_value: list[str] = []
    in_literal = False

    for line in fm_text.splitlines():
        stripped = line.rstrip()

        if in_literal:
            # Literal block: preserve indentation relative to base
            if stripped == "" or line.startswith("  ") or line.startswith("\t"):
                current_value.append(line)
                continue
            else:
                # End of literal block
                assert current_key is not None
                data[current_key] = "\n".join(current_value).rstrip("\n")
                in_literal = False
                current_key = None
                current_value = []
                # Fall through to process this line as a new key

        if not in_literal:
            # Check for key: value pattern
            m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", stripped)
            if m:
                key, val = m.group(1), m.group(2)
                if val == "|":
                    current_key = key
                    current_value = []
                    in_literal = True
                else:
                    data[key] = val
            # else: blank line or unrecognized, skip

    if in_literal and current_key is not None:
        data[current_key] = "\n".join(current_value).rstrip("\n")

    return data, body


def validate_plugin_json() -> None:
    path = os.path.join(REPO_ROOT, ".claude-plugin", "plugin.json")
    if not os.path.isfile(path):
        error("plugin.json: file not found")
        return

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        error(f"plugin.json: invalid JSON -- {e}")
        return

    if not isinstance(data, dict):
        error("plugin.json: root must be an object")
        return

    name = data.get("name")
    if name != "claude-code-agent-team":
        error(f"plugin.json: name must be 'claude-code-agent-team', got {name!r}")


def validate_agents() -> None:
    agent_dir = os.path.join(REPO_ROOT, "agents")
    if not os.path.isdir(agent_dir):
        error("agents/: directory not found")
        return

    agent_files = sorted(glob.glob(os.path.join(agent_dir, "*.md")))
    if not agent_files:
        error("agents/: no .md files found")
        return

    required_frontmatter_keys = {"name", "description", "model", "color"}

    for filepath in agent_files:
        filename = os.path.basename(filepath)
        name_from_file = os.path.splitext(filename)[0]

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
        except OSError as e:
            error(f"agents/{filename}: cannot read file -- {e}")
            continue

        fm, _ = parse_frontmatter(content)
        if fm is None:
            error(f"agents/{filename}: missing or malformed YAML frontmatter")
            continue

        missing_keys = required_frontmatter_keys - set(fm.keys())
        if missing_keys:
            error(f"agents/{filename}: frontmatter missing keys: {sorted(missing_keys)}")

        # name matches filename
        fm_name = fm.get("name", "")
        if fm_name != name_from_file:
            error(f"agents/{filename}: frontmatter name ({fm_name!r}) does not match filename")

        # tools field (except team-lead)
        if name_from_file != "team-lead":
            if "tools" not in fm:
                error(f"agents/{filename}: missing 'tools' field (required for non-team-lead agents)")

        # description length <= 700 chars
        desc = fm.get("description", "")
        if len(desc) > 700:
            error(f"agents/{filename}: description exceeds 700 characters ({len(desc)})")

        # description contains "When to invoke" reference
        if '"When to invoke"' not in desc and "'When to invoke'" not in desc and "When to invoke" not in desc:
            error(f"agents/{filename}: description must contain a 'When to invoke' reference")


def validate_skills() -> None:
    skills_dir = os.path.join(REPO_ROOT, "skills")
    if not os.path.isdir(skills_dir):
        error("skills/: directory not found")
        return

    skill_dirs = sorted([
        d for d in os.listdir(skills_dir)
        if not d.startswith(".") and os.path.isdir(os.path.join(skills_dir, d))
    ])
    if not skill_dirs:
        error("skills/: no skill directories found")
        return

    for skill_name in skill_dirs:
        skill_path = os.path.join(skills_dir, skill_name)
        skill_md = os.path.join(skill_path, "SKILL.md")

        if not os.path.isfile(skill_md):
            error(f"skills/{skill_name}/: missing SKILL.md")
            continue

        try:
            with open(skill_md, "r", encoding="utf-8") as f:
                content = f.read()
        except OSError as e:
            error(f"skills/{skill_name}/SKILL.md: cannot read file -- {e}")
            continue

        fm, _ = parse_frontmatter(content)
        if fm is None:
            error(f"skills/{skill_name}/SKILL.md: missing or malformed YAML frontmatter")
            continue

        missing_keys = {"name", "description"} - set(fm.keys())
        if missing_keys:
            error(f"skills/{skill_name}/SKILL.md: frontmatter missing keys: {sorted(missing_keys)}")

        fm_name = fm.get("name", "")
        if fm_name != skill_name:
            error(f"skills/{skill_name}/SKILL.md: frontmatter name ({fm_name!r}) does not match directory name")

        desc = fm.get("description", "")
        if not desc.startswith("This skill should be used"):
            error(f"skills/{skill_name}/SKILL.md: description must start with 'This skill should be used' (third person)")


def validate_readme() -> None:
    path = os.path.join(REPO_ROOT, "README.md")
    if not os.path.isfile(path):
        error("README.md: file not found")
        return

    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except OSError as e:
        error(f"README.md: cannot read file -- {e}")
        return

    # Check for non-existent agent abbreviations (not followed by word char or hyphen)
    bad_abbreviations = ["frontend-dev", "backend-dev", "ui-ux"]
    for abbrev in bad_abbreviations:
        pattern = r'(?<!\w)' + re.escape(abbrev) + r'(?!\w|-)'
        if re.search(pattern, content):
            error(f"README.md: contains non-existent agent abbreviation '{abbrev}'")

    # Required phrases
    required_phrases = [
        '"Explicit Team Mode"',
        '"Specialist Direct Mode"',
        '"This plugin does not currently provide slash commands, hooks, or MCP servers."',
    ]
    for phrase in required_phrases:
        # Strip outer quotes for the actual search
        search_text = phrase.strip('"')
        if search_text not in content:
            error(f"README.md: missing required phrase: {phrase}")


def main() -> int:
    validate_plugin_json()
    validate_agents()
    validate_skills()
    validate_readme()

    if errors:
        print("Plugin validation FAILED:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print("Plugin validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
