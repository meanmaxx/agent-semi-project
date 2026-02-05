"""Budget-related Pydantic schemas."""

from pydantic import BaseModel


class MonthlyIncomeCreate(BaseModel):
    """Schema for creating monthly income."""

    year_month: str
    amount: float
    description: str | None = None


class MonthlyIncomeResponse(BaseModel):
    """Schema for monthly income response."""

    id: int
    year_month: str
    amount: float
    description: str | None

    class Config:
        from_attributes = True


class FixedExpenseCreate(BaseModel):
    """Schema for creating fixed expense."""

    name: str
    amount: float
    category: str | None = None


class FixedExpenseResponse(BaseModel):
    """Schema for fixed expense response."""

    id: int
    name: str
    amount: float
    category: str | None
    is_active: bool

    class Config:
        from_attributes = True


class SavingsPlanCreate(BaseModel):
    """Schema for creating savings plan."""

    year_month: str
    target_amount: float


class SavingsPlanResponse(BaseModel):
    """Schema for savings plan response."""

    id: int
    year_month: str
    target_amount: float
    actual_amount: float

    class Config:
        from_attributes = True


class DailyExpenseCreate(BaseModel):
    """Schema for creating daily expense."""

    date: str
    amount: float
    category: str
    description: str | None = None


class DailyExpenseResponse(BaseModel):
    """Schema for daily expense response."""

    id: int
    date: str
    amount: float
    category: str
    description: str | None

    class Config:
        from_attributes = True


class MonthlySummary(BaseModel):
    """Schema for monthly summary."""

    year_month: str
    total_income: float
    total_fixed_expenses: float
    total_daily_expenses: float
    savings_target: float
    savings_actual: float
    remaining_budget: float


class CategoryAnalysis(BaseModel):
    """Schema for category analysis."""

    category: str
    total_amount: float
    count: int
    percentage: float


class BudgetStatus(BaseModel):
    """Schema for budget status."""

    year_month: str
    total_income: float
    total_expenses: float
    remaining: float
    savings_progress: float
    status: str  # "good", "warning", "over_budget"


# ============ Dashboard Schemas ============


class IncomeData(BaseModel):
    """Schema for income data in dashboard."""

    amount: float
    description: str | None


class FixedExpenseItem(BaseModel):
    """Schema for fixed expense item in dashboard."""

    id: int
    name: str
    amount: float
    category: str | None


class FixedExpensesData(BaseModel):
    """Schema for fixed expenses data in dashboard."""

    items: list[FixedExpenseItem]
    total: float


class SavingsData(BaseModel):
    """Schema for savings data in dashboard."""

    target: float
    actual: float
    progress_percentage: float


class DashboardResponse(BaseModel):
    """Schema for dashboard API response."""

    year_month: str
    income: IncomeData | None
    fixed_expenses: FixedExpensesData
    savings: SavingsData | None
    budget_status: BudgetStatus
    category_analysis: list[CategoryAnalysis]
