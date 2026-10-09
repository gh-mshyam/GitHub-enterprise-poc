#!/usr/bin/env python3
"""
Bootstrap Repository with Template Files

This script initializes a newly created repository with standard template files
from .github/templates/repo-scaffold/
"""

import os
import sys
import json
import shutil
import subprocess
import tempfile
import time
from datetime import datetime
from pathlib import Path


class RepositoryBootstrapper:
    """Bootstrap a new repository with template files"""

    def __init__(self, repo_name, repo_owner, github_token=None):
        self.repo_name = repo_name
        self.repo_owner = repo_owner
        self.github_token = github_token or os.environ.get("GITHUB_TOKEN")

        script_dir = Path(__file__).parent.parent.parent
        self.template_dir = script_dir / ".github/templates/repo-scaffold"
        self.temp_dir = None

    def run(self):
        """Execute bootstrap process"""
        try:
            print(f"🚀 Bootstrapping repository: {self.repo_name}")

            # Step 1: Create temp directory
            self.temp_dir = tempfile.mkdtemp(prefix=f"bootstrap_{self.repo_name}_")
            print(f"📁 Temp directory: {self.temp_dir}")

            # Step 2: Clone repository
            self._clone_repo()

            # Step 3: Copy template files
            self._copy_template_files()

            # Step 4: Commit and push
            self._commit_and_push()

            print(f"✅ Bootstrap complete: {self.repo_name}")
            return True

        except Exception as e:
            print(f"❌ Bootstrap failed: {e}")
            return False

        finally:
            self._cleanup()

    def _clone_repo(self):
        """Clone repository to temp workspace with retry logic"""
        print(f"📥 Cloning repository...")

        if self.github_token:
            repo_url = f"https://x-access-token:{self.github_token}@github.com/{self.repo_owner}/{self.repo_name}.git"
        else:
            repo_url = f"https://github.com/{self.repo_owner}/{self.repo_name}.git"

        # Retry logic: newly created repos may need a moment to replicate across GitHub's servers
        max_retries = 5
        retry_delay = 2  # Start with 2 seconds

        for attempt in range(max_retries):
            result = subprocess.run(
                ["git", "clone", repo_url, self.temp_dir],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                print(f"   ✓ Clone successful")
                return

            # If not the last attempt, retry with backoff
            if attempt < max_retries - 1:
                print(f"   ⏳ Clone failed (attempt {attempt + 1}/{max_retries}), retrying in {retry_delay}s...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                raise Exception(f"Failed to clone repo after {max_retries} attempts: {result.stderr}")

    def _copy_template_files(self):
        """Copy template files from source to repo"""
        print(f"📋 Copying template files...")

        if not self.template_dir.exists():
            raise Exception(f"Template directory not found: {self.template_dir}")

        # Count files for progress
        file_count = 0

        # Recursively copy all template files
        for src_path in self.template_dir.rglob("*"):
            if src_path.is_file():
                # Calculate relative path
                rel_path = src_path.relative_to(self.template_dir)
                dst_path = Path(self.temp_dir) / rel_path

                # Create parent directories
                dst_path.parent.mkdir(parents=True, exist_ok=True)

                # Copy file
                shutil.copy2(src_path, dst_path)
                file_count += 1
                print(f"   ✓ {rel_path}")

        print(f"   Copied {file_count} files")

    def _commit_and_push(self):
        """Commit template files and push to remote"""
        print(f"📤 Committing and pushing...")

        os.chdir(self.temp_dir)

        try:
            # Configure git
            subprocess.run(
                ["git", "config", "user.name", "Template Bootstrap Bot"],
                check=True,
                capture_output=True
            )
            subprocess.run(
                ["git", "config", "user.email", "bootstrap@company.com"],
                check=True,
                capture_output=True
            )

            # Stage all files
            subprocess.run(
                ["git", "add", "-A"],
                check=True,
                capture_output=True
            )

            # Create commit message
            commit_message = f"""Initialize repository with repo-scaffold template

Template Version: repo-scaffold
Initialized: {datetime.now().isoformat()}

This repository was auto-initialized with the standard repo-scaffold template.

Includes:
- Jenkinsfile (CI/CD pipeline)
- GitHub Actions workflows (ci.yml, deploy.yml)
- Terraform scaffolding (infra/default/)
- Security configuration (Prisma Cloud)
- Application manifest (apps.json)
- Configuration template (config.yml)

Next Steps:
1. Review and customize config.yml
2. Update README.md with project details
3. Add application code to apps/
4. Configure infrastructure in infra/default/main.tf
5. Customize Jenkinsfile if needed

See TEMPLATE_README.md for detailed guide.

Co-Authored-By: Template Bootstrap Bot <noreply@company.com>"""

            # Commit
            subprocess.run(
                ["git", "commit", "-m", commit_message],
                check=True,
                capture_output=True
            )

            # Push to main with authentication if token available
            if self.github_token:
                # Update remote URL to include token for authentication
                subprocess.run(
                    ["git", "remote", "set-url", "origin",
                     f"https://x-access-token:{self.github_token}@github.com/{self.repo_owner}/{self.repo_name}.git"],
                    check=True,
                    capture_output=True
                )

            subprocess.run(
                ["git", "push", "-u", "origin", "main"],
                check=True,
                capture_output=True
            )

            print(f"   ✓ Pushed to main branch")

        except subprocess.CalledProcessError as e:
            raise Exception(f"Git operation failed: {e}")

    def _cleanup(self):
        """Remove temporary directory"""
        if self.temp_dir and Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir, ignore_errors=True)
            print(f"🧹 Cleaned up temp directory")


def main():
    """Main entry point"""
    if len(sys.argv) < 3:
        print("Usage: bootstrap_repo.py <repo_name> <repo_owner>")
        print("Example: bootstrap_repo.py api-server myorg")
        sys.exit(1)

    repo_name = sys.argv[1]
    repo_owner = sys.argv[2]

    bootstrapper = RepositoryBootstrapper(repo_name, repo_owner)
    success = bootstrapper.run()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
