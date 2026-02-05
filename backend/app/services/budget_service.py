"""Budget business logic service."""

from datetime import datetime
from typing import Any

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.budget import DailyExpense, FixedExpense, MonthlyIncome, SavingsPlan


class BudgetService:
    """Service for managing budget data."""

    def __init__(self, db: Session) -> None:
        """Initialize with database session."""
        self.db = db

    # ============ Income ============

    def set_monthly_income(
        self,
        year_month: str,
        amount: float,
        description: str | None = None,
    ) -> MonthlyIncome:
        """Set or update monthly income."""
        income = (
            self.db.query(MonthlyIncome)
            .filter(MonthlyIncome.year_month == year_month)
            .first()
        )

        if income:
            income.amount = amount
            income.description = description
        else:
            income = MonthlyIncome(
                year_month=year_month,
                amount=amount,
                description=description,
            )
            self.db.add(income)

        self.db.commit()
        self.db.refresh(income)
        return income

    def get_monthly_income(self, year_month: str) -> MonthlyIncome | None:
        """Get monthly income for a specific month."""
        return (
            self.db.query(MonthlyIncome)
            .filter(MonthlyIncome.year_month == year_month)
            .first()
        )

    # ============ Fixed Expenses ============

    def add_fixed_expense(
        self,
        name: str,
        amount: float,
        category: str | None = None,
    ) -> FixedExpense:
        """Add a new fixed expense."""
        expense = FixedExpense(
            name=name,
            amount=amount,
            category=category,
        )
        self.db.add(expense)
        self.db.commit()
        self.db.refresh(expense)
        return expense

    def list_fixed_expenses(self, active_only: bool = True) -> list[FixedExpense]:
        """List all fixed expenses."""
        query = self.db.query(FixedExpense)
        if active_only:
            query = query.filter(FixedExpense.is_active == True)
        return query.all()

    def remove_fixed_expense(self, expense_id: int) -> bool:
        """Remove (deactivate) a fixed expense."""
        expense = (
            self.db.query(FixedExpense).filter(FixedExpense.id == expense_id).first()
        )
        if expense:
            expense.is_active = False
            self.db.commit()
            return True
        return False

    def get_total_fixed_expenses(self) -> float:
        """Get total of all active fixed expenses."""
        result = (
            self.db.query(func.sum(FixedExpense.amount))
            .filter(FixedExpense.is_active == True)
            .scalar()
        )
        return result or 0.0

    # ============ Savings ============

    def set_savings_plan(
        self,
        year_month: str,
        target_amount: float,
    ) -> SavingsPlan:
        """Set or update savings plan."""
        plan = (
            self.db.query(SavingsPlan)
            .filter(SavingsPlan.year_month == year_month)
            .first()
        )

        if plan:
            plan.target_amount = target_amount
        else:
            plan = SavingsPlan(
                year_month=year_month,
                target_amount=target_amount,
            )
            self.db.add(plan)

        self.db.commit()
        self.db.refresh(plan)
        return plan

    def update_savings(
        self,
        year_month: str,
        amount: float,
    ) -> SavingsPlan | None:
        """Update actual savings amount."""
        plan = (
            self.db.query(SavingsPlan)
            .filter(SavingsPlan.year_month == year_month)
            .first()
        )

        if plan:
            plan.actual_amount = amount
            self.db.commit()
            self.db.refresh(plan)
            return plan
        return None

    def get_savings_plan(self, year_month: str) -> SavingsPlan | None:
        """Get savings plan for a specific month."""
        return (
            self.db.query(SavingsPlan)
            .filter(SavingsPlan.year_month == year_month)
            .first()
        )

    # ============ Daily Expenses ============

    def add_daily_expense(
        self,
        date: str,
        amount: float,
        category: str,
        description: str | None = None,
    ) -> DailyExpense:
        """Add a daily expense."""
        expense = DailyExpense(
            date=date,
            amount=amount,
            category=category,
            description=description,
        )
        self.db.add(expense)
        self.db.commit()
        self.db.refresh(expense)
        return expense

    def get_expenses_by_date(self, date: str) -> list[DailyExpense]:
        """Get all expenses for a specific date."""
        return self.db.query(DailyExpense).filter(DailyExpense.date == date).all()

    def get_expenses_by_period(
        self,
        start_date: str,
        end_date: str,
    ) -> list[DailyExpense]:
        """Get expenses within a date range."""
        return (
            self.db.query(DailyExpense)
            .filter(DailyExpense.date >= start_date, DailyExpense.date <= end_date)
            .order_by(DailyExpense.date)
            .all()
        )

    def get_monthly_daily_expenses(self, year_month: str) -> list[DailyExpense]:
        """Get all daily expenses for a specific month."""
        return (
            self.db.query(DailyExpense)
            .filter(DailyExpense.date.like(f"{year_month}%"))
            .order_by(DailyExpense.date)
            .all()
        )

    def get_total_daily_expenses(self, year_month: str) -> float:
        """Get total daily expenses for a month."""
        result = (
            self.db.query(func.sum(DailyExpense.amount))
            .filter(DailyExpense.date.like(f"{year_month}%"))
            .scalar()
        )
        return result or 0.0

    # ============ Analysis ============

    def get_monthly_summary(self, year_month: str) -> dict[str, Any]:
        """Get comprehensive monthly summary."""
        income = self.get_monthly_income(year_month)
        savings = self.get_savings_plan(year_month)

        total_income = income.amount if income else 0.0
        total_fixed = self.get_total_fixed_expenses()
        total_daily = self.get_total_daily_expenses(year_month)
        savings_target = savings.target_amount if savings else 0.0
        savings_actual = savings.actual_amount if savings else 0.0

        total_expenses = total_fixed + total_daily
        remaining = total_income - total_expenses - savings_actual

        return {
            "year_month": year_month,
            "total_income": total_income,
            "total_fixed_expenses": total_fixed,
            "total_daily_expenses": total_daily,
            "total_expenses": total_expenses,
            "savings_target": savings_target,
            "savings_actual": savings_actual,
            "remaining_budget": remaining,
        }

    def get_category_analysis(self, year_month: str) -> list[dict[str, Any]]:
        """Get spending analysis by category."""
        expenses = self.get_monthly_daily_expenses(year_month)

        category_totals: dict[str, dict[str, Any]] = {}
        total = 0.0

        for expense in expenses:
            cat = expense.category
            if cat not in category_totals:
                category_totals[cat] = {"total": 0.0, "count": 0}
            category_totals[cat]["total"] += expense.amount
            category_totals[cat]["count"] += 1
            total += expense.amount

        result = []
        for category, data in sorted(
            category_totals.items(), key=lambda x: x[1]["total"], reverse=True
        ):
            percentage = (data["total"] / total * 100) if total > 0 else 0
            result.append(
                {
                    "category": category,
                    "total_amount": data["total"],
                    "count": data["count"],
                    "percentage": round(percentage, 1),
                }
            )

        return result

    def get_budget_status(self, year_month: str) -> dict[str, Any]:
        """Get current budget status."""
        summary = self.get_monthly_summary(year_month)

        total_income = summary["total_income"]
        total_expenses = summary["total_expenses"]
        remaining = summary["remaining_budget"]
        savings_target = summary["savings_target"]
        savings_actual = summary["savings_actual"]

        savings_progress = 0.0
        if savings_target > 0:
            savings_progress = (savings_actual / savings_target) * 100

        # Determine status
        if remaining < 0:
            status = "over_budget"
        elif remaining < total_income * 0.1:  # Less than 10% remaining
            status = "warning"
        else:
            status = "good"

        return {
            "year_month": year_month,
            "total_income": total_income,
            "total_expenses": total_expenses,
            "remaining": remaining,
            "savings_progress": round(savings_progress, 1),
            "status": status,
        }
