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
    path = "infra/terraform.tfstate"
  }
}

provider "github" {
  token = var.github_token
  owner = var.github_owner
}

module "repository" {
  source = "./modules/repository"

  for_each = var.repositories

  name               = each.key
  description        = each.value.description
  visibility         = each.value.visibility
  homepage_url       = each.value.homepage_url
  has_issues         = each.value.has_issues
  has_wiki           = each.value.has_wiki
  has_projects       = each.value.has_projects
  archive_on_destroy = each.value.archive_on_destroy
  topics             = each.value.topics
  github_owner       = var.github_owner
  github_token       = var.github_token
}

module "teams" {
  source = "./modules/teams"

  for_each = var.teams

  name         = each.key
  description  = each.value.description
  privacy      = each.value.privacy
  members      = each.value.members
  repositories = each.value.repositories
}

# Template sync for existing repositories
# This syncs repo-scaffold template files to managed repositories
locals {
  # Hash all template files to trigger re-sync on any template change
  template_files = fileset("${path.module}/../../.github/templates/repo-scaffold", "**/*")
  template_hash  = md5(join(",", [for f in local.template_files : filemd5("${path.module}/../../.github/templates/repo-scaffold/${f}")]))
}

module "template_sync" {
  source = "./modules/template-sync"

  # Sync backend-api as test case
  repo_name    = "backend-api"
  repo_owner   = var.github_owner
  github_token = var.github_token
  # Use absolute path for template directory
  template_dir = abspath("${path.module}/../../.github/templates/repo-scaffold")
  # Hash of all template files to trigger re-sync on ANY template change
  template_hash = local.template_hash

  depends_on = [module.repository]
}
