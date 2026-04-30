"""
Core business logic for the finance system.
"""
from datetime import datetime
from typing import Any, Dict, List, Tuple

from .config import OVERSPENDING_THRESHOLD
from .utils import get_month_year, round_decimal


class FinanceLogic:
    """Core finance calculations and analysis."""

    @staticmethod
    def calculate_balance(expenses: List[Dict[str, Any]]) -> Tuple[float, float, float]:
        """
        Calculate income, expense, and balance.
        Returns: (total_income, total_expense, balance)
        """
        total_income = 0.0
        total_expense = 0.0

        for expense in expenses:
            amount = float(expense.get("amount", 0))
            transaction_type = expense.get("type", "expense").lower()

            if transaction_type == "income":
                total_income += amount
            elif transaction_type == "expense":
                total_expense += amount
            elif transaction_type == "transfer":
                # Transfers don't affect balance
                pass

        balance = total_income - total_expense
        return (
            round_decimal(total_income),
            round_decimal(total_expense),
            round_decimal(balance),
        )

    @staticmethod
    def calculate_monthly_totals(
        expenses: List[Dict[str, Any]],
    ) -> Dict[str, Tuple[float, float]]:
        """
        Calculate monthly income and expenses.
        Returns: {month: (income, expense)}
        """
        monthly = {}

        for expense in expenses:
            month = get_month_year(expense.get("date", ""))
            amount = float(expense.get("amount", 0))
            transaction_type = expense.get("type", "expense").lower()

            if month not in monthly:
                monthly[month] = (0.0, 0.0)

            income, expenses_val = monthly[month]

            if transaction_type == "income":
                income += amount
            elif transaction_type == "expense":
                expenses_val += amount

            monthly[month] = (
                round_decimal(income),
                round_decimal(expenses_val),
            )

        return monthly

    @staticmethod
    def calculate_category_breakdown(
        expenses: List[Dict[str, Any]], category_type: str = "expense"
    ) -> Dict[str, float]:
        """
        Calculate breakdown by category.
        Returns: {category: total_amount}
        """
        breakdown = {}

        for expense in expenses:
            if expense.get("type", "").lower() == category_type.lower():
                category = expense.get("category", "Other")
                amount = float(expense.get("amount", 0))
                breakdown[category] = breakdown.get(category, 0.0) + amount

        return {k: round_decimal(v) for k, v in breakdown.items()}

    @staticmethod
    def get_insight_message(expenses: List[Dict[str, Any]]) -> str:
        """
        Generate insight message based on spending patterns.
        """
        if not expenses:
            return "No transactions yet. Start by adding your first transaction!"

        total_income, total_expense, _ = FinanceLogic.calculate_balance(expenses)
        
        # Calculate highest spending category
        expense_breakdown = FinanceLogic.calculate_category_breakdown(expenses, "expense")
        top_category = max(expense_breakdown.items(), key=lambda x: x[1], default=("None", 0))

        if total_expense > OVERSPENDING_THRESHOLD:
            return f"⚠️ Warning: Your expenses (₹{total_expense:,.2f}) exceed ₹{OVERSPENDING_THRESHOLD:,.2f}. Consider reviewing your spending."
            
        if top_category[1] > (OVERSPENDING_THRESHOLD * 0.5): # if one category is taking up 50% of threshold
            return f"⚠️ Alert: {top_category[0]} expenses are unusually high (₹{top_category[1]:,.2f})."

        if total_income > 0 and total_expense > 0:
            percentage = (total_expense / total_income) * 100
            if percentage < 50:
                return "💚 Excellent! You're saving well. Keep it up!"
            elif percentage < 80:
                return "👍 Good spending habits. You're on track!"
            else:
                return "⚠️ Your expenses are close to your income. Budget carefully!"

        if total_income > 0 and total_expense == 0:
            return "🎉 Great income with no expenses recorded. Don't forget to log your spending!"

        return "📊 Keep tracking your finances for better insights."

    @staticmethod
    def filter_by_month(expenses: List[Dict[str, Any]], month: str) -> List[Dict[str, Any]]:
        """Filter expenses by month (YYYY-MM format)."""
        return [e for e in expenses if get_month_year(e.get("date", "")).startswith(month)]

    @staticmethod
    def filter_by_category(
        expenses: List[Dict[str, Any]], category: str
    ) -> List[Dict[str, Any]]:
        """Filter expenses by category."""
        return [e for e in expenses if e.get("category") == category]

    @staticmethod
    def get_recent_expenses(expenses: List[Dict[str, Any]], limit: int = 10) -> List[Dict[str, Any]]:
        """Get most recent expenses."""
        sorted_expenses = sorted(
            expenses, key=lambda x: x.get("date", ""), reverse=True
        )
        return sorted_expenses[:limit]
