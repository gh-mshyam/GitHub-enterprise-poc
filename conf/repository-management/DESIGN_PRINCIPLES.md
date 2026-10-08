# Why We Built It This Way

Explains the decisions behind the system design.

---

## Core Idea

We chose to use **code as the source of truth**.

This means: Your repos.tfvars file is the official record. GitHub is a copy. Terraform keeps them in sync.

**Alternative:** Use GitHub as the official record. This causes problems because changes are hard to track.

**Our choice:** Code is official. GitHub follows.

---

## Five Design Decisions

### Decision 1: One File (repos.tfvars)

**What we chose:**
All repository configurations in one file: `repos.tfvars`

**Why:**
- Easy to find information
- Everyone looks in one place
- No duplication

**Alternative we rejected:**
- JSON file + Python conversion + Terraform
- Multiple config sources
- Risk: files get out of sync

**Trade-off:**
- Simpler (one file)
- Less flexible (cannot do complex logic)

**Verdict:** Simplicity wins.

---

### Decision 2: Import Separate from Management

**What we chose:**
- Import is a one-time operation (manual)
- Management is continuous (automatic)
- Two different workflows

**Why:**
- Clear intent: "Is this one-time or ongoing?"
- Safer: Import requires careful review
- No confusion: Different modes for different purposes

**Alternative we rejected:**
- Single workflow that imports and manages
- Automatic import when added to repos.tfvars

**Trade-off:**
- More workflows to maintain
- Extra step for users
- Clearer process

**Verdict:** Clarity wins.

---

### Decision 3: All Changes Through Git

**What we chose:**
Every change must go through git commits and pull requests.

**Why:**
- Audit trail: Who changed what and when?
- Review: Someone else checks before applying
- Reversible: Can undo with git revert

**Alternative we rejected:**
- Apply changes directly from your machine
- Create repositories in GitHub UI directly

**Trade-off:**
- Slower (extra PR step)
- More process
- Auditable

**Verdict:** Safety and audit win.

---

### Decision 4: Plan Before Apply

**What we chose:**
Show what will change before actually changing it.

**Why:**
- Prevents mistakes
- Everyone can review the plan
- Catch errors early

**Alternative we rejected:**
- Apply changes without showing plan first

**Trade-off:**
- Extra workflow step
- Takes time
- More safety

**Verdict:** Safety wins.

---

### Decision 5: User-Editable Pull Requests

**What we chose:**
Pull requests are auto-created but users can edit the title and message.

**Why:**
- Users add context (why is this change needed?)
- Better git history (easier to understand later)
- Team communication (someone reviewing sees the reason)

**Alternative we rejected:**
- Fully auto-generated PRs with no editing
- Fully manual PRs (users create from scratch)

**Trade-off:**
- Extra step (users must edit)
- More complete history

**Verdict:** Better history wins.

---

## What We Rejected and Why

### Rejected Option 1: GitHub UI Only

**Description:** Create and manage all repositories in GitHub's web interface.

**Why we rejected it:**
- No audit trail (who created what repo?)
- No code review (no safety gate)
- Not reproducible (cannot rebuild state)
- Compliance problems (no proof of authorization)

**Verdict:** Not suitable for enterprise.

---

### Rejected Option 2: Web Console

**Description:** Use a custom web application to manage repositories.

**Why we rejected it:**
- Extra tool to maintain
- Hard to debug
- No version control
- Adds complexity

**Verdict:** Git is simpler.

---

### Rejected Option 3: Full GitOps (ArgoCD, Flux)

**Description:** Use Kubernetes GitOps tools to manage GitHub repositories.

**Why we rejected it:**
- Overkill for repository management
- Adds dependency on extra system
- More complex to debug
- Better for Kubernetes configurations, not repos

**Verdict:** Terraform + GitHub Actions is simpler for this job.

---

### Rejected Option 4: JSON-Based (Old System)

**Description:** Use JSON files with Python scripts to convert to Terraform.

**Why we rejected it:**
- Multiple file formats (JSON, HCL, Python)
- Sync problems (files diverge)
- Extra conversion step
- More code to maintain
- More places for bugs

**Verdict:** Direct HCL is simpler.

---

## Important Principles

### Principle 1: Code Is Official

What your repos.tfvars says is what should exist on GitHub.

If they do not match, GitHub is wrong. The system fixes it.

**Example:**
```
repos.tfvars says: "api-server" visibility is private
GitHub shows: "api-server" visibility is public

System fixes it: Changes GitHub to private
```

---

### Principle 2: State is Never Manual

The terraform.tfstate file is maintained automatically. Never edit it by hand.

If you edit it, the system breaks.

**Never do this:**
```bash
vim terraform.tfstate
```

**Always do this:**
```bash
Let the workflows manage it
```

---

### Principle 3: Audit Trail Is Mandatory

Every change must be in git history.

Someone must review every change.

**This ensures:**
- We know who changed what
- We know when it changed
- We know why it changed
- We can undo if needed

---

### Principle 4: Fail Early

Catch problems as soon as possible.

The plan workflow runs on PRs. This catches errors before they reach production.

**Better to fail here:**
```
User commits → Workflow checks → Plan fails → User fixes → Tries again
```

**Worse to fail here:**
```
User commits → Merge → Apply runs → Apply fails → Everyone blocked
```

---

### Principle 5: Immutable Records

Once something is committed to git, you do not change it.

You revert it instead.

**Correct:**
```bash
git revert <old-commit-hash>
```

**Wrong:**
```bash
git reset --hard <old-commit-hash>
```

---

## When This System Works Well

Use this system when:

✅ You have 10 to 100 repositories

✅ Your team cares about audit trails

✅ You need to review changes before applying

✅ Your organization has compliance requirements

✅ You want consistent team permissions across repositories

✅ You want reproducible deployments

---

## When This System Is Not Ideal

This system might not be best when:

❌ You have 1,000+ repositories (state file becomes heavy)

❌ You need emergency changes immediately (process adds time)

❌ You create and delete repositories hourly (high churn)

❌ Your team is uncomfortable with git

❌ You want fully automated with no human review

---

## Trade-offs We Accepted

### Trade-off 1: No GitHub UI Creation

**Cost:** Cannot create repositories directly in GitHub.

**Benefit:** All creations are auditable and reviewable.

**Best for:** Compliance and governance.

---

### Trade-off 2: Two-Step Import

**Cost:** Users must run workflow, then manually add config.

**Benefit:** Users review config before it applies.

**Best for:** Careful migration of existing repositories.

---

### Trade-off 3: Slower Than Direct Changes

**Cost:** Changes take longer (must go through PR).

**Benefit:** Prevents accidental mistakes.

**Best for:** Reducing errors and incidents.

---

### Trade-off 4: Requires Git Knowledge

**Cost:** Team must understand branches and commits.

**Benefit:** Complete audit trail and version control.

**Best for:** Professional software teams.

---

## The Philosophy in One Sentence

We chose **safety and auditability** over speed and simplicity.

---

**Version:** 1.0  
**Language:** Simplified Technical English
