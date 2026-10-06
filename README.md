# GitHub Enterprise Repository Provisioning

Autonomous repository and team provisioning for GitHub using Terraform. Git-native infrastructure with simple workflows.

> **Agent Instructions:** See `CLAUDE.md` for agent-specific entry points (Claude, Codex, Grok) or `.ghdp/INSTRUCTIONS.md` for full agent-agnostic documentation.

## What Does This Do?

Creates and manages GitHub repositories and teams via Terraform, with two provisioning methods:
1. **Git-native** — Edit `.tfvars` files, commit, and let workflows handle deployment
2. **Workflow dispatch** — Use GitHub Actions UI for one-off repository operations

## Quick Start

### For Engineers

```bash
# Add a new repository
vi infra/repositories/repos.tfvars
# Add entry: "my-repo" = { description = "...", visibility = "private" }

git checkout -b add-my-repo
git add infra/repositories/repos.tfvars
git commit -m "Add my-repo"
git push

# Open PR → Review changes → Merge → Deployment
```

### For Business Users

1. Go to **Actions** → **Request Repository Operation** → **Run workflow**
2. Fill the form (operation, name, visibility)
3. Click **Run** → System creates PR and deploys

## Core Workflows

| Workflow | When | What |
|----------|------|------|
| `plan.yml` | PR to main | Terraform plan + PR comment |
| `apply.yml` | After merge | Execute terraform, commit state |
| `deploy.yml` | Manual trigger | Deploy specific .tfvars file |
| `import-repo.yml` | Manual trigger | Import existing repository |
| `request-operation.yml` | Manual trigger | Create/delete repos (no git) |

## Configuration Files

- **`infra/repositories/repos.tfvars`** — New repositories to create
- **`infra/repositories/teams.tfvars`** — Teams and members
- **`infra/repositories/imports.tfvars`** — Existing repos to import and manage

See `infra/repositories/README.md` for details.

## Infrastructure Modules

### Repository Module
Creates GitHub repositories with configurable options (visibility, topics, branch settings).

**Usage:** Add entries to `repositories/repos.tfvars`  
**See also:** `infra/modules/repository/README.md`

### Teams Module
Creates GitHub teams, manages members, and assigns repository access.

**Usage:** Add entries to `repositories/teams.tfvars`  
**See also:** `infra/modules/teams/README.md`

## Architecture

```
repositories/*.tfvars (configuration)
    ↓
.github/workflows/plan.yml (terraform plan)
    ↓
GitHub PR (review)
    ↓
.github/workflows/apply.yml (terraform apply)
    ↓
infra/modules/{repository,teams}/ (provision)
    ↓
GitHub API (create/update resources)
```

## State Management

- Terraform state (`infra/terraform.tfstate`) is committed to git
- Enables workflow reproducibility and auditability
- **Production:** Migrate to S3 backend for locking/encryption

## Testing

Run unit tests for CI/CD helpers:
```bash
python3 -m pytest apps/tests/ -v
```

## Quick Reference

- **Add repository:** Edit `repositories/repos.tfvars` → PR → Merge
- **Add team:** Edit `repositories/teams.tfvars` → PR → Merge
- **Import repo:** Use `import-repo.yml` workflow
- **Manual operation:** Use `request-operation.yml` workflow
- **Validate config:** `python3 apps/scripts/validate_tfvars.py repositories/repos.tfvars`

## Key Files

| File | Purpose |
|------|---------|
| `infra/main.tf` | Terraform provider + module calls |
| `infra/variables.tf` | Terraform input variables |
| `infra/modules/repository/` | Repository provisioning |
| `infra/modules/teams/` | Team provisioning |
| `repositories/` | Configuration files |
| `apps/scripts/` | CI/CD validation helpers |

## Documentation

- **Setup & usage:** See `repositories/README.md`
- **Repository management:** See `infra/modules/repository/README.md`
- **Team management:** See `infra/modules/teams/README.md`
- **Workflows:** See `.github/workflows/`

## Support

Check workflow logs for detailed error messages:
1. Go to **Actions** → Select workflow run
2. Expand failed step
3. Review terraform output or script errors

For GitHub API errors, verify:
- `GH_PROVISIONING_TOKEN` secret has `repo` and `admin:org` scopes
- Rate limits: `gh api rate_limit`
