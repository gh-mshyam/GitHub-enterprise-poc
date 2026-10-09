# Repository Management - Single Source of Truth
#
# Edit this file to create, update, or delete repositories.
# Changes are applied automatically via GitHub Actions workflows.
#
# Workflow: develop → PR → review → main → terraform apply
#
# To create a new repository:
#   1. Add entry below
#   2. Commit to develop
#   3. Create PR
#   4. Review plan
#   5. Merge to main
#   6. Workflow applies automatically
#
# To delete a repository:
#   1. Remove entry below
#   2. Commit to develop
#   3. Create PR
#   4. Merge to main
#   5. Workflow removes repository

repositories = {

  # Example: Create new repository
  # "api-server" = {
  #   name        = "api-server"
  #   visibility  = "private"
  #   description = "Core API service"
  #   has_issues  = true
  #   has_wiki    = false
  #   has_projects = true
  #   archive_on_destroy = true
  #   homepage_url = "https://api.example.com"
  #   owner = "backend-team"
  #   topics = ["api", "microservice", "golang"]
  #   teams = ["backend-team", "devops-team"]
  # }

  # Add repositories here
  "testing-api" = {
    name        = "testing-api"
    visibility  = "private"
    description = "Testing API service for deployment validation"
    teams       = ["backend-team"]
    topics      = ["api", "testing"]
  }

}
