terraform {
  required_version = ">= 1.5.0"

  required_providers {
    github = {
      source  = "integrations/github"
      version = "~> 6.0"
    }
  }

  # Local backend only. This is a POC trade-off: state is committed back to
  # the repo by apply.yml for demo visibility, not a production pattern
  # (no locking, no encryption at rest, no drift protection between runs).
  backend "local" {
    path = "terraform.tfstate"
  }
}

provider "github" {
  token = var.github_token
  owner = var.github_owner
}

locals {
  # Repositories that don't declare an explicit risk_tier are auto-tiered
  # from their visibility alone: anything other than "private" is Tier 1.
  # This is a conservative default only — it does not know about new teams,
  # deletions, or naming conventions. Those signals are evaluated separately
  # against the *plan diff* by scripts/classify_risk.py in plan.yml, which
  # is the source of truth for PR-time risk gating.
  repositories_with_tier = {
    for repo_name, repo in var.repositories : repo_name => merge(repo, {
      risk_tier = coalesce(repo.risk_tier, repo.visibility != "private" ? "1" : "0")
    })
  }
}

module "repository" {
  source = "./modules/repository"

  for_each = local.repositories_with_tier

  name               = each.key
  description        = each.value.description
  visibility         = each.value.visibility
  homepage_url       = each.value.homepage_url
  has_issues         = each.value.has_issues
  has_wiki           = each.value.has_wiki
  has_projects       = each.value.has_projects
  archive_on_destroy = each.value.archive_on_destroy
  topics             = each.value.topics
  risk_tier          = each.value.risk_tier
  teams              = each.value.teams
}
