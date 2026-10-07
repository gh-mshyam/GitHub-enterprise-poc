# GitHub Repository Management

Manage all repositories from one file: `infra/repos.tfvars`

---

## How to Add a New Repository

**Step 1:** Edit `infra/repos.tfvars`

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

**Step 2:** Commit and push

```bash
git add infra/repos.tfvars
git commit -m "Add new-api repository"
git push origin develop
```

**Step 3:** Review and merge

A pull request is created automatically. Review it. Merge it.

**Step 4:** Done

The repository appears on GitHub automatically.

---

## How to Add Existing Repository

**Step 1:** Run import workflow

Go to Actions tab. Select "Import Existing Repository". Fill in:
- repo_name: `legacy-api`
- repo_id: `789012345`
- visibility: `private`

Click "Run workflow".

**Step 2:** Copy the config

The workflow shows a config block. Copy it.

**Step 3:** Add to repos.tfvars

```hcl
repositories = {
  "legacy-api" = {
    name        = "legacy-api"
    visibility  = "private"
    description = "Imported repository"
    teams       = ["platform-team"]
  }
}
```

**Step 4:** Commit and push

```bash
git add infra/repos.tfvars
git commit -m "Import legacy-api"
git push origin develop
```

**Step 5:** Merge PR

A pull request is created. Merge it.

**Step 6:** Done

Repository is now managed.

---

## How to Add a New Team

**Step 1:** Edit `infra/repos.tfvars`

Add the team to the `teams` field:

```hcl
"api-server" = {
  teams = ["backend-team", "new-team"]  ← Added new team
}
```

**Step 2:** Commit and push

```bash
git add infra/repos.tfvars
git commit -m "Add new-team to api-server"
git push origin develop
```

**Step 3:** Merge PR

A pull request is created. Review it. Merge it.

**Step 4:** Done

The team now has access to the repository.

---

## How to Add Existing Team

**Step 1:** Edit `infra/repos.tfvars`

Add the existing team to the `teams` field:

```hcl
"api-server" = {
  teams = ["backend-team", "existing-team"]  ← Added existing team
}
```

**Step 2:** Commit and push

```bash
git add infra/repos.tfvars
git commit -m "Add existing-team to api-server"
git push origin develop
```

**Step 3:** Merge PR

A pull request is created. Review it. Merge it.

**Step 4:** Done

The team now has access to the repository.

---

## Documentation

For detailed information, read:

- **System overview:** `conf/repository-management/ARCHITECTURE.md`
- **Design philosophy:** `conf/repository-management/DESIGN_PRINCIPLES.md`
- **Step-by-step guides:** `conf/repository-management/SCENARIOS.md`
- **Import workflow:** `conf/IMPORT_WORKFLOW.md`

---

## Quick Reference

| Action | File | Location |
|--------|------|----------|
| Add new repo | `repos.tfvars` | `infra/repos.tfvars` |
| Import repo | Import workflow | Actions tab |
| Add team | `repos.tfvars` | `infra/repos.tfvars` |
| Remove repo | Edit `repos.tfvars` | Remove the repo entry |

---

**System Status:** ✅ Production Ready
