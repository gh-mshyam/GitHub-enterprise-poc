# GitHub Enterprise POC — Agent Instructions

**Agent-Agnostic Instructions** — Use this with Claude, Codex, Grok, or any coding agent.

## Project

GitHub Enterprise Repository Provisioning POC — autonomous, git-native repo and team provisioning.

## Quick Context

- **Goal:** Provision GitHub repos and teams via Terraform + workflows
- **Tech:** Terraform, GitHub Actions, Python helpers
- **Structure:** `infra/` (terraform), `apps/` (scripts), `.ghdp/` (governance)
- **Workflows:** plan.yml (PR), apply.yml (merge), request-operation.yml (manual)

## Before Work

**Read first:**
- `README.md` — What this repo does, quick start, workflows
- `infra/modules/repository/README.md` — How to add/import repos
- `infra/modules/teams/README.md` — How to create teams
- `infra/repositories/README.md` — Configuration file descriptions

**Key files:**
- `infra/main.tf` — Terraform provider + module calls
- `infra/variables.tf` — Input variables (repos, teams)
- `infra/modules/repository/` — Repository provisioning module
- `infra/modules/teams/` — Team provisioning module
- `.github/workflows/` — Automation (plan, apply, request-operation)
- `apps/scripts/` — Python helpers (validate, parse, import)

## Workflow

1. **Local development:**
   ```bash
   cd infra/
   terraform init
   terraform validate
   terraform plan -var-file=repositories/repos.tfvars
   ```

2. **Configuration changes:**
   - Edit `infra/repositories/repos.tfvars` (new repos)
   - Edit `infra/repositories/teams.tfvars` (new teams)
   - Edit `infra/repositories/imports.tfvars` (existing repos)

3. **Testing:**
   ```bash
   python3 apps/scripts/validate_tfvars.py infra/repositories/repos.tfvars
   python3 -m pytest apps/tests/ -v
   ```

4. **PR & Merge:**
   - Create PR → `plan.yml` runs terraform plan
   - Merge → `apply.yml` executes terraform apply
   - State commits to git automatically

## Code Principles

- **No risk classification** — All repos follow same provisioning path
- **Git-native** — All state changes in git with full audit trail
- **Independent** — This repo has NO Stratos/GHDP dependency
- **Modular** — Repos created here will have their own CI/CD (they can use Stratos)
- **Simple** — Direct terraform provisioning, no complex governance gates

## Folder Rules

At root level, only:
- `apps/` — Scripts and tests
- `infra/` — Terraform code and configurations
- `.github/` — Workflows
- `.ghdp/` — Governance/instructions
- `.claude/`, `.codex/`, `.grok/` — Agent entry points
- `README.md` — Main readme

All working files nested in appropriate subfolders.

## Testing Checklist

Before committing:
- [ ] `terraform validate` passes
- [ ] `terraform plan` succeeds (with stub token if needed)
- [ ] `python3 apps/scripts/validate_tfvars.py` passes for all configs
- [ ] `pytest apps/tests/` passes
- [ ] No uncommitted changes in git

## Common Tasks

**Add new repo:**
1. Edit `infra/repositories/repos.tfvars`
2. Add entry with name, description, visibility
3. Create PR, merge, workflows handle deployment

**Add new team:**
1. Edit `infra/repositories/teams.tfvars`
2. Add entry with name, members, repositories
3. Create PR, merge, workflows handle deployment

**Import existing repo:**
1. Add entry to `infra/repositories/imports.tfvars`
2. Run `terraform import 'module.repository["name"].github_repository.this' 'name'`
3. Commit state, push
4. Workflows manage it going forward

**Run manual operation:**
1. Go to Actions → Request Repository Operation
2. Fill form (create/delete, name, visibility)
3. Workflow creates PR and handles deployment

## Known Limitations

- Local backend (git-committed state) — for POC only
- Manual `terraform import` for existing repos (not automated)
- No branch protection automation (template in docs)

## Production Readiness

This is a **proof-of-concept**. For production:
- [ ] Migrate state backend to S3 + DynamoDB
- [ ] Add automated repo import workflow
- [ ] Set up branch protection policies
- [ ] Implement cost controls
- [ ] Add approval workflows for Tier 1 operations

## Support

Check workflow logs for errors:
1. Go to Actions → [workflow name]
2. Click run → expand failed step
3. Review terraform or script output

For GitHub API errors:
- Verify `GH_PROVISIONING_TOKEN` has `repo` + `admin:org` scopes
- Check rate limits: `gh api rate_limit`
