#!/usr/bin/env python3
"""
Verification script to test that the Smart Expense Tracker is correctly set up.
Run this to verify all components are working.
"""

import sys
import json
from pathlib import Path

def verify_structure():
    """Verify project structure."""
    print("🔍 Verifying project structure...\n")
    
    required_dirs = [
        "dhruvi/backend",
        "bimala/frontend",
        "archana/testing_auth",
        "data",
        "android_app"
    ]
    
    required_files = {
        "app.py": "Flask entry point",
        "requirements.txt": "Python dependencies",
        "dhruvi/backend/config.py": "Backend config",
        "dhruvi/backend/storage.py": "Data storage",
        "dhruvi/backend/logic.py": "Business logic",
        "dhruvi/backend/routes.py": "API routes",
        "bimala/frontend/index.html": "Main page",
        "bimala/frontend/style.css": "Styles",
        "bimala/frontend/script.js": "Frontend logic",
        "archana/testing_auth/auth.py": "Auth module",
        "archana/testing_auth/test_auth.py": "Auth tests",
        "data/user.json": "User storage",
        "data/expenses.json": "Expense storage",
    }
    
    # Check directories
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"✅ {dir_path}")
        else:
            print(f"❌ {dir_path} - NOT FOUND")
            return False
    
    print()
    
    # Check files
    for file_path, description in required_files.items():
        if Path(file_path).exists():
            size = Path(file_path).stat().st_size
            print(f"✅ {file_path} ({size} bytes) - {description}")
        else:
            print(f"❌ {file_path} - NOT FOUND")
            return False
    
    return True


def verify_imports():
    """Verify Python imports work."""
    print("\n🔍 Verifying Python imports...\n")
    
    try:
        import flask
        print(f"✅ Flask {flask.__version__} imported successfully")
    except ImportError as e:
        print(f"❌ Flask import failed: {e}")
        print("   Run: pip install -r requirements.txt")
        return False
    
    try:
        from dhruvi.backend.config import EXPENSE_CATEGORIES
        print(f"✅ Backend config imported - Found {len(EXPENSE_CATEGORIES)} expense categories")
    except ImportError as e:
        print(f"❌ Backend config import failed: {e}")
        return False
    
    try:
        from dhruvi.backend.storage import StorageManager
        print("✅ Storage manager imported successfully")
    except ImportError as e:
        print(f"❌ Storage manager import failed: {e}")
        return False
    
    try:
        from dhruvi.backend.logic import FinanceLogic
        print("✅ Finance logic imported successfully")
    except ImportError as e:
        print(f"❌ Finance logic import failed: {e}")
        return False
    
    try:
        from archana.testing_auth.auth import AuthenticationManager
        print("✅ Authentication manager imported successfully")
    except ImportError as e:
        print(f"❌ Auth manager import failed: {e}")
        return False
    
    try:
        from archana.testing_auth.validation import ValidationManager
        print("✅ Validation manager imported successfully")
    except ImportError as e:
        print(f"❌ Validation manager import failed: {e}")
        return False
    
    return True


def verify_data_files():
    """Verify data files are properly initialized."""
    print("\n🔍 Verifying data files...\n")
    
    try:
        with open("data/user.json", "r") as f:
            users = json.load(f)
            print(f"✅ user.json is valid JSON - {len(users)} users")
    except Exception as e:
        print(f"❌ user.json error: {e}")
        return False
    
    try:
        with open("data/expenses.json", "r") as f:
            expenses = json.load(f)
            print(f"✅ expenses.json is valid JSON - {len(expenses)} expenses")
    except Exception as e:
        print(f"❌ expenses.json error: {e}")
        return False
    
    return True


def verify_app_creation():
    """Verify Flask app can be created."""
    print("\n🔍 Verifying Flask app creation...\n")
    
    try:
        from app import create_app
        app = create_app()
        print(f"✅ Flask app created successfully")
        print(f"✅ App name: {app.name}")
        print(f"✅ Debug mode: {app.debug}")
        
        # List registered routes
        routes = []
        for rule in app.url_map.iter_rules():
            if rule.endpoint != 'static':
                routes.append(f"   {rule.rule} -> {rule.endpoint}")
        
        print(f"✅ Registered {len(routes)} routes:")
        for route in sorted(routes)[:10]:
            print(route)
        
        if len(routes) > 10:
            print(f"   ... and {len(routes) - 10} more routes")
        
        return True
    except Exception as e:
        print(f"❌ Flask app creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def verify_logic():
    """Test business logic."""
    print("\n🔍 Verifying business logic...\n")
    
    try:
        from dhruvi.backend.logic import FinanceLogic
        
        # Test with sample data
        sample_expenses = [
            {"amount": 100, "type": "expense", "date": "2024-04-30T10:00:00", "category": "Food"},
            {"amount": 50, "type": "expense", "date": "2024-04-30T11:00:00", "category": "Transport"},
            {"amount": 200, "type": "income", "date": "2024-04-30T12:00:00", "category": "Salary"},
        ]
        
        total_income, total_expense, balance = FinanceLogic.calculate_balance(sample_expenses)
        print(f"✅ Calculate balance: Income=${total_income}, Expense=${total_expense}, Balance=${balance}")
        
        breakdown = FinanceLogic.calculate_category_breakdown(sample_expenses, "expense")
        print(f"✅ Category breakdown: {breakdown}")
        
        insight = FinanceLogic.get_insight_message(sample_expenses)
        print(f"✅ Insight: {insight}")
        
        return True
    except Exception as e:
        print(f"❌ Logic verification failed: {e}")
        return False


def main():
    """Run all verifications."""
    print("=" * 70)
    print("🚀 Smart Expense Tracker - Verification Suite")
    print("=" * 70)
    
    checks = [
        ("Structure", verify_structure),
        ("Imports", verify_imports),
        ("Data Files", verify_data_files),
        ("App Creation", verify_app_creation),
        ("Logic", verify_logic),
    ]
    
    results = {}
    for name, check in checks:
        try:
            results[name] = check()
        except Exception as e:
            print(f"\n❌ {name} verification failed with error: {e}")
            import traceback
            traceback.print_exc()
            results[name] = False
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 Verification Summary")
    print("=" * 70)
    
    for name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 70)
    if all_passed:
        print("🎉 All verifications passed!")
        print("\n✨ Your Smart Expense Tracker is ready to use!")
        print("\n📍 To start the Flask app:")
        print("   python app.py")
        print("\n📍 Then visit:")
        print("   http://localhost:5000")
        print("\n📍 Demo credentials:")
        print("   Username: admin")
        print("   Password: 1234")
        return 0
    else:
        print("⚠️  Some verifications failed. Please check the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
