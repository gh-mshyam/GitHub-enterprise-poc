# Contributing: Repository Management

## Overview

Repository management is now simplified through **repositories.json**, a single source of truth for all repository configurations. No terminal commands needed—only GitHub UI.

## Workflow: Add/Update/Delete a Repository

### Two Paths — Choose One

You can edit `repositories.json` **two ways:**

#### Path A: GitHub Web UI (Easiest)
- No local tools needed
- Click "Edit" button in GitHub
- Make changes
- Commit directly to develop branch

#### Path B: Local Editor + Git (For Developers)
- Clone repo locally
- Edit `repositories.json` in your editor
- Commit changes
- Push to develop branch

### Step 1: Edit repositories.json

Open `repositories.json` in GitHub UI editor OR your local text editor.

**Create a new repository:**
```json
{
  "repositories": {
    "my-new-repo": {
      "operation": "create",
      "name": "my-new-repo",
      "visibility": "private",
      "description": "My new repository",
      "owner": "platform-team",
      "topics": ["microservice"],
      "teams": ["platform-team"]
    }
  }
}
```

**Update existing repository:**
```json
{
  "repositories": {
    "existing-repo": {
      "operation": "update",
      "name": "existing-repo",
      "description": "Updated description"
    }
  }
}
```

**Import existing repository:**
```json
{
  "repositories": {
    "external-repo": {
      "operation": "import",
      "name": "external-repo",
      "visibility": "private",
      "owner": "platform-team",
      "import_existing": {
        "owner": "gh-mshyam",
        "repo_id": 123456789
      }
    }
  }
}
```

**Delete repository:**
```json
{
  "repositories": {
    "old-repo": {
      "operation": "delete",
      "name": "old-repo"
    }
  }
}
```

### Step 2: Commit to develop

#### Option A: GitHub Web UI
1. Click the edit (pencil) icon on `repositories.json`
2. Make your changes
3. Scroll down, add commit message: "Add my-new-repo"
4. Choose "Commit directly to develop branch"
5. Click "Commit changes"

#### Option B: Local Git
```bash
# Clone (if not already)
git clone https://github.com/your-org/repo.git
cd repo

# Create/switch to develop
git checkout develop
git pull origin develop

# Edit repositories.json
# (use your editor: VS Code, vim, etc.)

# Commit changes
git add repositories.json
git commit -m "Add my-new-repo"

# Push to develop
git push origin develop
```

### Step 3: Create Pull Request

The workflow runs automatically after commit to develop:
1. GitHub Actions validates `repositories.json`
2. Generates terraform plan
3. Creates a PR: `develop` → `main` (this triggers validation)
4. The workflow runs automatically:
   - ✓ Validates JSON schema
   - ✓ Checks repository names (alphanumeric, hyphens only)
   - ✓ Generates terraform plan
   - ✓ Comments PR with summary

### Step 4: Review and Merge

1. Review the PR comments:
   - **Validation Results**: All required fields present
   - **Plan Summary**: What repositories will be created/updated/deleted
   - **Terraform Output**: Exact changes GitHub will see

2. Approve the PR
3. Merge to `develop`

### Step 5: Auto-Merge to Main

After merge to `develop`, the workflow automatically:
1. Runs terraform apply (creates/updates repositories)
2. Creates a PR: `develop` → `main`
3. Auto-merges if all Tier 0 operations (safe)

For risky operations (Tier 1), a human review is required before merge.

---

## Schema Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `operation` | string | ✓ | `create`, `import`, `update`, `delete` |
| `name` | string | ✓ | Repository name (alphanumeric, hyphens) |
| `visibility` | string | ✓ | `public` or `private` |
| `description` | string | | Repository description (≤300 chars) |
| `owner` | string | | Team or user responsible |
| `topics` | array | | GitHub topics for discovery |
| `teams` | array | | Teams with access |
| `auto_merge_develop_to_main` | boolean | | Auto-merge PRs when develop → main |
| `branch_protection` | object | | Branch protection rules (require reviews, etc.) |
| `import_existing` | object | (import only) | Source for importing: `owner`, `repo_id` |
| `custom_files` | object | | Template files to create |

---

## Example Workflow

### Path A: GitHub Web UI
```
Click edit pencil icon
         ↓
Edit repositories.json in browser
         ↓
Commit directly to develop
         ↓
GitHub Actions validates + plans
         ↓
PR auto-generated: develop → main
         ↓
Review & approve
         ↓
Merge (auto-merge for Tier 0)
         ↓
Repositories created ✓
```

### Path B: Local Git + Editor
```
git checkout develop
         ↓
Edit repositories.json locally
         ↓
git commit + git push
         ↓
GitHub Actions validates + plans
         ↓
PR auto-generated: develop → main
         ↓
Review & approve
         ↓
Merge (auto-merge for Tier 0)
         ↓
Repositories created ✓
```

**Both paths do the same thing — choose what's easiest for you.**

---

## Troubleshooting

### "JSON parse error"
- Check for missing commas, mismatched quotes
- Use GitHub's editor (it highlights errors)

### "Invalid name format"
- Names must be lowercase alphanumeric with hyphens
- ✓ `my-repo`, `repo-v2`, `a1b2c3`
- ✗ `My-Repo`, `repo_name`, `repo!`, `-repo`

### "Repository already exists"
- Use `operation: "import"` for existing repos
- Provide `import_existing` with owner and repo_id

### Workflow stuck or failed
- Check Actions tab for logs
- Look at the PR comment for error details
- If terraform fails, the apply step doesn't run

---

## Flexible Workflows

**For non-technical users:** GitHub web editor only (no terminal)
- Click edit, make changes, commit
- Review automation results
- Click merge

**For developers:** Local git + your editor (optional)
- Clone repo, edit locally, push
- Same automation results
- Click merge

**The terraform apply always runs in GitHub Actions** — no local CLI needed in either case.
