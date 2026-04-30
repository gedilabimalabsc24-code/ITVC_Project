"""
Main Flask application entry point.
"""
from flask import Flask, render_template, request, redirect, url_for, session, flash

from dhruvi.backend.config import SECRET_KEY, SESSION_TIMEOUT
from dhruvi.backend.logic import FinanceLogic
from dhruvi.backend.storage import StorageManager
from dhruvi.backend.utils import generate_id, get_timestamp
from archana.testing_auth.auth import AuthenticationManager
from archana.testing_auth.validation import ValidationManager

def create_app():
    """Create and configure Flask application."""
    app = Flask(__name__, template_folder="bimala/frontend", static_folder="bimala/frontend")
    
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["PERMANENT_SESSION_LIFETIME"] = SESSION_TIMEOUT
    app.config["SESSION_COOKIE_SECURE"] = False 
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

    @app.route("/", methods=["GET"])
    def index():
        if "username" in session:
            return redirect(url_for("dashboard"))
        return redirect(url_for("login_page"))

    @app.route("/login", methods=["GET", "POST"])
    def login_page():
        if request.method == "POST":
            # Determine if it's a login or register form submission
            action = request.form.get("action")
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "").strip()
            
            if action == "register":
                valid_user, user_err = AuthenticationManager.validate_username(username)
                valid_pass, pass_err = AuthenticationManager.validate_password(password)
                
                if not valid_user:
                    flash(f"Invalid registration: {user_err}", "error")
                elif not valid_pass:
                    flash(f"Invalid registration: {pass_err}", "error")
                else:
                    hashed_pwd = AuthenticationManager.hash_password(password)
                    if StorageManager.create_user(username, hashed_pwd):
                        flash("Registration successful! Please login.", "success")
                    else:
                        flash("User already exists.", "error")
            else:
                user = StorageManager.get_user(username)
                if user:
                    stored_pwd = user.get("password")
                    # Check plain password for backward compatibility or hashed password
                    if stored_pwd == password or AuthenticationManager.verify_password(password, stored_pwd):
                        session["username"] = username
                        return redirect(url_for("dashboard"))
                
                flash("Invalid credentials.", "error")
                    
        return render_template("login.html")

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for("login_page"))

    @app.route("/dashboard")
    def dashboard():
        if "username" not in session:
            return redirect(url_for("login_page"))
            
        username = session["username"]
        expenses = StorageManager.get_user_expenses(username)
        total_income, total_expense, balance = FinanceLogic.calculate_balance(expenses)
        insight_message = FinanceLogic.get_insight_message(expenses)
        
        return render_template("dashboard.html", 
                             total_income=total_income, 
                             total_expense=total_expense, 
                             balance=balance,
                             insight_message=insight_message)

    @app.route("/analytics")
    def analytics():
        if "username" not in session:
            return redirect(url_for("login_page"))
            
        username = session["username"]
        expenses = StorageManager.get_user_expenses(username)
        
        category_totals = FinanceLogic.calculate_category_breakdown(expenses, "expense")
        monthly_data = FinanceLogic.calculate_monthly_totals(expenses)
        
        total_income, total_expense, balance = FinanceLogic.calculate_balance(expenses)
        
        # Calculate this month stats
        from dhruvi.backend.utils import get_timestamp
        current_month = get_timestamp()[:7]  # YYYY-MM
        
        # We also need this_month_income, this_month_expense
        this_month_income = monthly_data.get(current_month, (0,0))[0] if monthly_data else 0
        this_month_expense = monthly_data.get(current_month, (0,0))[1] if monthly_data else 0
        
        # Format monthly data for JS
        formatted_monthly = {}
        for m, (inc, exp) in monthly_data.items():
            formatted_monthly[m] = {"income": inc, "expense": exp}
            
        return render_template("analytics.html", 
                             data=expenses,
                             category_totals=category_totals,
                             monthly_data=formatted_monthly,
                             current_month=current_month,
                             this_month_income=this_month_income,
                             this_month_expense=this_month_expense)

    @app.route("/transactions")
    def transactions():
        if "username" not in session:
            return redirect(url_for("login_page"))
            
        username = session["username"]
        expenses = StorageManager.get_user_expenses(username)
        
        # Sort transactions newest first
        sorted_expenses = FinanceLogic.get_recent_expenses(expenses, limit=500)
        
        return render_template("transactions.html", transactions=sorted_expenses)

    @app.route("/add", methods=["GET", "POST"])
    def add():
        if "username" not in session:
            return redirect(url_for("login_page"))
            
        if request.method == "POST":
            amount = request.form.get("amount")
            category = request.form.get("category", "Other")
            description = request.form.get("description", "")
            transaction_type = request.form.get("type", "expense")
            date_val = request.form.get("date", get_timestamp())
            
            try:
                valid_amt, amt_err = ValidationManager.validate_amount(amount)
                if not valid_amt:
                    flash(amt_err, "error")
                    return render_template("add.html")
                    
                amt_float = float(amount)
                transaction = {
                    "id": generate_id(),
                    "username": session["username"],
                    "amount": amt_float,
                    "category": ValidationManager.sanitize_input(category),
                    "description": ValidationManager.sanitize_input(description),
                    "type": transaction_type,
                    "date": date_val,
                    "created_at": get_timestamp(),
                }
                StorageManager.add_expense(transaction)
                return redirect(url_for("dashboard"))
            except ValueError:
                flash("Invalid amount entered.", "error")

        return render_template("add.html")

    @app.route("/delete/<transaction_id>", methods=["POST"])
    def delete(transaction_id):
        if "username" not in session:
            return redirect(url_for("login_page"))
            
        StorageManager.delete_expense(transaction_id)
        # Check referring page to redirect properly
        referrer = request.referrer or url_for("dashboard")
        if "transactions" in referrer:
            return redirect(url_for("transactions"))
        return redirect(url_for("dashboard"))

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="127.0.0.1", port=5000)
