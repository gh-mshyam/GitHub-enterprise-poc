variable "repo_name" {
  type        = string
  description = "Repository name"
}

variable "repo_owner" {
  type        = string
  description = "Repository owner"
}

variable "github_token" {
  type        = string
  sensitive   = true
  description = "GitHub token for authentication"
}

variable "template_dir" {
  type        = string
  description = "Path to template directory (relative to module)"
  default     = "../../../.github/templates/repo-scaffold"
}

variable "template_hash" {
  type        = string
  description = "Hash of template files to trigger sync on changes"
}
