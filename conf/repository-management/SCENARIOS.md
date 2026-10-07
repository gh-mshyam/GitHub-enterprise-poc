# Step-by-Step Operational Scenarios

Detailed walkthrough of common operations: create, import, update, delete repos.

---

## Table of Contents

1. [Scenario 1: Create New Repository](#scenario-1-create-new-repository)
2. [Scenario 2: Import Existing Repository](#scenario-2-import-existing-repository)
3. [Scenario 3: Update Repository Configuration](#scenario-3-update-repository-configuration)
4. [Scenario 4: Archive/Delete Repository](#scenario-4-archivedelete-repository)
5. [Scenario 5: Bulk Operations](#scenario-5-bulk-operations)
6. [Troubleshooting](#troubleshooting)

---

## Scenario 1: Create New Repository

**Goal:** Add a brand new repository to management.

**Participants:** Developer (editing code)

**Time:** ~10 minutes

### Step 1: Prepare Configuration

Edit `infra/repos.tfvars` locally:

```hcl
repositories = {
  # Existing repos...
  
  "payment-api" = {
    name        = "payment-api"
    visibility  = "private"
    description = "Payment processing API"
    has_issues  = true
    has_wiki    = false
    has_projects = false
    archive_on_destroy = true
    homepage_url = "https://api.example.com/payments"
    owner       = "platform-team"
    topics      = ["api", "payments", "go"]
    teams       = ["platform-team", "devops-team"]
  }
}
```

**What each field means:**
- `name` = GitHub repo name (must match key)
- `visibility` = `private` or `internal`
- `description` = Shows on GitHub
- `has_issues` = Enable GitHub Issues
- `has_wiki` = Enable GitHub Wiki
- `has_projects` = Enable GitHub Projects
- `archive_on_destroy` = Archive (not delete) if removed from config
- `homepage_url` = External link on GitHub
- `owner` = Team responsible (informational)
- `topics` = GitHub searchable tags
- `teams` = Teams with access

### Step 2: Commit Locally

```bash
cd ~/Downloads/git-repos/GitHub-enterprise-poc

git checkout develop  # Make sure on develop branch

git add infra/repos.tfvars

git commit -m "Add payment-api repository

New repository for processing payments via external provider.
- Private visibility for security
- Assign to platform-team and devops-team
- Enable issues for bug tracking"

git push origin develop
```

### Step 3: Auto-PR Created

The `manage-repos-create-pr` workflow automatically runs:

```
Workflow starts
  ↓
Detects: develop has changes, main doesn't
  ↓
Checks: Is there a PR from develop → main?
  ↓
Result: NO → Creates new PR
  ↓
PR #42 opens with:
  title: "chore: sync repos.tfvars (develop → main)"
  body: "Repositories managed: 3"
```

**In GitHub:** You see PR #42 open automatically. (Takes ~30 seconds)

### Step 4: Plan Validation Runs

The `manage-repos-plan-validate` workflow runs on the PR:

```
Workflow starts
  ↓
Runs: terraform init
  ↓
Runs: terraform plan -var-file=repos.tfvars
  ↓
Output shows:
  + module.repository["payment-api"].github_repository.this
  + module.repository_teams.github_team_repository["payment-api:platform-team"]
  + module.repository_teams.github_team_repository["payment-api:devops-team"]
  ↓
Posts summary to PR:
  "## Terraform Plan Summary
   Repositories: 3
   - payment-api (NEW)
   ..."
```

**In GitHub:** PR shows comment with plan details. (Takes ~20 seconds)

### Step 5: Review Plan

You see in PR:
- What will be created (payment-api repo + team assignments)
- No errors (terraform syntax is valid)
- Description shows 3 repos managed

**Check:**
- Is repo name correct?
- Is visibility correct (private/internal)?
- Are teams correct?

### Step 6: Merge PR

Click "Merge pull request" → "Confirm merge"

Git history now shows:
```
develop branch
  ↓ merged ←← payment-api commit
main branch
```

### Step 7: Apply Workflow Runs

The `manage-repos-apply` workflow triggers automatically:

```
Workflow starts (on push to main)
  ↓
Checks: What changed in infra/repos.tfvars?
  ↓
Runs: terraform apply -auto-approve
  ↓
Terraform sees:
  - "payment-api in repos.tfvars"
  - "payment-api NOT in state"
  → CREATE on GitHub ✅
  ↓
Updates state file:
  state["payment-api"] = { id: 123456, ... }
  ↓
Posts success comment to PR:
  "✅ Applied Successfully
   Repositories managed: 3
   - payment-api"
```

**Takes:** ~15 seconds

### Step 8: Verify on GitHub

Go to GitHub.com → Your org:
- New repo "payment-api" exists ✅
- Visibility: private ✅
- Description: "Payment processing API" ✅
- Teams assigned: platform-team, devops-team ✅
- Topics: api, payments, go ✅

**Result:** Repository created and managed. ✅

---

## Scenario 2: Import Existing Repository

**Goal:** Bring existing unmanaged repo under management.

**Participants:** DevOps engineer (triggering workflow), Developer (adding to config)

**Time:** ~15 minutes

### Prerequisites

You have an existing repository on GitHub that's not yet managed:
- Repo exists (you created it manually in GitHub UI)
- Not in `repos.tfvars`
- Terraform doesn't know about it

### Step 1: Gather Information

Go to GitHub repo → "About" section (top right):

```
Get: Repository ID
Example: 789012345
```

Or use CLI:
```bash
gh api repos/your-org/legacy-payment-system --jq '.id'
# Output: 789012345
```

**Collect:**
- repo_name: `legacy-payment-system`
- repo_id: `789012345`
- visibility: `private` (or `internal`)

### Step 2: Run Import Workflow

In GitHub: Go to **Actions** tab

Select: **Import Existing Repository** workflow

Click: **Run workflow**

Fill in inputs:
```
repo_name: legacy-payment-system
repo_id: 789012345
visibility: private
```

Click: **Run workflow**

Workflow starts running (takes ~10 seconds):

```
Workflow output (visible in logs):
  ✅ Inputs valid
  ✅ Repository found on GitHub
  ✅ Terraform init completed
  ✅ Import completed
  
  ## ✅ Repository Import Complete
  
  **Repo:** legacy-payment-system
  **Repo ID:** 789012345
  
  ### Next Steps
  
  1. Copy the config block below
  2. Edit `infra/repos.tfvars`
  3. Paste into the `repositories` object
  4. Commit to `develop` branch
  5. Create PR and merge
  6. Workflow will manage this repository automatically
  
  ### Config Block:
  
  ```hcl
  "legacy-payment-system" = {
    name        = "legacy-payment-system"
    visibility  = "private"
    description = "Imported repository"
    has_issues  = true
    has_wiki    = false
    has_projects = false
    archive_on_destroy = true
    topics      = []
    owner       = "your-org"
    teams       = []
  }
  ```
```

**What happened:**
- Workflow ran: `terraform import module.repository["legacy-payment-system"].github_repository.this 789012345`
- Terraform now knows this repo exists (added to state)
- Workflow outputs config block for manual copy-paste

### Step 3: Copy Config

In the workflow logs, find the "Generate config template" step.

Copy the config block:
```hcl
"legacy-payment-system" = {
  name        = "legacy-payment-system"
  visibility  = "private"
  description = "Imported repository"
  has_issues  = true
  has_wiki    = false
  has_projects = false
  archive_on_destroy = true
  topics      = []
  owner       = "your-org"
  teams       = []
}
```

### Step 4: Edit repos.tfvars

Locally, edit `infra/repos.tfvars`:

```hcl
repositories = {
  # Existing repos...
  
  "legacy-payment-system" = {
    name        = "legacy-payment-system"
    visibility  = "private"
    description = "Imported repository"
    has_issues  = true
    has_wiki    = false
    has_projects = false
    archive_on_destroy = true
    topics      = []
    owner       = "your-org"
    teams       = ["platform-team"]  ← Add team
  }
}
```

**Customize:**
- Update `description` to something meaningful
- Add `teams` as needed
- Add `topics` for discoverability
- Add `homepage_url` if needed

### Step 5: Commit & Create PR

```bash
git add infra/repos.tfvars

git commit -m "Import legacy-payment-system repository

This repository was previously unmanaged. Now bringing under
Terraform management for consistent team/permission control."

git push origin develop
```

### Step 6: PR & Merge (Like Normal)

Auto-PR workflow creates PR → Plan validates → User merges

### Step 7: Apply & Verify

Apply workflow runs:
- Sees: "legacy-payment-system in both code AND state"
- Action: Updates config (adds team assignment) ✅
- Result: No creation (already existed), just updates

**Verify on GitHub:**
- Team now has access: ✅
- Description updated: ✅
- Topics applied: ✅

**Result:** Repo now managed. Future changes go through code. ✅

---

## Scenario 3: Update Repository Configuration

**Goal:** Change settings of existing managed repo (e.g., add team, update description).

**Participants:** Developer

**Time:** ~5 minutes

### Step 1: Identify Change

Example: "The payment-api team needs access to api-server repo"

### Step 2: Edit repos.tfvars

```hcl
"api-server" = {
  name        = "api-server"
  visibility  = "private"
  description = "Core API service"
  # ... other fields ...
  teams       = ["backend-team", "devops-team", "payment-api"]  ← Added payment-api
}
```

### Step 3: Commit & Push

```bash
git add infra/repos.tfvars

git commit -m "Add payment-api team to api-server repository

Granting access so payment team can deploy new payment gateway integration."

git push origin develop
```

### Step 4: Auto-PR, Plan, Merge

- CREATE-PR: Auto-creates PR
- PLAN-VALIDATE: Shows `+ github_team_repository.payment-api (will be created)`
- User merges

### Step 5: Apply

Apply workflow sees:
- api-server in code ✅
- api-server in state ✅
- Teams changed (new entry)
- Runs: `terraform apply`
- Result: Adds payment-api team assignment ✅

**Verify on GitHub:**
- payment-api team now has access to api-server ✅

---

## Scenario 4: Archive/Delete Repository

**Goal:** Remove repo from management (archives on GitHub, not hard-delete).

**Participants:** DevOps engineer

**Time:** ~5 minutes

### Step 1: Remove from repos.tfvars

```hcl
repositories = {
  # Other repos...
  
  # "deprecated-api" = { ... }  ← Removed (commented out or deleted)
}
```

### Step 2: Commit & Push

```bash
git add infra/repos.tfvars

git commit -m "Archive deprecated-api repository

This API is no longer in use. Archiving to preserve history but make read-only."

git push origin develop
```

### Step 3: Auto-PR, Plan, Merge

- CREATE-PR: Auto-creates PR
- PLAN-VALIDATE: Shows `- github_repository.deprecated-api (will be destroyed)`
- User reviews and merges

### Step 4: Apply

Apply workflow sees:
- deprecated-api in state ✅
- deprecated-api NOT in code
- Checks config: `archive_on_destroy = true`
- Runs: `terraform apply`
- Result: Archives on GitHub (read-only), removes from state

**Verify on GitHub:**
- deprecated-api shows as "Archived" badge ✅
- Repo is read-only ✅
- History preserved ✅

---

## Scenario 5: Bulk Operations

**Goal:** Add 5 new repos at once.

**Participants:** Platform team

### Approach 1: One PR (Recommended)

```bash
# Edit repos.tfvars: add all 5 repos
git add infra/repos.tfvars
git commit -m "Add 5 new service repositories

- auth-service
- audit-service
- notification-service
- billing-service
- metrics-service"
git push origin develop
```

Result:
- One PR created
- One plan showing all 5 creations
- One review (5 repos at once)
- One apply (all created together)

**Benefit:** Single review point, all or nothing.

### Approach 2: Separate PRs (If risky)

```bash
# Commit 1: Add auth-service
# Create PR #50, merge
# Wait for apply
#
# Commit 2: Add audit-service
# Create PR #51, merge
# ...repeat for each
```

**Benefit:** Safer (isolate failures), but slower.

---

## Troubleshooting

### Issue: "Invalid syntax in repos.tfvars"

**Error message:**
```
Error: Unsupported block type; on repos.tfvars line 5 at column 10:
```

**Diagnosis:**
```hcl
# ❌ Wrong:
"api-server" {  # ← Missing =

# ✅ Right:
"api-server" = {  # ← Needs =
```

**Fix:** Check HCL syntax (= for assignments, not space).

---

### Issue: "Repository already exists on GitHub"

**Error message:**
```
Error: POST https://api.github.com/user/repos: 422 Repository already exists
```

**Cause:** Trying to create repo, but it already exists on GitHub.

**Diagnosis:**
```
You: "New repo creation"
Code: "api-server in repos.tfvars"
State: empty (doesn't know about it)
GitHub: api-server exists (from manual creation)
```

**Fix:** Run import workflow first to bring into state.

---

### Issue: "terraform.tfstate corruption"

**Error message:**
```
Error reading terraform.tfstate: JSON parse error
```

**Cause:** State file is corrupted (hand-edited or bad merge).

**Fix:**
```bash
# Delete corrupt state (risky!)
rm infra/.terraform/terraform.tfstate

# Re-run import for each repo
# Workflows will rebuild state from GitHub
```

---

### Issue: "Apply failed but can't rollback"

**Symptom:** Apply ran but errored halfway. Terraform and GitHub out of sync.

**Recovery:**
```bash
# Option 1: Revert the PR
git revert <commit-hash>
git push origin develop
# (Creates new PR to revert changes)

# Option 2: Fix and re-apply
# (Edit repos.tfvars to correct state)
# (Commit again)
# (New apply will sync)
```

---

### Issue: "Plan shows 100 changes (unexpected)"

**Cause:** State file got out of sync with GitHub (e.g., someone manually changed repos).

**Diagnosis:**
```
terraform plan sees drift between state and GitHub
```

**Fix:**
```bash
# Option 1: Accept the drift and let terraform fix it
# Merge the big plan (will synchronize everything)

# Option 2: Investigate what changed on GitHub
# Revert manual changes on GitHub to match state
# Then plan should show no changes
```

---

## Common Patterns

### Pattern 1: Regular Reviews

Run monthly:
```bash
terraform plan -var-file=repos.tfvars

# Look for unexpected changes
# If GitHub was manually modified, terraform will show it
```

### Pattern 2: Backup State

Before big changes:
```bash
cp infra/.terraform/terraform.tfstate \
   infra/.terraform/terraform.tfstate.backup
```

### Pattern 3: Test in Sandbox

Before making prod changes:
- Create test repo in repos.tfvars
- Run workflow
- Verify it works
- Remove test repo
- Then make prod changes

---

**Version:** 1.0  
**Last Updated:** 2026-10-08
