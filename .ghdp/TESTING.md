# Testing & Validation

## Local Validation (Before Pushing)

### Terraform Validation

```bash
cd infra

# Initialize
terraform init -input=false

# Validate syntax
terraform validate

# Check formatting
terraform fmt -check

# Plan (dry-run, no API calls)
terraform plan -var-file=../repositories/repos.tfvars -out=tfplan
terraform show tfplan

# Clean up
rm -f tfplan
```

### Validate Configuration

```bash
# Validate tfvars files
python3 apps/scripts/validate_tfvars.py repositories/repos.tfvars
python3 apps/scripts/validate_tfvars.py repositories/teams.tfvars
```

### Python Helpers

```bash
# Run unit tests
python3 -m pytest apps/tests/ -v

# Check code style (if available)
python3 -m black --check apps/scripts/
python3 -m flake8 apps/scripts/
```

## GitHub Actions Testing

### Plan Workflow
- Trigger: Create PR to main with tfvars changes
- Expected: plan.yml runs, terraform plan succeeds, posts PR comment
- Validate: PR comment shows plan summary

### Apply Workflow
- Trigger: Merge PR to main
- Expected: apply.yml runs, terraform apply succeeds, state committed
- Validate: Resources created/updated on GitHub, terraform.tfstate updated in git

### Deploy Workflow (Manual)
- Trigger: Manual dispatch with tfvars_file selection
- Expected: Workflow runs plan and optionally apply
- Validate: Resources deployed or staged for review

### Import Workflow
- Trigger: Manual dispatch with repo URL
- Expected: Workflow validates repo and creates import PR
- Validate: Import PR appears with repos.tfvars entry

### Request Operation Workflow
- Trigger: Manual dispatch with create/delete operation
- Expected: Workflow creates PR with repo definition
- Validate: PR appears with correct repo name and tfvars entry

## Manual Testing Checklist

Before merging workflow changes or major refactors:

- [ ] Local terraform plan completes without errors
- [ ] Terraform format check passes
- [ ] Configuration validation succeeds
- [ ] Unit tests pass (pytest)
- [ ] Test repo created via PR
- [ ] State file commits cleanly
- [ ] No terraform warnings or errors

## Testing Scenarios

### Scenario 1: Create Private Repository
1. Add entry to `repositories/repos.tfvars`
2. Create PR
3. Verify: plan.yml posts terraform plan comment
4. Verify: apply.yml applies on merge
5. Verify: Repo appears on GitHub
6. Clean up: Delete repo manually afterward

### Scenario 2: Create Team and Assign Repos
1. Add entry to `repositories/teams.tfvars`
2. Create PR
3. Verify: plan.yml shows team resource creation
4. Verify: apply.yml applies on merge
5. Verify: Team appears on GitHub with members
6. Clean up: Delete team manually afterward

### Scenario 3: Import Existing Repository
1. Trigger `import-repo.yml` with GitHub repo URL
2. Verify: Workflow validates repo access
3. Verify: Import PR created with entry in `repositories/imports.tfvars`
4. Merge import PR
5. Verify: Repo is managed by Terraform

### Scenario 4: Delete Repository
1. Remove repo entry from `repositories/repos.tfvars`
2. Create PR
3. Verify: plan.yml shows resource destruction
4. Merge PR
5. Verify: apply.yml runs and repo is archived

## Continuous Integration

All workflows run automatically on:
- PR creation/update (plan.yml)
- PR merge to main (apply.yml)
- Manual dispatch (deploy.yml, import-repo.yml, request-operation.yml)

No manual CI trigger needed.

## Troubleshooting

### Issue: Terraform plan fails
**Resolution:** Check terraform syntax with `terraform validate`

### Issue: GitHub API errors
**Resolution:** 
- Verify `GH_PROVISIONING_TOKEN` secret has `repo` and `admin:org` scopes
- Check rate limits: `gh api rate_limit`

### Issue: State file conflicts
**Resolution:** 
- Ensure apply.yml completes before next deployment
- Review git log for state file changes: `git log --oneline -- infra/terraform.tfstate`
