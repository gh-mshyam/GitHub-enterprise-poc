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

  "phase1-test-repo" = {
    description = "Phase 1 Test A: Create repo (Tier 0)"
    visibility  = "private"
    topics      = ["phase1", "test"]
    teams = {
      "platform-team" = "push"
    }
  }
}
