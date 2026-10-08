# Quick Start: Manage Repositories

## Option 1: Create New Repository

### Step 1: Create Branch
Go to GitHub Actions. Click **Create Branch** workflow.
Enter branch name. Default is `develop`. Click **Run workflow**.

### Step 2: Create PR
Edit `infra/default/repos.tfvars`. Add new repository block.
Commit and push to your branch.
Go to **Create PR** workflow. Click **Run workflow**.
A PR appears automatically.

### Step 3: Deploy
Go to your PR. Click the **Deploy** workflow link.
Select `full` mode. Click **Run workflow**.

The system does this:
- Shows terraform plan in PR comments
- Merges PR automatically
- Deletes your branch
- Creates repository on GitHub

**Result:** Your repository is live.

---

## Option 2: Import Existing Repository

You already have a GitHub repository. Bring it into this system.

### Import Step 1
Go to GitHub Actions. Click **Import Repo** workflow.
Enter:
- Repository name
- Repository ID (from GitHub)
- Visibility (private or internal)

Click **Run workflow**.

### Import Step 2
Copy the terraform config from workflow output.
Add it to `infra/default/repos.tfvars`.
Commit and push to your branch.

### Import Step 3
Now follow the 3-step process (above).
This makes terraform manage your existing repository.

---

## Common Tasks

**Delete a repository:**
Remove its block from `repos.tfvars`.
Follow the 3-step process.
Repository is archived on GitHub.

**Update a repository:**
Change fields in `repos.tfvars`.
Follow the 3-step process.
Changes apply automatically.

**View the plan:**
Check PR comments after Deploy workflow starts.
You see exactly what will change.
