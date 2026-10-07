# Auto-generated from infra/config/repositories.json
repositories = {
  "new-test-repo" = {
    name       = "new-test-repo"
    visibility = "private"
    description = "New test repo - created via dry run"
    topics = ["test", "dry-run"]
    teams = ["platform-team"]
  }
  "imported-repo" = {
    name       = "imported-repo"
    visibility = "private"
    topics = ["imported"]
    teams = ["platform-team"]
  }
  "imported-repo-updated" = {
    name       = "imported-repo-updated"
    visibility = "private"
    description = "Updated description after import"
    topics = ["imported", "updated"]
    teams = ["platform-team", "devops-team"]
  }
  "existing-repo-to-import" = {
    name       = "existing-repo-to-import"
    visibility = "private"
  }
}