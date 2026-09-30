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

variable "risk_tier" {
  description = "Risk tier for this repository: \"0\" (standard) or \"1\" (higher risk, stricter branch protection)"
  type        = string
  default     = "0"

  validation {
    condition     = contains(["0", "1"], var.risk_tier)
    error_message = "risk_tier must be \"0\" or \"1\"."
  }
}

variable "teams" {
  description = "Map of team slug to permission level (pull, triage, push, maintain, admin)"
  type        = map(string)
  default     = {}
}
