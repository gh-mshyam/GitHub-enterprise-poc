# GitHub Enterprise Repository Provisioning

Simplified repository and team provisioning for GitHub using JSON configuration + Terraform + GitHub Actions.

**No terminal needed.** Edit configuration via GitHub web UI or local editor.

---

## What This Does

- ✅ **Create** new GitHub repositories with full configuration
- ✅ **Import** existing repositories into management
- ✅ **Update** repository settings and team access
- ✅ **Delete** repositories safely from management
- ✅ **Manage** GitHub teams and team access

All operations through `infra/config/repositories.json` (single source of truth).

---

## Quick Start

### 1. Edit Configuration

Open `infra/config/repositories.json`:

**Path A: GitHub Web UI** (easiest, no tools needed)
- Click the file in the browser
- Click edit (pencil icon)
- Make changes
- Commit to `develop` branch

**Path B: Local Editor** (for developers)
```bash
git clone https://github.com/your-org/repo.git
cd repo
git checkout develop
# Edit infra/config/repositories.json in your editor
git add infra/config/repositories.json
git commit -m "Add my-repo"
git push origin develop
```

### 2. Workflows Run Automatically

1. **Commit to develop** → Workflow creates PR (develop → main)
2. **PR created** → Workflow validates + plans changes
3. **Merge PR** → Workflow applies changes to GitHub

---

## Operations Supported

### Create New Repository

```json
{
  "repositories": {
    "my-repo": {
      "operation": "create",
      "name": "my-repo",
      "visibility": "private",
      "description": "My new repository",
      "topics": ["microservice"],
      "has_issues": true,
      "has_wiki": false
    }
  }
}
```

### Import Existing Repository

```json
{
  "my-existing-repo": {
    "operation": "import",
    "name": "my-existing-repo",
    "visibility": "private",
    "import_existing": {
      "owner": "gh-username",
      "repo_id": 123456789
    }
  }
}
```

### Update Repository Settings

```json
{
  "my-repo": {
    "operation": "update",
    "name": "my-repo",
    "description": "Updated description",
    "topics": ["microservice", "updated"]
  }
}
```

### Delete Repository

```json
{
  "my-repo": {
    "operation": "delete",
    "name": "my-repo",
    "visibility": "private"
  }
}
```

---

## Configuration Schema

| Field | Required | Type | Notes |
|-------|----------|------|-------|
| `operation` | ✓ | string | `create`, `import`, `update`, `delete` |
| `name` | ✓ | string | Repository name (lowercase, alphanumeric, hyphens) |
| `visibility` | ✓* | string | `public` or `private` (*required for create/import) |
| `description` | | string | Repository description |
| `homepage_url` | | string | Homepage URL |
| `topics` | | array | GitHub topics for discovery |
| `has_issues` | | boolean | Enable Issues (default: true) |
| `has_wiki` | | boolean | Enable Wiki (default: false) |
| `has_projects` | | boolean | Enable Projects (default: false) |
| `archive_on_destroy` | | boolean | Archive instead of delete (default: true) |
| `owner` | | string | Team or user responsible (recommended) |
| `teams` | | array | Teams with access |
| `branch_protection` | | object | Branch protection rules |
| `import_existing` | | object | For import ops: `owner`, `repo_id` |

---

## Workflows

### 1. Create PR (Automatic)
- **Trigger:** Push to `develop` with changes to `infra/config/repositories.json`
- **Action:** Creates PR (develop → main) with summary
- **Example title:** "Repository changes: create 1, import 1, update 1"

### 2. Plan & Validate (Automatic)
- **Trigger:** PR created/updated OR user types `/plan` comment
- **Action:** 
  - Validates JSON schema
  - Handles imports (terraform import)
  - Generates terraform plan
  - Posts plan summary to PR (smart comment, no spam)

### 3. Apply (Automatic)
- **Trigger:** Merge to `main`
- **Action:**
  - Handles imports (terraform import)
  - Runs terraform apply (creates/updates)
  - Handles deletes (terraform destroy)
  - Posts success comment on original PR

---

## Documentation

- **Full user guide:** [`conf/CONTRIBUTING.md`](conf/CONTRIBUTING.md)
- **Architecture & rationale:** [`conf/docs/DECISION.md`](conf/docs/DECISION.md)
- **JSON schema reference:** [`infra/config/schema.json`](infra/config/schema.json)
- **Example config:** [`infra/config/repositories.json`](infra/config/repositories.json)

---

## Troubleshooting

### JSON Validation Error
- Check for missing commas, mismatched quotes
- Use GitHub editor (highlights syntax errors)
- See [`conf/CONTRIBUTING.md`](conf/CONTRIBUTING.md) for common issues

### Import Failed
- Verify `import_existing.repo_id` is correct
- Ensure repository exists in GitHub
- Check workflows tab for error details

### Delete Not Working
- Verify `operation: "delete"` is set
- Check workflow logs (Actions tab)
- Deletion happens automatically on merge to main

### Workflow Stuck
1. Go to **Actions** tab
2. Find the failed workflow
3. Expand failed step for error details
4. Common issue: `GH_TOKEN` missing `repo` + `admin:org` scopes

---

## Architecture

```
infra/config/repositories.json (user edits here)
           ↓
.github/workflows/manage-repos-plan-validate.yml
           ↓
terraform import (for import ops)
           ↓
terraform plan
           ↓
PR comment with plan summary
           ↓
User reviews + merges
           ↓
.github/workflows/manage-repos-apply.yml
           ↓
terraform apply (creates/updates)
terraform destroy (for deletes)
           ↓
GitHub repositories updated ✓
```

---

## Development

**Repository structure:**
- `.github/workflows/` — GitHub Actions workflows (3 workflows)
- `apps/scripts/` — Helper scripts (validation, terraform var generation)
- `infra/config/` — Configuration (repositories.json, schema.json)
- `infra/modules/` — Terraform modules (repository, teams)
- `conf/` — Documentation (CONTRIBUTING.md, DECISION.md)

**Running locally:**
```bash
# Validate config
python3 apps/scripts/validate_schema.py infra/config/repositories.json

# Generate terraform vars
python3 apps/scripts/generate_tfvars.py infra/config/repositories.json repos.tfvars

# Plan changes (requires GitHub token)
cd infra
terraform init
terraform plan -var-file=../repos.tfvars -var github_owner=your-org
```

---

## Support

For errors:
1. **Actions tab** → Select workflow → View logs
2. **PR comments** → Check validation results + plan summary
3. **Documentation** → See [`conf/CONTRIBUTING.md`](conf/CONTRIBUTING.md)

For GitHub API issues:
- Verify token has `repo` + `admin:org` scopes
- Check rate limits: `gh api rate_limit`

---

**Last Updated:** 2026-10-07  
**System Status:** ✅ Production Ready  
**Operations Supported:** Create, Import, Update, Delete
