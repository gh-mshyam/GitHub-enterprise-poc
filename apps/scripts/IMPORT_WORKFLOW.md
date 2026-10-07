# Repository Import Workflow

This document describes the complete workflow for importing existing GitHub repositories into Terraform management.

## Overview

The import workflow allows you to bring existing repositories under Terraform control. Once imported, all repository settings are managed through the provisioning system alongside new repositories created from scratch.

## Why Import?

- **Unified Management**: Existing and new repos managed in one place
- **Audit Trail**: All changes to existing repos are version-controlled
- **Consistency**: Apply standardized settings and team permissions
- **Automation**: Automatically update team access, topics, and settings

## Two Import Approaches

### Approach 1: Automatic Discovery (Recommended)

Best for most users. Terraform automatically discovers repository settings.

**Steps:**

1. Go to **Actions** tab in repository
2. Click **Discover Repository for Import**
3. Click **Run workflow**
4. Enter full repository URL: `https://github.com/my-org/my-repo`
5. Workflow runs and creates a PR with discovered configuration
6. Review the auto-generated `.tfvars` entry
7. Merge PR
8. Repository is now managed by Terraform

**Pros:**
- Fast and fully automated
- Accurate configuration discovery
- No manual Terraform commands needed
- Error detection built in

**Cons:**
- Limited to one repository per workflow run
- May not discover all custom settings

### Approach 2: Manual Import

For advanced use cases or multiple repositories.

**Prerequisites:**

```bash
# Install Terraform (if not already installed)
brew install terraform

# Navigate to Terraform configuration
cd infra/default

# Initialize (if not already done)
terraform init

# Set environment variables
export TF_VAR_github_token="ghp_YourTokenHere"
export TF_VAR_github_owner="my-org"
```

**Steps:**

1. **Create Configuration Entry**

   Edit `infra/default/repositories/imports.tfvars`:
   ```hcl
   "my-repo" = {
     description        = "Repository description from GitHub"
     visibility         = "private"
     has_issues         = true
     has_wiki           = false
     has_projects       = false
     archive_on_destroy = true
     topics             = ["existing-topic"]
   }
   ```

2. **Run Terraform Import**

   ```bash
   cd infra/default
   terraform import 'module.repository["my-repo"].github_repository.this' 'my-repo'
   ```

   Expected output:
   ```
   github_repository.this: Importing from `my-repo`
   module.repository["my-repo"].github_repository.this: Import successful!
   
   Import complete! Resources that were imported are marked as managed by the state.
   ...
   ```

3. **Verify State**

   ```bash
   # Check that repository is in state
   terraform state list | grep my-repo
   
   # Expected: module.repository["my-repo"].github_repository.this
   ```

4. **Preview Changes**

   ```bash
   # See if configuration matches actual repository
   terraform plan -var-file=repositories/imports.tfvars
   
   # Should show "No changes"
   ```

   If there are differences:
   - Update `.tfvars` to match actual settings, OR
   - Update the resource in code if Terraform settings are incomplete

5. **Commit Changes**

   ```bash
   # Terraform modified .terraform/ and state files
   git add terraform.tfstate
   git commit -m "terraform: import my-repo from GitHub"
   git push
   ```

6. **Create PR**

   Create PR with your commits and merge after review.

**Pros:**
- Full control over configuration
- Can import multiple repos in batch
- Can inspect and modify settings before committing

**Cons:**
- Requires Terraform commands
- Manual configuration entry needed
- More steps than automatic approach

## Validating Imports

After importing, validate that Terraform sees the repository correctly:

### 1. Check State

```bash
cd infra/default
terraform state show 'module.repository["my-repo"].github_repository.this'
```

Should show the repository ID and current settings.

### 2. Compare with GitHub

Visit the repository on GitHub and verify:
- [ ] Visibility matches (private/public/internal)
- [ ] Topics are correct
- [ ] Issues enabled/disabled as configured
- [ ] Wiki enabled/disabled as configured
- [ ] Projects enabled/disabled as configured
- [ ] Description matches

### 3. Dry Run

```bash
# Run plan to see if any changes are pending
terraform plan -var-file=repositories/imports.tfvars
```

Should show `No changes` for a successful import.

## Common Import Scenarios

### Importing Multiple Repositories

**Option 1:** Use Automatic Discovery multiple times
1. Run workflow once per repository
2. Review and merge each PR separately

**Option 2:** Manual batch import
1. Create entries for all repos in `imports.tfvars`
2. Run `terraform import` for each:
   ```bash
   terraform import 'module.repository["repo1"].github_repository.this' 'repo1'
   terraform import 'module.repository["repo2"].github_repository.this' 'repo2'
   terraform import 'module.repository["repo3"].github_repository.this' 'repo3'
   ```
