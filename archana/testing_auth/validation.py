"""
Input validation module.
"""
from typing import Any, List, Optional, Tuple


class ValidationManager:
    """Validate various input types."""

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format."""
        if not email:
            return False
        return "@" in email and "." in email.split("@")[-1]

    @staticmethod
    def validate_amount(amount: Any) -> Tuple[bool, Optional[str]]:
        """Validate transaction amount."""
        try:
            val = float(amount)
            if val <= 0:
                return False, "Amount must be greater than 0"
            if val > 999999999:
                return False, "Amount is too large"
            return True, None
        except (ValueError, TypeError):
            return False, "Invalid amount format"

    @staticmethod
    def validate_category(category: str, allowed: List[str]) -> bool:
        """Validate category against allowed list."""
        return category in allowed

    @staticmethod
    def validate_date(date_str: str) -> bool:
        """Validate date format (ISO format)."""
        from datetime import datetime
        try:
            datetime.fromisoformat(date_str)
            return True
        except (ValueError, TypeError):
            return False

    @staticmethod
    def validate_description(description: str, max_length: int = 500) -> bool:
        """Validate description."""
        if not isinstance(description, str):
            return False
        return 0 <= len(description) <= max_length

    @staticmethod
    def sanitize_input(value: str, max_length: int = 1000) -> str:
        """Sanitize string input."""
        if not isinstance(value, str):
            return ""
        return value.strip()[:max_length]
