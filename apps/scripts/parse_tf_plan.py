#!/usr/bin/env python3
"""Parse Terraform plan JSON and format for PR comments."""

import sys
import json
from pathlib import Path
from collections import defaultdict


def parse_plan_json(plan_path: str) -> dict:
    """Parse Terraform plan JSON file."""
    path = Path(plan_path)
    if not path.exists():
        return {}

    try:
        with open(path) as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error parsing plan: {e}", file=sys.stderr)
        return {}


def extract_changes(plan_data: dict) -> dict:
    """Extract resource changes from plan."""
    changes = defaultdict(lambda: {'create': [], 'update': [], 'delete': []})

    if 'resource_changes' not in plan_data:
        return changes

    for resource in plan_data['resource_changes']:
        resource_type = resource.get('type', 'unknown')
        change = resource.get('change', {})
        actions = change.get('actions', [])

        if not actions:
            continue

        action = actions[0]  # Primary action
        name = resource.get('name', 'unnamed')

        if action == 'create':
            changes[resource_type]['create'].append(name)
        elif action == 'update':
            changes[resource_type]['update'].append(name)
        elif action == 'delete':
            changes[resource_type]['delete'].append(name)

    return changes


def format_markdown(changes: dict) -> str:
    """Format changes as markdown for PR comment."""
    if not changes:
        return "### Terraform Plan\n\nNo changes detected."

    lines = ["### Terraform Plan Summary\n"]

    for resource_type in sorted(changes.keys()):
        items = changes[resource_type]
        if any([items['create'], items['update'], items['delete']]):
            lines.append(f"\n#### {resource_type}")

            if items['create']:
                lines.append(f"- **Create**: {', '.join(items['create'])}")
            if items['update']:
                lines.append(f"- **Update**: {', '.join(items['update'])}")
            if items['delete']:
                lines.append(f"- **Delete**: {', '.join(items['delete'])}")

    return '\n'.join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: parse_tf_plan.py <plan.json>")
        sys.exit(1)

    plan_json = parse_plan_json(sys.argv[1])
    changes = extract_changes(plan_json)
    markdown = format_markdown(changes)

    # Write to stdout or file if specified
    if len(sys.argv) > 2:
        Path(sys.argv[2]).write_text(markdown)
    else:
        print(markdown)


if __name__ == '__main__':
    main()
