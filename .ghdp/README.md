# Governance & Templates

Central hub for repository governance, instructions, and templates.

---

## Contents

### 📋 Instructions

**`INSTRUCTIONS.md`** — Complete agent-agnostic guidance
- Project overview and workflow
- Code principles and folder rules
- Testing checklist and common tasks
- Production readiness checklist

### 🧪 Testing

**`TESTING.md`** — Validation and testing approach
- Local validation steps (Terraform, Python, config)
- GitHub Actions testing procedures
- Manual testing checklist
- Testing scenarios for key features
- Troubleshooting guide

### 📦 Templates

**See: `.github/templates/`** — GHDP CLI standard repository template

Standard structure for all new repositories:

```
.github/templates/
├── .github/workflows/
│   ├── ci.yml              (Lint, test, validate, security scan)
│   └── deploy.yml          (Infrastructure deployment)
├── apps/
│   └── apps.json           (Application manifest)
├── infra/
│   └── default/
│       ├── main.tf         (Terraform template)
│       └── variables.tf    (Terraform variables)
├── config.yml              (Repository configuration)
├── prisma-cloud-config.yml (Security policies)
├── Jenkinsfile             (Jenkins CI/CD pipeline)
├── README.md               (Project documentation)
└── TEMPLATE_README.md      (Template usage guide)
```

**Features:**
- ✅ GitHub Actions: CI & Deploy workflows
- ✅ Jenkins: Pipeline with plan/apply stages
- ✅ Terraform: Infrastructure scaffolding
- ✅ Security: Prisma Cloud scanning config
- ✅ Documentation: Ready-to-customize templates

### 🏗️ Architecture Documents

**`TEST_SPECIFICATIONS.md`** — Complete test specifications

---

## Quick Reference

### For New Repository Creation

1. Provisioning system creates repo
2. Applies `repository_template = "ghdp-cli"`
3. Template files auto-populated from `.github/templates/`
4. New repo has:
   - GitHub Actions workflows (CI + Deploy)
   - Jenkins pipeline
   - Terraform scaffolding
   - Security & testing configs

### For Team Guidance

→ Read `INSTRUCTIONS.md` for complete project guidance

### For Testing

→ Read `TESTING.md` for validation procedures

### For Custom Workflows

→ Customize files in `templates/` for different templates

---

## File Structure

```
.ghdp/
├── README.md                (This file - Governance hub)
├── INSTRUCTIONS.md          (Complete guidance)
├── TESTING.md               (Validation & testing)
└── TEST_SPECIFICATIONS.md   (Test specs)

.github/templates/           (GHDP CLI template)
├── README.md
├── TEMPLATE_README.md
├── Jenkinsfile
├── config.yml
├── prisma-cloud-config.yml
├── .github/workflows/
│   ├── ci.yml
│   └── deploy.yml
├── apps/apps.json
└── infra/default/
    ├── main.tf
    └── variables.tf
```

---

## Usage

### Read First

1. **New agent/team member** → `INSTRUCTIONS.md`
2. **Testing & validation** → `TESTING.md`
3. **Creating new repo** → `templates/TEMPLATE_README.md`

### Customize

To use a different template:
1. Create new subfolder in `.github/templates/`
2. Add custom structure and workflows
3. Update repository_template in provisioning config
4. New repos will use that template instead

---

## Key Points

- **Single source of truth** — All governance in `.ghdp/`
- **Agent-agnostic** — Works with Claude, Codex, and any CI/CD
- **Reusable templates** — Standard structure for consistency
- **Both Jenkins & GitHub Actions** — Enterprise flexibility
- **Security-first** — Prisma Cloud scanning included
- **Well-documented** — Clear procedures and guides

---

## Support

For questions about:
- **Project guidance** → See `INSTRUCTIONS.md`
- **Testing procedures** → See `TESTING.md`
- **New repository setup** → See `templates/TEMPLATE_README.md`
- **Repository provisioning** → See root `README.md`
