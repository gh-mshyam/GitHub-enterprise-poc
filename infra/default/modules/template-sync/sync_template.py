#!/usr/bin/env python3
"""
Sync repo-scaffold template files to existing repositories
"""

import os
import sys
import shutil
import subprocess
import tempfile
from pathlib import Path


class TemplateSync:
    """Sync template files to existing repo"""

    def __init__(self):
        self.repo_name = os.environ.get("REPO_NAME")
        self.repo_owner = os.environ.get("REPO_OWNER")
        self.github_token = os.environ.get("GITHUB_TOKEN")
        self.template_dir = os.environ.get("TEMPLATE_DIR")
        self.sync_message = os.environ.get("SYNC_MESSAGE", "chore: sync template")
        self.temp_dir = None

        # Debug: print environment
        if not self.template_dir:
            print(f"⚠️  DEBUG: TEMPLATE_DIR not set in environment")
            print(f"   Available env vars: {list(os.environ.keys())[:10]}...")

    def run(self):
        """Execute template sync"""
        try:
            print(f"🔄 Syncing template to {self.repo_name}...")

            # Step 1: Create temp directory
            self.temp_dir = tempfile.mkdtemp(prefix=f"sync_{self.repo_name}_")
            print(f"📁 Temp directory: {self.temp_dir}")

            # Step 2: Clone repository
            self._clone_repo()

            # Step 3: Sync template files
            self._sync_template_files()

            # Step 4: Check if there are changes
            if not self._has_changes():
                print(f"✅ No changes needed - template already up to date")
                return True

            # Step 5: Commit and push
            self._commit_and_push()

            print(f"✅ Template sync complete: {self.repo_name}")
            return True

        except Exception as e:
            print(f"❌ Sync failed: {e}")
            import traceback
            traceback.print_exc()
            return False

        finally:
            self._cleanup()

    def _clone_repo(self):
        """Clone repository to temp workspace with retry"""
        print(f"📥 Cloning repository...")

        if self.github_token:
            repo_url = f"https://x-access-token:{self.github_token}@github.com/{self.repo_owner}/{self.repo_name}.git"
        else:
            repo_url = f"https://github.com/{self.repo_owner}/{self.repo_name}.git"

        # Retry logic for GitHub repo replication lag
        max_retries = 5
        retry_delay = 2

        for attempt in range(max_retries):
            result = subprocess.run(
                ["git", "clone", repo_url, self.temp_dir],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                print(f"   ✓ Clone successful")
                return

            if attempt < max_retries - 1:
                print(f"   ⏳ Retry in {retry_delay}s...")
                import time
                time.sleep(retry_delay)
                retry_delay *= 2
            else:
                raise Exception(f"Failed to clone repo: {result.stderr}")

    def _sync_template_files(self):
        """Sync template files to repo, excluding certain files"""
        print(f"📋 Syncing template files...")

        template_path = Path(self.template_dir).resolve()
        if not template_path.exists():
            raise Exception(f"Template directory not found: {template_path}")

        # Files to exclude from sync
        exclude_patterns = {".git", "__pycache__", ".pytest_cache"}

        synced_count = 0
        for src_path in template_path.rglob("*"):
            # Skip excluded patterns
            if any(pattern in str(src_path) for pattern in exclude_patterns):
                continue

            if src_path.is_file():
                # Calculate relative path
                rel_path = src_path.relative_to(template_path)
                dst_path = Path(self.temp_dir) / rel_path

                # Skip certain files that shouldn't be synced
                if rel_path.name in [".repo-meta.json"]:
                    continue

                # Create parent directories
                dst_path.parent.mkdir(parents=True, exist_ok=True)

                # Copy file
                shutil.copy2(src_path, dst_path)
                synced_count += 1
                print(f"   ✓ {rel_path}")

        print(f"   Synced {synced_count} files")

    def _has_changes(self):
        """Check if there are uncommitted changes"""
        os.chdir(self.temp_dir)

        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            check=True
        )

        return len(result.stdout.strip()) > 0

    def _commit_and_push(self):
        """Commit and push changes"""
        print(f"📤 Committing and pushing changes...")

        os.chdir(self.temp_dir)

        try:
            # Configure git
            subprocess.run(
                ["git", "config", "user.name", "Template Sync Bot"],
                check=True,
                capture_output=True
            )
            subprocess.run(
                ["git", "config", "user.email", "sync@company.com"],
                check=True,
                capture_output=True
            )

            # Stage all changes
            subprocess.run(
                ["git", "add", "-A"],
                check=True,
                capture_output=True
            )

            # Commit
            result = subprocess.run(
                ["git", "commit", "-m", self.sync_message],
                check=True,
                capture_output=True,
                text=True
            )

            # Push
            subprocess.run(
                ["git", "push", "origin", "main"],
                check=True,
                capture_output=True
            )

            print(f"   ✓ Changes pushed to main")

        except subprocess.CalledProcessError as e:
            raise Exception(f"Git operation failed: {e.stderr}")

    def _cleanup(self):
        """Clean up temp directory"""
        if self.temp_dir and Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)
            print(f"🧹 Cleaned up temp directory")


if __name__ == "__main__":
    sync = TemplateSync()
    success = sync.run()
    sys.exit(0 if success else 1)
