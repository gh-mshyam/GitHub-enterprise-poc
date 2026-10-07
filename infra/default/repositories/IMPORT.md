# Repository Import Workflow

This document describes how to import existing repositories from another GitHub organization into Terraform management.

## Quick Start

1. Go to **Actions** → **Discover Repository for Import** → **Run workflow**
2. Enter repository URL: `https://github.com/source-org/repo-name`
3. Workflow discovers repo metadata and teams
4. Review the generated PR
5. Merge to trigger automatic terraform import

## How It Works

### Phase 1: Discovery (Automatic)

When you trigger the workflow with a repo URL, the system:

1. **Validates** the repository exists and you have access
2. **Discovers** repository metadata:
   - Name, description, visibility
   - Topics and configuration
3. **Finds** all teams with access to the repository
4. **Generates** terraform configuration for both repo and teams
5. **Creates a PR** showing what will be imported

**What you see in the PR:**
- Updated `infra/repositories/imports.tfvars` with the repo entry
- Updated `infra/repositories/teams.tfvars` with discovered teams (if any)
- Summary showing repo details and teams found

### Phase 2: Review

Before merging the PR:

1. **Check the configuration** — Are the metadata values correct?
2. **Review teams** — Does the team list make sense?
3. **Edit if needed** — You can modify `.tfvars` files before merge
4. **Request review** — Have a teammate approve if needed

### Phase 3: Import (Automatic)

When you merge the PR:

1. Workflow runs `terraform import` for the repository
2. Workflow runs `terraform import` for each discovered team
3. Terraform state updates automatically
4. State commits to git
5. All resources now managed by Terraform

## Examples

### Import a Single Repository

```bash
# Trigger the workflow with:
Repository URL: https://github.com/my-org/api-server
```

**Result:**
- `api-server` added to `imports.tfvars`
- Any teams with access discovered and added to `teams.tfvars`
- PR created for review
- On merge: terraform imports the repository

### Import Multiple Repositories

Run the workflow multiple times, once per repository. Each creates a separate PR.

## Understanding the Generated Configuration

### imports.tfvars Entry

```hcl
"my-repo" = {
  description = "My existing repository"
  visibility  = "private"
  topics      = ["terraform", "provisioning"]
}
```

This matches the repository's current GitHub settings. You can modify before import.

### teams.tfvars Entries (if teams found)

```hcl
"backend-team" = {
  description  = "Imported team with access to my-repo"
  privacy      = "closed"
  members      = []  # Populate manually after import
  repositories = ["my-repo"]
}
```

**Note:** Team members must be added manually in `members = []` after import. The workflow discovers which teams have access, but you control team membership.

## Customization Before Import

You can edit the tfvars files in the PR before merging:

1. **Change visibility:** Edit `visibility` field
2. **Add/remove topics:** Modify `topics` list
3. **Skip team import:** Delete the team entry from `teams.tfvars`
4. **Adjust description:** Edit `description` field

All changes will be applied when the PR merges.

## Troubleshooting

### "Repository not found or not accessible"

**Causes:**
- Repository URL is incorrect
- You don't have access to the repository
- GitHub token has insufficient permissions

**Solution:**
- Verify repository exists: `gh repo view <owner>/<repo>`
- Check GitHub token has `repo` and `admin:org` scopes

### Teams not discovered

**Causes:**
- No teams have access to the repository
- GitHub token lacks team visibility permissions

**Solution:**
- This is normal — repository might not have team access
- Add teams manually to `teams.tfvars` if needed

### Import fails on merge

**Causes:**
- Repository already imported (idempotent — this is OK)
- Terraform state conflict
- Invalid configuration in .tfvars

**Solution:**
- Check workflow logs for details
- Verify configuration is valid: `terraform validate`
- Try merging again (terraform import is idempotent)

## State Consistency

When a repository is imported:

1. Repository entry created in `module.repository` with terraform state
2. Teams are imported to `module.teams` with terraform state
3. Repository-team relationships preserved
4. All state committed to git

**Result:** The imported repository is now fully managed by Terraform via `plan.yml` and `apply.yml` workflows.

## After Import

Once the import PR merges:

1. **Repo is managed** — Any changes to repo config go through PRs
2. **Team members** — Add actual members to `teams.tfvars` as needed
3. **Team repos** — Repo is already assigned to imported teams
4. **No more manual changes** — GitHub changes must go through Terraform

## Removing an Import

If you want to remove an imported repository from management:

1. Delete the entry from `infra/repositories/imports.tfvars`
2. Delete any team entries from `infra/repositories/teams.tfvars`
3. Create PR, merge
4. Workflow removes terraform management (repo stays on GitHub)

**Warning:** Removing from terraform management just stops tracking it — doesn't delete the repository.

## Bulk Operations

Currently, the import workflow handles one repository at a time. For multiple repositories:

1. Create separate workflows runs for each repo
2. Or manually edit `imports.tfvars` with multiple entries at once
3. Create single PR with all imports
4. Merge once to import all

## Support

For detailed instructions on using the workflows, see:
- `.ghdp/INSTRUCTIONS.md` — Full project instructions
- `README.md` — Quick start guide
- `.github/workflows/import-discover.yml` — Discovery workflow
- `.github/workflows/import-apply.yml` — Import workflow
