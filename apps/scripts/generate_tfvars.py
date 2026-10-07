#!/usr/bin/env python3
"""
Generate terraform.tfvars from repositories.json

Usage: python3 generate_tfvars.py repositories.json output/repos.tfvars
"""
import json
import sys
from pathlib import Path


def generate_tfvars(repos_json_path: str, output_path: str):
    """Convert repositories.json to terraform vars format."""

    # Load repositories.json
    config = json.loads(Path(repos_json_path).read_text())
    repositories = config.get("repositories", {})

    # Generate HCL
    lines = [
        '# Auto-generated from repositories.json',
        '# DO NOT EDIT MANUALLY - edit repositories.json and re-run workflow',
        '',
        'repositories = {',
    ]

    for repo_id, repo in repositories.items():
        operation = repo.get("operation", "create")

        # Skip delete operations (handled separately)
        if operation == "delete":
            lines.append(f'  # {repo_id} = {{ # DELETED }}')
            continue

        # Build repo config
        lines.append(f'  "{repo_id}" = {{')
        lines.append(f'    name        = "{repo.get("name", repo_id)}"')
        lines.append(f'    visibility  = "{repo.get("visibility", "private")}"')
        lines.append(f'    description = "{repo.get("description", "")}"')

        if repo.get("topics"):
            topics_list = ', '.join([f'"{t}"' for t in repo["topics"]])
            lines.append(f'    topics      = [{topics_list}]')

        if repo.get("owner"):
            lines.append(f'    owner       = "{repo["owner"]}"')

        if repo.get("auto_merge_develop_to_main"):
            lines.append(f'    auto_merge  = true')

        if repo.get("teams"):
            teams_list = ', '.join([f'"{t}"' for t in repo["teams"]])
            lines.append(f'    teams       = [{teams_list}]')

        lines.append('  }')

    lines.append('}')
    lines.append('')

    # Write to output
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text('\n'.join(lines))
    print(f"✓ Generated {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <input.json> <output.tfvars>")
        sys.exit(1)

    generate_tfvars(sys.argv[1], sys.argv[2])
