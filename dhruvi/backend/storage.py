"""
Storage module for JSON-based persistence.
"""
import json
import threading
from pathlib import Path
from typing import Any, Dict, List, Optional

from .config import EXPENSES_FILE, USER_FILE


class StorageManager:
    """Thread-safe JSON storage manager."""

    _lock = threading.RLock()

    @classmethod
    def _ensure_file_exists(cls, filepath: Path, default_content: Any) -> None:
        """Create file with default content if it doesn't exist."""
        if not filepath.exists():
            filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, "w") as f:
                json.dump(default_content, f, indent=2)

    @classmethod
    def load_users(cls) -> Dict[str, Dict[str, Any]]:
        """Load all users from JSON."""
        cls._ensure_file_exists(USER_FILE, {})
        with cls._lock:
            with open(USER_FILE, "r") as f:
                return json.load(f)

    @classmethod
    def save_users(cls, users: Dict[str, Dict[str, Any]]) -> None:
        """Save users to JSON."""
        with cls._lock:
            USER_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(USER_FILE, "w") as f:
                json.dump(users, f, indent=2)

    @classmethod
    def load_expenses(cls) -> List[Dict[str, Any]]:
        """Load all expenses from JSON."""
        cls._ensure_file_exists(EXPENSES_FILE, [])
        with cls._lock:
            with open(EXPENSES_FILE, "r") as f:
                return json.load(f)

    @classmethod
    def save_expenses(cls, expenses: List[Dict[str, Any]]) -> None:
        """Save expenses to JSON."""
        with cls._lock:
            EXPENSES_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(EXPENSES_FILE, "w") as f:
                json.dump(expenses, f, indent=2)

    @classmethod
    def get_user(cls, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username."""
        users = cls.load_users()
        return users.get(username)

    @classmethod
    def create_user(cls, username: str, password: str) -> bool:
        """Create new user."""
        users = cls.load_users()
        if username in users:
            return False
        users[username] = {"password": password, "created_at": _get_timestamp()}
        cls.save_users(users)
        return True

    @classmethod
    def get_user_expenses(cls, username: str) -> List[Dict[str, Any]]:
        """Get expenses for a specific user."""
        expenses = cls.load_expenses()
        return [e for e in expenses if e.get("username") == username]

    @classmethod
    def add_expense(cls, expense: Dict[str, Any]) -> bool:
        """Add new expense."""
        expenses = cls.load_expenses()
        expenses.append(expense)
        cls.save_expenses(expenses)
        return True

    @classmethod
    def delete_expense(cls, expense_id: str) -> bool:
        """Delete expense by ID."""
        expenses = cls.load_expenses()
        original_len = len(expenses)
        expenses = [e for e in expenses if e.get("id") != expense_id]
        if len(expenses) < original_len:
            cls.save_expenses(expenses)
            return True
        return False


def _get_timestamp() -> str:
    """Get current timestamp as ISO string."""
    from datetime import datetime
    return datetime.now().isoformat()
