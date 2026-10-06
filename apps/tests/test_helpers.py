#!/usr/bin/env python3
"""Unit tests for CI/CD helper scripts."""

import unittest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from validate_tfvars import validate_hcl_syntax, validate_repos_tfvars
from parse_tf_plan import extract_changes, format_markdown
from import_repo_validator import extract_repo_info


class TestValidateTfvars(unittest.TestCase):
    """Tests for validate_tfvars.py"""

    def test_balanced_braces(self):
        """Test validation of balanced braces."""
        valid, _ = validate_hcl_syntax('repositories = { }')
        self.assertTrue(valid)

        valid, msg = validate_hcl_syntax('repositories = { }}}')
        self.assertFalse(valid)
        self.assertIn('braces', msg)

    def test_balanced_brackets(self):
        """Test validation of balanced brackets."""
        valid, _ = validate_hcl_syntax('members = []')
        self.assertTrue(valid)

        valid, msg = validate_hcl_syntax('members = []]')
        self.assertFalse(valid)
        self.assertIn('brackets', msg)

    def test_repos_tfvars_structure(self):
        """Test repos.tfvars validation."""
        content = 'repositories = { }'
        valid, msg = validate_repos_tfvars(content)
        self.assertTrue(valid)

        invalid_content = 'teams = { }'
        valid, msg = validate_repos_tfvars(invalid_content)
        self.assertFalse(valid)


class TestParseTfPlan(unittest.TestCase):
    """Tests for parse_tf_plan.py"""

    def test_extract_changes_empty(self):
        """Test extraction with empty plan."""
        changes = extract_changes({})
        self.assertEqual(changes, {})

    def test_extract_changes_with_resources(self):
        """Test extraction with resource changes."""
        plan_data = {
            'resource_changes': [
                {
                    'type': 'github_repository',
                    'name': 'my-repo',
                    'change': {'actions': ['create']}
                },
                {
                    'type': 'github_team',
                    'name': 'backend-team',
                    'change': {'actions': ['update']}
                }
            ]
        }

        changes = extract_changes(plan_data)
        self.assertIn('github_repository', changes)
        self.assertIn('my-repo', changes['github_repository']['create'])
        self.assertIn('backend-team', changes['github_team']['update'])

    def test_format_markdown_empty(self):
        """Test markdown formatting with no changes."""
        md = format_markdown({})
        self.assertIn('No changes', md)

    def test_format_markdown_with_changes(self):
        """Test markdown formatting with changes."""
        changes = {
            'github_repository': {
                'create': ['repo1', 'repo2'],
                'update': [],
                'delete': []
            }
        }
        md = format_markdown(changes)
        self.assertIn('github_repository', md)
        self.assertIn('Create', md)
        self.assertIn('repo1', md)


class TestImportRepoValidator(unittest.TestCase):
    """Tests for import_repo_validator.py"""

    def test_extract_https_url(self):
        """Test extraction from HTTPS URL."""
        owner, repo, scheme = extract_repo_info(
            'https://github.com/myorg/my-repo'
        )
        self.assertEqual(owner, 'myorg')
        self.assertEqual(repo, 'my-repo')
        self.assertEqual(scheme, 'https')

    def test_extract_https_url_with_git(self):
        """Test extraction from HTTPS URL with .git."""
        owner, repo, scheme = extract_repo_info(
            'https://github.com/myorg/my-repo.git'
        )
        self.assertEqual(owner, 'myorg')
        self.assertEqual(repo, 'my-repo')

    def test_extract_ssh_url(self):
        """Test extraction from SSH URL."""
        owner, repo, scheme = extract_repo_info(
            'git@github.com:myorg/my-repo.git'
        )
        self.assertEqual(owner, 'myorg')
        self.assertEqual(repo, 'my-repo')
        self.assertEqual(scheme, 'ssh')

    def test_extract_invalid_url(self):
        """Test extraction from invalid URL."""
        owner, repo, scheme = extract_repo_info('not-a-url')
        self.assertIsNone(owner)
        self.assertIsNone(repo)


if __name__ == '__main__':
    unittest.main()
