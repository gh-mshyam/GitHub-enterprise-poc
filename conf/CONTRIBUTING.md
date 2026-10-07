# Contributing Guide

This document describes how to make changes to the GitHub Enterprise Repository Provisioning system.

## Overview

This repository is **human-operated**. All infrastructure changes are:
1. Made as code (via configuration files or scripts)
2. Committed to git with clear messages
3. Reviewed as pull requests
4. Automatically validated by CI/CD workflows
5. Applied automatically on merge

## Making Changes

### 1. Creating a New Repository

**Edit:** `infra/default/repositories/repos.tfvars`

Add an entry:
```hcl
"my-new-repo" = {
  description        = "What this repo does"
  visibility         = "private"              # or "internal", "public"
  topics             = ["topic1", "topic2"]   # optional
  homepage_url       = "https://example.com"  # optional
  has_issues         = true                   # enable issues
  has_wiki           = false                  # disable wiki
  has_projects       = false                  # disable projects
  archive_on_destroy = true                   # archive if destroyed
}
```

Then:
1. Create a PR with your changes
2. GitHub Actions will run `terraform plan` and comment with the expected changes
3. Review the plan to verify it's creating the repository you expect
4. Merge the PR
5. GitHub Actions will run `terraform apply` and create the repository

### 2. Creating a New Team

**Edit:** `infra/default/repositories/teams.tfvars`

Add an entry:
```hcl
"my-team" = {
  description  = "Team description"
  privacy      = "closed"              # or "secret"
  members      = ["user1", "user2"]   # GitHub usernames
  repositories = ["my-repo"]           # repo names to grant access
}
```

Then:
1. Create a PR with your changes
2. Review the Terraform plan
3. Merge when satisfied
4. GitHub Actions will create/update the team

### 3. Importing an Existing Repository

If you have repositories already on GitHub that you want to manage through Terraform:

**→ For detailed import procedures, see [`apps/scripts/IMPORT_WORKFLOW.md`](../../apps/scripts/IMPORT_WORKFLOW.md)**

**Option A: Automatic (recommended)**

1. Go to **Actions** tab
2. Select **Discover Repository for Import** workflow
3. Click **Run workflow**
4. Enter the full GitHub URL (e.g., `https://github.com/org/my-repo`)
5. Workflow runs and creates a PR
6. Review the generated configuration
7. Merge the PR to import the repository

**Option B: Manual**

