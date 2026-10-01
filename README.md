# GitHub Enterprise Repository Provisioning POC

**A git-native, autonomous Infrastructure-as-Code system for GitHub repository provisioning using Terraform and risk-based approval gates.**

---

## Executive Summary

This system enables **autonomous, compliant repository provisioning** by combining:
1. **Git-native workflow** — all operations flow through PRs (auditability, version control)
2. **Risk-based classification** — deterministic rules separate safe ops (auto-approve) from risky ones (manual review)
3. **Business user interface** — no Git knowledge required; operators use `workflow_dispatch` to request operations
4. **Terraform IaC** — infrastructure defined in code, deployable locally or in CI/CD

**Business Impact:**
- ✅ Instant provisioning for safe operations (Tier 0)
- ✅ Compliance-ready (all decisions audited in git)
- ✅ Zero-trust operations (risky ops require human confirmation)
- ✅ DevOps-friendly (uses standard tools and patterns)

## Architecture & Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                 Business User (Non-Technical)                │
│  Requests repo creation/deletion via workflow_dispatch UI   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
          ┌──────────────────────────────┐
          │  request-operation.yml       │
          │  (Workflow Dispatch Handler) │
          ├──────────────────────────────┤
          │ 1. Validate input (naming)   │
          │ 2. Modify tfvars             │
          │ 3. Create PR                 │
          └────────────┬─────────────────┘
                       │
                       ▼
          ┌──────────────────────────────┐
          │  plan.yml (Auto-triggered)   │
          │  (PR Event Handler)          │
          ├──────────────────────────────┤
          │ 1. Run terraform plan        │
          │ 2. Parse plan → JSON         │
          │ 3. Classify risk (Python)    │
          │ 4. Post decision to PR       │
          └────────────┬─────────────────┘
                       │
         ┌─────────────┴──────────────┐
         │                            │
    ┌────▼──────────┐       ┌────────▼────────┐
    │   TIER 0      │       │    TIER 1       │
    │  (Safe Ops)   │       │  (Risky Ops)    │
    ├───────────────┤       ├─────────────────┤
    │ Auto-merge    │       │ Manual approval │
    │ immediately   │       │ required        │
    └────┬──────────┘       └────────┬────────┘
         │                          │
         ▼                          ▼ (after manual merge)
    ┌──────────────────────────────────┐
    │  apply.yml (Merge Event Handler)  │
    │  (Execute Terraform)              │
    ├───────────────────────────────────┤
    │ 1. terraform apply                │
    │ 2. Create/destroy/update repos    │
    │ 3. Commit terraform.tfstate       │
    └──────────────────────────────────┘
         │
         ▼
    ✅ Repository created/deleted on GitHub
    📝 All decisions audited in git history
