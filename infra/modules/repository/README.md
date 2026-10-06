# Repository Module

This module creates and manages GitHub repositories with standard configurations.

## How to Add a New Repository?

1. Open `repositories/repos.tfvars` and add a new entry:

```hcl
repositories = {
  "my-new-repo" = {
    description = "My new repository"
    visibility  = "private"
    topics      = ["my-topic", "terraform"]
  }
}
```

2. Available options:
   - `description`: Repository description
   - `visibility`: "private", "internal", or "public" (default: "private")
   - `homepage_url`: Website URL (optional)
   - `has_issues`: Enable issues (default: true)
   - `has_wiki`: Enable wiki (default: false)
   - `has_projects`: Enable projects (default: false)
   - `topics`: List of repository topics (default: [])

3. Run `terraform plan` to review changes:
   ```bash
   cd infra
   terraform plan -var-file=../repositories/repos.tfvars
   ```

4. Create a PR and merge
5. Once merged, the deploy workflow will apply the changes

## How to Add an Existing Repository?

To import an existing GitHub repository into Terraform management:

1. Use the import workflow: `.github/workflows/import-repo.yml`
   - Trigger it via **Actions** → **Import Existing Repository**
   - Enter the repository URL and destination organization

2. Or manually import:
   - Add the repository to `repositories/imports.tfvars`
   - Run the import command:
     ```bash
     terraform import 'module.repository["repo-name"].github_repository.this' 'repo-name'
     ```
   - Commit the state and push

3. Once imported, manage it like any other repository via `imports.tfvars`

## Branch Protection Template

Once your repository is created, you can add branch protection rules. Example Terraform:

```hcl
resource "github_branch_protection" "main" {
  repository_id            = module.repository["my-repo"].id
  pattern                  = "main"
  enforce_admins           = true
  require_code_reviews     = true
  required_approving_reviews = 1

  require_status_checks = true
  strict                = true
  contexts              = ["build", "test"]
}
```

Add this to a separate `.tf` file in the `infra/` directory or extend the module as needed.
