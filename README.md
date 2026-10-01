# GitHub Enterprise Repository Provisioning POC

A proof-of-concept for git-native GitHub repository provisioning using Terraform and GitHub Actions workflows with risk-based approval gates.

## Overview

This POC demonstrates how to provision GitHub repositories declaratively using Infrastructure-as-Code (Terraform) with a git-native workflow:
- **Code changes** → **Pull Request** → **Risk classification** → **Auto-merge (Tier 0)** or **Manual review (Tier 1)** → **Terraform apply** → **Repositories created/updated**

### Key Features

- **Git-native provisioning**: All changes via PRs (auditability, version control)
- **Risk-based approval gates**: Tier 0 (safe ops, auto-merge) vs Tier 1 (dangerous ops, manual review)
- **Business user workflow**: `workflow_dispatch` interface—no Git knowledge required
- **Deterministic classification**: Python-based risk classifier with explicit rules
- **Local state persistence**: Terraform state committed to repo (POC choice)
- **Parallel-safe Terraform**: `-parallelism=1` prevents GitHub API timeouts

## Repository Structure

```
.
├── .github/workflows/           # GitHub Actions workflows
│   ├── plan.yml                # PR trigger: terraform plan + risk classification
│   ├── apply.yml               # Push trigger: terraform apply + state commit
│   └── request-operation.yml    # Workflow dispatch: business user interface
├── terraform/                   # Terraform infrastructure code
│   ├── main.tf                 # Provider config + root module
│   ├── variables.tf            # Input variables
│   ├── terraform.tfstate       # State file (committed for POC)
│   ├── .terraform.lock.hcl     # Provider lock file
│   └── modules/
│       └── repository/         # GitHub repository module
│           ├── main.tf         # Repository resource + team attachments
│           ├── variables.tf    # Module inputs
│           └── outputs.tf      # Module outputs
├── repositories/               # Repository definitions
│   └── example.tfvars          # HCL format: repo list, teams, settings
├── scripts/                    # Helper scripts
│   ├── classify_risk.py        # Risk classification logic
│   └── modify_tfvars.py        # Programmatic tfvars modification
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

## How It Works

### 1. Manual Repository Creation (Git-native)

**User modifies `repositories/example.tfvars`:**
```hcl
repositories = {
  "my-service" = {
    description = "My service repository"
    visibility  = "private"
    teams = {
      "platform-team" = "push"
    }
  }
}
```

**Create PR:**
```bash
git checkout -b add-my-service
git commit -am "Add my-service repository"
git push origin add-my-service
# Open PR on GitHub
```

**Workflow Execution:**
1. `plan.yml` triggers on PR
2. Runs `terraform plan`
3. Python classifier determines Tier 0 (safe) or Tier 1 (dangerous)
4. Posts classification to PR comment
5. Tier 0 → auto-merges PR
6. `apply.yml` triggers on merge
7. `terraform apply` creates repos
8. State file committed back to main

### 2. Business User Workflow (No Git Required)

**GitHub UI → Actions → request-operation workflow:**

**Inputs:**
- `operation`: "create" or "delete"
- `repo_name`: Repository name (lowercase, hyphens only)
- `visibility`: "private" or "internal"
- `team`: Team name to attach (optional)
- `description`: Repository description

**Result:**
- Workflow modifies `repositories/example.tfvars`
- Creates PR automatically
- Auto-merges if Tier 0 (safe operation)
- Terraform creates/deletes repository

## Risk Classification Rules

### Tier 0 (Auto-merge, no review)
✅ Private visibility  
✅ Standard repo name (`^[a-z0-9][a-z0-9-]*$`)  
✅ No delete operations  
✅ Existing teams only  

**Result:** PR auto-merges, apply runs immediately

### Tier 1 (Manual review required)
❌ Public or internal visibility  
❌ Non-standard repo name  
❌ Delete operations  
❌ New team creation  

**Result:** PR requires manual review before merge

## Setup & Configuration

### Prerequisites

- Terraform 1.9.8+
- GitHub CLI (`gh`)
- GitHub Personal Access Token with `repo`, `admin:org_hook`, `workflow` scopes

### Initial Setup

**1. Clone repository:**
```bash
git clone https://github.com/gh-mshyam/GitHub-enterprise-poc.git
cd GitHub-enterprise-poc
```

**2. Configure Terraform:**
```bash
cd terraform
terraform init
```

**3. Set GitHub token (in GitHub repo secrets):**

Add a secret `GH_PROVISIONING_TOKEN` to the repository with your PAT.

**4. Create first repository (manual):**
```bash
# Edit repositories/example.tfvars with your first repo
git checkout -b init-repos
git commit -am "Initialize example repositories"
git push origin init-repos
# Open PR and let workflow handle it
```

## Usage Examples

### Create Private Repository (Auto-merge)

**Option 1: Via Git (manual)**
```bash
# Edit repositories/example.tfvars
repositories = {
  "my-api" = {
    description = "My API service"
    visibility  = "private"
    teams = {
      "platform-team" = "push"
    }
  }
}
# Commit and push
```

**Option 2: Via Workflow Dispatch (business user)**
```bash
gh workflow run request-operation.yml \
  -f operation=create \
  -f repo_name=my-api \
  -f visibility=private \
  -f team=platform-team \
  -f description="My API service"
```

### Delete Repository (Manual review required)

**Remove from `repositories/example.tfvars` and create PR:**
```bash
# Edit: remove "my-api" entry
git checkout -b delete-my-api
git commit -am "Remove my-api repository"
git push origin delete-my-api
# Open PR → Tier 1 classification → requires manual approval
```

## State Management

**Important:** This POC commits `terraform/terraform.tfstate` to git (unconventional but intentional for POC).

**Why:**
- Workflow isolation: Each workflow run is isolated; state must persist
- No external S3/backend: Local backend suitable for POC
- Auditability: State changes tracked in git history

**Production note:** Use remote backend (S3, Terraform Cloud, etc.) in production.

## Troubleshooting

### Workflow Not Triggering

- Check `.github/workflows/*.yml` syntax: `gh workflow view plan.yml`
- Verify GitHub token has correct scopes: `gh auth status`
- Check workflow permissions in repo settings

### Terraform Apply Fails

- Verify `GH_PROVISIONING_TOKEN` is set correctly
- Check GitHub API rate limits: `gh api rate_limit`
- Review apply job logs in Actions tab

### Risk Classification Wrong

- Edit `scripts/classify_risk.py` to adjust rules
- Tier 0 rules: lines 44–85
- Tier 1 rules: lines 86–95
- Commit changes and re-run workflow

## Limitations

- **Delete operations**: Requires `terraform import` setup (deferred)
- **Branch protection**: Free/private GitHub plans have limited support
- **Team auto-creation**: Not implemented (manual team creation required)

## Next Steps

- **Phase 4**: `terraform import` for existing repository state synchronization
- **Phase 5**: Team auto-creation workflow
- **Phase 6**: Multi-org support

## References

- [Terraform GitHub Provider](https://registry.terraform.io/providers/integrations/github/latest)
- [GitHub Actions Workflows](https://docs.github.com/en/actions/using-workflows)
- [GitHub CLI](https://cli.github.com/)
