# Repository Name

Brief description of what this repository does.

## Structure

```
.github/workflows/     - GitHub Actions CI/CD workflows (child workflows)
apps/                  - Application code and configurations
infra/                 - Infrastructure-as-Code (Terraform)
  └── default/         - Default infrastructure configuration
config.yml             - Repository configuration
prisma-cloud-config.yml - Security scanning configuration
Jenkinsfile            - Jenkins pipeline definition
```

## Quick Start

### Local Development

1. Clone repository
2. Install dependencies
3. Run locally: `make dev` or equivalent

### CI/CD

**GitHub Actions:**
- Child workflows automatically triggered on PR and merge
- See `.github/workflows/` for details

**Jenkins:**
- Triggered by Jenkinsfile
- See Jenkinsfile for pipeline stages

## Configuration

- `config.yml` - Application and deployment config
- `prisma-cloud-config.yml` - Security scanning rules

## Deployment

Deployments are automated via:
- GitHub Actions workflows (for GitHub-based CI/CD)
- Jenkins pipeline (for enterprise CI/CD integration)

See CI/CD workflow files for deployment process.

## Support

For issues or questions, contact the team or create an issue in this repository.
