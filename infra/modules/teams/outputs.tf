output "team_id" {
  description = "The ID of the GitHub team"
  value       = github_team.this.id
}

output "team_slug" {
  description = "The slug of the GitHub team"
  value       = github_team.this.slug
}

output "team_name" {
  description = "The name of the GitHub team"
  value       = github_team.this.name
}
