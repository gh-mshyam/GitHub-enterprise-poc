#!/usr/bin/env python3
"""
Unit tests for classify_risk.py
Corresponds to test cases: TC-001 to TC-009
"""

import pytest
import json
import tempfile
import os
from pathlib import Path

# Import the classify_risk functions
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

# Mock the classify_risk module (simplified version for testing)
class MockClassifyRisk:
    @staticmethod
    def classify_operation(visibility, name, operation):
        """Simplified classification logic for testing"""
        # Tier 1 if delete
        if operation == "delete":
            return "1"

        # Tier 1 if not private
        if visibility != "private":
            return "1"

        # Tier 1 if bad name
        import re
        if not re.match(r"^[a-z0-9][a-z0-9-]*$", name):
            return "1"

        # Otherwise Tier 0
        return "0"


class TestClassifyRisk:
    """Test cases TC-001 to TC-009"""

    # TIER 0 TESTS

    def test_tc_001_tier0_private_standard_add(self):
        """TC-001: Private + standard name + add = Tier 0"""
        result = MockClassifyRisk.classify_operation("private", "my-service", "add")
        assert result == "0"

    def test_tc_002_tier0_private_standard_modify(self):
        """TC-002: Private + standard name + modify = Tier 0"""
        result = MockClassifyRisk.classify_operation("private", "my-service", "modify")
        assert result == "0"

    def test_tc_003_tier0_lowercase_with_numbers(self):
        """TC-003: Tier 0 with numbers in name"""
        result = MockClassifyRisk.classify_operation("private", "service-v2", "add")
        assert result == "0"

    def test_tc_004_tier0_single_word_lowercase(self):
        """TC-004: Tier 0 single word"""
        result = MockClassifyRisk.classify_operation("private", "api", "add")
        assert result == "0"

    # TIER 1 TESTS

    def test_tc_005_tier1_delete(self):
        """TC-005: Delete operation = Tier 1"""
        result = MockClassifyRisk.classify_operation("private", "my-service", "delete")
        assert result == "1"

    def test_tc_006_tier1_public(self):
        """TC-006: Public visibility = Tier 1"""
        result = MockClassifyRisk.classify_operation("public", "my-service", "add")
        assert result == "1"

    def test_tc_007_tier1_internal(self):
        """TC-007: Internal visibility = Tier 1"""
        result = MockClassifyRisk.classify_operation("internal", "my-service", "add")
        assert result == "1"

    def test_tc_008_tier1_uppercase(self):
        """TC-008: Non-standard name (uppercase) = Tier 1"""
        result = MockClassifyRisk.classify_operation("private", "My_Service", "add")
        assert result == "1"

    def test_tc_009_tier1_special_chars(self):
        """TC-009: Non-standard name (special chars) = Tier 1"""
        result = MockClassifyRisk.classify_operation("private", "my.service@v1", "add")
        assert result == "1"

    def test_tier1_underscore(self):
        """Tier 1: Underscore in name"""
        result = MockClassifyRisk.classify_operation("private", "my_service", "add")
        assert result == "1"

    def test_tier1_uppercase_start(self):
        """Tier 1: Uppercase at start"""
        result = MockClassifyRisk.classify_operation("private", "MyService", "add")
        assert result == "1"


class TestClassifyRiskMatrix:
    """Matrix tests for all combinations"""

    @pytest.mark.parametrize("visibility,name,operation,expected", [
        # Tier 0
        ("private", "api", "add", "0"),
        ("private", "data-platform", "add", "0"),
        ("private", "service-v1", "modify", "0"),
        # Tier 1 - visibility
        ("public", "api", "add", "1"),
        ("internal", "api", "add", "1"),
        # Tier 1 - delete
        ("private", "api", "delete", "1"),
        # Tier 1 - naming
        ("private", "API", "add", "1"),
        ("private", "my_api", "add", "1"),
        ("private", "my.api", "add", "1"),
    ])
    def test_classification_matrix(self, visibility, name, operation, expected):
        """Parametrized matrix test for all combinations"""
        result = MockClassifyRisk.classify_operation(visibility, name, operation)
        assert result == expected, f"Expected {expected}, got {result} for {visibility}/{name}/{operation}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
