output "repository_full_name" {
  description = "Full name (owner/repo) of the created repository"
  value       = github_repository.this.full_name
}

output "repository_node_id" {
  description = "GraphQL node ID of the repository, used for branch protection resources"
  value       = github_repository.this.node_id
}

output "risk_tier" {
  description = "Risk tier applied to this repository"
  value       = var.risk_tier
}
