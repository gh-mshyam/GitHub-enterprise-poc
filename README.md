# GitHub Enterprise Repository Provisioning POC

**Production-ready architecture for autonomous repository provisioning with parent-child workflow governance.**

- **Git-native** — Infrastructure as Code with audit trail
- **Risk-based automation** — Tier 0 (auto-approve) vs Tier 1 (manual review)
- **Parent-child workflows** — Immutable governance, scalable to 100s of repos
- **Test-first design** — 31 unit tests + integration tests via act
- **Enterprise-ready** — Complete governance framework with CODEOWNERS + immutability

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
├── infra/
│   ├── main.tf
│   ├── variables.tf
│   ├── terraform.tfstate (committed)
│   └── modules/
│       ├── repository/
│       │   ├── main.tf
│       │   ├── variables.tf
│       │   └── outputs.tf
│       └── team/ (scaffold)
├── repositories/
│   └── example.tfvars
├── scripts/
│   ├── classify_risk.py
│   └── modify_tfvars.py
├── gHDPL/
├── codex/
└── apps/
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

- `terraform/terraform.tfstate` is committed to git (POC only)
- Enables workflow isolation and reproducibility
- **Production:** Migrate to **S3 + DynamoDB** for locking/encryption
- **Future Plan:** State migration to S3 backend in Phase 4

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

- [ ] **Phase 4:** Migrate state backend to S3 + DynamoDB (locking, encryption)
- [ ] Add CODEOWNERS for Tier 1 approval routing
- [ ] Set up cost estimation for destructive operations
- [ ] Audit existing repos via `terraform import`
- [ ] Test approval workflow with real teams
- [ ] Document operational runbooks
- [ ] Set up external audit logging

## Parent-Child Workflow Architecture

This POC demonstrates a **scalable governance model** where:
- **Parent (main branch):** Immutable workflows + risk rules (v1.0 tagged)
- **Child (develop branch):** References parent, uses parent's governance logic

### Parent Components (Immutable)

```
main branch (v1.0 release)
├── scripts/classify_risk.py ← Risk rules (governance)
├── .github/workflows/plan.yml ← Risk classification workflow
└── .github/workflows/apply.yml ← Terraform execution workflow
```

### Child Components (Customizable)

```
develop branch
├── .github/workflows/plan-child.yml ← Fetches parent, verifies immutability
├── .github/workflows/apply-child.yml ← Uses parent logic
└── repositories/example.tfvars ← Child's own repo definitions
```

### How Child Uses Parent

1. **Child PR triggers** → `plan-child.yml` starts
2. **Fetch parent components** → `git show origin/main:scripts/classify_risk.py`
3. **Verify immutability** → Checks divergence from parent@main
4. **Execute parent logic** → Uses parent's risk classification
5. **Result** → Tier 0 or Tier 1 classification (from parent)

### Benefits

✅ **Centralized governance** — 1 set of rules for 100s of repos  
✅ **No drift** — Children always use parent's latest logic  
✅ **Immutable enforcement** — Can't bypass governance locally  
✅ **Versioning** — Track rule changes with semantic tags (v1.0, v1.1)  
✅ **Scalability** — 1 parent, infinite children

### For Enterprise Replication

1. Create central repo (e.g., `common-workflows`)
2. Move parent components there
3. Child repos reference `common-workflows@main` or `common-workflows@v1.0`
4. Update `workflow-contract.json` with parent reference
5. All children auto-sync to latest parent rules

See `.ghdp/PARENT_ARCHITECTURE.md` for detailed parent-child model.

---

## Testing & Validation

### Unit Tests (pytest)

```bash
pytest tests/ -v
# 31 tests covering:
# - Tier 0/1 classification (18 tests)
# - CODEOWNERS detection (5 tests)
# - Contract resolution (8 tests)
```

**Test matrix:**
```
Tier 0: private + standard name + add/modify = auto-approve
Tier 1: delete | public | bad naming = manual review
CODEOWNERS: present | missing | empty
Contract: immutable component validation
```

### Integration Tests (act)

```bash
# Test parent workflows
act pull_request -j plan
act push -j apply

# Test child workflows
act pull_request -j plan -W .github/workflows/plan-child.yml
act push -j apply -W .github/workflows/apply-child.yml
```

### Test Coverage

| Component | Tests | Coverage |
|-----------|-------|----------|
| classify_risk.py | 18 | All Tier 0/1 scenarios |
| check_codeowners.py | 5 | Present, missing, empty |
| resolve_contract.py | 8 | Load, validate, immutability |
| Workflows | act | Plan, apply, child references |

See `tests/README.md` for full test execution guide.

---

## Contract-Based Integration

**File:** `workflow-contract.json` (defines parent-child relationship)

```json
{
  "parent_components": {
    "scripts": [
      {
        "name": "classify_risk.py",
        "immutable": true,
        "reason": "Core governance logic"
      }
    ],
    "workflows": [
      {"name": "plan.yml", "immutable": true},
      {"name": "apply.yml", "immutable": true}
    ]
  },
  "child_requirements": {
    "inherit_from_parent": ["scripts/classify_risk.py"],
    "can_override": ["scripts/modify_tfvars.py"]
  }
}
```

Child validates contract before execution:
```bash
python3 scripts/resolve_contract.py
# ✓ All immutable components present
# ✓ Contract resolved successfully
```

---

## CODEOWNERS Integration

**File:** `.github/CODEOWNERS` (code ownership framework)

```
* @gh-mshyam
infra/ @gh-mshyam
scripts/classify_risk.py @gh-mshyam
.ghdp/contracts/ @gh-mshyam
```

**PR Comments include:**
- Risk tier (Tier 0 or 1)
- CODEOWNERS status (✓ assigned, ⚠️ missing, ℹ️ info)

Tier 1 PRs flag missing CODEOWNERS as concern for manual review.

---

## References

- [Terraform GitHub Provider](https://registry.terraform.io/providers/integrations/github/latest)
- [GitHub Actions](https://docs.github.com/en/actions)
- [GitHub CLI](https://cli.github.com/)
- **Architecture docs:** `.ghdp/PARENT_ARCHITECTURE.md`
- **Child implementation:** `.ghdp/CHILD_IMPLEMENTATION.md`
- **Contract spec:** `workflow-contract.json`
- **Test guide:** `tests/README.md`
