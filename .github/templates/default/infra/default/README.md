# Default Infrastructure Configuration

This folder contains the main Terraform configuration for your infrastructure.

## What's Here

- **`main.tf`** — Provider setup and resource instantiation
- **`variables.tf`** — Input variables and their definitions
- **`modules/`** — Reusable Terraform modules
- **`repositories/`** — Configuration files (.tfvars) for your resources

## Quick Start

```bash
cd infra/default
terraform init
terraform plan -var-file=repositories/repos.tfvars
```

## Structure

```
infra/default/
├── main.tf                  # Infrastructure code
├── variables.tf             # Variable definitions
├── modules/                 # Reusable modules
│   ├── repository/          # Repository module
│   └── teams/               # Teams module
└── repositories/            # Configuration files
    ├── repos.tfvars         # Repository configs
    ├── teams.tfvars         # Team configs
    └── imports.tfvars       # Import configs
```

## Next Steps

1. Edit `repositories/*.tfvars` files to define your resources
2. Run `terraform plan` to preview changes
3. Merge PR to apply changes automatically

See `conf/CONTRIBUTING.md` for detailed workflows.