3. Commit state and create one PR

### Importing and Modifying Settings

1. Import the repository
2. In `imports.tfvars`, modify settings you want to change:
   ```hcl
   "my-repo" = {
     description = "Updated description"
     topics      = ["new-topic", "added"]  # Add new topic
     visibility  = "internal"               # Change visibility
   }
   ```
3. Run `terraform apply` to update on GitHub
4. Commit and merge

### Importing to Add Team Access

1. Import repository using either approach
2. Edit corresponding team config in `teams.tfvars`:
   ```hcl
   "my-team" = {
     repositories = ["my-repo"]  # Add imported repo
   }
   ```
3. Merge PR
4. Team now has access to the imported repository

## Troubleshooting

### Import Command Failed

**Error: `error: resource address "..." does not exist in the configuration`**

Make sure you've added the configuration entry in `imports.tfvars` first.

**Error: `Repository not found`**

- Verify repository name is correct (case-sensitive)
- Verify you have GitHub token with correct permissions
- Check: `export TF_VAR_github_token="your-token-here"`

### State Out of Sync

If state doesn't match GitHub reality:

```bash
# Refresh state from GitHub
terraform refresh

# Check what changed
terraform plan
```

If the differences are incorrect, you can:
- Edit `.tfvars` to match GitHub, OR
- Use `terraform state` commands to fix state manually

### Multiple Repositories with Same Name

GitHub allows org-level and user-level repositories. If importing user repo:

```bash
# For user repository (not org repo)
terraform import 'module.repository["my-repo"].github_repository.this' 'my-username/my-repo'
```

### Workflow Didn't Create PR

Check the workflow logs in **Actions** tab:
1. Click the failed workflow run
2. Review the error output
3. Common issues:
   - Repository URL is invalid
   - GitHub API rate limited
   - Token missing or invalid

## Workflow Configuration

The automatic discovery workflow (`.github/workflows/import-discover.yml`) handles:

1. Accepts repository URL input
2. Fetches repository metadata from GitHub
3. Generates `.tfvars` configuration
4. Creates PR with suggested configuration
5. User reviews and merges

The workflow is designed to be:
- **Accurate**: Fetches actual settings from GitHub
- **Safe**: Creates PR for review, doesn't auto-apply
- **Repeatable**: Can be run multiple times
- **Reversible**: PR can be rejected without applying

## Best Practices

### 1. Import in Batches

Group similar repositories and import them together. This:
- Reduces PR churn
- Makes audit trail clearer
- Allows grouped team access changes

### 2. Review Imported Configuration

Always review the generated/discovered configuration:
- Does it match your intentions?
- Are there settings you want to modify?
- Are topics correct?

### 3. Consistent Naming

Use consistent naming across:
- GitHub repository name
- `.tfvars` entry name
- Terraform resource name (should all match)

### 4. Document Custom Settings

If you modify imported repository settings:
```hcl
"my-repo" = {
  # ... existing settings ...
  
  # Modified to enforce 2FA for this team
  teams = ["security-team"]
}
```

### 5. Backup Before Large Imports

Before importing many repositories:

```bash
# Backup current state
cp terraform.tfstate terraform.tfstate.backup
git add terraform.tfstate.backup
git commit -m "backup: state before batch import"
```

## What Gets Imported?

The import captures these repository settings:

- ✅ Repository name and description
- ✅ Visibility (private/public/internal)
- ✅ Topics (tags)
- ✅ Issue tracking enabled/disabled
- ✅ Wiki enabled/disabled
- ✅ Projects enabled/disabled
- ✅ Homepage URL

Not imported (manual setup):

- ❌ Branch protection rules
- ❌ Webhook configurations
- ❌ Deploy keys
- ❌ Release notes
- ❌ PR template
- ❌ Code owners file

For these, you'll need to:
1. Import the repository
2. Add configuration for branch rules, webhooks, etc. if needed
3. Merge PR

## Next Steps After Import

1. **Add Team Access**
   - Edit `teams.tfvars`
   - Add repository to team's `repositories` list
   - Merge PR

2. **Add to Team Scaffold**
   - If this repo should apply templates to new repos, update template references

3. **Document in Repo**
   - Add README section noting it's Terraform-managed
   - Link to this repository for context

4. **Monitor Changes**
   - GitHub Actions will detect if repository settings change on GitHub
   - If out of sync, `terraform plan` will show drift

## Related Documentation

- `conf/CONTRIBUTING.md` — General contribution workflow
- `conf/ARCHITECTURE.md` — System design and structure
- `infra/default/repositories/IMPORT.md` — Detailed import procedures
- `.github/workflows/import-discover.yml` — Workflow implementation
