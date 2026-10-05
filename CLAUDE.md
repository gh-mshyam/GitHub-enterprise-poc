# CLAUDE Quick Guide

## Project

GitHub Enterprise Repository Provisioning POC — autonomous, git-native repo creation/deletion with risk-based approval gates.

## Agent Guidance

Before work, read:
- `.ghdp/contracts/ARCHITECTURE.md` — Design principles and workflow logic
- `.ghdp/contracts/CONTRIBUTION_RULES.md` — PR requirements and code standards
- `.ghdp/TESTING.md` — Local validation steps

## Preferred Behavior

- Output concise plan + ordered todo list before edits
- Run local validation: `cd infra && terraform plan -var-file=../repositories/example.tfvars`
- Keep commits focused and well-documented
- Reference `.ghdp/` for architectural decisions

## Key Files

- `infra/` — Terraform code (provider, modules, state)
- `repositories/example.tfvars` — Repo definitions
- `scripts/classify_risk.py` — Risk classification logic
- `.github/workflows/` — Automation (plan, apply, request-operation)

## Quick Start

```bash
cd infra
terraform init
terraform plan -var-file=../repositories/example.tfvars
```

See `.ghdp/` for detailed guidance.
