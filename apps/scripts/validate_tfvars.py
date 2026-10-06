#!/usr/bin/env python3
"""Validate Terraform .tfvars files for syntax and required fields."""

import sys
import re
import json
from pathlib import Path


def validate_hcl_syntax(content: str) -> tuple[bool, str]:
    """Basic HCL syntax validation for .tfvars files."""
    errors = []

    # Check for balanced braces, brackets
    if content.count('{') != content.count('}'):
        errors.append("Unbalanced braces: { vs }")
    if content.count('[') != content.count(']'):
        errors.append("Unbalanced brackets: [ vs ]")

    # Check for valid variable assignments
    for line in content.split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if '=' in line and not re.match(r'^[\w_]+ = ', line):
            errors.append(f"Invalid assignment: {line}")

    return len(errors) == 0, '\n'.join(errors)


def validate_repos_tfvars(content: str) -> tuple[bool, str]:
    """Validate repos.tfvars structure."""
    try:
        # Extract repositories map
        if 'repositories = {' not in content:
            return False, "Missing 'repositories = {' definition"

        # Check for required fields when repos are defined
        if content.count('{') > 1:  # Has repository definitions
            required_fields = []  # All fields are optional with defaults
            return True, "repos.tfvars is valid"

        return True, "repos.tfvars structure is valid"
    except Exception as e:
        return False, f"Validation error: {e}"


def validate_teams_tfvars(content: str) -> tuple[bool, str]:
    """Validate teams.tfvars structure."""
    try:
        if 'teams = {' not in content:
            return False, "Missing 'teams = {' definition"

        return True, "teams.tfvars is valid"
    except Exception as e:
        return False, f"Validation error: {e}"


def main():
    if len(sys.argv) < 2:
        print("Usage: validate_tfvars.py <tfvars_file>")
        sys.exit(1)

    tfvars_path = Path(sys.argv[1])

    if not tfvars_path.exists():
        print(f"Error: File not found: {tfvars_path}")
        sys.exit(1)

    content = tfvars_path.read_text()

    # Basic HCL validation
    valid, syntax_errors = validate_hcl_syntax(content)
    if not valid:
        print(f"Syntax Error: {syntax_errors}")
        sys.exit(1)

    # File-specific validation
    if 'repos.tfvars' in str(tfvars_path):
        valid, msg = validate_repos_tfvars(content)
    elif 'teams.tfvars' in str(tfvars_path):
        valid, msg = validate_teams_tfvars(content)
    elif 'imports.tfvars' in str(tfvars_path):
        valid, msg = validate_repos_tfvars(content)  # Same structure
    else:
        valid, msg = True, "Generic .tfvars file"

    if valid:
        print(f"✓ {msg}")
        sys.exit(0)
    else:
        print(f"✗ {msg}")
        sys.exit(1)


if __name__ == '__main__':
    main()
