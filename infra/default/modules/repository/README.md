# Repository Module

## How to Add a New Repository?

1. Edit `infra/repositories/repos.tfvars`
2. Add entry:
   ```hcl
   "my-repo" = {
     description = "My new repository"
     visibility  = "private"
     topics      = ["my-topic"]
   }
   ```
3. Create PR → On merge, repository is created

## How to Add an Existing Repository?

1. Go to **Actions** → **Discover Repository for Import** → **Run workflow**
2. Enter repository URL: `https://github.com/org/repo`
3. Workflow creates PR with discovered configuration
4. Review PR → Merge → Repository is imported into Terraform

## Configuration Options

- `description` — Repository description
- `visibility` — "private", "internal", or "public"
- `topics` — List of topics (optional)
- `homepage_url` — Website URL (optional)
- `has_issues` — Enable issues (default: true)
- `has_wiki` — Enable wiki (default: false)
- `has_projects` — Enable projects (default: false)
