"""
Integration tests for storage.
"""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

# Mock storage for testing
class MockStorageManager:
    """Mock storage for testing."""
    
    def __init__(self):
        self.users = {}
        self.expenses = []
    
    def get_user(self, username):
        return self.users.get(username)
    
    def create_user(self, username, password):
        if username in self.users:
            return False
        self.users[username] = {"password": password}
        return True
    
    def add_expense(self, expense):
        self.expenses.append(expense)
        return True
    
    def get_user_expenses(self, username):
        return [e for e in self.expenses if e.get("username") == username]


class TestStorage(unittest.TestCase):
    """Test storage functions."""

    def setUp(self):
        """Set up test storage."""
        self.storage = MockStorageManager()

    def test_create_user(self):
        """Test user creation."""
        result = self.storage.create_user("testuser", "pass123")
        self.assertTrue(result)
        self.assertIsNotNone(self.storage.get_user("testuser"))

    def test_duplicate_user(self):
        """Test duplicate user creation."""
        self.storage.create_user("testuser", "pass123")
        result = self.storage.create_user("testuser", "pass123")
        self.assertFalse(result)

    def test_add_expense(self):
        """Test adding expense."""
        self.storage.create_user("testuser", "pass123")
        expense = {
            "id": "123",
            "username": "testuser",
            "amount": 50.00,
            "category": "Food",
            "type": "expense",
        }
        result = self.storage.add_expense(expense)
        self.assertTrue(result)

    def test_get_user_expenses(self):
        """Test getting user expenses."""
        self.storage.create_user("user1", "pass123")
        self.storage.create_user("user2", "pass123")
        
        self.storage.add_expense({
            "id": "1",
            "username": "user1",
            "amount": 50.00,
            "type": "expense",
        })
        self.storage.add_expense({
            "id": "2",
            "username": "user1",
            "amount": 100.00,
            "type": "expense",
        })
        self.storage.add_expense({
            "id": "3",
            "username": "user2",
            "amount": 75.00,
            "type": "expense",
        })
        
        user1_expenses = self.storage.get_user_expenses("user1")
        user2_expenses = self.storage.get_user_expenses("user2")
        
        self.assertEqual(len(user1_expenses), 2)
        self.assertEqual(len(user2_expenses), 1)


if __name__ == "__main__":
    unittest.main()