```

---

## Code Structure

```
.
├── .github/workflows/
│   ├── plan.yml                 # PR trigger: terraform plan + risk classification
│   ├── apply.yml                # Main push trigger: execute terraform
│   └── request-operation.yml    # Manual dispatch: business user interface
├── terraform/
│   ├── main.tf                  # Root module + provider config
│   ├── variables.tf             # Inputs (github_token, owner, repositories)
│   ├── terraform.tfstate        # Committed state (audit trail)
│   └── modules/repository/
│       ├── main.tf              # github_repository resource
│       ├── variables.tf         # Per-repo config
│       └── outputs.tf           # Repository outputs
├── repositories/
│   └── example.tfvars           # Repository definitions (HCL format)
├── scripts/
│   ├── classify_risk.py         # Deterministic risk classification
│   └── modify_tfvars.py         # Tfvars generator (workflow helper)
└── README.md                    # This file
```

## Workflows & Triggers

### 1. `plan.yml` — Terraform Plan + Risk Classification

**Trigger:** Pull request to `main`

**Steps:**
1. **Checkout & Initialize Terraform**
   - Load code at PR branch state
   - Initialize Terraform with GitHub provider

2. **Terraform Plan**
   - Run `terraform plan` against tfvars
   - Generate JSON output for analysis

3. **Risk Classification**
   - Python script parses plan JSON
   - Applies deterministic rules (see below)
   - Outputs: Tier 0 or Tier 1

4. **Post Decision to PR**
   - Comment shows: risk tier, reasons, required action
   - Visible to all reviewers

**Outputs:**
- Classification comment on PR
- Terraform plan artifact (for review)
- Exit code: success = classification done

---

### 2. `apply.yml` — Execute Terraform

**Trigger:** 
- Push to `main` branch
- Manual `workflow_dispatch` (for testing)

**Steps:**
1. **Checkout Latest Main**
2. **Terraform Init & Apply**
   - Run `terraform apply -auto-approve` (non-interactive)
   - Uses tfvars to provision repos
3. **Commit State Back**
   - Add `terraform.tfstate` changes to git
   - Commit and push to main
   - Ensures state stays in sync

**Permissions:** `contents:write` (to commit state)

---

### 3. `request-operation.yml` — Business User Interface

**Trigger:** Manual `workflow_dispatch` (GitHub Actions → Workflows → Request Repository Operation)

**Inputs:**
```
operation      : "create" or "delete"
repo_name      : lowercase, hyphens only (validated)
visibility     : "private" or "internal" (create only)
team           : optional, team name (create only)
description    : optional, repo description (create only)
```

**Steps:**
1. **Validate Input**
   - Name format: must match `^[a-z0-9][a-z0-9-]*$`
   - Required fields check

2. **Modify tfvars**
   - Call `modify_tfvars.py` script
   - Add or remove repo entry
   - Generates clean HCL

3. **Create PR**
   - Branch name: `ops/{operation}-{repo_name}-{timestamp}`
   - PR title: `[{operation}] {repo_name}`
   - Includes operation metadata in PR body

4. **Auto-trigger plan.yml**
   - PR event fires `plan.yml` automatically
   - Classification happens transparently

5. **Conditional Auto-merge**
   - If Tier 0: `gh pr merge --auto --squash`
   - If Tier 1: Waits for manual merge

**Current Limitation:** Requires PAT with `createPullRequest` scope (default GITHUB_TOKEN lacks this)

## Risk Classification System

The core innovation: **Deterministic classification of risk based on terraform plan analysis**, not on operation type.

### How Classification Works

1. **Parse Terraform Plan JSON**
   - Extract all resource changes (add, modify, delete)
   - Get resource attributes (visibility, name, teams)

2. **Apply Rules**
   - Check each repo against Tier 0 criteria
   - If all pass → Tier 0
   - If any fail → Tier 1

3. **Output Decision**
   - Post comment to PR with reasons
   - Return exit code for workflow decision

### Tier 0 Rules (Auto-Approved)

**Repo must meet ALL criteria:**

| Criteria | Required | Example |
|----------|----------|---------|
| Visibility | `private` | ✅ `private` |
| Name format | `^[a-z0-9][a-z0-9-]*$` | ✅ `my-service`, ❌ `My_Service` |
| Operation | Add or modify only | ✅ Add new, ❌ Delete repo |
| No destructive | State doesn't decrease | ✅ Add feature, ❌ Delete branch |

**Decision:** ✅ **Auto-merge** — apply runs immediately

---

### Tier 1 Rules (Manual Review Required)

**Repo triggers Tier 1 if ANY criterion is true:**

| Trigger | Why Risky | Example |
|---------|-----------|---------|
| **Public visibility** | Cost, compliance exposure | `visibility = "public"` |
| **Internal visibility** | Org-wide access, intent unclear | `visibility = "internal"` |
| **Delete operation** | Destructive, data loss | Removing repo from tfvars |
| **Bad naming** | Standards violation | `My_Service`, `MYSERVICE` |
| **Team changes** | Org-level decision | Attaching to new team |

**Decision:** ⏸️ **Wait for manual approval** — PR stays open until reviewed

---

### Real-World Examples

| Scenario | Decision | Reasoning |
|----------|----------|-----------|
| Create private `data-platform-tools` | **Tier 0** | All criteria met (private, good name, no delete) |
| Create public `my-api` | **Tier 1** | Public visibility is risky |
| Create private `My_Service` | **Tier 1** | Bad naming convention |
| Delete any repository | **Tier 1** | Destructive operation always risky |
| Update repo description | **Tier 0** | Modify only, no risky attributes |

---

### Implementation: `scripts/classify_risk.py`

The classifier is deterministic and version-controlled:

```python
# Simplified logic (see actual script for full rules)
def classify_risk(plan_json):
    for resource in plan.resources:
        if resource.type == "github_repository":
            if resource.mode == "destroyed":
                return "Tier 1"  # Delete = risky
            if resource.visibility != "private":
                return "Tier 1"  # Non-private = risky
            if not matches_naming(resource.name):
                return "Tier 1"  # Bad name = risky
    
    return "Tier 0"  # All safe
