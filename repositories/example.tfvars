github_owner = "gh-mshyam"

repositories = {
  "enterprise-test-repo" = {
    description = "Test repo for testing the engineer persona for reproduction"
    visibility  = "private"
    topics      = ["test", "engineering"]
    teams = {
      "data-platform" = "push"
    }
  }
}
