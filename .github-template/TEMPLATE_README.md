# GitHub Enterprise POC - Repository Template

This folder contains the standard template for new repositories created via the provisioning system.

## What's Included

**GHDP CLI Standard Structure:**
- ✅ `Jenkinsfile` — Jenkins CI/CD pipeline
- ✅ `.github/workflows/` — GitHub Actions workflows
- ✅ `apps/` — Application code scaffolding
- ✅ `infra/default/` — Terraform infrastructure template
- ✅ `config.yml` — Repository configuration
- ✅ `prisma-cloud-config.yml` — Security scanning config
- ✅ `README.md` — Project documentation

## Workflows Included

### GitHub Actions

**1. CI Workflow (`.github/workflows/ci.yml`)**
- Lint (flake8, black, isort)
- Test (pytest)
- Validate infrastructure (Terraform)
- Security scan (Trivy)
- Runs on: Pull requests

**2. Deploy Workflow (`.github/workflows/deploy.yml`)**
- Terraform plan & apply
- AWS credentials via OIDC
- Environment-specific deployment
- Runs on: Push to main

### Jenkins

**Jenkinsfile**
- Plan & apply stages
- Environment selection (dev/staging/prod)
- Dry-run support
- Post-deployment validation

## How Repos Get This Template

When a new repository is created via provisioning with `repository_template = "ghdp-cli"`, these files are automatically added:

```
new-repository/
├── .github/workflows/ci.yml → CI/CD child workflows
├── .github/workflows/deploy.yml → Deployment workflows
├── apps/apps.json → Application manifest
├── infra/default/main.tf → Terraform template
├── infra/default/variables.tf → Terraform variables
├── config.yml → Repository config
├── prisma-cloud-config.yml → Security policies
├── Jenkinsfile → Jenkins pipeline
└── README.md → Project documentation
```

## Customization

After a new repository is created from this template:

1. **Update README.md** — Replace placeholders with actual project info
2. **Update config.yml** — Set repository name, team, language
3. **Customize Jenkinsfile** — Add project-specific stages
4. **Adjust workflows** — Tailor CI/CD to your needs
5. **Update Terraform** — Add actual infrastructure code

## File Descriptions

| File | Purpose |
|------|---------|
| `Jenkinsfile` | Jenkins pipeline definition |
| `.github/workflows/ci.yml` | Lint, test, validate |
| `.github/workflows/deploy.yml` | Infrastructure deployment |
| `apps/apps.json` | Application manifest |
| `infra/default/main.tf` | Infrastructure code |
| `infra/default/variables.tf` | Terraform variables |
| `config.yml` | Repository configuration |
| `prisma-cloud-config.yml` | Security scanning rules |
| `README.md` | Project documentation |

## Next Steps

1. New repo is created from this template
2. Team customizes files for their use case
3. CI/CD workflows run on every PR and push
4. Infrastructure is deployed via Jenkins or GitHub Actions

## Support

For template updates or issues, contact the DevOps/Platform team or submit an issue to the provisioning repository.
