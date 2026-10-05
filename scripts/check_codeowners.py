#!/usr/bin/env python3
"""
Check if .github/CODEOWNERS file exists and is valid.
Used by workflows to detect ownership requirements for PR comments.
"""

import json
import sys
import os

def check_codeowners(repo_root="."):
    """
    Check if .github/CODEOWNERS exists.

    Returns:
        dict: {
            "exists": bool,
            "owners": str or None,
            "status": "present" | "missing",
            "message": str
        }
    """
    codeowners_path = os.path.join(repo_root, ".github", "CODEOWNERS")

    if os.path.exists(codeowners_path):
        try:
            with open(codeowners_path, "r") as f:
                content = f.read().strip()
                if content:
                    return {
                        "exists": True,
                        "status": "present",
                        "message": "✓ CODEOWNERS file found",
                        "path": codeowners_path
                    }
                else:
                    return {
                        "exists": True,
                        "status": "empty",
                        "message": "⚠️ CODEOWNERS file is empty",
                        "path": codeowners_path
                    }
        except Exception as e:
            return {
                "exists": True,
                "status": "error",
                "message": f"Error reading CODEOWNERS: {str(e)}",
                "path": codeowners_path
            }
    else:
        return {
            "exists": False,
            "status": "missing",
            "message": "⚠️ CODEOWNERS file not found - manual review may be needed",
            "path": codeowners_path
        }


def get_pr_comment_status(tier, codeowners_status):
    """
    Generate PR comment snippet for CODEOWNERS status.

    Args:
        tier: "0" or "1"
        codeowners_status: dict from check_codeowners()

    Returns:
        str: Markdown snippet for PR comment
    """
    if codeowners_status["status"] == "present":
        return "✓ **CODEOWNERS:** Assigned and will be notified\n"
    elif codeowners_status["status"] == "missing":
        if tier == "1":
            return "⚠️ **CODEOWNERS:** File missing - Tier 1 operation requires manual review assignment\n"
        else:
            return "ℹ️ **CODEOWNERS:** File missing (not required for Tier 0)\n"
    elif codeowners_status["status"] == "empty":
        if tier == "1":
            return "⚠️ **CODEOWNERS:** File empty - Tier 1 operation requires reviewer assignment\n"
        else:
            return "ℹ️ **CODEOWNERS:** File empty (Tier 0 auto-approved)\n"
    else:
        return f"⚠️ **CODEOWNERS:** {codeowners_status['message']}\n"


if __name__ == "__main__":
    # Usage: python3 scripts/check_codeowners.py [repo_root] [tier] [output_file]

    repo_root = sys.argv[1] if len(sys.argv) > 1 else "."
    tier = sys.argv[2] if len(sys.argv) > 2 else None
    output_file = sys.argv[3] if len(sys.argv) > 3 else None

    status = check_codeowners(repo_root)

    if output_file:
        # Write status as JSON
        with open(output_file, "w") as f:
            json.dump(status, f, indent=2)

        # If tier provided, also generate PR comment snippet
        if tier:
            comment_snippet = get_pr_comment_status(tier, status)
            with open(output_file.replace(".json", ".md"), "w") as f:
                f.write(comment_snippet)
    else:
        # Print to stdout
        print(json.dumps(status, indent=2))
