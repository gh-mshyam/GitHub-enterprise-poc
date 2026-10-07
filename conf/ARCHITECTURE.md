# Architecture

This document describes the technical structure and design of the GitHub Enterprise Repository Provisioning system.

## Overview

This is a **Terraform-based infrastructure automation system** that manages GitHub repositories and teams as code. The project uses GitHub Actions workflows to detect configuration changes and automatically provision or update resources.

## Folder Structure

```
github-enterprise-poc/
├── infra/                           # Terraform infrastructure code
│   ├── default/                     # Main Terraform configuration
│   │   ├── main.tf                  # Provider + module instantiation
│   │   ├── variables.tf             # Input variable definitions
│   │   ├── modules/                 # Reusable Terraform modules
│   │   │   ├── repository/          # Module for managing repositories
│   │   │   └── teams/               # Module for managing teams
│   │   └── repositories/            # Configuration files (.tfvars)
│   │       ├── repos.tfvars         # New repositories to create
│   │       ├── teams.tfvars         # Teams and membership
│   │       └── imports.tfvars       # Existing repos to import
│   └── setup/                       # Future setup modules (OIDC, etc.)
│
├── apps/                            # Application code
│   ├── scripts/                     # Utility scripts
│   │   ├── bootstrap_repo.py        # Scaffolding for new repos
│   │   └── sync_templates.py        # Template synchronization
│   └── tests/                       # Test suite
│
├── .github/                         # GitHub-specific configuration
│   ├── workflows/                   # CI/CD workflows
│   │   ├── plan.yml                 # PR validation: terraform plan
│   │   ├── apply.yml                # Main branch: terraform apply
│   │   └── import-discover.yml      # Repository import workflow
│   └── templates/                   # Repository templates
│
├── conf/                            # Human-friendly documentation
│   ├── ARCHITECTURE.md              # This file
│   └── CONTRIBUTING.md              # Contribution guide
│
└── .ghdp/                           # Agent-specific guidance (optional)
```

## Data Flow

```
User edits .tfvars file
         ↓
    Create PR
         ↓
  GitHub Actions: plan.yml
  (terraform plan, post comment)
         ↓
  User reviews plan
         ↓
    Merge PR
         ↓
  GitHub Actions: apply.yml
  (terraform apply, commit state)
         ↓
Resources created/updated on GitHub
```

## Core Components

### 1. Terraform Configuration (`infra/default/`)

**Main entry point:** `main.tf`
- Configures the GitHub provider
- Instantiates `repository` and `teams` modules for each configuration entry
- Uses local backend for POC (state is committed to repo for visibility)

**Module: Repository** (`modules/repository/`)
- Creates or manages individual GitHub repositories
- Handles visibility, topics, branch protection, and archival
- **Usage**: Controlled via `repos.tfvars` entries

**Module: Teams** (`modules/teams/`)
- Creates or manages GitHub teams
- Handles team membership and repository access
- **Usage**: Controlled via `teams.tfvars` entries

### 2. Configuration Files (`infra/default/repositories/`)

Three `.tfvars` files drive all infrastructure decisions:

- **`repos.tfvars`** — Repository declarations (name, visibility, topics, etc.)
- **`teams.tfvars`** — Team declarations (members, permissions)
- **`imports.tfvars`** — Configuration for existing repos to import

Each entry in these files becomes a Terraform resource instantiation.

### 3. Workflows (`.github/workflows/`)

**`plan.yml`** — Triggered by `/plan` comment on PR
- Runs `terraform plan` in PR context
- Posts plan output as comment for review

**`apply.yml`** — Triggered by push to `main`
- Runs `terraform apply` (auto-approved for POC)
- Commits state back to repo (POC pattern only)

**`import-discover.yml`** — Manual workflow for importing repos
- Accepts GitHub URL
- Generates Terraform configuration
- Creates PR with discovered config

### 4. Helper Scripts (`apps/scripts/`)

**`bootstrap_repo.py`** — Scaffolds new repository configuration
- Generates stub `.tfvars` entries
- Can be used in templates for onboarding

**`sync_templates.py`** — Synchronizes repository templates
- Copies template files to newly created repos
- Enables consistent file structure across repos

## Design Decisions

### Why Terraform?

- **Infrastructure-as-Code**: Repository configuration is versionable and reviewable
- **Declarative**: Configuration describes desired state, not imperative steps
- **Idempotent**: Re-applying same config is safe and produces same result
- **GitHub Provider**: HashiCorp maintains official GitHub provider

### Why `.tfvars` files?

- **Human-readable**: Easy to understand and edit
- **Version-controlled**: Full audit trail of all changes
- **PR workflow**: Changes go through review before applying
- **Modular**: Different teams can manage different tfvars files

### Why Local Backend?

- **POC trade-off**: State is committed to repo for visibility
- **No remote infrastructure needed**: Reduces complexity for demo
- **Note**: Production use requires remote backend (S3, Terraform Cloud, etc.)

### Why GitHub Actions?

- **Built-in**: No external CI/CD system needed
- **Natural fit**: Workflows access GitHub directly
- **Audit trail**: Actions logs show exactly what Terraform did

## Folder Reorganization (Phase 1)

The `infra/` folder was restructured into `default/` and `setup/`:

- **`infra/default/`** — Main Terraform configuration (current)
- **`infra/setup/`** — Optional setup modules (future: OIDC for AWS)

This allows:
1. Multiple Terraform "stacks" in the same repo
2. Clear separation between default infrastructure and optional setups
3. Easier onboarding for new configurations

## Workflow: Creating a New Repository

1. Edit `infra/default/repositories/repos.tfvars`
2. Add new entry:
   ```hcl
   "my-new-repo" = {
     description = "Description here"
     visibility  = "private"
     topics      = ["tag1", "tag2"]
   }
   ```
3. Commit and push → Create PR
4. GitHub Actions runs `terraform plan` and comments
5. Review the plan
6. Merge PR
7. GitHub Actions runs `terraform apply`
8. Repository is created on GitHub

## Workflow: Importing Existing Repository

1. Go to **Actions** → **Discover Repository for Import**
2. Enter repository URL (e.g., `https://github.com/org/repo`)
3. Workflow creates PR with discovered configuration
4. Review the auto-generated config in `imports.tfvars`
5. Merge PR
6. Repository is now managed by Terraform

## Security & Access

- **GitHub Token**: Provided via `GH_PROVISIONING_TOKEN` secret
  - Requires `repo` scope (read/write to repositories)
  - Requires `admin:org` scope (manage teams and organization)
- **State Management**: POC commits state to repo (not production-safe)
- **Approval**: All changes require PR review before applying

## Future Enhancements

See `infra/setup/` for planned:
- **OIDC Setup**: Enable GitHub Actions to assume AWS roles
- **Advanced Access Control**: Role-based team and repository permissions
- **Multi-environment Configs**: Separate prod/staging/dev stacks

## Support & Troubleshooting

### Workflow Failed

1. Go to **Actions** tab
2. Select the failed workflow run
3. Expand the failed step
4. Check Terraform error output

### Common Issues

- **GitHub API Rate Limit**: Check `gh api rate_limit`
- **Invalid Token**: Verify `GH_PROVISIONING_TOKEN` has correct scopes
- **Module Not Found**: Ensure `modules/` directory structure is intact
- **State Conflict**: Check Terraform state file integrity

## Related Documentation

- `CONTRIBUTING.md` — How to make changes
- `.ghdp/INSTRUCTIONS.md` — Full technical instructions (agent-focused)
- `README.md` — Quick start and core procedures
