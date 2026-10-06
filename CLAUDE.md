# GitHub Enterprise POC — Project Instructions

**This repository works with any coding agent.**

## Agent Entry Points

Pick the one matching your agent:

- **Claude users** → `.claude/CLAUDE.md`
- **Codex users** → `.codex/CLAUDE.md`
- **Grok users** → `.grok/CLAUDE.md`
- **Other agents** → `.ghdp/INSTRUCTIONS.md`

Each entry point provides quick start and links to full instructions.

## Full Instructions

**Read:** `.ghdp/INSTRUCTIONS.md` — Complete agent-agnostic instructions covering:
- Project context and structure
- Workflow (local dev → PR → merge → deploy)
- Code principles and folder rules
- Testing checklist
- Common tasks
- Known limitations

## Quick Overview

- **What:** Autonomous GitHub repo/team provisioning via Terraform
- **How:** `plan.yml` (PR) → `apply.yml` (merge) → workflows deploy
- **Where:** `infra/` (terraform), `apps/` (helpers), `.ghdp/` (governance)
- **Config:** `infra/repositories/` (repos.tfvars, teams.tfvars, imports.tfvars)

## Next Steps

1. **Open the entry point for your agent** (see above)
2. **Read `.ghdp/INSTRUCTIONS.md`** for full context
3. **Check `README.md`** for project overview
4. **Review module READMEs** for specific tasks

---

**All instructions are agent-agnostic** — managed in `.ghdp/INSTRUCTIONS.md`.  
**Agent-specific entry points** in `.claude/`, `.codex/`, `.grok/` for convenience.