```

**Why This Approach?**
- ✅ Deterministic (same input → same output always)
- ✅ Version-controlled (changes tracked in git)
- ✅ Explainable (rules are in code, auditable)
- ✅ Business rules encoded (policy as code)

## Code Principles

### 1. Git as Single Source of Truth
- Repository definitions stored in `repositories/example.tfvars`
- All changes must flow through Git (PRs)
- Terraform state file committed (audit trail)
- Enables deterministic, reproducible deployments

### 2. Infrastructure as Code (Terraform)
- Repositories defined declaratively in HCL
- Module-based design (`modules/repository/`)
- No manual GitHub UI operations
- Local testing: `terraform plan` on any branch

### 3. Risk-Based Automation
- **Tier 0:** Safe operations bypass human review (instant provisioning)
- **Tier 1:** Risky operations require human confirmation (compliance)
- Classification is deterministic (same rules always apply)

### 4. Local Terraform Backend (POC)
- State committed to git (trade-off: no locking, no encryption)
- Enables workflows without external infrastructure
- **Production:** Migrate to S3/Terraform Cloud

### 5. GitHub Actions Orchestration
- `plan.yml` handles classification
- `apply.yml` handles execution
- `request-operation.yml` handles business users
- Each workflow is single-responsibility (Unix philosophy)

---

## Usage: Two Paths

### Path 1: Git-Native (Engineers)

**Create or modify repository via Git:**
```bash
# Edit repositories/example.tfvars
git checkout -b add-my-service
git add repositories/example.tfvars
git commit -m "Add my-service repository"
git push origin add-my-service

# Open PR on GitHub
# plan.yml auto-runs
# If Tier 0: auto-merges
# If Tier 1: wait for manual approval
# apply.yml runs on merge
```

### Path 2: Workflow Dispatch (Business Users)

**Request operation via GitHub UI (no Git knowledge required):**

1. Go to: **Actions** → **Request Repository Operation** → **Run workflow**
2. Fill form:
   - Operation: `create`
   - Repo name: `my-service`
   - Visibility: `private`
   - Description: `My service code`
3. **Run workflow**
4. System handles everything:
   - Creates PR automatically
   - Classifies risk
   - Merges if Tier 0, or waits if Tier 1
   - Applies Terraform
   - Creates repository on GitHub

---

## Real Example: Business User Creates Service Repo

**User action:** Click "Request Repository Operation" workflow

**What happens behind the scenes:**

```
1. request-operation.yml validates:
   ✓ repo_name = "data-platform-tools" (valid format)
   ✓ operation = "create"
   ✓ visibility = "private"

2. modify_tfvars.py adds entry:
   repositories = {
     "data-platform-tools" = {
       description = "Data platform tooling"
       visibility = "private"
       topics = ["service"]
     }
   }

3. Workflow creates PR: ops/create-data-platform-tools-1728043200

4. plan.yml triggered on PR:
   - terraform plan → 1 resource to add
   - classify_risk.py: all criteria met
   - posts: "✓ Tier 0 - Auto-approved"

5. Workflow auto-merges PR

6. apply.yml triggered on main push:
   - terraform apply -auto-approve
   - Creates github_repository resource
   - Commits terraform.tfstate

7. ✅ Repository "data-platform-tools" created on GitHub
   📝 Entire flow audited in PR comments + git commits
