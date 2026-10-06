"""
Unit tests for sync_templates.py
"""

import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

import pytest

# Import the sync class
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from sync_templates import TemplateSync


class TestTemplateSync:
    """Test TemplateSync class"""

    @pytest.fixture
    def config(self):
        """Create a test config"""
        return {
            "repo1": {"custom_files": {}},
            "repo2": {"custom_files": {"Jenkinsfile": "custom/repo2-Jenkinsfile"}},
            "repo3": {"custom_files": {}}
        }

    @pytest.fixture
    def config_file(self):
        """Create a temporary config file"""
        config = {
            "api-server": {"custom_files": {}},
            "web-app": {"custom_files": {}},
            "payment-api": {"custom_files": {"Jenkinsfile": "custom/payment-Jenkinsfile"}}
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config, f)
            return f.name

    def test_initialization(self):
        """Test TemplateSync initialization"""
        with patch.dict('os.environ', {'GITHUB_TOKEN': 'test-token', 'GITHUB_ORG': 'test-org'}):
            sync = TemplateSync(github_token='test-token', config_file='repos-config.json')

            assert sync.github_token == 'test-token'
            assert sync.github_org == 'test-org'
            assert sync.api_base == "https://api.github.com"

    def test_missing_token(self):
        """Test that missing token raises error"""
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(Exception, match="GITHUB_TOKEN"):
                TemplateSync(github_token=None)

    def test_config_loading(self, config_file):
        """Test configuration file loading"""
        with patch.dict('os.environ', {'GITHUB_TOKEN': 'test-token'}):
            sync = TemplateSync(github_token='test-token', config_file=config_file)

            assert len(sync.config) == 3
            assert "api-server" in sync.config
            assert "payment-api" in sync.config

    def test_config_file_not_found(self):
        """Test error when config file not found"""
        with patch.dict('os.environ', {'GITHUB_TOKEN': 'test-token'}):
            with pytest.raises(Exception, match="Config file not found"):
                TemplateSync(github_token='test-token', config_file='nonexistent.json')

    def test_custom_file_detection(self, config):
        """Test detection of custom file overrides"""
        repo_config = config['repo2']
        custom_files = repo_config.get('custom_files', {})

        assert 'Jenkinsfile' in custom_files
        assert custom_files['Jenkinsfile'] == 'custom/repo2-Jenkinsfile'

    def test_results_structure(self):
        """Test that results have correct structure"""
        results = {
            "success": ["repo1", "repo2"],
            "failed": [("repo3", "Error message")]
        }

        assert isinstance(results["success"], list)
        assert isinstance(results["failed"], list)
        assert len(results["success"]) == 2
        assert len(results["failed"]) == 1


class TestConfigIntegration:
    """Integration tests with actual config file"""

    def test_repos_config_exists(self):
        """Test that repos-config.json exists"""
        config_file = Path("repos-config.json")
        assert config_file.exists(), "repos-config.json not found in project root"

    def test_repos_config_valid_json(self):
        """Test that repos-config.json is valid JSON"""
        with open("repos-config.json") as f:
            config = json.load(f)

        assert isinstance(config, dict), "Config should be a dictionary"

    def test_repos_config_structure(self):
        """Test repos-config.json has correct structure"""
        with open("repos-config.json") as f:
            config = json.load(f)

        for repo_name, repo_config in config.items():
            assert isinstance(repo_config, dict), f"Repo config for {repo_name} should be dict"
            assert "custom_files" in repo_config, f"Missing custom_files in {repo_name}"
            assert isinstance(repo_config["custom_files"], dict), f"custom_files should be dict for {repo_name}"


class TestTemplateDirectory:
    """Test template directory structure"""

    def test_template_dir_exists(self):
        """Test that template directory exists"""
        template_dir = Path(".github/templates/repo-scaffold")
        assert template_dir.exists(), f"Template directory not found: {template_dir}"

    def test_essential_template_files(self):
        """Test that essential template files exist"""
        template_dir = Path(".github/templates/repo-scaffold")

        essential_files = [
            "Jenkinsfile",
            "config.yml",
            ".github/workflows/ci.yml",
            ".github/workflows/deploy.yml",
            "infra/default/main.tf",
            "apps/apps.json",
            "README.md"
        ]

        for file in essential_files:
            file_path = template_dir / file
            assert file_path.exists(), f"Essential template file missing: {file}"
            assert file_path.is_file(), f"Template path is not a file: {file}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
