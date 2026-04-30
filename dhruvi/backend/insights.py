"""
Insights and analytics module.
"""
from typing import Any, Dict, List

from .logic import FinanceLogic


class InsightsGenerator:
    """Generate financial insights and analytics."""

    @staticmethod
    def get_dashboard_summary(expenses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get dashboard summary data."""
        total_income, total_expense, balance = FinanceLogic.calculate_balance(expenses)
        insight = FinanceLogic.get_insight_message(expenses)

        return {
            "total_income": total_income,
            "total_expense": total_expense,
            "balance": balance,
            "insight_message": insight,
            "transaction_count": len(expenses),
        }

    @staticmethod
    def get_category_insights(expenses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get category-wise insights."""
        expense_breakdown = FinanceLogic.calculate_category_breakdown(
            expenses, "expense"
        )
        income_breakdown = FinanceLogic.calculate_category_breakdown(
            expenses, "income"
        )

        return {
            "expenses_by_category": expense_breakdown,
            "income_by_category": income_breakdown,
            "top_expense_category": max(expense_breakdown.items(), default=("N/A", 0))[
                0
            ]
            if expense_breakdown
            else "N/A",
        }

    @staticmethod
    def get_monthly_insights(expenses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get monthly insights."""
        monthly_totals = FinanceLogic.calculate_monthly_totals(expenses)

        return {"monthly_summary": monthly_totals}

    @staticmethod
    def get_full_analytics(expenses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get complete analytics."""
        return {
            "summary": InsightsGenerator.get_dashboard_summary(expenses),
            "categories": InsightsGenerator.get_category_insights(expenses),
            "monthly": InsightsGenerator.get_monthly_insights(expenses),
        }
