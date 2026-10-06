# GitHub Workflows

This directory contains 3 focused workflows for repository and team provisioning.

---

## 1. Terraform Plan (`plan.yml`)

**Trigger:** PR comment `/plan`

### What It Does
Runs `terraform plan` to show what changes will be applied.

### When to Use
- After creating a PR with configuration changes
- To review changes before merging
- To validate configuration is correct

### Step-by-Step

1. Create PR with changes to `infra/repositories/*.tfvars`
2. On the PR, write a comment: `/plan`
3. Workflow runs automatically
4. Results posted as a comment on the PR
5. Review the changes
6. If OK, merge the PR

### Example

```
User creates PR editing infra/repositories/repos.tfvars

Then comments on PR:
  /plan

Workflow responds with:
  ✅ Terraform Plan Succeeded
  Configuration is valid. Ready to merge.

OR

  ❌ Terraform Plan Failed
  Check the workflow logs for details.
```

---

## 2. Discover Repository (`import-discover.yml`)

**Trigger:** Manual → Actions → "Discover Repository for Import"

### What It Does
1. Discovers existing GitHub repository metadata
2. Finds teams with access to the repo
3. Validates configuration
4. Creates a PR with import configuration

### When to Use
When you want to import an existing repository into Terraform management.

### Step-by-Step

1. Go to **Actions** tab
2. Click **Discover Repository for Import**
3. Click **Run workflow**
4. Enter repository URL:
   - Example: `https://github.com/my-org/my-repo`
5. Workflow runs:
   - Validates repo exists
   - Discovers metadata (visibility, topics, description)
   - Finds all teams with access
   - Creates PR with configuration
6. Review the PR
7. Merge the PR → Import workflow runs automatically

### PR Preview

When the workflow creates a PR, you'll see:

```
## Repository Import Summary

**Repository:** `my-repo`
**Owner:** my-org
**URL:** https://github.com/my-org/my-repo
**Visibility:** private
**Description:** My existing repository

**Topics:** terraform, provisioning

**Teams with access (2):**
- `backend-team` (push)
- `devops-team` (maintain)

### Next Steps
1. Review the configuration above
2. Adjust infra/repositories/imports.tfvars if needed
3. Merge this PR to trigger terraform import
4. Verify terraform.tfstate includes imported repo
```

---

## 3. Terraform Apply (`apply.yml`)

**Trigger:** Automatic on PR merge

### What It Does
Applies Terraform changes to GitHub.

Detects whether it's an import or normal operation:
- **Import PR** (title starts with "Import:") → Imports repo + teams, then applies
- **Normal PR** → Applies configuration changes

### When It Runs
Automatically when you merge a PR to main.

### What Happens

**For Normal PRs:**
1. Runs terraform plan (validates changes)
2. Runs terraform apply (creates/updates resources)
3. Commits state to git

**For Import PRs:**
1. Runs terraform import for repositories
2. Runs terraform import for teams
3. Runs terraform plan (validates imports)
4. Runs terraform apply
5. Commits state to git

### Step-by-Step (Normal Flow)

1. Create PR with config changes
2. Comment `/plan` to review (optional)
3. Merge PR
4. Workflow runs automatically
5. Resources are created/updated on GitHub
6. State is committed

### Step-by-Step (Import Flow)

1. Run "Discover Repository for Import"
2. Review the created PR
3. Merge PR (title will be "Import: repo-name")
4. Workflow detects "Import:" in title
5. Runs terraform import commands
6. Repo is now managed by Terraform
7. State is committed

---

## Complete Examples

### Example 1: Add New Repository

**Step 1:** Edit `infra/repositories/repos.tfvars`
```hcl
repositories = {
  "my-new-repo" = {
    description = "My brand new repository"
    visibility  = "private"
    topics      = ["terraform"]
  }
}
```

**Step 2:** Create PR
```bash
git checkout -b add-new-repo
git add infra/repositories/repos.tfvars
git commit -m "Add: my-new-repo"
git push origin add-new-repo
```

**Step 3:** Create PR on GitHub, comment `/plan`

**Step 4:** Merge PR

**Result:** Repository created on GitHub, state committed

---

### Example 2: Add New Team

**Step 1:** Edit `infra/repositories/teams.tfvars`
```hcl
teams = {
  "backend-team" = {
    description  = "Backend engineers"
    privacy      = "closed"
    members      = ["alice", "bob"]
    repositories = ["my-new-repo"]
  }
}
```

**Step 2:** Create PR, comment `/plan`, merge

**Result:** Team created, members added, repo assigned

---

### Example 3: Import Existing Repository

**Step 1:** Go to Actions → "Discover Repository for Import" → Run workflow

**Step 2:** Enter URL: `https://github.com/my-org/existing-repo`

**Step 3:** Review created PR with discovered config

**Step 4:** Merge PR (auto-titled "Import: existing-repo")

**Result:** Existing repo imported into Terraform, now managed like any other

---

## Troubleshooting

### "Plan not running when I comment /plan"

**Check:**
1. Are you commenting on a PR (not an issue)?
2. Is the comment exactly `/plan` (no typos)?
3. Check workflow logs if nothing happens

---

### "Terraform plan shows errors"

**Check:**
1. Configuration syntax in `.tfvars` files
2. Run locally: `cd infra && terraform validate`
3. Check workflow logs for details

---

### "Import workflow not finding my repo"

**Check:**
1. Repository URL is correct (exact case-sensitive)
2. You have access to the repo
3. GitHub token has `repo` scope
4. Check workflow logs

---

### "Apply failed after merge"

**Check:**
1. Workflow logs show the error
2. If state conflict: this is rare, check logs for guidance
3. Terraform import is idempotent (safe to retry)

---

## Quick Reference

| Need | Do This |
|------|---------|
| Create new repo | Edit `repos.tfvars` → PR → `/plan` → Merge |
| Create new team | Edit `teams.tfvars` → PR → `/plan` → Merge |
| Import existing repo | Trigger "Discover" → Review PR → Merge |
| Check what will happen | Comment `/plan` on PR |
| Deploy changes | Merge PR (automatic) |
| Fix state | Check workflow logs, usually just re-merge |

---

## More Information

- **Full instructions:** `.ghdp/INSTRUCTIONS.md`
- **Repository module:** `infra/modules/repository/README.md`
- **Teams module:** `infra/modules/teams/README.md`
- **Import details:** `infra/repositories/IMPORT.md`
- **Configuration:** `infra/repositories/README.md`