```

**Total time:** ~30 seconds (fully automated)

## State Management

**Design Choice:** `terraform.tfstate` is committed to git (intentional for POC)

| Aspect | Trade-off |
|--------|-----------|
| **Locking** | None (POC only; production needs S3/Terraform Cloud) |
| **Encryption** | None (acceptable for public operations only) |
| **Auditability** | ✅ All state changes tracked in git history |
| **Reproducibility** | ✅ Any PR can be re-run locally with same state |
| **Workflow Independence** | ✅ Each CI/CD run has state snapshot |

**Production Recommendation:** Migrate to remote backend (S3 + DynamoDB for locking, or Terraform Cloud)

---

## Compliance & Audit Trail

**Every operation is fully auditable:**

1. **PR Comments** — Risk classification decision visible to all stakeholders
2. **Git Commits** — All tfvars changes tracked with author/timestamp
3. **Terraform State** — State changes committed, diff visible in git history
4. **GitHub Actions Logs** — All workflow steps logged and searchable
5. **Audit Trail** — Trace any repo from inception to deletion in git blame

**Example audit query:**
```bash
git log --all --grep="repo-name" -- repositories/example.tfvars
git show <commit>:repositories/example.tfvars  # See exact state at that time
```

---

## Troubleshooting

### PR Not Auto-Merging (Expected Tier 0)
**Check:** Review plan.yml PR comment for actual tier classification
- If Tier 1: review the reasons given (visibility, naming, operation type)
- If comment missing: check plan.yml logs in Actions tab

### Terraform Apply Fails
**Check:** `GH_PROVISIONING_TOKEN` secret
- Run: `gh secret list` to verify it exists
- Verify scopes: requires `repo` + `workflow`
- Check GitHub API rate limit: `gh api rate_limit --jq '.resources.core'`

### Workflow Trigger Not Firing
**Check:**
- PR is to `main` branch (not feature branch)
- `.github/workflows/*.yml` syntax is valid
- Repository settings: Actions enabled + workflows allowed
- Branch protection: if enabled, doesn't block workflow events

### Risk Classification Seems Wrong
**Update rules in `scripts/classify_risk.py`:**
```python
# Tier 0 rules (lines ~40-50)
if visibility != "private": return "Tier 1"  # Change this line to allow internal

# Tier 1 rules (lines ~50-60)
# Add/remove risk triggers here
```
Commit changes and re-run workflow.

---

## Known Limitations

| Limitation | Reason | Workaround |
|-----------|--------|-----------|
| **Delete requires manual approval** | Tier 1 trigger (safe default) | OK for governance |
| **Team attachment on personal accounts** | GitHub feature limitation | Use org account for production |
| **Branch protection on free tier** | GitHub plan limitation | Upgrade to Pro or use org |
| **No auto-rollback** | POC design | Manual PR revert + apply |
| **request-operation.yml needs PAT** | GITHUB_TOKEN scope limitation | Use Personal Access Token |

---

## Next Steps (Future Phases)

| Phase | Capability | Timeline |
|-------|-----------|----------|
| **Phase 1** ✅ | Create/delete basic repos | Complete |
| **Phase 2** ✅ | Risk classification (Tier 0/1) | Complete |
| **Phase 3** ✅ | Business user workflow | Complete |
| **Phase 4** 🔄 | Fix request-operation permissions | Blocked on PAT setup |
| **Phase 5** 📋 | Team management workflow | Design phase |
| **Phase 6** 📋 | Multi-org federation | Backlog |
| **Phase 7** 📋 | Cost estimation in Tier 1 reviews | Backlog |

---

## Architecture Decisions

### Why Deterministic Classification?
- ✅ Reproducible (same rules always apply)
- ✅ Auditable (rules in git, changes tracked)
- ✅ Fast (no ML models, instant decisions)
- ✅ Explainable (humans can understand why Tier was chosen)

### Why Git-Native?
- ✅ Compliance ready (immutable audit trail)
- ✅ Reversible (git revert any change)
- ✅ Integration ready (works with any Git tooling)
- ✅ Team-friendly (familiar workflow)

### Why Local Terraform Backend?
- ✅ POC simplicity (no external infrastructure)
- ✅ Learnable (terraform works identically locally)
- ❌ Not production-ready (no locking, state sync issues)

## For Developers

### Local Testing

```bash
# Test terraform locally (no API calls)
cd terraform
terraform init
terraform plan -var-file=../repositories/example.tfvars -out=tfplan

# Test risk classifier locally
python3 scripts/classify_risk.py terraform/tfplan.json

# Dry-run workflow locally (requires act)
act pull_request -j plan
```

### Modifying Classification Rules

Edit `scripts/classify_risk.py`:
- Tier 0 logic: Check all criteria must pass
- Tier 1 logic: Check if any risk trigger exists
- Commit changes to git
- Next PR will use new rules

### Adding New Resource Types

1. Update `terraform/modules/repository/` for new resources
2. Add variable to `terraform/modules/repository/variables.tf`
3. Update `repositories/example.tfvars` with new fields
4. Test locally: `terraform plan`
5. New classification rules automatically apply

---

## References

- **Terraform GitHub Provider:** https://registry.terraform.io/providers/integrations/github/latest
- **GitHub Actions:** https://docs.github.com/en/actions/using-workflows
- **GitHub CLI:** https://cli.github.com/
- **Terraform:** https://www.terraform.io/docs

---

## Questions & Support

For issues or questions about this POC:
1. Check workflow logs in GitHub Actions
2. Review risk classification in PR comments
3. Inspect git history: `git log --all -- repositories/example.tfvars`
4. Read the code: logic is in `.github/workflows/` and `scripts/`
