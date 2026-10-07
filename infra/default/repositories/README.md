# Repositories Configuration

This directory contains Terraform variable files for managing GitHub resources via the unified provisioning workflow.

## Files

### `repos.tfvars`
Defines **new repositories** to create in the GitHub organization.

Usage:
```bash
terraform plan -var-file=repositories/repos.tfvars
```

### `teams.tfvars`
Defines **GitHub teams**, their members, and repository access.

Usage:
```bash
terraform plan -var-file=repositories/teams.tfvars
```

### `imports.tfvars`
Defines **existing repositories** to import into Terraform management.

Usage:
1. Add repository config to `imports.tfvars`
2. Run `terraform import` to bind the existing repo:
   ```bash
   terraform import 'module.repository["repo-name"].github_repository.this' 'repo-name'
   ```
3. Commit and push
4. Workflows will manage it via `imports.tfvars`

## Quick Start

1. **Create a new repository:**
   - Add entry to `repos.tfvars`
   - Create a PR
   - On merge, workflows apply the changes

2. **Create a new team:**
   - Add entry to `teams.tfvars`
   - Create a PR
   - On merge, workflows apply the changes

3. **Import an existing repository:**
   - Add entry to `imports.tfvars`
   - Follow import steps above
   - Commit changes
   - On merge, Terraform will manage it

## Workflow Integration

Workflows automatically detect changed `.tfvars` files and apply them. For manual runs:

```bash
cd infra
terraform plan -var-file=repositories/repos.tfvars
terraform apply -var-file=repositories/repos.tfvars
```
