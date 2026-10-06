# Repository Name

Replace with your project description.

## 📋 Structure

```
├── apps/                    # Applications
├── infra/                   # Terraform infrastructure
├── .github/workflows/       # GitHub Actions workflows
├── Jenkinsfile             # Jenkins pipeline
├── config.yml              # Repository configuration
└── README.md               # This file
```

## 🚀 Quick Start

1. Clone this repository
2. Configure AWS credentials
3. Update `config.yml` with your values
4. Add your application code to `apps/`
5. Add infrastructure code to `infra/default/main.tf`

## 🔄 CI/CD

- **CI**: Runs on pull requests (lint, test, validate)
- **Deploy**: Runs on main branch push (terraform apply)

See `.github/workflows/` for details.

## 🏗️ Infrastructure

Infrastructure is managed with Terraform in `infra/default/`.

```bash
cd infra
terraform init
terraform plan
terraform apply
```

## 📝 Configuration

Update `config.yml` with:
- Repository name
- Team name
- Environment settings
- CI/CD flags

## ⚠️ Important Notes

- `Jenkinsfile`, `config.yml`, and `.github/workflows/` are template-managed files
- Do not edit these directly; they're updated via template sync
- For custom pipeline stages, create `infra/Jenkinsfile`
- For custom workflows, create them in `.github/custom-workflows/`

## 📚 See Also

- `TEMPLATE_README.md` - Template usage guide
- `.ghdp/INSTRUCTIONS.md` - Project guidance
- `infra/default/README.md` - Infrastructure details

## 🤝 Contributing

Follow the guidelines in `.ghdp/INSTRUCTIONS.md`.
