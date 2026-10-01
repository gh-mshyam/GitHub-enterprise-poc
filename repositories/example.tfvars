github_owner = "gh-mshyam"

repositories = {
  "enterprise-test-repo-1" = {
    description = "Test repo for testing the engineer persona for reproduction"
    visibility  = "private"
    topics      = ["test", "engineering"]
    teams = {
      "data-platform" = "push"
    }
  }
}
