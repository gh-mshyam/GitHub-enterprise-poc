# Parent Workflow Architecture (v1.0)

This repository serves as both PARENT and CHILD for the POC. In production:
- **Parent:** Hosted in central repository (e.g., `common-workflows`)
- **Child:** Individual repos reference parent via `workflow-contract.json`

## Parent Components

### Immutable (Parent-Controlled)

```
scripts/classify_risk.py
├─ Deterministic risk classification (Tier 0 vs 1)
├─ NO child modifications allowed
├─ Hosted on: main branch
└─ Versioned: v1.0, v1.1, etc.

.github/workflows/plan.yml
├─ Terraform plan + risk classification
├─ Calls classify_risk.py (from parent)
├─ NO child modifications allowed
└─ Versioned: v1.0

.github/workflows/apply.yml
├─ Execute terraform, commit state
├─ Triggered on PR merge (Tier 0 auto, Tier 1 manual)
├─ NO child modifications allowed
└─ Versioned: v1.0
```

### Child-Customizable

```
scripts/modify_tfvars.py
├─ Operational helper (not critical governance)
└─ Children CAN override for custom logic

.github/workflows/request-operation.yml
├─ Business user interface
├─ Implementation details can vary per child
└─ Children CAN customize for their workflows
```

## Parent Versioning

- **Branch:** `main` (stable)
- **Tags:** `v1.0`, `v1.1`, `v2.0` (releases)
- **Child references:** `parent@main` or `parent@v1.0`
- **Update strategy:** Children auto-sync to latest parent main (no locking)

## Child Integration

**Step 1: Child reads contract**
```json
// workflow-contract.json
{
  "parent_components": {
    "scripts": ["classify_risk.py"],
    "workflows": ["plan.yml", "apply.yml"]
  }
}
```

**Step 2: Child fetches from parent**
```yaml
# .github/workflows/plan-child.yml
- name: Fetch Parent Components
  run: |
    curl -o scripts/classify_risk.py \
      https://raw.githubusercontent.com/[parent-repo]/main/scripts/classify_risk.py
```

**Step 3: Child executes with parent logic**
```yaml
- name: Classify Risk (uses parent script)
  run: python3 scripts/classify_risk.py terraform/tfplan.json
```

## Immutability Enforcement

- Parent components tagged as `immutable: true` in contract
- Child validation: checks if local copy differs from parent@main
- If divergence detected: fail with error "Component diverged from parent"
- This prevents governance drift

## Governance Flow

```
Parent Main Branch (v1.0)
  ├─ classify_risk.py (immutable governance rules)
  ├─ plan.yml (consistent risk classification)
  └─ apply.yml (consistent execution)

Child Repo (develop)
  ├─ workflow-contract.json (declares parent reference)
  ├─ plan-child.yml (fetches classify_risk.py from parent@main)
  └─ apply-child.yml (uses parent logic)

Change Flow:
  1. Update parent rule → test on parent main
  2. Tag parent: v1.1
  3. Children can opt-in: parent@v1.1
  4. Automatic via parent@main (latest)
```

## Benefits

✅ **Centralized governance** — One source of truth for risk rules  
✅ **No drift** — Children always use parent's latest logic  
✅ **Immutability** — Can't bypass governance at child level  
✅ **Versioning** — Can track and audit rule changes  
✅ **Scalability** — 100s of children, 1 parent source  

## Current State (POC)

- Parent: main branch
- Child: develop branch
- Same repo (dual-role for demo)
- In production: separate repos with different permissions
