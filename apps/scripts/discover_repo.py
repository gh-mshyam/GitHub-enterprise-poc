#!/usr/bin/env python3
"""Discover GitHub repository metadata and team access for import."""

import sys
import json
import subprocess
from urllib.parse import urlparse
from pathlib import Path


def parse_repo_url(url: str) -> tuple[str, str]:
    """Extract owner and repo from GitHub URL."""
    # Handle: https://github.com/owner/repo or git@github.com:owner/repo.git
    if url.startswith('git@github.com:'):
        path = url.replace('git@github.com:', '').strip('/')
        parts = path.split('/')
        if len(parts) >= 2:
            return parts[0], parts[1].replace('.git', '')
    else:
        parsed = urlparse(url)
        if 'github.com' in parsed.netloc:
            parts = parsed.path.strip('/').split('/')
            if len(parts) >= 2:
                return parts[0], parts[1].replace('.git', '')

    raise ValueError(f"Invalid GitHub URL: {url}")


def get_repo_metadata(owner: str, repo: str) -> dict:
    """Fetch repository metadata from GitHub API."""
    try:
        result = subprocess.run(
            ['gh', 'repo', 'view', f"{owner}/{repo}",
             '--json', 'name,description,visibility,topics,isPrivate,url'],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode != 0:
            raise RuntimeError(f"Repository not found: {owner}/{repo}")

        return json.loads(result.stdout)
    except Exception as e:
        raise RuntimeError(f"Error fetching repo metadata: {e}")


def get_repo_teams(owner: str, repo: str) -> list[dict]:
    """Fetch teams with access to repository."""
    try:
        result = subprocess.run(
            ['gh', 'api', f'repos/{owner}/{repo}/teams',
             '--paginate', '--jq', '.[] | {name, permission, slug}'],
            capture_output=True,
            text=True,
            timeout=15
        )

        if result.returncode != 0:
            return []

        teams = []
        for line in result.stdout.strip().split('\n'):
            if line:
                teams.append(json.loads(line))
        return teams
    except Exception as e:
        print(f"Warning: Could not fetch teams: {e}", file=sys.stderr)
        return []


def generate_repos_tfvars(owner: str, repo_name: str, metadata: dict) -> str:
    """Generate terraform config for repository."""
    visibility = "private" if metadata.get('isPrivate') else "public"
    topics = metadata.get('topics', [])
    description = metadata.get('description', '')

    topics_str = ', '.join([f'"{t}"' for t in topics])

    return f'''  "{repo_name}" = {{
    description = "{description}"
    visibility  = "{visibility}"
    topics      = [{topics_str}]
  }}'''


def generate_teams_tfvars(teams: list[dict], repo_name: str) -> str:
    """Generate terraform config for discovered teams."""
    if not teams:
        return ""

    config_entries = []
    for team in teams:
        team_name = team.get('slug', team.get('name', ''))
        if team_name:
            config_entries.append(f'''  "{team_name}" = {{
    description  = "Imported team with access to {repo_name}"
    privacy      = "closed"
    members      = []  # Populate manually after import
    repositories = ["{repo_name}"]
  }}''')

    return '\n'.join(config_entries) if config_entries else ""


def generate_summary(owner: str, repo_name: str, metadata: dict, teams: list[dict]) -> str:
    """Generate human-readable import summary."""
    lines = [
        f"## Repository Import Summary",
        f"",
        f"**Repository:** `{repo_name}`",
        f"**Owner:** {owner}",
        f"**URL:** {metadata.get('url', 'N/A')}",
        f"**Visibility:** {metadata.get('visibility', 'unknown')}",
        f"**Description:** {metadata.get('description', '(none)')}",
        f"",
    ]

    if metadata.get('topics'):
        lines.append(f"**Topics:** {', '.join(metadata['topics'])}")
        lines.append("")

    if teams:
        lines.append(f"**Teams with access ({len(teams)}):**")
        for team in teams:
            lines.append(f"- `{team.get('slug', team.get('name'))}` ({team.get('permission', 'unknown')})")
        lines.append("")
    else:
        lines.append("**Teams with access:** None discovered")
        lines.append("")

    lines.append("### Next Steps")
    lines.append("1. Review the configuration above")
    lines.append("2. Adjust `infra/repositories/imports.tfvars` if needed")
    lines.append("3. Merge this PR to trigger terraform import")
    lines.append("4. Verify `terraform.tfstate` includes imported repo")

    return '\n'.join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: discover_repo.py <repo_url>")
        sys.exit(1)

    repo_url = sys.argv[1]

    try:
        # Parse URL
        owner, repo_name = parse_repo_url(repo_url)
        print(f"Discovering: {owner}/{repo_name}", file=sys.stderr)

        # Fetch metadata
        metadata = get_repo_metadata(owner, repo_name)
        print(f"✓ Found repository", file=sys.stderr)

        # Fetch teams
        teams = get_repo_teams(owner, repo_name)
        print(f"✓ Found {len(teams)} teams with access", file=sys.stderr)

        # Generate configs
        repos_config = generate_repos_tfvars(owner, repo_name, metadata)
        teams_config = generate_teams_tfvars(teams, repo_name)
        summary = generate_summary(owner, repo_name, metadata, teams)

        # Output JSON
        result = {
            "owner": owner,
            "repo_name": repo_name,
            "repos_tfvars_entry": repos_config,
            "teams_tfvars_entries": teams_config,
            "summary": summary,
            "teams_count": len(teams),
            "discovered_teams": [t.get('slug', t.get('name')) for t in teams]
        }

        print(json.dumps(result, indent=2))
        sys.exit(0)

    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
