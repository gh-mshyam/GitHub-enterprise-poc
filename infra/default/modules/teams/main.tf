terraform {
  required_providers {
    github = {
      source = "integrations/github"
    }
  }
}

resource "github_team" "this" {
  name        = var.name
  description = var.description
  privacy     = var.privacy
}

resource "github_team_membership" "this" {
  for_each = toset(var.members)

  team_id  = github_team.this.id
  username = each.value
  role     = "member"
}

resource "github_team_repository" "this" {
  for_each = toset(var.repositories)

  team_id    = github_team.this.id
  repository = each.value
  permission = "push"
}
