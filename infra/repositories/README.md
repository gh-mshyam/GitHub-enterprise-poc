# Repository Configuration

> **Note:** This folder contains old tfvars files from previous implementation. **The current system uses `infra/config/repositories.json` as the single source of truth.**

---

## Current System: repositories.json

All repository, team, and import management is now done through:

**`infra/config/repositories.json`** — Single source of truth

See:
- [`infra/config/repositories.json`](../config/repositories.json) — Configuration file
- [`infra/config/schema.json`](../config/schema.json) — Schema definition
- [`conf/CONTRIBUTING.md`](../../conf/CONTRIBUTING.md) — User guide

---

## Legacy Files (No Longer Used)

This directory contains old configuration files from the previous implementation:

- `repos.tfvars` — Deprecated (use repositories.json instead)
- `teams.tfvars` — Deprecated (use repositories.json instead)
- `imports.tfvars` — Deprecated (use repositories.json instead)

**These files are kept for reference only and are not used by workflows.**

---

## How to Make Changes

### Via GitHub Web UI (No Tools Needed)

1. Open [`infra/config/repositories.json`](../config/repositories.json)
2. Click edit (pencil icon)
3. Add/modify repository entries
4. Commit to `develop` branch
5. Workflow creates PR automatically
6. Review → Merge → Done ✓

### Via Local Editor

1. Clone repository
2. Edit `infra/config/repositories.json`
3. Commit to `develop` branch
4. Push
5. Workflow creates PR automatically
6. Review → Merge → Done ✓

---

## Examples

### Create Repository

```json
{
  "repositories": {
    "my-service": {
      "operation": "create",
      "name": "my-service",
      "visibility": "private",
      "description": "My microservice"
    }
  }
}
```

### Import Existing Repository

```json
{
  "legacy-repo": {
    "operation": "import",
    "name": "legacy-repo",
    "visibility": "private",
    "import_existing": {
      "owner": "gh-mshyam",
      "repo_id": 123456789
    }
  }
}
```

### Update Repository

```json
{
  "my-service": {
    "operation": "update",
    "name": "my-service",
    "description": "Updated description"
  }
}
```

### Delete Repository

```json
{
  "my-service": {
    "operation": "delete",
    "name": "my-service",
    "visibility": "private"
  }
}
```

---

## Workflow

```
Edit infra/config/repositories.json
    ↓
Commit to develop branch
    ↓
Workflow creates PR (develop → main)
    ↓
Workflow validates + generates plan
    ↓
PR comment shows plan summary
    ↓
Review PR → Merge to main
    ↓
Workflow applies changes automatically
    ├─ Creates new repositories
    ├─ Imports existing repositories
    ├─ Updates repository settings
    └─ Deletes repositories
    ↓
Done ✓
```

---

## Troubleshooting

### "JSON validation failed"
- Check syntax (missing commas, quotes, brackets)
- Use GitHub editor (shows syntax errors)
- See [`conf/CONTRIBUTING.md`](../../conf/CONTRIBUTING.md) for help

### "Operation failed"
- Check workflow logs (Actions tab)
- Verify configuration is correct
- See [`conf/CONTRIBUTING.md`](../../conf/CONTRIBUTING.md)

### "Workflow not running"
- Ensure commit is to `develop` branch
- Ensure `infra/config/repositories.json` is modified
- Workflows trigger on changes to this file only

---

## Full Documentation

- **User Guide:** [`conf/CONTRIBUTING.md`](../../conf/CONTRIBUTING.md)
- **Architecture:** [`conf/docs/DECISION.md`](../../conf/docs/DECISION.md)
- **Workflows:** [`.github/workflows/`](../../.github/workflows/)
- **Schema:** [`infra/config/schema.json`](../config/schema.json)

---

**Last Updated:** 2026-10-07  
**Current System:** repositories.json + JSON Schema + Workflows  
**Status:** ✅ Production Ready
