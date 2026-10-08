# Repository Module

This module manages GitHub repositories using configuration from `infra/config/repositories.json`.

---

## How It Works

1. User edits `infra/config/repositories.json`
2. Workflows generate terraform vars
3. This module creates/updates/imports repositories
4. Branch protection rules applied automatically

---

## Configuration

### Create a New Repository

Edit `infra/config/repositories.json`:

```json
{
  "repositories": {
    "my-repo": {
      "operation": "create",
      "name": "my-repo",
      "visibility": "private",
      "description": "My new repository",
      "homepage_url": "https://example.com",
      "has_issues": true,
      "has_wiki": false,
      "has_projects": false,
      "archive_on_destroy": true,
      "topics": ["microservice"],
      "owner": "platform-team",
      "teams": ["platform-team"],
      "branch_protection": {
        "main_branch": "main",
        "require_code_owner_reviews": true,
        "required_approving_review_count": 1,
        "dismiss_stale_reviews": true
      }
    }
  }
}
```

Commit → Workflow creates PR → Merge → Repository created ✓

### Import an Existing Repository

Edit `infra/config/repositories.json`:

```json
{
  "existing-repo": {
    "operation": "import",
    "name": "existing-repo",
    "visibility": "private",
    "owner": "platform-team",
    "import_existing": {
      "owner": "gh-mshyam",
      "repo_id": 123456789
    }
  }
}
```

Workflow runs `terraform import` → Repository now under Terraform management ✓

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

Commit → Workflow plans changes → Merge → Changes applied ✓

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

Commit → Workflow plans deletion → Merge → Repository destroyed ✓

---

## Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `operation` | string | required | `create`, `import`, `update`, `delete` |
| `name` | string | required | Repository name |
| `visibility` | string | required* | `public` or `private` (*required for create/import) |
| `description` | string | "" | Repository description |
| `homepage_url` | string | null | Website URL |
| `has_issues` | boolean | true | Enable Issues |
| `has_wiki` | boolean | false | Enable Wiki |
| `has_projects` | boolean | false | Enable Projects |
| `archive_on_destroy` | boolean | true | Archive instead of delete |
| `topics` | array | [] | GitHub topics |
| `owner` | string | null | Owner team/user |
| `teams` | array | [] | Teams with access |
| `branch_protection` | object | null | Branch protection rules |
| `import_existing` | object | null | Source for import (owner, repo_id) |

---

## Branch Protection

Automatically applied when configured:

```json
{
  "my-repo": {
    "branch_protection": {
      "main_branch": "main",
      "require_code_owner_reviews": true,
      "required_approving_review_count": 1,
      "dismiss_stale_reviews": true
    }
  }
}
```

---

## Workflow

When you edit `infra/config/repositories.json`:

```
1. Push to develop branch
   ↓
2. Workflow creates PR (develop → main)
   ↓
3. Workflow validates JSON + handles imports
   ↓
4. Workflow generates terraform plan
   ↓
5. Plan posted to PR as comment
   ↓
6. Review PR + merge to main
   ↓
7. Workflow applies changes
   ├─ Create new repos
   ├─ Import existing repos
   ├─ Update repo settings
   ├─ Delete repos
   └─ Apply branch protection
   ↓
8. Done ✓
```

---

## Variables

Module accepts:

- `name` — Repository name
- `description` — Description text
- `visibility` — Visibility setting
- `homepage_url` — Homepage URL
- `has_issues`, `has_wiki`, `has_projects` — Feature flags
- `archive_on_destroy` — Archive vs delete
- `topics` — Topic tags
- `github_owner` — GitHub organization
- `github_token` — GitHub token
- `branch_protection_rules` — Protection configuration

---

## Resources Created

- `github_repository` — The repository itself
- `github_repository_vulnerability_alerts` — Security alerts
- `github_branch_protection` — Branch rules (if configured)

---

## Troubleshooting

### "Repository already exists"
- Use `operation: "import"` with `import_existing` metadata
- Workflow will run `terraform import` automatically

### "Delete failed"
- Check repository isn't locked in GitHub
- Verify `archive_on_destroy: true` if you want to archive instead
- Check workflow logs for details

### "Branch protection not applied"
- Ensure `branch_protection` object is configured
- Verify branch name matches repository's default branch
- Check that repository was created before protection is applied

---

## See Also

- **User Guide:** [`conf/CONTRIBUTING.md`](../../conf/CONTRIBUTING.md)
- **Architecture:** [`conf/docs/DECISION.md`](../../conf/docs/DECISION.md)
- **Configuration:** [`infra/config/repositories.json`](../config/repositories.json)
- **Workflows:** [`.github/workflows/`](../../.github/workflows/)
