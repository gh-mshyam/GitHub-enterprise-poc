# Repo Bootstrap & Agent Guidance

This repository's detailed guidance lives in `.ghdp/` — treat it as the authoritative source of truth for architecture, contribution rules, and testing strategy.

## Quick Pointers

- **Architecture & design:** Read `.ghdp/contracts/ARCHITECTURE.md` first
- **Contribution rules & PR requirements:** `.ghdp/contracts/CONTRIBUTION_RULES.md`
- **Testing & validation:** `.ghdp/TESTING.md`
- **Quick setup:** See `CLAUDE.md` for concise quick-guide

## Key Principles

1. Git-native workflow — all changes through PRs
2. Deterministic risk classification — Tier 0 (auto-merge) vs Tier 1 (manual)
3. Infrastructure as Code — Terraform manages repos
4. Audit trail — all decisions in git + PR comments

## Before Contributing

1. Read `.ghdp/contracts/CONTRIBUTION_RULES.md`
2. Run local validation: `terraform plan -var-file=../repositories/example.tfvars`
3. Follow PR template security & code quality checklist

## Ground Truth

- `.ghdp/contracts/ARCHITECTURE.md` defines design decisions
- `.ghdp/contracts/CONTRIBUTION_RULES.md` defines PR standards
- Do not change `.ghdp/` without updating relevant documentation
- Update `.ghdp/` if architectural decisions change

For detailed guidance, open the `.ghdp/` folder.
