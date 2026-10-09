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

  allow_merge_commit = true
  allow_squash_merge = true
  allow_rebase_merge = false
}

resource "github_repository_vulnerability_alerts" "this" {
  repository = github_repository.this.name
}

# Bootstrap repository with template files
resource "null_resource" "bootstrap_template" {
  depends_on = [github_repository.this]

  provisioner "local-exec" {
    command = "python3 ../../apps/scripts/bootstrap_repo.py ${var.name} ${var.github_owner}"

    environment = {
      GITHUB_TOKEN = var.github_token
    }
  }
}

# Basic branch protection for main branch
# NOTE: Requires GitHub Pro or public repository. Disabled for free accounts.
# resource "github_branch_protection" "main" {
#   repository_id = github_repository.this.id
#   pattern       = "main"
#
#   enforce_admins            = false
#   require_conversation_resolution = true
# }
