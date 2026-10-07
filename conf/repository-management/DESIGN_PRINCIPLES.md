# Design Principles & Philosophy

Deep dive into why this system is designed this way and the philosophical choices behind it.

---

## Core Philosophy

This system follows a **"code as source of truth"** model with **"state as verification"** pattern.

### The Three Layers

```
Layer 1: CODE (repos.tfvars)
  ↓ "What we want"
  
Layer 2: STATE (terraform.tfstate)
  ↓ "What Terraform knows about"
  
Layer 3: REALITY (GitHub)
  ← "What actually exists"
```

**Goal:** Keep all three in sync.

**Check:** `git diff` tells you code changes. `terraform plan` shows you state→reality delta. Workflow runs apply if needed.

---

## Five Core Principles

### 1. Explicit > Implicit

**Statement:** Actions should have clear, visible intent. Never hide decisions.

**Applied Here:**

✅ **Good:**
```hcl
repositories = {
  "api-server" = {
    visibility = "private"
    archive_on_destroy = true
  }
}
```
Clear: We want this private, and when deleted, archive it.

❌ **Bad:**
```python
# Python script that auto-generates repos.tfvars
# (hidden logic about which repos to include)
```
Hidden: Users don't see the decision logic.

**Trade-off:** More lines of code in repos.tfvars, but crystal clear intent.

---

### 2. DRY (Don't Repeat Yourself)

**Statement:** Single source of truth for each piece of information.

**Applied Here:**

✅ **Good:**
```
One repos.tfvars file → One location for all repo config
```
If you need repo name, look in repos.tfvars. One place.

❌ **Bad (Old System):**
```
repositories.json (JSON)
  ↓ (Python conversion)
terraform.tfvars (HCL)
  ↓ (Terraform resource generation)
main.tf (resource definitions)
```
Same data in 3 formats = sync problems.

