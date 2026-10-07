# Teams Module

## How to Add a New Team?

1. Edit `infra/repositories/teams.tfvars`
2. Add entry:
   ```hcl
   "backend-team" = {
     description  = "Backend engineers"
     privacy      = "closed"
     members      = ["user1", "user2"]
     repositories = ["repo1", "repo2"]
   }
   ```
3. Create PR → On merge, team is created

## How to Add an Existing Team?

1. Edit `infra/repositories/teams.tfvars`
2. Add team configuration:
   ```hcl
   "existing-team" = {
     description  = "Existing team description"
     privacy      = "closed"
     members      = ["user1", "user2"]
     repositories = ["repo-name"]
   }
   ```
3. Get team ID: `gh api orgs/ORGNAME/teams/existing-team --jq '.id'`
4. Import: `terraform import 'module.teams["existing-team"].github_team.this' TEAM_ID`
5. Create PR with changes → Merge → Team is imported

## Configuration Options

- `description` — Team description
- `privacy` — "closed" (members visible) or "secret" (hidden)
- `members` — List of GitHub usernames
- `repositories` — List of repo names to assign to team
