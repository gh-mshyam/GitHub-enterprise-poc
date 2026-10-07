# TODO: AWS Integration Tasks

## 1. S3 State File Backend

**Status:** Not implemented

**What:** Configure Terraform to store state file in AWS S3 instead of locally.

**Why:** 
- Team collaboration (shared state)
- Remote backup (safer)
- Version history (track changes)

**Implementation:**
1. Create S3 bucket for terraform state
2. Add `backend.tf` to infra/ folder
3. Configure S3 + DynamoDB lock
4. Add AWS credentials to GitHub workflows

**Files to modify:**
- `infra/backend.tf` (create)
- `.github/workflows/manage-repos-plan-validate.yml`
- `.github/workflows/manage-repos-apply.yml`

**Blocked by:** AWS account setup and S3 bucket creation

---

## 2. Token Retrieval from AWS Secrets Manager

**Status:** Not implemented

**What:** Fetch GitHub token from AWS Secrets Manager using OIDC instead of hardcoding.

**Why:**
- Secure (no static tokens in GitHub)
- Automatic rotation support
- Audit trail in AWS

**Implementation:**
1. Setup AWS IAM role with OIDC trust policy
2. Store GitHub token in AWS Secrets Manager
3. Add OIDC configuration to all 4 workflows
4. Use `aws-actions/configure-aws-credentials@v4`
5. Fetch token at runtime from Secrets Manager

**Pattern to use:**

```yaml
permissions:
  id-token: write

steps:
  - name: Configure AWS Credentials (OIDC)
    uses: aws-actions/configure-aws-credentials@v4
    with:
      role-to-assume: ${{ vars.GHDP_WORKFLOW_ROLE_ARN || secrets.GHDP_WORKFLOW_ROLE_ARN }}
      role-session-name: repo-management
      aws-region: us-west-2

  - name: Fetch GitHub token from AWS Secrets Manager
    run: |
      TOKEN=$(aws secretsmanager get-secret-value \
        --secret-id github-token \
        --query SecretString --output text)
      echo "GH_TOKEN=$TOKEN" >> $GITHUB_ENV
```

**Files to modify:**
- `.github/workflows/import-repo.yml`
- `.github/workflows/manage-repos-create-pr.yml`
- `.github/workflows/manage-repos-plan-validate.yml`
- `.github/workflows/manage-repos-apply.yml`

**Blocked by:** AWS account setup and OIDC trust policy creation

---

## Dependencies

Both tasks require:
- ✅ AWS account with access
- ✅ S3 bucket created (for state backend)
- ✅ AWS Secrets Manager secret created (for tokens)
- ✅ IAM role for GitHub OIDC trust
- ✅ GitHub variables/secrets configuration

---

## Order to Implement

1. **First:** AWS Secrets Manager token (Task 2)
   - Simpler setup
   - Improves security immediately
   - No state migration needed

2. **Second:** S3 state file backend (Task 1)
   - Requires state migration
   - Better after team has used local state

---

**Created:** 2026-10-08  
**Priority:** Medium  
**Blocked by:** AWS infrastructure setup
