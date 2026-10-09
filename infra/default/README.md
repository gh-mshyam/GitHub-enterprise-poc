# Repository Management (Default)

Terraform configuration for managing GitHub repositories.

## Files

- `main.tf` — Terraform root config and provider setup
- `variables.tf` — Input variable definitions
- `repos.tfvars` — Repository configuration (single source of truth)
- `modules/` — Reusable Terraform modules
  - `repository/` — GitHub repository module
  - `teams/` — GitHub teams module

## What Goes Here

Repository management only:
- Repository creation, update, deletion
- Team assignments
- Branch protection policies
- Repository settings

## What Goes in `infra/setup/`

Infrastructure setup and prerequisites:
- AWS OIDC configuration
- GitHub Actions secrets
- Terraform state backend (S3)
- IAM roles and policies
- Network and access setup

## Usage

Edit `repos.tfvars` to manage repositories. Follow the 3-step workflow:
1. Create branch
2. Create PR
3. Deploy

See `conf/QUICKSTART.md` for details.
