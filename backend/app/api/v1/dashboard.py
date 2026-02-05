"""Dashboard endpoint."""

from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.budget import (
    BudgetStatus,
    CategoryAnalysis,
    DashboardResponse,
    FixedExpenseItem,
    FixedExpensesData,
    IncomeData,
    SavingsData,
)
from app.services.budget_service import BudgetService

router = APIRouter()


def get_current_year_month() -> str:
    """Get current year-month string."""
    return datetime.now().strftime("%Y-%m")


@router.get("", response_model=DashboardResponse)
async def get_dashboard(
    year_month: str | None = None,
    db: Session = Depends(get_db),
) -> DashboardResponse:
    """Get dashboard data for a specific month."""
    if year_month is None:
        year_month = get_current_year_month()

    budget_service = BudgetService(db)

    # Get income data
    income_record = budget_service.get_monthly_income(year_month)
    income_data = None
    if income_record:
        income_data = IncomeData(
            amount=income_record.amount,
            description=income_record.description,
        )

    # Get fixed expenses data
    fixed_expenses_list = budget_service.list_fixed_expenses(active_only=True)
    fixed_expense_items = [
        FixedExpenseItem(
            id=expense.id,
            name=expense.name,
            amount=expense.amount,
            category=expense.category,
        )
        for expense in fixed_expenses_list
    ]
    fixed_expenses_total = budget_service.get_total_fixed_expenses()
    fixed_expenses_data = FixedExpensesData(
        items=fixed_expense_items,
        total=fixed_expenses_total,
    )

    # Get savings data
    savings_record = budget_service.get_savings_plan(year_month)
    savings_data = None
    if savings_record:
        progress = 0.0
        if savings_record.target_amount > 0:
            progress = (savings_record.actual_amount / savings_record.target_amount) * 100
        savings_data = SavingsData(
            target=savings_record.target_amount,
            actual=savings_record.actual_amount,
            progress_percentage=round(progress, 1),
        )

    # Get budget status
    budget_status_dict = budget_service.get_budget_status(year_month)
    budget_status = BudgetStatus(**budget_status_dict)

    # Get category analysis
    category_analysis_list = budget_service.get_category_analysis(year_month)
    category_analysis = [
        CategoryAnalysis(**cat) for cat in category_analysis_list
    ]

    return DashboardResponse(
        year_month=year_month,
        income=income_data,
        fixed_expenses=fixed_expenses_data,
        savings=savings_data,
        budget_status=budget_status,
        category_analysis=category_analysis,
    )
