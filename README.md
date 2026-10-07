# GitHub Enterprise Repository Provisioning

Autonomous repository and team provisioning for GitHub using Terraform.

> **Instructions:** See `CLAUDE.md` for agent-specific guidance, or `.ghdp/INSTRUCTIONS.md` for full documentation.

## What This Does

- Creates new GitHub repositories via Terraform
- Creates and manages GitHub teams
- Imports existing repositories into Terraform management
- Manages team members and repository access

## Core Procedures

### Repositories

**📖 See: [`infra/modules/repository/README.md`](infra/modules/repository/README.md)**

1. **How to add a new repository?**
2. **How to add an existing repository?**

### Teams

**📖 See: [`infra/modules/teams/README.md`](infra/modules/teams/README.md)**

1. **How to add a new team?**
2. **How to add an existing team?**

---

## Quick Workflow

```
Edit infra/default/repositories/*.tfvars
    ↓
Create PR
    ↓
Workflows run terraform plan
    ↓
Merge PR
    ↓
Workflows run terraform apply
    ↓
Resources created/updated on GitHub
```

## Configuration Files

- `infra/default/repositories/repos.tfvars` — New repositories
- `infra/default/repositories/teams.tfvars` — Teams and members
- `infra/default/repositories/imports.tfvars` — Existing repos to import

See [`infra/default/repositories/README.md`](infra/default/repositories/README.md) for details.

## Documentation

### Human-Friendly Guides

- **📐 Architecture:** `conf/ARCHITECTURE.md` — System design and folder structure
- **📝 Contributing:** `conf/CONTRIBUTING.md` — How to make changes and workflow guide

### Technical Reference

- **Full instructions:** `.ghdp/INSTRUCTIONS.md`
- **Repository procedures:** `infra/default/modules/repository/README.md`
- **Team procedures:** `infra/default/modules/teams/README.md`
- **Import workflow:** `infra/default/repositories/IMPORT.md`
- **Configuration guide:** `infra/default/repositories/README.md`
- **Agent guidance:** `CLAUDE.md`

## Support

For errors, check:
1. Go to **Actions** → Select workflow
2. Expand failed step
3. Review terraform/script output

For GitHub API issues:
- Verify `GH_PROVISIONING_TOKEN` has `repo` + `admin:org` scopes
- Check rate limits: `gh api rate_limit`
