# Pull Request

## Description
<!-- What changes are you making and why? -->

## Type of Change
- [ ] Bugfix (non-breaking change fixing an issue)
- [ ] Feature (new functionality)
- [ ] Refactoring (code reorganization, no behavior change)
- [ ] Documentation
- [ ] Infrastructure/workflow update

## Risk Classification
<!-- If you know the expected tier, indicate it -->
- Expected Tier: **Tier 0** / **Tier 1** / **Unknown** (plan.yml will classify)

**Note:** plan.yml will post a comment showing:
- Risk classification (Tier 0 or Tier 1)
- CODEOWNERS status (✓ assigned, ⚠️ missing, ℹ️ info)

## Testing & Validation

### Local Validation
- [ ] `cd infra && terraform init` succeeds
- [ ] `terraform plan -var-file=../repositories/example.tfvars` succeeds
- [ ] No terraform warnings or errors
- [ ] Terraform formatting is correct

### Risk Classifier (if modified)
- [ ] Classifier logic tested with sample plans
- [ ] New rules documented in code
- [ ] `.ghdp/contracts/ARCHITECTURE.md` updated if rules changed

### Workflow Changes (if applicable)
- [ ] Workflow paths are correct (infra/, repositories/, scripts/)
- [ ] Environment variables documented
- [ ] Trigger conditions validated

## Security Checklist
- [ ] No credentials, tokens, or passwords in code
- [ ] No sensitive data (API keys, endpoints) committed
- [ ] GitHub token only in secrets (GH_PROVISIONING_TOKEN)
- [ ] `.env`, `.env.secret`, `.envrc` in `.gitignore`

## Code Quality
- [ ] Code follows existing style and patterns
- [ ] Variable names are clear and descriptive
- [ ] No commented-out code blocks
- [ ] Changes align with `.ghdp/contracts/CONTRIBUTION_RULES.md`

## Documentation
- [ ] README updated if needed
- [ ] Workflow logic clear in PR description
- [ ] Architecture docs updated if design changes
- [ ] `.ghdp/` updated if new rules or decisions introduced

## Terraform Changes (if applicable)
- [ ] Module structure makes sense
- [ ] Variables properly documented
- [ ] Outputs clear and useful
- [ ] No hardcoded values

## Related Issues
<!-- Link issues if applicable: Closes #123 -->

## Checklist
- [ ] PR title is clear and concise
- [ ] Description explains what and why
- [ ] All security checks pass
- [ ] All code quality checks pass
- [ ] Local validation completed
- [ ] Ready for review
