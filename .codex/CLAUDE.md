# Codex — Repository Provisioning POC

**See:** `../../.ghdp/INSTRUCTIONS.md` for complete agent-agnostic instructions.

This repository is designed to work with any coding agent (Claude, Codex, Grok, etc.). The main instructions are in `.ghdp/` for consistency and maintainability.

## Quick Start (Codex)

```bash
# Validate configuration
python3 apps/scripts/validate_tfvars.py infra/repositories/repos.tfvars

# Run tests
python3 -m pytest apps/tests/ -v

# Plan deployment
cd infra/
terraform init
terraform plan -var-file=repositories/repos.tfvars
```

## Key Files

- **`.ghdp/INSTRUCTIONS.md`** — Full instructions (read this)
- **`README.md`** — Project overview
- **`infra/repositories/`** — Configuration files (repos, teams, imports)
- **`infra/modules/`** — Terraform modules (repository, teams)
- **`.github/workflows/`** — Automation workflows

## Next Steps

1. Read `.ghdp/INSTRUCTIONS.md`
2. Review `README.md` for project context
3. Check module READMEs for specific tasks
4. Edit configuration files to make changes
5. Create PR and merge

See `.ghdp/INSTRUCTIONS.md` for all details.
