# Test Specifications (Test-First Design)

All tests must pass before implementation is complete.

---

## Unit Tests: classify_risk.py

### Test Suite: Tier 0 Classification

**TC-001: Private repo + standard naming + add operation**
```
Input:
  - visibility: "private"
  - name: "my-service"
  - operation: "add"

Expected Output:
  - tier: "0"
  - reason: "Safe operation (private, standard naming, add only)"

Assert:
  - classify_risk.py returns {"tier": "0"}
  - Reason includes all three criteria met
```

**TC-002: Modify existing private repo**
```
Input:
  - operation: "modify"
  - existing_visibility: "private"

Expected Output:
  - tier: "0"

Assert:
  - Classify returns "0"
```

### Test Suite: Tier 1 Classification

**TC-003: Delete operation detected**
```
Input:
  - operation: "delete"
  - repo_name: "my-service"

Expected Output:
  - tier: "1"
  - reason: "Risky: Delete operation"

Assert:
  - classify_risk.py returns {"tier": "1"}
  - Reason explicitly mentions delete
```

**TC-004: Public visibility**
```
Input:
  - visibility: "public"
  - name: "my-service"

Expected Output:
  - tier: "1"
  - reason: "Risky: Public visibility"

Assert:
  - classify_risk.py returns {"tier": "1"}
```

**TC-005: Internal visibility**
```
Input:
  - visibility: "internal"

Expected Output:
  - tier: "1"
  - reason: "Risky: Internal visibility"

Assert:
  - classify_risk.py returns {"tier": "1"}
```

**TC-006: Non-standard naming (uppercase)**
```
Input:
  - name: "My_Service"
  - visibility: "private"

Expected Output:
  - tier: "1"
  - reason: "Risky: Non-standard naming"

Assert:
  - classify_risk.py returns {"tier": "1"}
```

**TC-007: Non-standard naming (special chars)**
```
Input:
  - name: "my.service@v1"
  - visibility: "private"

Expected Output:
  - tier: "1"
```

### Test Suite: Mock Terraform Plans

**TC-008: Parse terraform plan JSON (Tier 0)**
```
Input:
  - terraform plan output (mock): 1 resource to add (private repo)

Expected:
  - classify_risk.py parses JSON correctly
  - Returns tier "0"
```

**TC-009: Parse terraform plan JSON (Tier 1)**
```
Input:
  - terraform plan output (mock): 1 resource to destroy

Expected:
  - classify_risk.py parses JSON correctly
  - Returns tier "1"
```

---

## Integration Tests: GitHub Workflows (act)

### Test Suite: plan.yml Workflow

**TC-010: plan.yml triggers on PR**
```
Setup:
  - Create mock PR to main
  - Modify repositories/example.tfvars (add private repo)

Expected:
  - plan.yml workflow runs
  - Outputs terraform plan
  - Calls classify_risk.py
  - Posts PR comment with risk tier

Assert:
  - PR comment contains "Tier 0" or "Tier 1"
  - Terraform plan visible in comment
```

**TC-011: plan.yml classifies Tier 0**
```
Input: Private repo, standard name, add operation
Expected: PR comment shows "Tier 0 - Auto-approved"
Assert: Comment matches expected format
```

**TC-012: plan.yml classifies Tier 1**
```
Input: Delete operation
Expected: PR comment shows "Tier 1 - Needs review"
Assert: Comment mentions risky operation, flags CODEOWNERS
```

### Test Suite: apply.yml Workflow

**TC-013: apply.yml triggers on PR merge**
```
Setup:
  - Merge PR to main

Expected:
  - apply.yml workflow runs
  - terraform apply executes
  - terraform.tfstate commits to git

Assert:
  - New commit on main contains updated state
  - Commit message: "Update terraform.tfstate after apply"
```

**TC-014: apply.yml Tier 0 (auto-merge)**
```
Setup:
  - Create Tier 0 PR (private repo)
  - Verify auto-merge happens

Expected:
  - PR auto-merges
  - apply.yml runs on merge
  - Repo created on GitHub

Assert:
  - Repo exists on GitHub
  - terraform.tfstate updated
```

**TC-015: apply.yml Tier 1 (manual merge)**
```
Setup:
  - Create Tier 1 PR (delete operation)
  - Verify PR does NOT auto-merge
  - Manually merge PR

Expected:
  - PR requires manual action
  - apply.yml runs after manual merge
  - Repo deleted/archived

Assert:
  - Repo archived on GitHub
  - terraform.tfstate reflects deletion
```

---

## Integration Tests: CODEOWNERS

### Test Suite: CODEOWNERS Detection

**TC-016: CODEOWNERS present**
```
Setup:
  - .github/CODEOWNERS file exists with valid entries

Expected:
  - PR comment includes: "✓ CODEOWNERS assigned: @team/review"

Assert:
  - PR comment shows owner name
```

**TC-017: CODEOWNERS missing on Tier 1**
```
Setup:
  - .github/CODEOWNERS file missing
  - Create Tier 1 PR (delete operation)

Expected:
  - PR comment includes: "⚠️ CODEOWNERS missing"

Assert:
  - Warning appears alongside Tier 1 flag
  - Indicates manual review still needed
```

**TC-018: CODEOWNERS missing on Tier 0**
```
Setup:
  - .github/CODEOWNERS missing
  - Create Tier 0 PR (private repo)

Expected:
  - No warning (Tier 0 auto-merges regardless)

Assert:
  - PR auto-merges without CODEOWNERS blocking
```

---

## Contract Resolution Tests

### Test Suite: Child References Parent

**TC-019: Child reads workflow-contract.json**
```
Setup:
  - Child workflow on develop branch starts

Expected:
  - Child reads workflow-contract.json
  - Identifies: classify_risk.py is in parent@main

Assert:
  - Contract is valid JSON
  - All required fields present
```

**TC-020: Child fetches classify_risk.py from parent@main**
```
Setup:
  - Child workflow needs to classify risk
  - Parent has classify_risk.py on main branch

Expected:
  - Child fetches classify_risk.py from parent@main
  - Executes parent's script

Assert:
  - Classification uses parent's logic (not local)
  - Result is Tier 0 or 1 as expected
```

**TC-021: Child cannot modify immutable components**
```
Setup:
  - Try to override classify_risk.py in child

Expected:
  - Validation fails
  - Error: "classify_risk.py is immutable (parent-controlled)"

Assert:
  - Child cannot change governance logic
```

---

## Test Execution Matrix

| Test ID | Component | Type | Priority | Status |
|---------|-----------|------|----------|--------|
| TC-001 to TC-009 | classify_risk.py | Unit | P0 | Pending |
| TC-010 to TC-015 | Workflows | Integration | P0 | Pending |
| TC-016 to TC-018 | CODEOWNERS | Integration | P1 | Pending |
| TC-019 to TC-021 | Contract | Integration | P1 | Pending |

---

## Test Execution Commands

### Unit Tests (pytest)
```bash
pytest tests/test_classify_risk.py -v
pytest tests/test_classify_risk.py::test_tier_0_private_repo -v
pytest tests/test_classify_risk.py::test_tier_1_delete -v
```

### Workflow Tests (act)
```bash
act pull_request -j plan
act push -j apply
act workflow_dispatch -j request-operation
```

### All Tests
```bash
pytest tests/ -v && act --list
```

---

## Pass Criteria

**All tests must pass before:**
1. Phase 3 implementation
2. PR merge to main
3. Enterprise release

**Failure handling:**
- If test fails: Debug, fix code, re-run
- If test design wrong: Update test spec, re-run
- If contract needs change: Update workflow-contract.json, re-run tests
