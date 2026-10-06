"""
Unit tests for bootstrap_repo.py
"""

import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

import pytest

# Import the bootstrapper class
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from bootstrap_repo import RepositoryBootstrapper


class TestRepositoryBootstrapper:
    """Test RepositoryBootstrapper class"""

    @pytest.fixture
    def bootstrapper(self):
        """Create a bootstrapper instance"""
        return RepositoryBootstrapper(
            repo_name="test-repo",
            repo_owner="test-org",
            github_token="test-token"
        )

    def test_initialization(self, bootstrapper):
        """Test bootstrapper initialization"""
        assert bootstrapper.repo_name == "test-repo"
        assert bootstrapper.repo_owner == "test-org"
        assert bootstrapper.github_token == "test-token"
        assert bootstrapper.template_dir == Path(".github/templates/repo-scaffold")

    def test_metadata_creation(self, bootstrapper):
        """Test metadata file creation"""
        with tempfile.TemporaryDirectory() as temp_dir:
            bootstrapper.temp_dir = temp_dir
            bootstrapper._create_metadata()

            metadata_file = Path(temp_dir) / ".repo-meta.json"
            assert metadata_file.exists()

            with open(metadata_file) as f:
                metadata = json.load(f)

            assert metadata["template_version"] == "repo-scaffold"
            assert metadata["repository_name"] == "test-repo"
            assert metadata["repository_owner"] == "test-org"
            assert "initialized_at" in metadata


class TestTemplateFileHeaders:
    """Test that template files have proper headers"""

    @pytest.mark.parametrize("filename", [
        "Jenkinsfile",
        "config.yml",
        ".github/workflows/ci.yml",
        ".github/workflows/deploy.yml",
        "infra/default/main.tf",
        "infra/default/variables.tf"
    ])
    def test_managed_file_headers(self, filename):
        """Test that managed files have the managed file header"""
        file_path = Path(".github/templates/repo-scaffold") / filename

        assert file_path.exists(), f"File not found: {file_path}"

        with open(file_path) as f:
            content = f.read()

        assert "TEMPLATE MANAGED FILE" in content, f"Missing header in {filename}"


class TestTemplateFileExistence:
    """Test that template files exist"""

    def test_template_files_exist(self):
        """Test that all expected template files exist"""
        template_dir = Path(".github/templates/repo-scaffold")

        # Check that template directory exists
        assert template_dir.exists(), f"Template directory not found: {template_dir}"

        # Check for expected files
        expected_files = [
            "Jenkinsfile",
            "config.yml",
            "prisma-cloud-config.yml",
            ".github/workflows/ci.yml",
            ".github/workflows/deploy.yml",
            "infra/default/main.tf",
            "infra/default/variables.tf",
            "apps/apps.json",
            "README.md",
            "TEMPLATE_README.md"
        ]

        for file in expected_files:
            file_path = template_dir / file
            assert file_path.exists(), f"Template file not found: {file}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
