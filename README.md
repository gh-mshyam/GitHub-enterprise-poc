# GitHub Repository Management

Manage all repositories from one file: `infra/default/repos.tfvars`

Use GitHub Actions workflows. No manual git commands needed.

---

## How to Add a New Repository

**Step 1:** Create branch

Go to Actions. Run **Create Branch** workflow. Default branch is `develop`.

**Step 2:** Edit `infra/default/repos.tfvars`

Add new repository block:

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

Commit and push to your branch.

**Step 3:** Create PR

Go to Actions. Run **Create PR** workflow. A pull request appears.

**Step 4:** Deploy

Go to your PR. Click **Deploy** workflow. Select `full` mode.

Workflow merges PR, deletes branch, and creates repository on GitHub automatically.

---

## How to Add Existing Repository

**Step 1:** Run Import Repo workflow

Go to Actions. Run **Import Repo** workflow. Enter:
- repo_name: `legacy-api`
- repo_id: `789012345`
- visibility: `private`

**Step 2:** Copy generated config

Workflow output shows HCL config block. Copy it.

**Step 3:** Create branch and add config

Run **Create Branch** workflow. Edit `infra/default/repos.tfvars`. Paste config.

**Step 4:** Create PR and Deploy

Run **Create PR** workflow. Run **Deploy** workflow on resulting PR.

Workflow merges PR and brings existing repository under Terraform management.

---

## How to Add a New Team

**Step 1:** Create branch

Run **Create Branch** workflow.

**Step 2:** Edit `infra/default/repos.tfvars`

Add team to the `teams` field:

```hcl
"api-server" = {
  teams = ["backend-team", "new-team"]
}
```

**Step 3 & 4:** Create PR and Deploy

Run **Create PR** workflow. Run **Deploy** workflow.

Team now has access to repository.

---

## How to Add Existing Team

**Step 1:** Create branch

Run **Create Branch** workflow.

**Step 2:** Edit `infra/default/repos.tfvars`

Add team to the `teams` field:

```hcl
"api-server" = {
  teams = ["backend-team", "existing-team"]
}
```

**Step 3 & 4:** Create PR and Deploy

Run **Create PR** workflow. Run **Deploy** workflow.

Team now has access to repository.

---

## Documentation

For detailed information, read:

- **Quick start:** `conf/QUICKSTART.md`
- **Workflow reference:** `conf/WORKFLOWS.md`
- **Architecture:** `conf/WORKFLOW_ARCHITECTURE.md`

---

## Quick Reference

| Action | Workflow | Then Edit |
|--------|----------|-----------|
| Add new repo | Create Branch → Create PR → Deploy | `infra/default/repos.tfvars` |
| Import repo | Import Repo → Create Branch → Create PR → Deploy | `infra/default/repos.tfvars` |
| Add team | Create Branch → Create PR → Deploy | `infra/default/repos.tfvars` |
| Remove repo | Create Branch → Create PR → Deploy | Delete entry in `repos.tfvars` |

---

**System Status:** ✅ Production Ready
