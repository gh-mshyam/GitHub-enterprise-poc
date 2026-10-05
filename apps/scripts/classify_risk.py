#!/usr/bin/env python3
"""Classify a terraform plan (in `terraform show -json` format) into a
risk tier for the GitHub Enterprise provisioning POC.

Tier 0 (safe / auto-mergeable candidate):
    - github_repository resources are private
    - repository names follow standard naming (lowercase, digits, hyphens)
    - no delete actions anywhere in the plan
    - no brand-new github_team resource being created

Tier 1 (needs review):
    - any github_repository resource is public or internal
    - any repository name is non-standard (uppercase, underscores, spaces, etc.)
    - any resource anywhere in the plan is being deleted
    - a new github_team is being created (as opposed to attaching an
      already-existing team via github_team_repository)
    - any resource type outside the known allowlist appears in the plan
      (treated as "unknown" and therefore risky by default)

Usage:
    python3 classify_risk.py <plan.json> <github_output_path> <comment_body_path>

Writes:
    - `tier=0` or `tier=1` (plus `reasons`) to the GITHUB_OUTPUT file
    - a human-readable Markdown risk report to <comment_body_path>
"""
from __future__ import annotations

import json
import re
import sys

STANDARD_NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")

KNOWN_RESOURCE_TYPES = {
    "github_repository",
    "github_repository_vulnerability_alerts",
    "github_team_repository",
    "github_branch_protection",
    "github_team",
}


def classify(plan: dict) -> tuple[str, list[str]]:
    """Return (tier, reasons) for the given terraform plan JSON."""
    reasons: list[str] = []
    tier = "0"

    resource_changes = plan.get("resource_changes", [])

    for change in resource_changes:
        resource_type = change.get("type", "")
        address = change.get("address", resource_type)
        actions = change.get("change", {}).get("actions", [])
        after = change.get("change", {}).get("after") or {}

        if resource_type not in KNOWN_RESOURCE_TYPES:
            tier = "1"
            reasons.append(f"{address}: unknown resource type '{resource_type}'")
            continue

        if "delete" in actions:
            tier = "1"
            reasons.append(f"{address}: delete operation")

        if resource_type == "github_repository":
            visibility = after.get("visibility")
            name = after.get("name")

            if visibility and visibility != "private":
                tier = "1"
                reasons.append(f"{address}: visibility is '{visibility}' (not private)")

            if name and not STANDARD_NAME_RE.match(name):
                tier = "1"
                reasons.append(f"{address}: repository name '{name}' is non-standard")

        if resource_type == "github_team" and "create" in actions:
            tier = "1"
            reasons.append(f"{address}: creating a brand-new team")

    if not reasons:
        reasons.append("private repositories, standard naming, existing teams, no deletions")

    return tier, reasons


def render_comment(tier: str, reasons: list[str]) -> str:
    label = "Tier 0 - Standard" if tier == "0" else "Tier 1 - Needs Review"
    lines = [
        "### Terraform Plan Risk Classification",
        "",
        f"**Risk Tier:** {label}",
        "",
        "**Reasons:**",
    ]
    lines.extend(f"- {reason}" for reason in reasons)
    lines.append("")
    if tier == "1":
        lines.append("_This change requires CODEOWNERS review before merge._")
    else:
        lines.append("_This change matches the low-risk profile for standard provisioning._")
    return "\n".join(lines) + "\n"


def main() -> int:
    if len(sys.argv) != 4:
        print("usage: classify_risk.py <plan.json> <github_output_path> <comment_body_path>", file=sys.stderr)
        return 2

    plan_path, github_output_path, comment_body_path = sys.argv[1:4]

    with open(plan_path, encoding="utf-8") as plan_file:
        plan = json.load(plan_file)

    tier, reasons = classify(plan)

    with open(github_output_path, "a", encoding="utf-8") as output_file:
        output_file.write(f"tier={tier}\n")
        output_file.write(f"reasons={'; '.join(reasons)}\n")

    with open(comment_body_path, "w", encoding="utf-8") as comment_file:
        comment_file.write(render_comment(tier, reasons))

    print(f"risk tier: {tier}")
    for reason in reasons:
        print(f"  - {reason}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
