#!/usr/bin/env python3
"""
Sync Template Files to All Managed Repositories

This script pushes template files to all managed repositories using GitHub API.
Supports custom exceptions per repository.
"""

import os
import sys
import json
import base64
import requests
from datetime import datetime
from pathlib import Path


class TemplateSync:
    """Sync template files to all managed repositories"""

    def __init__(self, github_token=None, config_file="repos-config.json"):
        self.github_token = github_token or os.environ.get("GITHUB_TOKEN")
        self.github_org = os.environ.get("GITHUB_ORG", "myorg")
        self.api_base = "https://api.github.com"

        self.template_dir = Path(".github/templates/repo-scaffold")
        self.config_file = Path(config_file)
        self.config = self._load_config()

        if not self.github_token:
            raise Exception("GITHUB_TOKEN environment variable not set")

    def run(self):
        """Execute sync process"""
        print("=" * 70)
        print(f"Template Sync: {datetime.now()}")
        print("=" * 70)

        try:
            # Get list of repos from config
            repos = list(self.config.keys())
            print(f"\n📋 Managed repositories: {len(repos)}")
            for repo in repos:
                print(f"   - {repo}")

            # Push to all repos
            print(f"\n🔄 Syncing to all repositories...")
            results = self._push_to_all_repos()

            # Report results
            self._report_results(results)

            return results

        except Exception as e:
            print(f"❌ Sync failed: {e}")
            return {"success": [], "failed": [(None, str(e))]}

    def _load_config(self):
        """Load repository configuration"""
        if not self.config_file.exists():
            raise Exception(f"Config file not found: {self.config_file}")

        with open(self.config_file) as f:
            return json.load(f)

    def _push_to_all_repos(self):
        """Push template files to all managed repositories"""
        results = {
            "success": [],
            "failed": []
        }

        for repo_name, repo_config in self.config.items():
            try:
                self._push_to_repo(repo_name, repo_config)
                results["success"].append(repo_name)
                print(f"   ✅ {repo_name}")

            except Exception as e:
                results["failed"].append((repo_name, str(e)))
                print(f"   ❌ {repo_name}: {e}")

        return results

    def _push_to_repo(self, repo_name, repo_config):
        """Push template files to single repository"""
        # Get all template files
        template_files = list(self.template_dir.rglob("*"))
        template_files = [f for f in template_files if f.is_file()]

        custom_files = repo_config.get("custom_files", {})

        for template_file in template_files:
            # Get relative path from template dir
            rel_path = template_file.relative_to(self.template_dir)
            rel_path_str = str(rel_path).replace("\\", "/")

            # Check if this repo has a custom version
            if rel_path_str in custom_files:
                # Use custom file
                custom_path = Path(custom_files[rel_path_str])
                if custom_path.exists():
                    file_content = self._read_file(custom_path)
                else:
                    print(f"   ⚠️  Custom file not found: {custom_path}, using default")
                    file_content = self._read_file(template_file)
            else:
                # Use template file
                file_content = self._read_file(template_file)

            # Push to repo
            self._push_file(repo_name, rel_path_str, file_content)

    def _push_file(self, repo_name, file_path, file_content):
        """Push single file to repository using GitHub API"""
        url = f"{self.api_base}/repos/{self.github_org}/{repo_name}/contents/{file_path}"

        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }

        # Encode content
        file_content_b64 = base64.b64encode(file_content).decode()

        # Get current file SHA (if exists)
        response = requests.get(url, headers=headers)
        file_sha = None

        if response.status_code == 200:
            file_sha = response.json()["sha"]
        elif response.status_code != 404:
            raise Exception(f"Failed to check file: {response.status_code}")

        # Prepare commit data
        commit_data = {
            "message": f"Update: {Path(file_path).name} (Template sync)",
            "content": file_content_b64,
            "branch": "main"
        }

        if file_sha:
            commit_data["sha"] = file_sha

        # Push file
        response = requests.put(url, json=commit_data, headers=headers)

        if response.status_code not in [200, 201]:
            raise Exception(f"GitHub API error: {response.status_code} - {response.text}")

    def _read_file(self, file_path):
        """Read file content as bytes"""
        with open(file_path, "rb") as f:
            return f.read()

    def _report_results(self, results):
        """Report sync results"""
        print(f"\n📊 Sync Results:")
        print(f"   ✅ Success: {len(results['success'])} repositories")

        for repo in results['success']:
            print(f"      - {repo}")

        if results['failed']:
            print(f"\n   ❌ Failed: {len(results['failed'])} repositories")
            for repo, error in results['failed']:
                print(f"      - {repo}: {error}")


def main():
    """Main entry point"""
    try:
        sync = TemplateSync()
        results = sync.run()

        # Exit with error code if any failed
        sys.exit(0 if not results['failed'] else 1)

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
