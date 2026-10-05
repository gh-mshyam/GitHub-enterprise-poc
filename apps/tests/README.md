# Test Suite

Comprehensive test coverage for parent-child workflow architecture.

## Test Files

### Unit Tests (pytest)

```
tests/test_classify_risk.py
├─ TC-001 to TC-009: Risk classification
├─ Tier 0: private, standard naming, add/modify
├─ Tier 1: delete, public, internal, bad naming
└─ Matrix parametrized tests
   
tests/test_codeowners.py
├─ TC-016 to TC-018: CODEOWNERS detection
├─ Present: flag as assigned
├─ Missing Tier 1: flag as concern
└─ Missing Tier 0: info only

tests/test_contract_resolution.py
├─ TC-019 to TC-021: Contract validation
├─ Load and parse contract
├─ Parent reference resolution
├─ Immutability validation
└─ Divergence detection
```

### Integration Tests (act)

Workflows tested locally:

```
.github/workflows/plan.yml
  - Terraform plan succeeds
  - Risk classified Tier 0 or 1
  - PR comment posted
  
.github/workflows/apply.yml
  - Terraform apply succeeds on merge
  - State committed
  
.github/workflows/plan-child.yml
  - Fetches parent components
  - Verifies immutability
  - Uses parent classification
  
.github/workflows/apply-child.yml
  - References parent logic
  - Applies terraform on develop merge
```

## Running Tests

### Prerequisites

```bash
pip install pytest
# For act (workflow testing)
brew install act
```

### All Unit Tests

```bash
pytest tests/ -v
```

### Specific Test Suite

```bash
# Classification tests
pytest tests/test_classify_risk.py -v

# CODEOWNERS tests
pytest tests/test_codeowners.py -v

# Contract resolution tests
pytest tests/test_contract_resolution.py -v
```

### Matrix Tests Only

```bash
pytest tests/test_classify_risk.py::TestClassifyRiskMatrix -v
```

### Single Test Case

```bash
pytest tests/test_classify_risk.py::TestClassifyRisk::test_tc_001_tier0_private_standard_add -v
```

### Workflow Integration Tests (with act)

```bash
# Test plan workflow locally (main branch)
act pull_request -j plan --input operation=create

# Test apply workflow locally
act push -j apply

# Test child workflows (develop branch)
git checkout develop
act pull_request -j plan -W .github/workflows/plan-child.yml
act push -j apply -W .github/workflows/apply-child.yml
```

## Test Coverage Matrix

| Component | Test Type | Coverage | Pass Criteria |
|-----------|-----------|----------|---------------|
| classify_risk.py | Unit | 18 tests | All Tier 0/1 scenarios |
| check_codeowners.py | Unit | 5 tests | Present, missing, empty |
| resolve_contract.py | Unit | 8 tests | Load, validate, immutability |
| plan.yml | Integration | act | Plan succeeds, comment posted |
| apply.yml | Integration | act | Apply succeeds, state committed |
| plan-child.yml | Integration | act | Fetches parent, verifies |
| apply-child.yml | Integration | act | Uses parent logic |

## Test Scenarios

### Tier 0 Flow (Auto-Approve)

**Test:** Create private repo with standard name

```bash
# Modify tfvars
echo "data-service" >> repositories/example.tfvars

# Create PR
git checkout -b test/tier0
git commit -am "Add data-service"
git push

# Expected: PR shows "Tier 0 - Auto-approved"
# Test passes: classify_risk.py returns "0"
```

### Tier 1 Flow (Manual Review)

**Test:** Delete operation

```bash
# Modify tfvars (remove entry)
sed -i '/data-service/d' repositories/example.tfvars

# Create PR
git checkout -b test/tier1
git commit -am "Delete data-service"
git push

# Expected: PR shows "Tier 1 - Needs review"
# Test passes: classify_risk.py returns "1"
```

### CODEOWNERS Detection

**Test:** Missing CODEOWNERS on Tier 1

```bash
# Remove CODEOWNERS
rm .github/CODEOWNERS

# Create Tier 1 PR
# Expected: PR comment shows "⚠️ CODEOWNERS missing"
# Test passes: check_codeowners.py flags concern
```

### Contract Validation

**Test:** Child fetches parent immutable component

```bash
# On develop branch
git checkout develop

# Trigger plan-child.yml
# Expected: Fetches classify_risk.py from main@v1.0
# Test passes: Divergence check succeeds
```

## Continuous Integration

All tests run automatically on:
- PR to main: plan.yml test
- PR to develop: plan-child.yml test
- Push to main: apply.yml test
- Push to develop: apply-child.yml test

## Pass/Fail Criteria

### All Unit Tests Must Pass

```
pytest tests/ -v
# Expected: 31 passed
```

### All Integration Tests Must Pass

```
act pull_request -j plan
# Expected: Job succeeds, PR comment posted

act push -j apply
# Expected: Job succeeds, state committed
```

### Contract Validation Must Pass

```
python3 scripts/resolve_contract.py
# Expected: "✓ Contract resolved successfully"
```

## Known Issues

None at this time. All test cases passing as of v1.0.

## Adding New Tests

When adding new workflows or components:

1. Write unit test in `tests/test_*.py`
2. Run locally: `pytest tests/test_newfeature.py -v`
3. Write integration test in `tests/` or via act commands
4. Run: `act pull_request -j newjob`
5. Update this README with test coverage matrix
