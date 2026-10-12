terraform {
  required_providers {
    github = {
      source = "integrations/github"
    }
  }
}

# Sync template files to existing repository
resource "null_resource" "template_sync" {
  triggers = {
    repo_name  = var.repo_name
    repo_owner = var.repo_owner
    # Trigger when template files change
    template_hash = var.template_hash
  }

  provisioner "local-exec" {
    command = "python3 ${path.module}/sync_template.py"

    environment = {
      REPO_NAME      = var.repo_name
      REPO_OWNER     = var.repo_owner
      GITHUB_TOKEN   = var.github_token
      TEMPLATE_DIR   = var.template_dir
      SYNC_MESSAGE   = "chore: sync repo-scaffold template"
    }
  }
}
