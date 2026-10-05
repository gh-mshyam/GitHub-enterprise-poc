# Child Implementation (develop branch)

This branch demonstrates how a CHILD repository references and uses PARENT components.

## Child Workflows

### plan-child.yml
- Triggers on PRs to `develop` (child branch)
- **Fetches parent components:**
  - `scripts/classify_risk.py` from `main@v1.0`
  - `scripts/check_codeowners.py` from main
- **Verifies immutability:** Checks that classify_risk.py hasn't diverged from parent
- **Runs classification:** Uses parent's governance rules
- **Posts PR comment:** Risk tier + CODEOWNERS status

### apply-child.yml
- Triggers on PR merge to `develop`
- **Uses parent logic:** No modifications to core governance
- **Executes terraform:** Creates/deletes repos per child's tfvars
- **Commits state:** Updates terraform.tfstate on develop

## Child Contract

**File:** `workflow-contract.json` (same as parent)

**Declares:**
```json
{
  "parent_reference": "main",
  "semantic_version": "v1.0",
  "parent_components": {
    "scripts": ["classify_risk.py"],
    "workflows": ["plan.yml", "apply.yml"]
  },
  "child_requirements": {
    "inherit_from_parent": ["scripts/classify_risk.py", ".github/workflows/plan.yml"],
    "can_override": ["scripts/modify_tfvars.py", ".github/workflows/request-operation.yml"]
  }
}
```

## How Child Uses Parent

1. **PR created on develop** → Triggers plan-child.yml
2. **plan-child.yml fetches parent components:**
   ```bash
   git fetch origin main:main
   git show origin/main:scripts/classify_risk.py > scripts/classify_risk.py
   ```
3. **Verifies immutability:**
   - Checks if local copy differs from parent@main
   - Fails if divergence detected
4. **Executes parent logic:**
   - `python3 scripts/classify_risk.py` (parent's rules)
   - Classifies as Tier 0 or Tier 1
5. **PR comment shows:**
   - Risk classification (from parent logic)
   - CODEOWNERS status
6. **If Tier 0:** Auto-merge → apply-child.yml runs
7. **If Tier 1:** Manual approval needed

## Immutability Enforcement

**Cannot override (parent-controlled):**
- `scripts/classify_risk.py` ← Must always use parent's version
- `.github/workflows/plan.yml` (referenced, not modified)
- `.github/workflows/apply.yml` (referenced, not modified)

**Can override (child-specific):**
- `scripts/modify_tfvars.py` ← Child can customize
- `.github/workflows/request-operation.yml` ← Child can customize
- `.github/CODEOWNERS` ← Child's own ownership rules

## Validation

Run contract resolver:
```bash
python3 scripts/resolve_contract.py
```

Output:
```
=== Contract Resolution Report ===

Contract Version: 1.0
Parent Reference: main
Resolved Parent: main@v1.0

Parent Components (Immutable):
  • classify_risk.py: scripts/classify_risk.py

Immutability Validation:
  ✓ All immutable components validated

✓ Contract resolved successfully
```

## Benefits (Child Perspective)

✅ **Always use latest parent rules** — No governance drift  
✅ **Cannot bypass governance** — Immutable components enforced  
✅ **Updates automatic** — When parent@main changes, child gets it  
✅ **Transparency** — Contract declares all parent references  
✅ **Scalability** — 1 parent, 100s of children, 1 set of rules

## Upgrade Path

When parent releases v1.1:
1. Parent tags `v1.1`
2. Update contract: `"semantic_version": "v1.1"`
3. Next PR run fetches from `main@v1.1`
4. No breaking changes (immutability ensured)
