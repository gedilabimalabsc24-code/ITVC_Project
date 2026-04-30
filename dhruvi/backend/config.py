"""
Configuration module for Flask app.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"

# File paths
USER_FILE = DATA_DIR / "user.json"
EXPENSES_FILE = DATA_DIR / "expenses.json"

# Flask config
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-prod-use-env")
SESSION_TIMEOUT = 3600  # 1 hour in seconds

# Thresholds
OVERSPENDING_THRESHOLD = 10000

# Categories
EXPENSE_CATEGORIES = [
    "Food",
    "Transport",
    "Entertainment",
    "Utilities",
    "Healthcare",
    "Shopping",
    "Education",
    "Other",
]

INCOME_CATEGORIES = ["Salary", "Freelance", "Investment", "Bonus", "Other"]

TRANSFER_CATEGORIES = ["Bank Transfer", "Internal Transfer"]
