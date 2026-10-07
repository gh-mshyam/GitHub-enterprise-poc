# Phase 3: Import Workflow Solution

**Date**: 2026-10-07  
**Status**: Complete  
**Decision**: Implement **Option B: Import-First Workflow**

## Problem Statement

Three approaches to importing existing repositories:

| Option | Approach | State Safety | User Experience | Score |
|--------|----------|-------------|-----------------|-------|
| **A** | Code-first: Edit repos.tfvars → Manual import step | Manual risk | Simple (edit file) | 7/10 |
| **B** | Import-first: Import via GitHub UI/API → Auto PR | Auto-managed | One-step | **8.5/10** ✅ |
| **C** | Parallel: Edit + Import simultaneously | Auto-managed | Complex | 6/10 |

## Selected Solution: Option B (Import-First)

### Why Import-First?

**Better state consistency**
- Workflow discovers actual repository state from GitHub
- Configuration auto-generated from reality
- Reduces manual config errors

**Safer PR-based workflow**
- Import happens in PR context
- User reviews generated configuration
- Merge applies the change
- Can rollback by reverting PR

**Simpler for users**
- Single entry point: "Import this repo"
- System handles configuration discovery
- No need to know Terraform commands

### How It Works

```
User provides repo URL
       ↓
Workflow discovers settings from GitHub
       ↓
Generates .tfvars configuration
       ↓
Creates PR with configuration
       ↓
User reviews PR
       ↓
Merge PR
       ↓
Terraform manages the repository
```

## Implementation

### Two Import Methods

#### Method 1: Automatic (Recommended)

**Workflow**: `.github/workflows/import-discover.yml`

```
Actions tab
    ↓
"Discover Repository for Import"
    ↓
Enter URL
    ↓
Workflow generates PR
    ↓
Review & Merge
```

**Pros**: Fully automated, no local setup needed  
**Cons**: One repo at a time

#### Method 2: Manual (Power Users)

**For**: Advanced workflows, batch imports

```bash
cd infra/default
terraform init
terraform import 'module.repository["name"].github_repository.this' 'repo-name'
git add terraform.tfstate
git commit -m "terraform: import repo-name"
```

**Pros**: Batch capability, local control  
**Cons**: Requires Terraform knowledge

## Documentation

### User-Facing

1. **`conf/CONTRIBUTING.md`** — Quick import procedures
2. **`apps/scripts/IMPORT_WORKFLOW.md`** — Detailed reference guide
3. **`infra/default/repositories/IMPORT.md`** — Terraform-specific details

### Validation Approach

Imports are validated automatically:

1. **PR validation** (via `plan.yml`)
   - Terraform plan runs
   - Shows expected changes
   - User can verify configuration

2. **State validation** (after merge via `apply.yml`)
   - Terraform apply runs
   - Confirms GitHub state matches config
   - Commits state file

3. **Manual validation**
   - Users can verify on GitHub UI
   - Check repo settings match config
   - Run `terraform plan` locally to verify

## Why This Works

### Addresses Core Requirements

✅ **Consistency**: Terraform source of truth for all repos  
✅ **Auditability**: All imports tracked in git  
✅ **Safety**: PR-based review before applying  
✅ **Scalability**: Supports bulk imports  
✅ **Simplicity**: One workflow for users  

### Trade-offs Made

| Trade-off | Decision | Rationale |
|-----------|----------|-----------|
| Auto vs Manual | Both supported | Users choose based on needs |
| Validation timing | PR + apply phases | Catches errors early |
| State management | POC: local (can improve) | Works for demo, upgrade later |
| Batch vs single | Both methods available | Flexibility for different workflows |

## Comparison with Alternatives

### Why Not Option A (Code-first)?

```hcl
# Code-first flow:
# User edits manually:
"my-repo" = {
  description = "..."  # Have to look this up
  visibility = "private"  # Guess setting
  topics = ["?"]  # May miss topics
}
# Then run import manually
```

**Problems**:
- Manual configuration error-prone
- Settings can differ from GitHub reality
- No validation until apply

### Why Not Option C (Parallel)?

Parallel workflow where import + code changes happen simultaneously:
- Complex state management
- Hard to debug if something fails
- More moving parts
- Higher risk of conflicts

## Future Improvements

The import-first approach is extensible:

1. **Template Application**
   - After import, apply standard template files
   - Auto-add CONTRIBUTING.md, etc.

2. **Validation Rules**
   - Check for naming conventions
   - Enforce topic standardization
   - Verify team access patterns

3. **Batch Import Dashboard**
   - UI to bulk-import multiple repos
   - Status tracking for each repo
   - Batch rollback capability

4. **Import Analytics**
   - Track what's imported vs created from scratch
   - Identify outliers in configuration
   - Report on import coverage

## Testing the Import Workflow

### Test Case 1: Single Repository Import (Automatic)

```bash
# Scenario: Import existing repo via workflow
# Expected: PR created with config, can review and merge
```

✅ Verified: Works via import-discover.yml

### Test Case 2: Multiple Repositories (Manual Batch)

```bash
# Scenario: Import 3 repos manually
terraform import 'module.repository["repo1"].github_repository.this' 'repo1'
terraform import 'module.repository["repo2"].github_repository.this' 'repo2'
terraform import 'module.repository["repo3"].github_repository.this' 'repo3'
git commit -m "terraform: batch import repos"
```

✅ Verified: Works for batch operations

### Test Case 3: Import with Configuration Changes

```bash
# Scenario: Import repo and update settings in same PR
# Add to imports.tfvars:
"my-repo" = {
  visibility = "internal"  # Change from private
  topics = ["updated-topic"]
}
# After merge: Repo visibility updated on GitHub
```

✅ Verified: Terraform apply updates settings

## Rollout Plan

### Step 1: Documentation Ready ✅
- User guides written
- Workflow documented
- Decision recorded

### Step 2: User Communication (Ready)
- Share IMPORT_WORKFLOW.md with team
- Run import-discover.yml on existing repos
- Gather feedback

### Step 3: Monitoring (Ready)
- Track successful imports
- Monitor failed imports
- Collect user feedback
- Iterate if needed

## Conclusion

**Import-First Workflow (Option B) Selected**

This approach provides:
- ✅ Better state consistency (auto-discovered)
- ✅ Safer workflow (PR-based review)
- ✅ Simpler UX (one entry point)
- ✅ Audit trail (git history)
- ✅ Flexibility (both auto and manual methods)

The workflow is now documented and ready for team use. See:
- `conf/CONTRIBUTING.md` — Quick start
- `apps/scripts/IMPORT_WORKFLOW.md` — Detailed reference
