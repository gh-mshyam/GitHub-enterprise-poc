# How to Do Things

Step-by-step guides for common tasks.

---

## Task 1: Create a New Repository

**Goal:** Add a new repository to GitHub and manage it.

**Time:** 5 minutes

### Step 1: Edit repos.tfvars

Open the file: `infra/repos.tfvars`

Add your new repository:

```hcl
repositories = {
  "new-api" = {
    name        = "new-api"
    visibility  = "private"
    description = "New API service"
    teams       = ["backend-team"]
    topics      = ["api", "go"]
  }
}
```

### Step 2: Commit Your Changes

```bash
cd ~/your-repo-path

git add infra/repos.tfvars

git commit -m "Add new-api repository"

git push origin develop
```

### Step 3: Wait for Pull Request

A pull request is created automatically within 30 seconds.

The PR shows:
- Title: "chore: sync repos.tfvars (develop → main)"
- Description: "Repositories managed: 3"

### Step 4: System Checks Your Changes

The plan workflow runs automatically. It shows:

```
Planning to create:
  - new-api repository
  - new-api team assignment
```

This appears as a comment on your pull request.

### Step 5: Review and Merge

Look at the plan. Does it look correct?

- Repository name: correct?
- Visibility: correct?
- Teams: correct?

If yes, click "Merge pull request".

### Step 6: Changes Are Applied

The apply workflow runs automatically. It creates the repository on GitHub.

**Done!** Your new repository exists and is managed.

---

## Task 2: Import Existing Repository

**Goal:** Bring an existing repository into management.

**Prerequisites:** Repository already exists on GitHub.

**Time:** 10 minutes

### Step 1: Get Repository ID

Go to your GitHub repository. Click "About" (top right).

Find: "Repository ID"

Example: `789012345`

Or use command:

```bash
gh api repos/your-org/legacy-repo --jq '.id'
```

### Step 2: Run Import Workflow

Go to your GitHub repository:

1. Click **Actions** tab
2. Select **Import Existing Repository** workflow
3. Click **Run workflow**
4. Fill in:
   - repo_name: `legacy-repo`
   - repo_id: `789012345`
   - visibility: `private`
5. Click **Run workflow**

The workflow runs (takes 10 seconds).

### Step 3: Get the Config Block

Look at the workflow results.

Find the step: "Generate config template"

Copy the config block. Example:

```hcl
"legacy-repo" = {
  name        = "legacy-repo"
  visibility  = "private"
  description = "Imported repository"
  teams       = []
}
```

### Step 4: Add to repos.tfvars

Edit `infra/repos.tfvars`

Paste the config:

```hcl
repositories = {
  # Other repos...
  
  "legacy-repo" = {
    name        = "legacy-repo"
    visibility  = "private"
    description = "Imported repository"
    teams       = ["your-team"]  ← Add your team
  }
}
```

### Step 5: Commit and Push

```bash
git add infra/repos.tfvars

git commit -m "Import legacy-repo into management"

git push origin develop
```

### Step 6: PR, Review, Merge

Same as Task 1:
- PR is created automatically
- Plan shows what will update
- You merge
- Changes are applied

**Done!** Repository is now managed.

---

## Task 3: Change Repository Settings

**Goal:** Update settings of an existing repository (e.g., add a team).

**Time:** 5 minutes

### Step 1: Edit repos.tfvars

Find your repository in `repos.tfvars`

Example: You want to add a team

```hcl
# Before:
"api-server" = {
  teams = ["backend-team"]
}

# After:
"api-server" = {
  teams = ["backend-team", "devops-team"]  ← Added devops-team
}
```

### Step 2: Commit and Push

```bash
git add infra/repos.tfvars

git commit -m "Add devops-team to api-server repository"

git push origin develop
```

### Step 3: PR, Plan, Merge

Same process:
- PR created
- Plan shows: "Will add team assignment"
- You merge
- Team is added to GitHub

**Done!**

---

## Task 4: Archive Repository

**Goal:** Remove repository from management (archive on GitHub).

**Time:** 5 minutes

### Step 1: Remove from repos.tfvars

Find the repository you want to archive.

```hcl
# Before:
repositories = {
  "old-api" = { ... }
}

# After:
repositories = {
  # "old-api" = { ... }  ← Removed (commented out)
}
```

### Step 2: Commit and Push

```bash
git add infra/repos.tfvars

git commit -m "Archive old-api repository"

git push origin develop
```

### Step 3: PR, Plan, Merge

- PR created
- Plan shows: "Will destroy (archive) old-api"
- You merge
- Repository is archived on GitHub

**Result:** Repository is read-only. Data is safe. History is preserved.

---

## Task 5: Add Multiple Repositories at Once

**Goal:** Add several repositories in one go.

**Time:** 15 minutes

### Step 1: Edit repos.tfvars

Add all repositories you need:

```hcl
repositories = {
  # Existing repos...
  
  "auth-service" = { ... }
  "audit-service" = { ... }
  "billing-service" = { ... }
}
```

### Step 2: Commit Once

```bash
git add infra/repos.tfvars

git commit -m "Add three new service repositories

- auth-service
- audit-service
- billing-service"

git push origin develop
```

### Step 3: Single PR, Single Review

One PR is created with all three repositories.

Plan shows all three will be created.

You review once. You merge once.

All are applied together.

**Benefit:** Single review point. All or nothing.

---

## Troubleshooting

### Problem: "Invalid syntax error"

**What it means:** You have a typo in repos.tfvars.

**Example wrong:**
```hcl
"api-server" {  # ← Missing =
```

**Example correct:**
```hcl
"api-server" = {  # ← Has =
```

**Fix:** Read the error message. Find the line number. Fix the syntax.

---

### Problem: "Repository already exists on GitHub"

**What it means:** You added a repository to repos.tfvars but did not import first.

**What to do:**
1. Undo your commit: `git reset HEAD~1`
2. Run import workflow
3. Try again

---

### Problem: "Plan shows 100 changes"

**What it means:** GitHub was changed manually. System is detecting drift.

**What to do:**
1. Review the changes
2. If correct, merge the PR (system will fix GitHub)
3. If incorrect, undo the GitHub changes manually first

---

### Problem: "Workflow failed"

**What to do:**
1. Go to Actions tab
2. Click the failed workflow
3. Read the error message
4. Fix the problem
5. Push again

---

## Quick Reference

### Create New Repository

```bash
Edit repos.tfvars
git add .
git commit -m "Add new-repo"
git push origin develop
# PR created automatically
# Review plan
# Merge PR
# Done
```

### Import Existing Repository

```bash
# 1. Run import workflow (manual)
# 2. Copy config
# 3. Add to repos.tfvars
git add .
git commit -m "Import repo-name"
git push origin develop
# 4. PR created, review, merge
```

### Change Repository Settings

```bash
Edit repos.tfvars
git add .
git commit -m "Update repo-name: add team"
git push origin develop
# PR created automatically
# Review plan
# Merge PR
# Done
```

### Archive Repository

```bash
Remove from repos.tfvars
git add .
git commit -m "Archive repo-name"
git push origin develop
# PR created automatically
# Review plan
# Merge PR
# Done (repo archived)
```

---

## Rules to Remember

1. **Always use repos.tfvars.** Do not create repositories in GitHub directly.

2. **Import before managing.** If repository exists, import first.

3. **Never edit terraform.tfstate.** Let the system manage it.

4. **Always commit and push.** All changes go through git.

5. **Review the plan.** Before merging, check what will change.

---

**Version:** 1.0  
**Language:** Simplified Technical English
