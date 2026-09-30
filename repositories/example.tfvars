github_owner = "gh-mshyam"

repositories = {
  "svc-payments-api" = {
    description = "Tier 0: private repo, existing platform team, standard naming"
    visibility  = "private"
    topics      = ["service", "payments"]
    teams = {
      "platform-team" = "push"
    }
  }

  "test-repo-001" = {
    description = "Test: new private repo with platform team attachment"
    visibility  = "private"
    topics      = ["test"]
    teams = {
      "platform-team" = "push"
    }
  }

  "analytics-pipeline" = {
    description = "Private analytics data pipeline service"
    visibility  = "private"
    topics      = ["analytics", "data-pipeline"]
    teams = {
      "platform-team" = "push"
    }
  }
}
