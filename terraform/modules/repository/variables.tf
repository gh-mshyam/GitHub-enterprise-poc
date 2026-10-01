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