1. Edit `infra/default/repositories/imports.tfvars` and add your config
2. Commit and push (don't merge yet)
3. Run import command locally (see below)
4. Commit the state changes
5. Create PR and merge

### 4. Modifying Repository Settings

To modify an existing repository (e.g., change visibility, add topics):

1. Find the repository entry in `infra/default/repositories/repos.tfvars`
2. Edit the configuration
3. Create a PR
4. Review the Terraform plan
5. Merge when satisfied

Example: Make a repository public
```hcl
"my-repo" = {
  description = "..."
  visibility  = "public"  # changed from "private"
  ...
}
```

### 5. Adding Members to a Team

To add members to an existing team:

1. Find the team in `infra/default/repositories/teams.tfvars`
2. Add usernames to the `members` list
3. Create a PR
4. Merge after review

Example:
```hcl
"my-team" = {
  ...
  members = ["user1", "user2", "user3"]  # added user3
  ...
}
```

### 6. Granting Team Access to a Repository

To grant a team access to a repository:

1. Edit the team configuration in `infra/default/repositories/teams.tfvars`
2. Add the repository name to the `repositories` list
3. Create a PR
4. Merge after review

Example:
```hcl
"my-team" = {
  ...
  repositories = ["my-repo", "new-repo"]  # added new-repo
  ...
}
```

## Local Development

### Prerequisites

- Terraform 1.5.0+
- GitHub token with `repo` + `admin:org` scopes

### Setup

```bash
cd infra/default
terraform init
```

### Plan Changes

Before making any infrastructure changes:

```bash
cd infra/default
export TF_VAR_github_token="your-github-token"
export TF_VAR_github_owner="your-org"

# See what Terraform would do
terraform plan -var-file=repositories/repos.tfvars
```

### Apply Changes

```bash
cd infra/default

# Apply all changes
terraform apply -var-file=repositories/repos.tfvars

# Or apply specific changes only (verify first!)
terraform apply -var-file=repositories/repos.tfvars -target='module.repository["my-repo"]'
```

### Import a Repository (Manual)

```bash
cd infra/default

# First, add configuration to imports.tfvars
# Then, import the resource:
terraform import 'module.repository["my-repo"].github_repository.this' 'my-repo'

# Verify it was imported
terraform state list | grep my-repo

# Commit the state change
git add terraform.tfstate
git commit -m "terraform: import my-repo"
```

## Code Review Checklist

When reviewing a PR that changes infrastructure:

- [ ] Configuration syntax is correct (valid HCL)
- [ ] Repository/team names follow naming conventions
- [ ] Terraform plan shows expected resources
- [ ] No accidental deletions or destructive changes
- [ ] Description explains the change
- [ ] Commit message is clear

Example good commit message:
```
infra: create data-pipeline team and grant access to data-processor repo

- Add 'data-pipeline' team in teams.tfvars
- Grant team access to 'data-processor' repository
- Add team members: alice, bob, charlie
```

## Troubleshooting

### Workflow Failed During Plan

1. Go to **Actions** tab
2. Click the failed workflow
3. Expand the failed step
4. Check Terraform error message
5. Common issues:
   - Invalid HCL syntax in .tfvars files
   - GitHub token missing or has wrong scopes
   - Repository/team already exists with different config

### State Out of Sync

If Terraform state is out of sync with GitHub:

```bash
cd infra/default

# Refresh state
terraform refresh -var-file=repositories/repos.tfvars

# See what changed
terraform plan -var-file=repositories/repos.tfvars

# Update state if needed
terraform apply -auto-approve -var-file=repositories/repos.tfvars
```

### Manual State Fix

If state is corrupted:

```bash
cd infra/default

# Backup current state
cp terraform.tfstate terraform.tfstate.backup

# Remove the problematic resource
terraform state rm 'module.repository["bad-repo"]'

# Re-import or recreate
terraform import 'module.repository["repo-name"].github_repository.this' 'repo-name'
```

## Testing Changes

All changes go through CI/CD:

1. **Pull Request**: Triggers `terraform plan`
   - Plan runs in PR context
   - Results are posted as a comment
   - You can see exactly what will change

2. **Merge to Main**: Triggers `terraform apply`
   - Changes are applied to GitHub
   - State is committed back to repo
   - GitHub shows the resources created/modified

## Release Process

This is a **continuous deployment** system:

1. Make changes in a feature branch
2. Create PR with clear description
3. Get approval from team member
4. Merge to `main`
5. GitHub Actions automatically applies changes

No separate release branches or manual deployment steps.

## Architecture Changes

For larger changes (adding new modules, reorganizing folders, etc.):

1. Discuss approach with team
2. Create design document or RFC
3. Implement in feature branch with clear commit messages
4. Submit PR with full context
5. Review and merge

## Workspace Organization

```
infra/default/
├── main.tf                          # Provider & modules
├── variables.tf                     # Variable definitions
├── modules/
│   ├── repository/                  # Repository module
│   └── teams/                       # Teams module
└── repositories/                    # Configuration
    ├── repos.tfvars                 # Repository configs
    ├── teams.tfvars                 # Team configs
    └── imports.tfvars               # Import configs
```

**Rule**: Do not edit files in `modules/` unless you're changing module logic. Use `.tfvars` files to control behavior.

## Support

- For questions about specific repositories/teams, check `infra/default/repositories/`
- For implementation issues, see `conf/ARCHITECTURE.md`
- For workflow/automation issues, check `.github/workflows/`
