# Importing Existing Repositories

Import existing GitHub repositories into Terraform management.

---

## Overview

When you have existing repositories not yet managed by Terraform, use the import workflow to bring them under management.

**Key Points:**
- Import is a **one-time operation** per repository
- After import, repo is treated like any other managed repository
- Works entirely through GitHub UI (no terminal needed)

---

## Step-by-Step Process

### Step 1: Gather Information

You need:
- **Repo name** (e.g., `legacy-system`)
- **Repo ID** (numeric ID from GitHub)
- **Visibility** (private or internal)

To find repo ID:
1. Go to GitHub repository
2. Click "About" (top right)
3. Look for "Repository ID" or use:
   ```bash
   gh api repos/owner/repo-name --jq '.id'
   ```

### Step 2: Run Import Workflow

1. Go to repo → **Actions** tab
2. Select **Import Existing Repository** workflow
3. Click **Run workflow**
4. Fill in inputs:
   - **repo_name:** `legacy-system`
   - **repo_id:** `123456789`
   - **visibility:** `private`
5. Click **Run workflow**

### Step 3: Workflow Execution

Workflow will:
1. ✅ Validate inputs
2. ✅ Verify repo exists on GitHub
3. ✅ Run `terraform import`
4. ✅ Generate config block
5. ✅ Display config in workflow output

### Step 4: Copy Config to repos.tfvars

1. Go to workflow run
2. Find "Generate config template" step
3. Copy the config block
4. Edit `infra/repos.tfvars`
5. Paste config into `repositories` object

**Example:**

Before:
```hcl
repositories = {
  # existing repos
}
```

After:
```hcl
repositories = {
  # existing repos
  
  "legacy-system" = {
    name        = "legacy-system"
    visibility  = "private"
    description = "Imported repository"
    has_issues  = true
    has_wiki    = false
    has_projects = false
    archive_on_destroy = true
    topics      = []
    owner       = "platform-team"
    teams       = []
  }
}
```

### Step 5: Commit and Merge

1. Commit to `develop` branch
2. Create PR
3. Workflow validates plan
4. Merge PR to main
5. Workflow applies
6. ✅ Repository now managed

---

## What Happens After Import

Once added to `repos.tfvars`, the repository is **fully managed**:

- ✅ Can update description, topics, teams
- ✅ Can enable/disable issues, wiki, projects
- ✅ Can set branch protection
- ✅ Can archive on deletion
- ✅ Can delete when removed from config

Just edit `repos.tfvars` and merge like any other change.

---

## Troubleshooting

### "Repository not found"
- Verify repo exists in GitHub
- Verify repo name spelling
- Verify you have access to the repo

### "Import failed"
- Check workflow logs (Actions tab)
- Verify repo ID is correct
- Ensure Terraform state is clean

### "Config doesn't work in repos.tfvars"
- Paste entire config block
- Ensure proper indentation (2 spaces)
- Verify comma after each repo block

---

## Examples

### Import with Minimal Config

```hcl
"imported-repo" = {
  name       = "imported-repo"
  visibility = "private"
  # Uses defaults for all other fields
}
```

### Import with Full Config

```hcl
"legacy-system" = {
  name        = "legacy-system"
  visibility  = "private"
  description = "Legacy application (imported)"
  has_issues  = true
  has_wiki    = true
  has_projects = true
  archive_on_destroy = true
  homepage_url = "https://legacy.example.com"
  owner = "legacy-team"
  topics = ["legacy", "python"]
  teams = ["legacy-team", "platform-team"]
}
```

---

## Multiple Repositories

To import multiple repos:
- Run workflow once per repository
- Copy each config block
- Paste all into `repos.tfvars`
- Commit once with all imports

---

**See:** `conf/REPOS_TFVARS_SCHEMA.md` for complete field documentation
