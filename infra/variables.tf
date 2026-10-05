variable "github_owner" {
  description = "GitHub organization or user that owns the repositories"
  type        = string
}

variable "github_token" {
  description = "GitHub PAT with repo and admin:org scope, supplied via TF_VAR_github_token"
  type        = string
  sensitive   = true
}

variable "repositories" {
  description = "Map of repository name to its desired configuration"
  type = map(object({
    description        = optional(string, "")
    visibility         = optional(string, "private")
    homepage_url       = optional(string, null)
    has_issues         = optional(bool, true)
    has_wiki           = optional(bool, false)
    has_projects       = optional(bool, false)
    archive_on_destroy = optional(bool, true)
    topics             = optional(list(string), [])
    risk_tier          = optional(string, null)
    teams              = optional(map(string), {})
  }))
}
