variable "name" {
  description = "Repository name"
  type        = string
}

variable "description" {
  description = "Repository description"
  type        = string
  default     = ""
}

variable "visibility" {
  description = "Repository visibility: private, public, or internal"
  type        = string
  default     = "private"
}

variable "homepage_url" {
  description = "Optional homepage URL for the repository"
  type        = string
  default     = null
}

variable "has_issues" {
  description = "Enable GitHub Issues for this repository"
  type        = bool
  default     = true
}

variable "has_wiki" {
  description = "Enable the GitHub Wiki for this repository"
  type        = bool
  default     = false
}

variable "has_projects" {
  description = "Enable GitHub Projects for this repository"
  type        = bool
  default     = false
}

variable "archive_on_destroy" {
  description = "Archive instead of deleting the repository on destroy"
  type        = bool
  default     = true
}

variable "topics" {
  description = "List of topic tags for the repository"
  type        = list(string)
  default     = []
}

variable "github_owner" {
  description = "GitHub organization/owner"
  type        = string
}

variable "github_token" {
  description = "GitHub token for bootstrap provisioner"
  type        = string
  sensitive   = true
}

variable "branch_protection_rules" {
  description = "Branch protection rules for main branch"
  type = object({
    main_branch                    = string
    require_code_owner_reviews     = bool
    required_approving_review_count = number
    dismiss_stale_reviews          = bool
  })
  default = null
}
