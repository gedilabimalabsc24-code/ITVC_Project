"""
Utility functions for the application.
"""
import uuid
from datetime import datetime
from typing import Any, Dict, List


def generate_id() -> str:
    """Generate unique ID."""
    return str(uuid.uuid4())


def get_timestamp() -> str:
    """Get current timestamp as ISO string."""
    return datetime.now().isoformat()


def parse_date(date_str: str) -> datetime:
    """Parse ISO date string to datetime."""
    return datetime.fromisoformat(date_str)


def format_date(dt: datetime) -> str:
    """Format datetime to ISO string."""
    return dt.isoformat()


def get_month_year(date_str: str) -> str:
    """Get month-year from date string (YYYY-MM format)."""
    try:
        dt = parse_date(date_str)
        return dt.strftime("%Y-%m")
    except (ValueError, TypeError):
        return ""



def validate_amount(amount: float) -> bool:
    """Validate transaction amount."""
    try:
        val = float(amount)
        return val > 0
    except (ValueError, TypeError):
        return False


def validate_category(category: str, category_list: List[str]) -> bool:
    """Validate category against allowed list."""
    return category in category_list


def format_currency(amount: float) -> str:
    """Format amount as currency string."""
    return f"${amount:,.2f}"


def round_decimal(value: float, decimals: int = 2) -> float:
    """Round value to specified decimals."""
    return round(value, decimals)
