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
terraform plan -var-file=../repositories/example.tfvars -out=tfplan
terraform show tfplan

# Clean up
rm -f tfplan
```

### Python Risk Classifier

```bash
# Test classification logic
python3 scripts/classify_risk.py <path-to-plan.json> /tmp/output.md

# Check code style (if available)
python3 -m black --check scripts/classify_risk.py
python3 -m flake8 scripts/classify_risk.py
```

### HCL Validation

```bash
# Check tfvars syntax
cd infra
terraform validate -var-file=../repositories/example.tfvars
```

## GitHub Actions Testing

### Plan Workflow
- Trigger: Create PR to main
- Expected: plan.yml runs, posts risk classification
- Validate: PR comment shows "Tier 0" or "Tier 1" with reasons

### Apply Workflow (Tier 0)
- Trigger: Merge Tier 0 PR
- Expected: apply.yml runs, terraform apply succeeds, state committed
- Validate: New repo appears on GitHub, terraform.tfstate updated in git

### Apply Workflow (Tier 1)
- Trigger: Manually merge Tier 1 PR
- Expected: apply.yml runs, terraform apply succeeds
- Validate: Repo deleted/modified on GitHub, state reflects change

### Request Operation Workflow
- Trigger: Manual dispatch with create operation
- Expected: Workflow creates PR with repo definition
- Validate: PR appears with correct repo name and tfvars entry
- Note: May fail on PR creation (Phase 4 fix); manually create PR as workaround

## Manual Testing Checklist

Before releasing new workflows or changes:

- [ ] Local terraform plan completes without errors
- [ ] Risk classifier runs without errors
- [ ] Test repo created via manual PR (if Tier 0)
- [ ] Test repo deleted via manual PR (if Tier 1)
- [ ] State file commits cleanly
- [ ] PR comments show correct risk tier
- [ ] No terraform warnings

## Testing Scenarios

### Scenario 1: Create Private Repo (Tier 0)
1. Add entry to repositories/example.tfvars
2. Create PR
3. Verify: plan.yml posts "Tier 0 - Auto-approved"
4. Verify: PR auto-merges
5. Verify: apply.yml runs and repo created
6. Delete repo manually afterward

### Scenario 2: Request Delete (Tier 1)
1. Remove repo entry from repositories/example.tfvars
2. Create PR
3. Verify: plan.yml posts "Tier 1 - Manual review"
4. Verify: PR stays open (no auto-merge)
5. Manually merge PR
6. Verify: apply.yml runs and repo archived

### Scenario 3: Public Repo (Tier 1)
1. Add entry with `visibility = "public"`
2. Create PR
3. Verify: plan.yml posts "Tier 1 - Public visibility"
4. Manually approve & merge
5. Verify: apply.yml runs

## Continuous Integration

All workflows run automatically on:
- PR creation (plan.yml)
- PR merge (apply.yml)
- Manual dispatch (request-operation.yml)

No manual CI trigger needed.

## Known Issues & Workarounds

### Issue: request-operation.yml PR creation fails
**Workaround:** Manually create PR with same changes

### Issue: Terraform state sync issues
**Resolution:** Revert last commit, re-run apply.yml

See `.ghdp/contracts/ARCHITECTURE.md` for known limitations.
