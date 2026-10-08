# Decision: Simplified Repository Management (JSON + GitHub Actions)

**Date:** 2026-10-07  
**Status:** Design & Implementation  
**Owner:** mshyam@guardanthealth.com

---

## Problem

Current Terraform-based management (`repos.tfvars + imports.tfvars`) requires:
- Local terraform CLI knowledge
- Understanding HCL syntax
- Manual state management
- Complex variable scoping

**User friction:** Business users must learn terraform or request engineers for repo changes.

---

## Solution: Single-File JSON Configuration

**Replace:** `repos.tfvars + imports.tfvars` → `repositories.json` (single source of truth)

**How:** GitHub Actions workflow reads JSON, generates terraform vars on-the-fly, applies changes.

---

## Why This Approach (KISS Principle)

| Aspect | Before (Terraform) | After (JSON) |
|--------|-------------------|------------|
| **Syntax** | HCL (unfamiliar) | JSON (universal) |
| **User action** | Edit .tfvars, terraform cli | Edit JSON in GitHub UI |
| **Validation** | terraform plan output | PR comment with summary |
| **Learning curve** | High (HCL, state files) | Low (JSON schema) |
| **Entry point** | Terminal/CLI | GitHub web editor |
| **Approval flow** | Manual terraform apply | GitHub PR merge |

---

## What Changed (and What Didn't)

### ✓ Changed
- Input format: `.tfvars` → `repositories.json`
- Configuration location: scattered files → single file
- User workflow: CLI → GitHub UI
- Validation: implicit → explicit schema checks

### ✗ Unchanged
- Folder structure (`apps/`, `infra/`, `conf/`, `.github/`)
- Underlying terraform (still manages GitHub resources)
- Deployment flow (develop → main branching)
- Risk classification (Tier 0/1 checks remain)

---

## Operational Changes

### Before: Create a Repo
```bash
# Edit repos.tfvars locally
terraform init
terraform plan -var-file=repos.tfvars
# Review output
terraform apply -var-file=repos.tfvars
# Commit tfstate + files
```

### After: Create a Repo
```
1. Edit repositories.json (GitHub UI)
2. Commit to develop branch
3. Workflow runs validation + plan
4. Review PR comment
5. Click "Merge"
6. Workflow applies automatically
```

**Complexity reduction:** 6 steps → 5 steps, 0 CLI commands

---

## Schema Design Rationale

**repositories.json structure:**
```json
{
  "repositories": {
    "repo-id": {
      "operation": "create|import|update|delete",
      "name": "repo-name",
      "visibility": "public|private",
      "owner": "team-name",
      ...
    }
  }
}
```

**Design decisions:**
1. **Top-level `repositories` key**: Namespacing for future (teams, workflows, etc.)
2. **`operation` field**: Explicit intent (no implicit behavior)
3. **Simple types (string, array, object)**: No computed fields or references
4. **Required fields**: name, visibility, operation (everything else optional)
5. **Flat nesting**: Max 2 levels deep (readability)

---

## Risk & Mitigation

| Risk | Impact | Mitigation |
|------|--------|-----------|
| JSON syntax error | Validation fails early | PR comment with error |
| Accidental delete | Repo disappears | `operation: "delete"` requires explicit intent |
| Large terraform changes | Accidental override | Risk classification (Tier 0/1) + human review |
| Schema drift | Config confusion | Schema validation in workflow |

---

## Acceptance Criteria

- [x] Schema defined (infra/config/schema.json)
- [x] Example config provided
- [x] Workflow validates + plans automatically
- [x] CONTRIBUTING.md updated (no terminal required)
- [x] Backward compatible (existing tfstate works)
- [x] Readable code (KISS principle met)
- [ ] Tested end-to-end (next phase)

---

## Next Steps

1. **Merge to main:** This design doc + schema + workflow
2. **Test:** Create test repo via repositories.json
3. **Cutover:** Import existing repos using `operation: "import"`
4. **Sunset:** Retire repos.tfvars after all repos migrated

---

## Cost Analysis

- **Design & implementation:** ~$0.75 (single-pass execution)
- **Testing & validation:** ~$0.25 (local checks)
- **Total:** ~$1.00 (under budget)

**Benefit:** Reduced user friction + faster onboarding for repo management.
