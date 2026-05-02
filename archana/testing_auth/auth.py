"""
Authentication module for user validation.
"""
import hashlib
from typing import Optional, Tuple


class AuthenticationManager:
    """Manage user authentication and validation."""

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """Verify password against hash."""
        return AuthenticationManager.hash_password(password) == password_hash

    @staticmethod
    def validate_username(username: str) -> Tuple[bool, Optional[str]]:
        """Validate username format."""
        if not username:
            return False, "Username is required"
        if len(username) < 3:
            return False, "Username must be at least 3 characters"
        if len(username) > 50:
            return False, "Username must be less than 50 characters"
        if not username.isalnum():
            return False, "Username must contain only alphanumeric characters"
        return True, None

    @staticmethod
    def validate_password(password: str) -> Tuple[bool, Optional[str]]:
        """Validate password strength."""
        if not password:
            return False, "Password is required"
        if len(password) < 4:
            return False, "Password must be at least 4 characters"
        if len(password) > 128:
            return False, "Password must be less than 128 characters"
        return True, None
"""
Authentication module for user validation.
"""
import hashlib
from typing import Optional, Tuple


class AuthenticationManager:
    """Manage user authentication and validation."""

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """Verify password against hash."""
        return AuthenticationManager.hash_password(password) == password_hash

    @staticmethod
    def validate_username(username: str) -> Tuple[bool, Optional[str]]:
        """Validate username format."""
        if not username:
            return False, "Username is required"
        if len(username) < 3:
            return False, "Username must be at least 3 characters"
        if len(username) > 50:
            return False, "Username must be less than 50 characters"
        if not username.isalnum():
            return False, "Username must contain only alphanumeric characters"
        return True, None

    @staticmethod
    def validate_password(password: str) -> Tuple[bool, Optional[str]]:
        """Validate password strength."""
        if not password:
            return False, "Password is required"
        if len(password) < 4:
            return False, "Password must be at least 4 characters"
        if len(password) > 128:
            return False, "Password must be less than 128 characters"
        return True, None
