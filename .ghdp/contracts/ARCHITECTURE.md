# Architecture & Design Principles

## System Overview

Git-native, autonomous repository provisioning using Terraform + GitHub Actions + deterministic risk classification.

**Core Flow:**
```
Request (workflow_dispatch or git PR)
    ↓
plan.yml: terraform plan + classify_risk.py
    ↓
Tier 0 (safe) → auto-merge | Tier 1 (risky) → manual approval
    ↓
apply.yml: terraform apply + state commit
    ↓
Repository created/deleted on GitHub
```

## Design Principles

1. **Git as Source of Truth** — All changes through PRs, auditable, reversible
2. **Deterministic Risk Classification** — Same rules always apply (policy as code)
3. **Risk-Based Automation** — Tier 0 instant, Tier 1 requires human confirmation
4. **Infrastructure as Code** — Terraform defines repos, reproducible deployments
5. **Local Backend (POC)** — State committed to git; migrate to S3 in Phase 4

## Risk Tiers

### Tier 0 (Auto-Approved)
**All criteria must be met:**
- Visibility: `private`
- Name: matches `^[a-z0-9][a-z0-9-]*$`
- Operation: add/modify only (no delete)

**Action:** Auto-merge PR → apply.yml runs → repo created instantly

### Tier 1 (Manual Review)
**Any criterion triggers Tier 1:**
- Public or internal visibility
- Delete operation
- Non-standard naming
- Team attachment changes

**Action:** PR waits for manual approval before apply.yml runs

## Workflows

### plan.yml
- **Trigger:** PR to main
- **Steps:** terraform plan → convert to JSON → classify_risk.py → post comment
- **Output:** Risk tier classification visible in PR

### apply.yml
- **Trigger:** PR merge to main or manual dispatch
- **Steps:** terraform apply → commit terraform.tfstate
- **Output:** Repos created/deleted, state updated

### request-operation.yml
- **Trigger:** Manual workflow_dispatch (business user)
- **Steps:** validate input → modify tfvars → create PR → plan/classify/apply
- **Note:** Requires PAT with `createPullRequest` scope (Phase 4 fix)

## Code Structure

```
infra/
  ├── main.tf (provider + root module)
  ├── variables.tf
  └── modules/
      ├── repository/ (github_repository resource)
      └── team/ (scaffold for future)

repositories/
  └── example.tfvars (repo definitions)

scripts/
  ├── classify_risk.py (deterministic rules)
  └── modify_tfvars.py (workflow helper)

.github/workflows/
  ├── plan.yml
  ├── apply.yml
  └── request-operation.yml
```

## Compliance & Audit

- All decisions logged in PR comments
- All changes tracked in git history
- Terraform state committed (audit trail)
- Fully reversible via git revert

## Future Phases

- Phase 4: S3 backend migration (state locking, encryption)
- Phase 5: Team management workflow
- Phase 6: Multi-org federation
