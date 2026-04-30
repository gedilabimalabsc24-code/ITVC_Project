"""
Flask routes for the finance application.
"""
from datetime import datetime
from functools import wraps

from flask import jsonify, request, session

from .config import EXPENSE_CATEGORIES, INCOME_CATEGORIES, TRANSFER_CATEGORIES
from .insights import InsightsGenerator
from .logic import FinanceLogic
from .storage import StorageManager
from .utils import generate_id, get_timestamp, validate_amount, validate_category


def login_required(f):
    """Decorator to require login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" not in session:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_function


def register_routes(app):
    """Register all Flask routes."""

    # =========================
    # Authentication Routes
    # =========================

    @app.route("/api/register", methods=["POST"])
    def register():
        """Register new user."""
        data = request.get_json()
        username = data.get("username", "").strip()
        password = data.get("password", "").strip()

        if not username or not password:
            return jsonify({"error": "Username and password required"}), 400

        if len(password) < 4:
            return jsonify({"error": "Password must be at least 4 characters"}), 400

        if StorageManager.create_user(username, password):
            return jsonify({"message": "User created successfully"}), 201
        else:
            return jsonify({"error": "User already exists"}), 409

    @app.route("/api/login", methods=["POST"])
    def login():
        """Login user."""
        data = request.get_json()
        username = data.get("username", "").strip()
        password = data.get("password", "").strip()

        user = StorageManager.get_user(username)
        if user and user.get("password") == password:
            session["username"] = username
            return jsonify({"message": "Login successful", "username": username}), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401

    @app.route("/api/logout", methods=["POST"])
    @login_required
    def logout():
        """Logout user."""
        session.clear()
        return jsonify({"message": "Logged out successfully"}), 200

    @app.route("/api/profile", methods=["GET"])
    @login_required
    def get_profile():
        """Get user profile."""
        username = session.get("username")
        user = StorageManager.get_user(username)
        return jsonify({"username": username, "created_at": user.get("created_at")}), 200

    # =========================
    # Transaction Routes
    # =========================

    @app.route("/api/transactions", methods=["GET"])
    @login_required
    def get_transactions():
        """Get all transactions for user."""
        username = session.get("username")
        expenses = StorageManager.get_user_expenses(username)
        
        # Get recent transactions (sorted by date, newest first)
        sorted_expenses = FinanceLogic.get_recent_expenses(expenses, limit=100)
        
        return jsonify({"transactions": sorted_expenses}), 200

    @app.route("/api/transactions", methods=["POST"])
    @login_required
    def add_transaction():
        """Add new transaction."""
        username = session.get("username")
        data = request.get_json()

        # Validation
        amount = data.get("amount")
        category = data.get("category", "").strip()
        description = data.get("description", "").strip()
        transaction_type = data.get("type", "expense").lower()

        if not validate_amount(amount):
            return jsonify({"error": "Invalid amount"}), 400

        if transaction_type == "expense":
            if not validate_category(category, EXPENSE_CATEGORIES):
                return jsonify({"error": "Invalid expense category"}), 400
        elif transaction_type == "income":
            if not validate_category(category, INCOME_CATEGORIES):
                return jsonify({"error": "Invalid income category"}), 400
        elif transaction_type == "transfer":
            if not validate_category(category, TRANSFER_CATEGORIES):
                return jsonify({"error": "Invalid transfer category"}), 400
        else:
            return jsonify({"error": "Invalid transaction type"}), 400

        # Create transaction
        transaction = {
            "id": generate_id(),
            "username": username,
            "amount": float(amount),
            "category": category,
            "description": description,
            "type": transaction_type,
            "date": data.get("date", get_timestamp()),
            "created_at": get_timestamp(),
        }

        StorageManager.add_expense(transaction)
        return jsonify({"message": "Transaction added", "transaction": transaction}), 201

    @app.route("/api/transactions/<transaction_id>", methods=["DELETE"])
    @login_required
    def delete_transaction(transaction_id):
        """Delete transaction."""
        username = session.get("username")
        
        # Verify ownership
        expenses = StorageManager.get_user_expenses(username)
        if not any(e.get("id") == transaction_id for e in expenses):
            return jsonify({"error": "Transaction not found"}), 404

        if StorageManager.delete_expense(transaction_id):
            return jsonify({"message": "Transaction deleted"}), 200
        else:
            return jsonify({"error": "Failed to delete transaction"}), 500

    # =========================
    # Dashboard Routes
    # =========================

    @app.route("/api/dashboard", methods=["GET"])
    @login_required
    def get_dashboard():
        """Get dashboard data."""
        username = session.get("username")
        expenses = StorageManager.get_user_expenses(username)

        total_income, total_expense, balance = FinanceLogic.calculate_balance(expenses)
        insight_message = FinanceLogic.get_insight_message(expenses)
        recent_transactions = FinanceLogic.get_recent_expenses(expenses, limit=5)

        return jsonify({
            "summary": {
                "total_income": total_income,
                "total_expense": total_expense,
                "balance": balance,
            },
            "insight": insight_message,
            "recent_transactions": recent_transactions,
        }), 200

    # =========================
    # Analytics Routes
    # =========================

    @app.route("/api/analytics", methods=["GET"])
    @login_required
    def get_analytics():
        """Get analytics data."""
        username = session.get("username")
        expenses = StorageManager.get_user_expenses(username)

        analytics = InsightsGenerator.get_full_analytics(expenses)
        return jsonify(analytics), 200

    @app.route("/api/category-breakdown", methods=["GET"])
    @login_required
    def get_category_breakdown():
        """Get expense breakdown by category."""
        username = session.get("username")
        expenses = StorageManager.get_user_expenses(username)

        breakdown = FinanceLogic.calculate_category_breakdown(expenses, "expense")
        return jsonify({"breakdown": breakdown}), 200

    # =========================
    # Metadata Routes
    # =========================

    @app.route("/api/categories", methods=["GET"])
    def get_categories():
        """Get available categories."""
        return jsonify({
            "expense_categories": EXPENSE_CATEGORIES,
            "income_categories": INCOME_CATEGORIES,
            "transfer_categories": TRANSFER_CATEGORIES,
        }), 200

    @app.route("/api/health", methods=["GET"])
    def health_check():
        """Health check endpoint."""
        return jsonify({"status": "healthy"}), 200
