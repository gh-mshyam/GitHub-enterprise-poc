# Workflows Reference

## Workflow 1: Create Branch

**File:** `create-branch.yml`

**Purpose:** Create a feature branch from main.

**When to use:** 
Start a new feature. Want a clean branch.

**What it does:**
- Creates new branch from main
- Pushes branch to remote
- Fails if branch already exists

**Input:**
- `branch_name` (default: develop)

**Output:**
- New branch appears on GitHub
- Ready for code changes

**Command:**
```bash
gh workflow run create-branch.yml -f branch_name=develop
```

---

## Workflow 2: Create PR

**File:** `create-pr.yml`

**Purpose:** Create a pull request with your changes.

**When to use:**
After you commit changes to your branch.

**What it does:**
- Checks that both branches exist
- Detects changes in `repos.tfvars`
- Creates PR if changes exist
- Updates PR if it already exists

**Input:**
- `from_branch` (default: develop)
- `to_branch` (default: main)

**Output:**
- PR appears on GitHub
- Instructions in PR description

**Command:**
```bash
gh workflow run create-pr.yml \
  -f from_branch=develop \
  -f to_branch=main
```

---

## Workflow 3: Deploy

**File:** `deploy.yml`

**Purpose:** Review plan, merge PR, create repositories.

**When to use:**
After PR is created. Ready to deploy changes.

**What it does (full mode):**
1. Runs terraform plan
2. Posts plan to PR comments
3. Merges PR automatically
4. Deletes your branch
5. Runs terraform apply
6. Posts result to PR

**What it does (apply-only mode):**
- Skips plan and merge
- Runs terraform apply only
- Used for recovery after failures

**Input:**
- `pr_number` (required)
- `mode`: `full` or `apply-only`

**Output:**
- Plan comment on PR
- PR is merged
- Branch is deleted
- Repositories created on GitHub
- Success or error comment

**Command (full):**
```bash
gh workflow run deploy.yml \
  -f pr_number=45 \
  -f mode=full
```

**Command (recovery):**
```bash
gh workflow run deploy.yml \
  -f pr_number=45 \
  -f mode=apply-only
```

---

## Workflow 4: Import Repo

**File:** `import-repo.yml`

**Purpose:** Bring existing GitHub repository under terraform management.

**When to use:**
You have a repository on GitHub already.
Want to manage it with terraform.

**What it does:**
- Imports repository into terraform state
- Generates terraform config template
- Prints config to workflow output

**Input:**
- `repo_name` (required)
- `repo_id` (required - from GitHub)
- `visibility` (required - private or internal)

**Output:**
- Terraform import completes
- Config template in workflow logs
- Copy template to `repos.tfvars`

**Command:**
```bash
gh workflow run import-repo.yml \
  -f repo_name=my-repo \
  -f repo_id=12345 \
  -f visibility=private
```

---

## Workflow Order

Always use this order:

1. **Create Branch** — start work
2. **Create PR** — prepare changes
3. **Deploy** — apply changes
4. **Import Repo** — (optional, one-time only)

After import, use the 3-step process (1→2→3) for that repository.
