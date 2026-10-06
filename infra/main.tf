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
