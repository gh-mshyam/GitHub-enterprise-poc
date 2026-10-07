# Repository Management System Architecture

Complete guide to the tfvars-based repository management system: structure, workflows, scenarios, and design philosophy.

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Folder Structure & Responsibilities](#folder-structure--responsibilities)
3. [Workflow Architecture](#workflow-architecture)
4. [Terraform State Management](#terraform-state-management)
5. [Operational Scenarios](#operational-scenarios)
6. [Design Philosophy](#design-philosophy)
7. [Principles & Trade-offs](#principles--trade-offs)

---

## System Overview

This system manages GitHub repositories through a **single source of truth**: `infra/repos.tfvars`.

**Key Concept:** Terraform state tracks GitHub reality. Code (repos.tfvars) defines desired state. Workflows keep them in sync.

```
GitHub Reality
    ↑ ↓
Terraform State (tracks what exists)
    ↑ ↓
repos.tfvars (desired config)
    ↑ ↓
4 Workflows (orchestrate sync)
```

---

## Folder Structure & Responsibilities

```
.
├── .github/workflows/
│   ├── import-repo.yml                    ← One-time import (manual)
│   ├── manage-repos-create-pr.yml         ← Auto-PR creation (develop)
│   ├── manage-repos-plan-validate.yml     ← Validation on PR
│   └── manage-repos-apply.yml             ← Apply on main
│
├── infra/
│   ├── repos.tfvars                       ← SOURCE OF TRUTH (user edits)
│   ├── variables.tf                       ← Schema definition
│   ├── main.tf                            ← Terraform resources
│   ├── .terraform/                        ← State & plugins
│   └── terraform.tfstate                  ← State file (tracks reality)
│
└── conf/
    ├── IMPORT_WORKFLOW.md                 ← How to import repos
    └── repository-management/
        ├── ARCHITECTURE.md                ← This file
        ├── SCENARIOS.md                   ← Step-by-step workflows
        └── DESIGN_PRINCIPLES.md           ← Philosophy & trade-offs
```

### Key Files Explained

| File | Purpose | Owner | Edited By |
|------|---------|-------|-----------|
| `repos.tfvars` | Desired state of all repos | Terraform | Users (git commits) |
| `variables.tf` | Type/schema definition | System | Developers (refactoring) |
| `.terraform/` | Terraform plugins & lock | System | Auto-maintained |
| `terraform.tfstate` | **Current GitHub state** | System | Terraform workflows |

**Critical:** `terraform.tfstate` = source of truth for what's on GitHub. Never edit by hand.

---

## Workflow Architecture

### 4 Core Workflows

```
┌─ IMPORT WORKFLOW (Manual Dispatch)
│  └─ Runs: terraform import
│     Result: Adds existing repo to state
│
├─ CREATE-PR WORKFLOW (Auto on develop push)
│  └─ Detects: Changes between develop ↔ main
│     Result: Creates PR (develop → main) if none exists, or updates existing
│
├─ PLAN-VALIDATE WORKFLOW (Auto on PR changes to repos.tfvars)
│  └─ Runs: terraform plan
│     Result: Shows what changes will happen, posts to PR
│
└─ APPLY WORKFLOW (Auto on main merge)
   └─ Runs: terraform apply
      Result: Actually updates GitHub repositories
```

### Trigger Conditions

```yaml
import-repo:
  trigger: Manual (workflow_dispatch)
  inputs: repo_name, repo_id, visibility
  branch: (any)

manage-repos-create-pr:
  trigger: Push
  branch: develop
  paths: infra/repos.tfvars
  
manage-repos-plan-validate:
  trigger: Pull request opened/updated OR /plan comment
  branch: main (target)
  paths: infra/repos.tfvars
  
manage-repos-apply:
  trigger: Push
  branch: main
  paths: infra/repos.tfvars
```

### Workflow Dependency Graph

```
User edits repos.tfvars locally
         ↓
    Commit to develop
         ↓
  CREATE-PR WORKFLOW ← Auto runs
         ↓
    PR created (or updated)
         ↓
  PLAN-VALIDATE WORKFLOW ← Auto runs
         ↓
  User reviews plan in PR
         ↓
  User merges to main
         ↓
  APPLY WORKFLOW ← Auto runs
         ↓
  GitHub repos updated
```

---

## Terraform State Management

### What is State?

State file = Terraform's record of what exists on GitHub.

```
terraform.tfstate = {
  "api-server": { id: 123456, name: "api-server", visibility: "private", ... },
  "legacy-system": { id: 789012, name: "legacy-system", visibility: "private", ... }
}
```

### State vs Code vs Reality

```
SCENARIO 1: Everything matches (✅ Healthy)
───────────────────────────────────────
Code (repos.tfvars):
  "api-server" = { visibility = "private", ... }

State (terraform.tfstate):
  "api-server" = { visibility = "private", ... }

GitHub Reality:
  api-server exists, visibility = private

Action: No change needed ✅


SCENARIO 2: Code adds new field (✅ Update)
───────────────────────────────────────
Code (repos.tfvars):
  "api-server" = { visibility = "private", topics = ["api"] }

State:
  "api-server" = { visibility = "private" }

GitHub Reality:
  api-server exists, no topics set

Action: terraform apply → adds topics ✅


SCENARIO 3: Missing from state (❌ Error or import needed)
───────────────────────────────────────
Code (repos.tfvars):
  "api-server" = { ... }

State:
  (empty - no api-server)

GitHub Reality:
  api-server exists (unmanaged)

Action: terraform apply → tries to CREATE (conflict!)
Solution: Run import workflow first ✅


SCENARIO 4: Deleted from code (⚠️ Archive/destroy)
───────────────────────────────────────
Code (repos.tfvars):
  (api-server removed)

State:
  "api-server" = { archive_on_destroy = true, ... }

GitHub Reality:
  api-server exists

Action: terraform apply → archives repo ✅
```

---

## Operational Scenarios

### Scenario 1: Create New Repository

**Goal:** Add a brand new repo to be managed.

**Steps:**

1. Edit `infra/repos.tfvars`:
   ```hcl
   repositories = {
     "new-api" = {
       name        = "new-api"
       visibility  = "private"
       description = "New API service"
       has_issues  = true
       has_wiki    = false
       teams       = ["api-team"]
       topics      = ["api", "go"]
     }
   }
   ```

2. Commit to develop:
   ```bash
   git add infra/repos.tfvars
   git commit -m "Add new-api repository"
   git push origin develop
   ```

3. CREATE-PR workflow runs automatically:
   - Detects changes between develop and main
   - Creates PR (develop → main)

4. PR opens → PLAN-VALIDATE runs:
   - Shows: `+ github_repository.new-api` (will create)
   - Posts plan to PR

5. User reviews and merges PR

6. APPLY workflow runs:
   - `terraform apply` sees: "new-api in code but not in state"
   - **Creates** new repo on GitHub
   - Adds to state file
   - Sets description, teams, topics ✅

**State Transition:**
```
Before: state = {}
After:  state = { "new-api": { id: 999123, name: "new-api", ... } }
```

---

### Scenario 2: Import Existing Repository

**Goal:** Bring an existing unmanaged repo under Terraform management.

**Before State:**
```
GitHub: repo exists (created manually)
State:  empty (Terraform doesn't know about it)
Code:   empty (not in repos.tfvars)
```

**Steps:**

1. Run Import Workflow:
   - Go to Actions → "Import Existing Repository"
   - Fill in:
     - repo_name: `legacy-system`
     - repo_id: `789012` (from GitHub)
     - visibility: `private`
   - Click "Run workflow"

2. Import workflow runs:
   ```bash
   terraform import 'module.repository["legacy-system"].github_repository.this' 789012
   ```
   
   **Result:** State file now has:
   ```json
   { "legacy-system": { id: 789012, name: "legacy-system", ... } }
   ```

3. Workflow outputs config block (visible in logs):
   ```hcl
   "legacy-system" = {
     name        = "legacy-system"
     visibility  = "private"
     description = "Imported repository"
     has_issues  = true
     has_wiki    = false
     has_projects = false
     archive_on_destroy = true
     topics      = []
     owner       = "org-name"
     teams       = []
   }
   ```

4. User copies config → edits `infra/repos.tfvars`:
   ```hcl
   repositories = {
     "legacy-system" = {
       # ... pasted config ...
       teams = ["platform-team"]  ← User customizes
     }
   }
   ```

5. Commit & create PR (like normal)

6. PLAN-VALIDATE runs:
   - Shows: no creation (repo already exists in state)
   - Shows: team assignment change

7. APPLY runs:
   - Sees: "legacy-system in code AND in state"
   - **Updates** (no creation) ✅

**State Transition:**
```
Before: state = {}              (unmanaged)
After:  state = { "legacy-system": { ... } }  (now managed)
```

**Key Point:** Import brings it into state. Code config manages it going forward.

---

### Scenario 3: Update Existing Repository

**Goal:** Change config of managed repository (e.g., add team, change description).

**Before State:**
```
Code:   "api-server" = { teams = [], ... }
State:  { "api-server": { teams = [], ... } }
GitHub: api-server exists, no teams assigned
```

**Steps:**

1. Edit `repos.tfvars`:
   ```hcl
   "api-server" = {
     teams = ["backend-team", "devops-team"]  ← Added teams
   }
   ```

2. Commit to develop, push

3. CREATE-PR workflow creates PR

4. PLAN-VALIDATE shows:
   ```
   ~ github_repository_collaborator.backend-team will be created
   ~ github_repository_collaborator.devops-team will be created
   ```

5. User merges

6. APPLY workflow:
   - Sees: "api-server in code AND in state"
   - Detects: teams changed
   - **Updates** team assignments ✅

**State Transition:**
```
Before: state = { "api-server": { teams = [] } }
After:  state = { "api-server": { teams = ["backend-team", "devops-team"] } }
```

---

### Scenario 4: Delete (Archive) Repository

**Goal:** Remove repo from management (archives it on GitHub).

**Before State:**
```
Code:   "legacy-system" = { ... }
State:  { "legacy-system": { archive_on_destroy = true } }
GitHub: legacy-system exists
```

**Steps:**

1. Remove from `repos.tfvars`:
   ```hcl
   repositories = {
     # "legacy-system" = { ... }  ← Removed
   }
   ```

2. Commit to develop, push

3. CREATE-PR workflow creates PR

4. PLAN-VALIDATE shows:
   ```
   - github_repository.legacy-system will be destroyed
   ```

5. User reviews and merges

6. APPLY workflow:
   - Sees: "legacy-system in state but NOT in code"
   - Checks: `archive_on_destroy = true`
   - **Archives** repo on GitHub (doesn't delete, soft-delete)
   - Removes from state ✅

**State Transition:**
```
Before: state = { "legacy-system": { ... } }
After:  state = {}  (removed from state)
GitHub: legacy-system is archived (read-only)
```

---

## Design Philosophy

### 1. Single Source of Truth

**Principle:** One file (repos.tfvars) defines all repos. No JSON, no Python scripts, no manual state files.

**Why:** Eliminates sync problems, version control friendly, easy to review.

**Trade-off:** Can't auto-detect drift; must update code if someone manually changes GitHub.

---

### 2. Separation of Concerns

**Import** = Infrastructure orchestration (one-time)
**Management** = Code-driven (continuous)

```
Import:
  - Temporal: one-time per repo
  - Orchestrates: terraform import
  - Boundary: gets repo into state
  - User action: copies config into repos.tfvars

Management:
  - Temporal: continuous (every commit)
  - Orchestrates: terraform plan/apply
  - Boundary: keeps code and reality in sync
  - User action: edit repos.tfvars like normal code
```

**Why:** Clear intent, no mixing of one-time and continuous operations.

**Trade-off:** Two separate workflows instead of one; more UI clicks to import.

---

### 3. Idempotent Operations

**Principle:** Running the same workflow twice = same result.

**Example:**
```bash
# First run: creates repo, adds teams
terraform apply

# Second run: repo exists, teams already assigned
terraform apply
# Result: no changes (idempotent)
```

**Why:** Safe to re-run, consistent behavior, no hidden side effects.

**Trade-off:** Slightly more complex state tracking; must be careful with apply semantics.

---

### 4. Centered Workflows (User-Editable)

**Principle:** Auto-created PRs are editable. User can change title, description, add context.

```
Auto-PR created:
  title: "chore: sync repos.tfvars (develop → main)"
  body: (auto-generated)

User can edit:
  title: "chore: sync repos.tfvars + add backend-team to api-server"
  body: (add context about why)
```

**Why:** Adds context to version control, easier to review history.

**Trade-off:** Extra step for user; could use fully manual PR creation instead.

---

### 5. Git-Centric Workflow

**Principle:** All state changes flow through git commits and PRs.

```
Edit locally → Commit → Push → PR → Review → Merge → Apply
```

**Why:** Audit trail, code review, rollback capability, team collaboration.

**Trade-off:** Can't use GitHub UI to directly update repos (must go through git).

---

## Principles & Trade-offs

### Design Principles

| Principle | What It Means | Example |
|-----------|--------------|---------|
| **DRY** | Don't repeat config | One repos.tfvars, no JSON duplication |
| **Explicit > Implicit** | Clear intent | Import is separate from manage |
| **Fail Fast** | Error early | Plan phase catches mistakes |
| **Audit Trail** | Track changes | All changes in git history |
| **Immutable State** | Don't hand-edit state | Only workflows modify state |

### Trade-offs Accepted

| Trade-off | Benefit | Cost |
|-----------|---------|------|
| No auto-creation on GitHub UI | Centralized control via code | Can't create repos directly in GitHub |
| Separate import workflow | Clear one-time operation | Extra step for first-time repos |
| No JSON validation | Simpler, Terraform validates | If tfvars is invalid, terraform errors occur later |
| User-editable PRs | Context in commits | Extra step to review/edit each PR |
| State file required | Terraform can track drift | Must maintain .terraform/ directory |

### When NOT to Use This System

- ❌ If you need to create repos directly in GitHub UI (bypass code)
- ❌ If you have 1000s of repos (state management becomes heavy)
- ❌ If repos are created/deleted hourly (not designed for high churn)
- ❌ If you want fully automated, no-review deployments (git-centric means review gates)

### When This System Shines

- ✅ 10-100 repos in active management
- ✅ Team collaboration (code review before changes)
- ✅ Audit requirements (git history)
- ✅ Consistent team/permissions across repos
- ✅ Reproducible deployments (code → apply → predictable state)

---

## Troubleshooting Guide

### Issue: "State has repo but code doesn't"
**Cause:** Repo in state but removed from repos.tfvars
**Solution:** Either add back to repos.tfvars or run apply to archive

### Issue: "Code has repo but state doesn't"
**Cause:** Added to repos.tfvars but didn't import first
**Solution:** Run import workflow first, then add to repos.tfvars

### Issue: "Plan shows creation when repo already exists"
**Cause:** Repo exists on GitHub but not in state file
**Solution:** Run import workflow to bring into state

### Issue: "terraform.tfstate corrupted"
**Cause:** Manual edits or workflow failure
**Solution:** Delete and run workflows again (will re-import all)

---

## Next Steps

- Read: `SCENARIOS.md` for step-by-step examples
- Read: `DESIGN_PRINCIPLES.md` for philosophy deep-dive
- Read: `conf/IMPORT_WORKFLOW.md` for import how-to
- Action: Review `infra/repos.tfvars` to understand current state

---

**Architecture Version:** 1.0  
**Last Updated:** 2026-10-08  
**Maintainer:** Platform Team
