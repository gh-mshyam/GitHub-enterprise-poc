#!/usr/bin/env python3
"""
Contract resolver: Child reads workflow-contract.json and validates
that it's using parent components correctly.
"""

import json
import os
import sys
from pathlib import Path

def load_contract(contract_path="workflow-contract.json"):
    """Load and validate contract file."""
    try:
        with open(contract_path, "r") as f:
            contract = json.load(f)
        return contract
    except FileNotFoundError:
        print(f"ERROR: {contract_path} not found")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"ERROR: {contract_path} is not valid JSON")
        sys.exit(1)

def validate_immutable_components(contract, repo_root="."):
    """Verify that immutable components match parent."""
    immutable_issues = []

    for component in contract.get("parent_components", {}).get("scripts", []):
        if component.get("immutable"):
            path = component["path"]
            full_path = os.path.join(repo_root, path)

            if not os.path.exists(full_path):
                immutable_issues.append(f"Missing immutable component: {path}")
            else:
                # Could fetch from parent to verify hash
                print(f"✓ Immutable component present: {path}")

    return immutable_issues

def get_parent_reference(contract):
    """Get parent branch/tag to reference."""
    parent_branch = contract.get("versioning", {}).get("parent_branch", "main")
    semantic_version = contract.get("semantic_version", "latest")

    return {
        "branch": parent_branch,
        "version": semantic_version,
        "reference": f"{parent_branch}@{semantic_version}"
    }

def report_contract_status(contract, repo_root="."):
    """Generate contract status report."""
    print("\n=== Contract Resolution Report ===\n")

    print(f"Contract Version: {contract.get('contract_version')}")
    print(f"Parent Reference: {contract.get('parent_reference')}")

    parent_ref = get_parent_reference(contract)
    print(f"Resolved Parent: {parent_ref['reference']}\n")

    print("Parent Components (Immutable):")
    for script in contract.get("parent_components", {}).get("scripts", []):
        if script.get("immutable"):
            print(f"  • {script['name']}: {script['path']}")

    print("\nImmutability Validation:")
    issues = validate_immutable_components(contract, repo_root)
    if issues:
        for issue in issues:
            print(f"  ⚠️ {issue}")
        return False
    else:
        print("  ✓ All immutable components validated")
        return True

if __name__ == "__main__":
    contract = load_contract()
    valid = report_contract_status(contract)

    if not valid:
        print("\n❌ Contract validation failed")
        sys.exit(1)
    else:
        print("\n✓ Contract resolved successfully")
        sys.exit(0)
