#!/usr/bin/env python3
"""
Validate repositories.json against schema.

Usage: python3 validate_schema.py <repositories.json> [schema.json]
"""
import json
import sys
import re
from pathlib import Path


class RepositoriesValidator:
    """Validate repositories.json configuration."""

    VALID_OPERATIONS = {"create", "import", "update", "delete"}
    VALID_VISIBILITY = {"public", "private"}
    REPO_NAME_PATTERN = re.compile(r"^[a-z0-9]([a-z0-9-]*[a-z0-9])?$")

    def __init__(self, config_path: str):
        """Load and validate configuration."""
        self.config_path = Path(config_path)
        self.errors = []
        self.warnings = []

    def load_config(self) -> dict:
        """Load JSON config file."""
        try:
            return json.loads(self.config_path.read_text())
        except FileNotFoundError:
            self.errors.append(f"File not found: {self.config_path}")
            return {}
        except json.JSONDecodeError as e:
            self.errors.append(f"JSON parse error: {e}")
            return {}

    def validate_structure(self, config: dict) -> bool:
        """Validate top-level structure."""
        if not isinstance(config, dict):
            self.errors.append("Root must be an object")
            return False

        if "repositories" not in config:
            self.errors.append("Missing required key: 'repositories'")
            return False

        if not isinstance(config["repositories"], dict):
            self.errors.append("'repositories' must be an object")
            return False

        return True

    def validate_repo_name_format(self, name: str) -> bool:
        """Validate repository name format."""
        if not name:
            return False
        return self.REPO_NAME_PATTERN.match(name) is not None

    def validate_repository(self, repo_id: str, repo: dict) -> bool:
        """Validate single repository configuration."""
        valid = True

        # Check operation
        if "operation" not in repo:
            self.errors.append(f"{repo_id}: Missing required field 'operation'")
            valid = False
        elif repo["operation"] not in self.VALID_OPERATIONS:
            self.errors.append(
                f"{repo_id}: Invalid operation '{repo['operation']}'. "
                f"Must be one of: {', '.join(self.VALID_OPERATIONS)}"
            )
            valid = False

        # Check name
        if "name" not in repo:
            self.errors.append(f"{repo_id}: Missing required field 'name'")
            valid = False
        elif not self.validate_repo_name_format(repo["name"]):
            self.errors.append(
                f"{repo_id}: Invalid name format '{repo['name']}'. "
                "Must be lowercase alphanumeric with hyphens (no leading/trailing hyphens)"
            )
            valid = False

        # Check visibility
        if "visibility" not in repo:
            self.errors.append(f"{repo_id}: Missing required field 'visibility'")
            valid = False
        elif repo["visibility"] not in self.VALID_VISIBILITY:
            self.errors.append(
                f"{repo_id}: Invalid visibility '{repo['visibility']}'. "
                f"Must be: {', '.join(self.VALID_VISIBILITY)}"
            )
            valid = False

        # Operation-specific validation
        if repo.get("operation") == "import":
            if "import_existing" not in repo:
                self.errors.append(
                    f"{repo_id}: Operation 'import' requires 'import_existing' field"
                )
                valid = False
            else:
                import_cfg = repo["import_existing"]
                if "owner" not in import_cfg or "repo_id" not in import_cfg:
                    self.errors.append(
                        f"{repo_id}: 'import_existing' must have 'owner' and 'repo_id'"
                    )
                    valid = False

        # Optional field validation
        if "description" in repo:
            if not isinstance(repo["description"], str):
                self.errors.append(f"{repo_id}: 'description' must be a string")
                valid = False
            elif len(repo["description"]) > 300:
                self.errors.append(
                    f"{repo_id}: 'description' exceeds 300 characters"
                )
                valid = False

        if "topics" in repo:
            if not isinstance(repo["topics"], list):
                self.errors.append(f"{repo_id}: 'topics' must be an array")
                valid = False
            elif not all(isinstance(t, str) for t in repo["topics"]):
                self.errors.append(f"{repo_id}: 'topics' must contain only strings")
                valid = False

        if "teams" in repo:
            if not isinstance(repo["teams"], list):
                self.errors.append(f"{repo_id}: 'teams' must be an array")
                valid = False
            elif not all(isinstance(t, str) for t in repo["teams"]):
                self.errors.append(f"{repo_id}: 'teams' must contain only strings")
                valid = False

        # Warnings
        if not repo.get("owner"):
            self.warnings.append(f"{repo_id}: No owner specified (recommended)")

        return valid

    def validate(self) -> bool:
        """Run full validation."""
        config = self.load_config()

        if not config:
            return len(self.errors) == 0

        if not self.validate_structure(config):
            return False

        all_valid = True
        for repo_id, repo in config.get("repositories", {}).items():
            if not self.validate_repository(repo_id, repo):
                all_valid = False

        return all_valid

    def report(self):
        """Print validation report."""
        if self.errors:
            print("❌ Validation FAILED\n")
            print("Errors:")
            for error in self.errors:
                print(f"  - {error}")
            print()

        if self.warnings:
            print("⚠️  Warnings:")
            for warning in self.warnings:
                print(f"  - {warning}")
            print()

        if not self.errors:
            print("✅ Validation PASSED")
            if self.warnings:
                print(f"   ({len(self.warnings)} warning(s))")


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <repositories.json> [schema.json]")
        sys.exit(1)

    validator = RepositoriesValidator(sys.argv[1])
    validator.validate()
    validator.report()

    sys.exit(0 if not validator.errors else 1)


if __name__ == "__main__":
    main()
