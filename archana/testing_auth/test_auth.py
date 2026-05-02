"""
Unit tests for authentication.
"""
import unittest
from .auth import AuthenticationManager


class TestAuthentication(unittest.TestCase):
    """Test authentication functions."""

    def test_validate_username_valid(self):
        """Test valid username."""
        valid, error = AuthenticationManager.validate_username("john123")
        self.assertTrue(valid)
        self.assertIsNone(error)

    def test_validate_username_too_short(self):
        """Test username too short."""
        valid, error = AuthenticationManager.validate_username("ab")
        self.assertFalse(valid)
        self.assertIn("at least 3", error)

    def test_validate_username_invalid_chars(self):
        """Test username with invalid characters."""
        valid, error = AuthenticationManager.validate_username("john@123")
        self.assertFalse(valid)

    def test_validate_password_valid(self):
        """Test valid password."""
        valid, error = AuthenticationManager.validate_password("password123")
        self.assertTrue(valid)
        self.assertIsNone(error)

    def test_validate_password_too_short(self):
        """Test password too short."""
        valid, error = AuthenticationManager.validate_password("123")
        self.assertFalse(valid)
        self.assertIn("at least 4", error)

    def test_hash_and_verify_password(self):
        """Test password hashing and verification."""
        password = "mysecurepass"
        hashed = AuthenticationManager.hash_password(password)
        self.assertTrue(AuthenticationManager.verify_password(password, hashed))
        self.assertFalse(AuthenticationManager.verify_password("wrongpass", hashed))


if __name__ == "__main__":
    unittest.main()
