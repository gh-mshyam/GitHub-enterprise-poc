# GitHub Enterprise Repository Provisioning POC

Git-native, autonomous repository provisioning using Terraform + GitHub Actions + risk-based approval gates.

## How It Works

```
Business User Request (workflow_dispatch)
    ↓
request-operation.yml (create/delete repo)
    ├─ Validate input
    ├─ Modify repositories/example.tfvars
    └─ Create PR
         ↓
plan.yml (auto-triggers on PR)
    ├─ Run: terraform plan
    ├─ Classify risk (Python script)
    └─ Post decision to PR
         ↓
    ┌────────────────┬────────────────┐
    ↓                ↓
 TIER 0          TIER 1
 (Safe)          (Risky)
    ↓                ↓
Auto-merge      Manual Approval
    ↓                ↓
apply.yml (on merge)
    ├─ terraform apply
    ├─ Create/delete repos
    └─ Commit state
         ↓
✅ Done (audited in git)
```

## Risk Classification

### Tier 0 (Auto-Approved)
✅ Visibility = private  
✅ Name matches `^[a-z0-9][a-z0-9-]*$`  
✅ Only add/modify (no delete)  

→ **Result:** Auto-merge, instant provisioning

### Tier 1 (Manual Review)
❌ Public or internal visibility  
❌ Delete operation  
❌ Bad naming convention  

→ **Result:** PR waits for manual approval

## Workflows

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `plan.yml` | PR to main | Terraform plan + risk classification |
| `apply.yml` | Push to main | Execute terraform, commit state |
| `request-operation.yml` | Manual dispatch | Business user interface (create/delete) |

## Directory Structure

```
.
├── .github/workflows/
│   ├── plan.yml
│   ├── apply.yml
│   └── request-operation.yml
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── terraform.tfstate (committed)
│   └── modules/repository/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
├── repositories/
│   └── example.tfvars
└── scripts/
    ├── classify_risk.py
    └── modify_tfvars.py
```

## Usage

### For Engineers (Git-native)
```bash
# Edit repositories/example.tfvars
git checkout -b add-my-repo
git add repositories/example.tfvars
git commit -m "Add my-repo"
git push

# Open PR → plan.yml runs → classified as Tier 0 or 1
# If Tier 0: auto-merges → apply.yml runs → repo created
# If Tier 1: waits for manual merge
```

### For Business Users (No Git Required)
1. Go to: **Actions** → **Request Repository Operation** → **Run workflow**
2. Fill form: operation (create/delete), repo_name, visibility, description
3. Click **Run**
4. System handles everything automatically

## Key Principles

1. **Git as source of truth** — all changes through PRs, auditable
2. **Deterministic classification** — same rules always apply
3. **Risk-based automation** — safe ops auto-approved, risky ops require review
4. **Infrastructure as Code** — Terraform manages repos, reproducible
5. **Local backend (POC)** — state committed to git (production: use S3/Terraform Cloud)

## Code Principles

- **Tier 0 rules** in `scripts/classify_risk.py` (line ~40-50)
- **Tier 1 rules** in `scripts/classify_risk.py` (line ~50-60)
- **Repo module** in `terraform/modules/repository/main.tf`
- **Tfvars** in `repositories/example.tfvars`

## State Management

- `terraform/terraform.tfstate` is committed to git
- Enables workflow isolation and reproducibility
- **Production:** Migrate to remote backend (S3 + DynamoDB or Terraform Cloud)

## Compliance & Audit

Every operation is fully audited:
- ✅ PR comments show risk decision
- ✅ Git commits track all tfvars changes
- ✅ Terraform state diffs visible in git
- ✅ GitHub Actions logs all steps

Trace any repo: `git log --all -- repositories/example.tfvars`

## Troubleshooting

**PR not auto-merging (expected Tier 0)?**
- Check plan.yml comment for actual tier and reasons

**Terraform apply fails?**
- Verify `GH_PROVISIONING_TOKEN` secret exists with `repo` scope
- Check GitHub API rate limit: `gh api rate_limit`

**Risk classification wrong?**
- Edit `scripts/classify_risk.py` and commit
- Re-run workflow with new rules

## Known Limitations

- `request-operation.yml` needs PAT with `createPullRequest` scope (GITHUB_TOKEN insufficient)
- Team attachment not supported on personal GitHub accounts
- Branch protection requires GitHub Pro on private repos
- Delete operation always Tier 1 (safe default for governance)

## Production Checklist

- [ ] Update backend to S3 or Terraform Cloud
- [ ] Add CODEOWNERS for Tier 1 approval routing
- [ ] Set up cost estimation for destructive operations
- [ ] Audit existing repos via `terraform import`
- [ ] Test approval workflow with real teams
- [ ] Document operational runbooks
- [ ] Set up external audit logging

## References

- [Terraform GitHub Provider](https://registry.terraform.io/providers/integrations/github/latest)
- [GitHub Actions](https://docs.github.com/en/actions)
- [GitHub CLI](https://cli.github.com/)
