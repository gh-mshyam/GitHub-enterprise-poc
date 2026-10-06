#!/usr/bin/env python3
"""Validate that a repository exists and can be imported."""

import sys
import subprocess
import json
from urllib.parse import urlparse


def extract_repo_info(repo_url: str) -> tuple[str, str, str]:
    """Extract owner, repo, and platform from URL."""
    # Handle SSH URLs: git@github.com:owner/repo.git
    if repo_url.startswith('git@github.com:'):
        path = repo_url.replace('git@github.com:', '').strip('/')
        parts = path.split('/')
        if len(parts) >= 2:
            owner = parts[0]
            repo = parts[1].replace('.git', '')
            return owner, repo, 'ssh'
        return None, None, None

    # Handle HTTPS URLs
    parsed = urlparse(repo_url)

    if 'github.com' not in parsed.netloc:
        return None, None, None

    if parsed.scheme in ['http', 'https']:
        parts = parsed.path.strip('/').split('/')
        if len(parts) >= 2:
            owner = parts[0]
            repo = parts[1].replace('.git', '')
            return owner, repo, 'https'

    return None, None, None


def validate_repo_exists(owner: str, repo: str) -> tuple[bool, str]:
    """Validate that repository exists using GitHub CLI."""
    try:
        result = subprocess.run(
            ['gh', 'repo', 'view', f"{owner}/{repo}"],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            return True, f"Repository found: {owner}/{repo}"
        else:
            return False, f"Repository not found or not accessible: {owner}/{repo}"
    except subprocess.TimeoutExpired:
        return False, "Timeout checking repository"
    except FileNotFoundError:
        return False, "GitHub CLI (gh) not found in PATH"
    except Exception as e:
        return False, f"Error checking repository: {e}"


def validate_import_permissions(owner: str, repo: str) -> tuple[bool, str]:
    """Check if authenticated user has permission to import repository."""
    try:
        # Get authenticated user
        result = subprocess.run(
            ['gh', 'auth', 'status', '-t'],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode != 0:
            return False, "Not authenticated with GitHub CLI"

        # Check if user has access to repo
        result = subprocess.run(
            ['gh', 'repo', 'view', f"{owner}/{repo}", '--json', 'nameWithOwner'],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            return True, "Permission to import repository confirmed"
        else:
            return False, "Insufficient permissions to access repository"

    except subprocess.TimeoutExpired:
        return False, "Timeout checking permissions"
    except Exception as e:
        return False, f"Error checking permissions: {e}"


def main():
    if len(sys.argv) < 2:
        print("Usage: import_repo_validator.py <repo_url>")
        sys.exit(1)

    repo_url = sys.argv[1]
    owner, repo, scheme = extract_repo_info(repo_url)

    if not owner or not repo:
        print(f"✗ Invalid repository URL: {repo_url}")
        sys.exit(1)

    print(f"Validating repository: {owner}/{repo}")

    # Check if repo exists
    valid, msg = validate_repo_exists(owner, repo)
    print(f"  {'✓' if valid else '✗'} {msg}")
    if not valid:
        sys.exit(1)

    # Check permissions
    valid, msg = validate_import_permissions(owner, repo)
    print(f"  {'✓' if valid else '✗'} {msg}")
    if not valid:
        sys.exit(1)

    print("\n✓ Repository is ready for import")
    sys.exit(0)


if __name__ == '__main__':
    main()
