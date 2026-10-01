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

,
  "test-phase3-repo" = {
    description = "Phase 3 test repo for business user workflow"
    visibility  = "private"
    topics      = ["service"]
    teams = {
      "platform-team" = "push"
    }
  }
}