"""Budget tools module."""

from app.tools.builtin.budget.analysis import (
    GetBudgetStatusTool,
    GetCategoryAnalysisTool,
    GetMonthlySummaryTool,
)
from app.tools.builtin.budget.daily_expenses import (
    AddDailyExpenseTool,
    GetExpensesByDateTool,
    GetExpensesByPeriodTool,
)
from app.tools.builtin.budget.fixed_expenses import (
    AddFixedExpenseTool,
    ListFixedExpensesTool,
    RemoveFixedExpenseTool,
)
from app.tools.builtin.budget.income import GetMonthlyIncomeTool, SetMonthlyIncomeTool
from app.tools.builtin.budget.savings import SetSavingsPlanTool, UpdateSavingsTool

__all__ = [
    # Income
    "SetMonthlyIncomeTool",
    "GetMonthlyIncomeTool",
    # Fixed Expenses
    "AddFixedExpenseTool",
    "ListFixedExpensesTool",
    "RemoveFixedExpenseTool",
    # Savings
    "SetSavingsPlanTool",
    "UpdateSavingsTool",
    # Daily Expenses
    "AddDailyExpenseTool",
    "GetExpensesByDateTool",
    "GetExpensesByPeriodTool",
    # Analysis
    "GetMonthlySummaryTool",
    "GetCategoryAnalysisTool",
    "GetBudgetStatusTool",
]


def get_all_budget_tools() -> list:
    """Get instances of all budget tools."""
    return [
        SetMonthlyIncomeTool(),
        GetMonthlyIncomeTool(),
        AddFixedExpenseTool(),
        ListFixedExpensesTool(),
        RemoveFixedExpenseTool(),
        SetSavingsPlanTool(),
        UpdateSavingsTool(),
        AddDailyExpenseTool(),
        GetExpensesByDateTool(),
        GetExpensesByPeriodTool(),
        GetMonthlySummaryTool(),
        GetCategoryAnalysisTool(),
        GetBudgetStatusTool(),
    ]
