# Template Guide

This repository was auto-initialized with the standard GHDP CLI repo-scaffold template.

## ✅ What You Have

Your repository now includes:

- ✅ **Jenkinsfile** - Jenkins CI/CD pipeline
- ✅ **GitHub Actions workflows** - CI and deploy automation
- ✅ **Terraform scaffold** - Infrastructure-as-Code starter
- ✅ **Security configs** - Prisma Cloud configuration
- ✅ **Applications manifest** - apps.json
- ✅ **Repository config** - config.yml

## 📝 Next Steps

### 1. Customize Configuration
```bash
# Edit with your project details
vim config.yml
```

Update:
- `repository.name` - Your repo name
- `repository.team` - Your team name
- `repository.language` - Your primary language
- `environments` - Your deployment targets

### 2. Update Documentation
```bash
# Edit main README
vim README.md
```

Replace template content with:
- Project description
- How to run the application
- How to deploy
- Architecture notes

### 3. Add Your Code
```bash
# Add application code
mkdir -p apps/my-app
# Add your source code here
```

### 4. Configure Infrastructure
```bash
# Edit Terraform configuration
vim infra/default/main.tf
```

Add your AWS resources (S3, RDS, EC2, etc.)

### 5. Customize Applications Manifest
```bash
# Edit app manifest
vim apps/apps.json
```

List your applications and their details.

## 🚀 Deployment

### First Deployment
```bash
cd infra
terraform init
terraform plan
terraform apply
```

### CI/CD Pipeline
- **Push to main** → GitHub Actions CI runs (lint, test, validate)
- **Merge to main** → GitHub Actions Deploy runs (terraform apply)
- **Jenkins available** for additional pipeline stages

## ⚠️ Template Managed Files

These files are **template-managed** and will be updated automatically:
- `Jenkinsfile`
- `config.yml` (metadata only, values are customizable)
- `.github/workflows/ci.yml`
- `.github/workflows/deploy.yml`
- `infra/default/main.tf`
- `infra/default/variables.tf`
- `prisma-cloud-config.yml`

**Do not edit these directly**. If you need custom versions:
1. Create custom files in `custom/` directory
2. Reference them in Jenkins or GitHub Actions
3. Maintain template-managed files as-is for consistency

## 📚 Resources

- **CI/CD Workflows**: `.github/workflows/`
- **Infrastructure**: `infra/default/`
- **Application Code**: `apps/`
- **Security**: `prisma-cloud-config.yml`
- **Configuration**: `config.yml`

## 🔄 Template Updates

This repository periodically receives template updates for:
- New security scanning rules
- Updated CI/CD best practices
- Infrastructure improvements
- Bug fixes

Updates are automatically applied. All your customizations are preserved.

## ❓ Questions?

See:
- `.ghdp/INSTRUCTIONS.md` - Complete project guidance
- `.ghdp/TESTING.md` - Testing procedures
- Infrastructure team documentation
