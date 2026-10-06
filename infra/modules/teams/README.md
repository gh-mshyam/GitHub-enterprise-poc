# Teams Module

This module creates and manages GitHub teams, team members, and team repository access.

## How to Add a New Team?

1. Open `repositories/teams.tfvars` and add a new entry:

```hcl
teams = {
  "backend-team" = {
    name        = "Backend Team"
    description = "Backend engineers"
    privacy     = "closed"
    members     = ["user1", "user2"]
    repositories = ["api-server", "database-utils"]
  }
}
```

2. Run `terraform plan` to review changes
3. Create a PR and merge
4. Once merged, the deploy workflow will apply the changes

## How to Add an Existing Team?

If you have an existing GitHub team that you want to import into Terraform:

1. Identify the team slug (e.g., `backend-team`)
2. Add the import statement to `infra/main.tf`:

```bash
terraform import 'module.teams["backend-team"].github_team.this' TEAM_ID
```

3. Add the configuration to `repositories/teams.tfvars`
4. Commit and push

## Team Configuration Options

- **name**: Team name (displayed in GitHub)
- **description**: Team description (optional)
- **privacy**: `closed` (members visible to org) or `secret` (members hidden)
- **members**: List of GitHub usernames to add
- **repositories**: List of repository names to grant access to

All team members get "push" permission on assigned repositories.
