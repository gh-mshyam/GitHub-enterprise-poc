# GHDP Contracts & Guidance

Source of truth for architecture, contribution rules, and testing strategy.

## Files

- **contracts/ARCHITECTURE.md** — Design principles, risk tiers, workflow logic
- **contracts/CONTRIBUTION_RULES.md** — Security, code quality, PR requirements
- **TESTING.md** — Local validation and testing approach

## Quick Reference

- Risk classification: Deterministic rules in `scripts/classify_risk.py`
- Tier 0: Auto-merge safe operations (private repos, standard naming)
- Tier 1: Manual approval for risky operations (deletions, public repos)
- Workflows: plan.yml → classify → apply.yml

See contracts/ for detailed guidance.