**Trade-off:** Less flexibility (can't have repos.tfvars do smart logic), but fewer bugs.

---

### 3. Immutable State

**Statement:** Terraform state is the source of truth for GitHub reality. Never edit it by hand.

**Applied Here:**

✅ **Right Way:**
```bash
# User wants to change something
git edit infra/repos.tfvars
git commit & push
workflow runs terraform apply
# State auto-updates as side effect
```

❌ **Wrong Way:**
```bash
# "I'll just edit terraform.tfstate directly"
# (breaks everything, Terraform gets confused)
```

**Why:** If you edit state by hand, Terraform's assumptions break. It loses track of what it owns.

**Principle:** State is auto-maintained by workflows. Users never touch it.

---

### 4. Fail Fast

**Statement:** Catch problems as early as possible in the pipeline.

**Applied Here:**

```
User commits bad config
    ↓
Push to develop
    ↓
CREATE-PR workflow (checks branches exist) ← Early check
    ↓
PR opens
    ↓
PLAN-VALIDATE workflow runs terraform plan ← Catches syntax/schema errors
    ↓
Plan fails → PR shows error ← User sees immediately
    ↓
User fixes locally, pushes again
```

vs.

```
User commits bad config
    ↓
... workflow waits ...
    ↓
Apply runs on main
    ↓
Apply fails → Everyone's blocked ← Too late!
```

**Trade-off:** Extra PR step (slower), but catches errors before they block the whole team.

---

### 5. Audit Trail

**Statement:** Every change should be auditable. Who changed what, when, why.

**Applied Here:**

All changes flow through git:
```bash
git log --oneline infra/repos.tfvars

2026-10-08 Add api-server repository
2026-10-07 Update backend-team on api-server
2026-10-06 Import legacy-system
```

Each commit has:
- Author (who)
- Timestamp (when)
- Message (why)
- Diff (what)

**Compliance:** If auditor asks "who created this repo and when?", git history shows it.

**Trade-off:** Can't make urgent changes directly (must go through git/PR); takes longer.

---

## Workflow Architecture Decisions

### Decision 1: Four Workflows (Not One)

**Could have done:** Single mega-workflow that does everything.

**Why we split:**

| Workflow | Trigger | Concern |
|----------|---------|---------|
| **import** | Manual | One-time ops (careful) |
| **create-pr** | Auto | Detect changes (fast feedback) |
| **plan-validate** | Auto | Catch errors (safety gate) |
| **apply** | Auto | Commit changes (automatic) |

**Benefit:** Each has single responsibility. Import doesn't mess with plan, etc.

**Cost:** 4 separate files to maintain, 4 places for bugs.

**Decision:** Worth it for clarity.

---

### Decision 2: Import Separate from Manage

**Could have done:** Single workflow that imports + manages.

**Why we split:**

**Import is:**
- One-time per repo
- Stateful (adds to state file)
- Requires repo to already exist on GitHub
- Manual trigger (careful, review before)

**Manage is:**
- Continuous (every commit)
- Idempotent (same result if run twice)
- Can create or update repos
- Auto trigger (fast feedback)

Mixing them = confusion about which mode you're in.

**Decision:** Separate workflows = clear intent.

---

### Decision 3: Centered (User-Editable) PRs

**Could have done:** Fully auto-generated PRs, no editing.

**Why we allow editing:**

```
Auto-PR created with generic message:
  "chore: sync repos.tfvars (develop → main)"

User can enhance:
  "chore: sync repos.tfvars: add backend-team, update api-server description"
  
  "This adds the newly formed backend-team to api-server 
   to grant deploy access. Also updates description to 
   reflect new SLA (99.99% uptime)."
```

**Benefit:** Git history is richer, easier to understand later.

**Cost:** Extra step for user (must remember to edit PR message).

**Decision:** Worth it for audit trail.

---

### Decision 4: Develop Branch (Not Direct to Main)

**Could have done:** Edit repos.tfvars directly on main.

**Why we use develop:**

```
User edits → develop
    ↓
CREATE-PR runs (detect changes)
    ↓
PR created (develop → main)
    ↓
Code review happens
    ↓
Merge to main
    ↓
PLAN runs (final check)
    ↓
APPLY runs
```

**Benefit:** Extra review gate before apply.

**Cost:** Extra branch, extra merge step.

**Decision:** Git flow is standard for a reason; worth the step.

---

## State Management Philosophy

### The State File Contract

Terraform maintains a "contract" with GitHub:

```
Contract: "I know about these repos and have their IDs/permissions/config"

If you break the contract (edit state by hand):
  Terraform: "I don't trust this state anymore"
  Result: Chaos (tries to recreate repos, fails)
```

**Our approach:** Never break the contract.

```
✅ Right:
  terraform import <repo-id>  (Terraform learns about repo)
  
✅ Right:
  terraform apply  (Terraform updates config)
  
✅ Right:
  terraform state rm <repo>  (Intentionally drop contract)
  
❌ Wrong:
  vim terraform.tfstate  (Hand-edit, break contract)
```

---

## Operational Philosophy

### Users Should...

1. **Edit Code, Not State**
   ```bash
   ✅ git edit infra/repos.tfvars
   ❌ terraform state rm repos
   ```

2. **Review Before Merging**
   ```bash
   ✅ terraform plan in PR (see what will happen)
   ❌ terraform apply in dark (no visibility)
   ```

3. **Import Existing Repos First**
   ```bash
   ✅ Run import workflow, then add to repos.tfvars
   ❌ Add to repos.tfvars and hope terraform imports
   ```

4. **Treat repos.tfvars Like Application Code**
   ```bash
   ✅ git diff, code review, commit messages
   ❌ Manual copy-paste of config
   ```

---

## Tradeoffs We Accepted

### Tradeoff 1: Cannot Create Repos in GitHub UI

**Cost:** No direct GitHub UI repo creation. Must edit code.

**Benefit:** Audit trail, centralized control, reproducible.

**Reasoning:** GitHub UI creation leaves no trace. Code creation is reviewable.

**When this hurts:** Rapid experimentation, need to spin up 10 test repos quickly.

**When this helps:** Compliance audit (show proof all repos went through code review).

---

### Tradeoff 2: Two-Step Import Process

**Cost:** User must run workflow, then manually paste config.

**Benefit:** Two-step = deliberate. User reviews config before it takes effect.

**Reasoning:** One-step import could accidentally add wrong config to repos.tfvars.

**When this hurts:** 100 repos to import at once (tedious manual copying).

**When this helps:** Careful migration (each repo gets reviewed).

---

### Tradeoff 3: Requires Git Knowledge

**Cost:** Team must understand git, branches, commits.

**Benefit:** All changes are auditable, reviewable, reversible.

**Reasoning:** Git is the audit trail. Can't skip it.

**When this hurts:** Team new to git (learning curve).

**When this helps:** Regulated industry (compliance requires git history).

---

### Tradeoff 4: Slower Than Manual Changes

**Cost:** Can't immediately apply changes (must go through PR).

**Benefit:** Forces review before changes are live.

**Reasoning:** Slowing down = preventing mistakes.

**When this hurts:** Operational emergencies (need to fix NOW).

**When this helps:** Normal development (prevents accidental damage).

---

## Why NOT Other Approaches

### Approach 1: Pure GitHub UI (No Code)

**Why we didn't:**
- No audit trail (who created what repo and when?)
- No reproducibility (can't rebuild)
- No code review (no safety gate)

**Conclusion:** For enterprise governance, not viable.

---

### Approach 2: Click-and-Wait Web Console

**Why we didn't:**
- GitHub UI would do click → logic → apply
- Feels fast but is actually fragile
- No version control

**Conclusion:** Moves complexity into UI instead of code.

---

### Approach 3: Full GitOps (ArgoCD, Flux)

**Why we didn't (for now):**
- Overcomplicated for repo management
- Adds dependency (GitOps controller in cluster)
- Harder to debug
- Better suited for Kubernetes configs

**Conclusion:** Overkill for GitHub repos; plain Terraform + GitHub Actions is simpler.

---

### Approach 4: JSON-Driven (Like Old System)

**Why we didn't:**
- JSON + Python conversion = two languages
- Sync problems (JSON gets out of sync with tfvars)
- More code to maintain

**Conclusion:** HCL is Terraform native language; use it directly.

---

## Evolution & Future

### Possible Future Changes

**If scale grows (1000s of repos):**
- Might split repos.tfvars into multiple files
- Could add auto-discovery (terraform import all)

**If team scales (100+ engineers):**
- Might add approval gates per team
- Could add different permissions per folder

**If compliance tightens:**
- Might add immutable audit log
- Could add encrypted state

**If gitops becomes standard:**
- Might integrate with ArgoCD
- Could add Helm/Kustomize layers

---

## Design Integrity Checks

**Every design decision is tested against:**

1. **Simplicity:** Can a new engineer understand it?
2. **Safety:** Does it prevent mistakes?
3. **Auditability:** Can we prove who changed what?
4. **Recoverability:** Can we rollback if something breaks?
5. **Scalability:** Does it work at 10 repos? 100? 1000?

**This design scores:**
- Simplicity: ⭐⭐⭐⭐ (HCL is readable)
- Safety: ⭐⭐⭐⭐⭐ (plan gate catches errors)
- Auditability: ⭐⭐⭐⭐⭐ (git history is perfect)
- Recoverability: ⭐⭐⭐⭐ (git rollback works, state can be re-imported)
- Scalability: ⭐⭐⭐ (works great to ~200 repos, then might need splitting)

---

## Summary: Why This Design

> We chose **code-driven, git-centric, plan-first repository management** because:
>
> 1. **Auditable:** Every change is in git history
> 2. **Safe:** Plan phase catches errors before apply
> 3. **Reproducible:** Same code = same state every time
> 4. **Reviewable:** PRs force human eyes on changes
> 5. **Reversible:** Can rollback with `git revert`
>
> The cost is speed (can't change immediately) and git knowledge (team must understand branches).
> The benefit is enterprise governance (compliance, audit, safety).

---

**Version:** 1.0  
**Last Updated:** 2026-10-08
