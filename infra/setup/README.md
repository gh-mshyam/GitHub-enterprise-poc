# Infrastructure Setup

Placeholder for infrastructure setup and prerequisites.

## What Goes Here

AWS integration and infrastructure configuration:
- AWS OIDC (OpenID Connect) for GitHub Actions
- Secrets Manager integration for credentials
- Terraform S3 backend configuration
- IAM roles and policies
- Network access and permissions

## What Goes in `infra/default/`

Repository management:
- Repository creation and configuration
- Terraform variables and state
- Team assignments
- Branch protection policies

## TODO

See `infra/default/main.tf` and `.github/workflows/*.yml` for AWS integration TODOs:
- `TODO: Add id-token: write for AWS OIDC`
- `TODO: Add S3 backend configuration`
- `TODO: Replace secrets.GITHUB_TOKEN with AWS Secrets Manager retrieval`
