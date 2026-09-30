terraform {
  required_providers {
    github = {
      source = "integrations/github"
    }
  }
}

resource "github_repository" "this" {
  name        = var.name
  description = var.description
  visibility  = var.visibility

  homepage_url = var.homepage_url

  has_issues   = var.has_issues
  has_wiki     = var.has_wiki
  has_projects = var.has_projects

  topics = var.topics

  archive_on_destroy = var.archive_on_destroy

  delete_branch_on_merge = true

  # Tier 1 repositories (public, new team, or otherwise flagged as higher
  # risk) are restricted to squash-only merges to keep history linear and
  # reduce the surface area for an accidental force-push style rewrite.
  # Tier 0 repositories keep merge commits available for normal workflow.
  allow_merge_commit = var.risk_tier == "0"
  allow_squash_merge = true
  allow_rebase_merge = false
}

resource "github_repository_vulnerability_alerts" "this" {
  repository = github_repository.this.name
}

resource "github_team_repository" "this" {
  for_each = var.teams

  team_id    = each.key
  repository = github_repository.this.name
  permission = each.value
}

locals {
  # Branch protection strictness is keyed off risk_tier. Tier 1 gets a
  # second required reviewer, mandatory CODEOWNERS sign-off, admins held
  # to the same rule, stale-review dismissal on new pushes, and required
  # conversation resolution before merge. Tier 0 keeps a lighter single
  # reviewer gate so routine, low-risk changes aren't slowed down.
  branch_protection_by_tier = {
    "0" = {
      required_approving_review_count = 1
      require_code_owner_reviews      = false
      enforce_admins                  = false
      dismiss_stale_reviews           = false
      require_conversation_resolution = false
    }
    "1" = {
      required_approving_review_count = 2
      require_code_owner_reviews      = true
      enforce_admins                  = true
      dismiss_stale_reviews           = true
      require_conversation_resolution = true
    }
  }

  branch_protection_settings = local.branch_protection_by_tier[var.risk_tier]
}

resource "github_branch_protection" "default" {
  repository_id = github_repository.this.node_id
  # Not read from github_repository.this.default_branch: that attribute is
  # deprecated by the provider. This POC assumes "main" as the default
  # branch for every repository it provisions.
  pattern = "main"

  required_pull_request_reviews {
    required_approving_review_count = local.branch_protection_settings.required_approving_review_count
    require_code_owner_reviews      = local.branch_protection_settings.require_code_owner_reviews
    dismiss_stale_reviews           = local.branch_protection_settings.dismiss_stale_reviews
  }

  enforce_admins                  = local.branch_protection_settings.enforce_admins
  require_conversation_resolution = local.branch_protection_settings.require_conversation_resolution
}
