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

  "gh-enterprise-poc-public-demo" = {
    description = "Tier 1: public visibility auto-classifies as higher risk"
    visibility  = "public"
    topics      = ["demo", "public"]
    teams = {
      "platform-team" = "push"
    }
  }

  "new-data-initiative" = {
    description = "Tier 1: private repo but provisioning a brand-new team"
    visibility  = "private"
    risk_tier   = "1"
    topics      = ["data", "new-initiative"]
    teams = {
      "data-initiative-new-team" = "admin"
    }
  }

  "test-repo-001" = {
    description = "Test: public repo with platform team (Tier 1 - visibility change)"
    visibility  = "public"
    topics      = ["test", "public"]
    teams = {
      "platform-team" = "push"
    }
  }
}
