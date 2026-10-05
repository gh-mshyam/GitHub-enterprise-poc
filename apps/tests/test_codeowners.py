#!/usr/bin/env python3
"""
Unit tests for CODEOWNERS detection.
Corresponds to test cases: TC-016, TC-017, TC-018
"""

import pytest
import os
import tempfile
import json
from pathlib import Path

# Import the check_codeowners function
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from check_codeowners import check_codeowners, get_pr_comment_status


class TestCodeownersDetection:
    """Test cases TC-016 to TC-018: CODEOWNERS detection"""

    def test_tc_016_codeowners_present(self):
        """TC-016: CODEOWNERS present - should report as found"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create .github/CODEOWNERS
            github_dir = Path(tmpdir) / ".github"
            github_dir.mkdir()
            codeowners_file = github_dir / "CODEOWNERS"
            codeowners_file.write_text("* @team/review\n")

            # Check
            result = check_codeowners(tmpdir)

            # Assert (TC-016)
            assert result["exists"] == True
            assert result["status"] == "present"
            assert "✓ CODEOWNERS file found" in result["message"]

    def test_tc_017_codeowners_missing_tier_1(self):
        """TC-017: CODEOWNERS missing on Tier 1 - should flag warning"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # No CODEOWNERS file
            result = check_codeowners(tmpdir)

            # Assert (TC-017)
            assert result["exists"] == False
            assert result["status"] == "missing"
            assert "⚠️ CODEOWNERS file not found" in result["message"]

            # Generate Tier 1 comment
            comment = get_pr_comment_status("1", result)
            assert "⚠️ CODEOWNERS" in comment
            assert "Tier 1 operation requires manual review" in comment

    def test_tc_018_codeowners_missing_tier_0(self):
        """TC-018: CODEOWNERS missing on Tier 0 - should NOT block"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # No CODEOWNERS file
            result = check_codeowners(tmpdir)

            # Assert (TC-018)
            assert result["exists"] == False
            assert result["status"] == "missing"

            # Generate Tier 0 comment
            comment = get_pr_comment_status("0", result)
            assert "ℹ️ CODEOWNERS" in comment
            assert "not required for Tier 0" in comment

    def test_empty_codeowners_file(self):
        """Test: CODEOWNERS file exists but is empty"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create empty .github/CODEOWNERS
            github_dir = Path(tmpdir) / ".github"
            github_dir.mkdir()
            codeowners_file = github_dir / "CODEOWNERS"
            codeowners_file.write_text("")

            # Check
            result = check_codeowners(tmpdir)

            # Assert
            assert result["exists"] == True
            assert result["status"] == "empty"
            assert "⚠️ CODEOWNERS file is empty" in result["message"]

    def test_pr_comment_snippets(self):
        """Test: PR comment generation for all scenarios"""
        # Scenario 1: CODEOWNERS present, Tier 0
        status_present = {"status": "present", "exists": True}
        comment = get_pr_comment_status("0", status_present)
        assert "✓ CODEOWNERS" in comment
        assert "will be notified" in comment

        # Scenario 2: CODEOWNERS missing, Tier 1
        status_missing = {"status": "missing", "exists": False}
        comment = get_pr_comment_status("1", status_missing)
        assert "⚠️ CODEOWNERS" in comment
        assert "manual review" in comment

        # Scenario 3: CODEOWNERS missing, Tier 0
        comment = get_pr_comment_status("0", status_missing)
        assert "ℹ️ CODEOWNERS" in comment
        assert "not required for Tier 0" in comment


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
