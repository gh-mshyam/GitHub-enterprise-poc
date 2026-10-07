variable "name" {
  description = "Team name"
  type        = string
}

variable "description" {
  description = "Team description"
  type        = string
  default     = ""
}

variable "privacy" {
  description = "Team privacy level (closed or secret)"
  type        = string
  default     = "closed"

  validation {
    condition     = contains(["closed", "secret"], var.privacy)
    error_message = "Privacy must be 'closed' or 'secret'."
  }
}

variable "members" {
  description = "List of GitHub usernames to add as team members"
  type        = list(string)
  default     = []
}

variable "repositories" {
  description = "List of repository names to add to team"
  type        = list(string)
  default     = []
}
