"""
Unit tests for validation.
"""
import unittest
from .validation import ValidationManager


class TestValidation(unittest.TestCase):
    """Test validation functions."""

    def test_validate_amount_valid(self):
        """Test valid amount."""
        valid, error = ValidationManager.validate_amount(100.50)
        self.assertTrue(valid)
        self.assertIsNone(error)

    def test_validate_amount_zero(self):
        """Test zero amount."""
        valid, error = ValidationManager.validate_amount(0)
        self.assertFalse(valid)

    def test_validate_amount_negative(self):
        """Test negative amount."""
        valid, error = ValidationManager.validate_amount(-50)
        self.assertFalse(valid)

    def test_validate_amount_invalid(self):
        """Test invalid amount."""
        valid, error = ValidationManager.validate_amount("abc")
        self.assertFalse(valid)

    def test_validate_category(self):
        """Test category validation."""
        allowed = ["Food", "Transport", "Entertainment"]
        self.assertTrue(ValidationManager.validate_category("Food", allowed))
        self.assertFalse(ValidationManager.validate_category("Other", allowed))

    def test_validate_date_valid(self):
        """Test valid date."""
        valid = ValidationManager.validate_date("2024-04-30T10:30:00")
        self.assertTrue(valid)

    def test_validate_date_invalid(self):
        """Test invalid date."""
        valid = ValidationManager.validate_date("invalid-date")
        self.assertFalse(valid)

    def test_validate_description(self):
        """Test description validation."""
        valid = ValidationManager.validate_description("A valid description")
        self.assertTrue(valid)

    def test_sanitize_input(self):
        """Test input sanitization."""
        result = ValidationManager.sanitize_input("  hello  ")
        self.assertEqual(result, "hello")


if __name__ == "__main__":
    unittest.main()
