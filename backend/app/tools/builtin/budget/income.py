"""Income-related tools."""

from typing import Any

from app.db.database import SessionLocal
from app.services.budget_service import BudgetService
from app.tools.base import BaseTool, ToolParameter


class SetMonthlyIncomeTool(BaseTool):
    """Tool for setting monthly income."""

    @property
    def name(self) -> str:
        return "set_monthly_income"

    @property
    def description(self) -> str:
        return "월 수입을 설정합니다. 이미 해당 월의 수입이 있으면 업데이트합니다."

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter(
                name="year_month",
                type="string",
                description="년월 (형식: YYYY-MM, 예: 2024-01)",
                required=True,
            ),
            ToolParameter(
                name="amount",
                type="number",
                description="월 수입 금액 (원)",
                required=True,
            ),
            ToolParameter(
                name="description",
                type="string",
                description="수입에 대한 설명 (선택사항)",
                required=False,
            ),
        ]

    async def execute(
        self,
        year_month: str,
        amount: float,
        description: str | None = None,
        **kwargs: Any,
    ) -> str:
        db = SessionLocal()
        try:
            service = BudgetService(db)
            income = service.set_monthly_income(year_month, amount, description)
            return (
                f"{year_month}의 월 수입이 ₩{income.amount:,.0f}으로 설정되었습니다."
                + (f" (설명: {income.description})" if income.description else "")
            )
        finally:
            db.close()


class GetMonthlyIncomeTool(BaseTool):
    """Tool for getting monthly income."""

    @property
    def name(self) -> str:
        return "get_monthly_income"

    @property
    def description(self) -> str:
        return "특정 월의 수입을 조회합니다."

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter(
                name="year_month",
                type="string",
                description="년월 (형식: YYYY-MM, 예: 2024-01)",
                required=True,
            ),
        ]

    async def execute(self, year_month: str, **kwargs: Any) -> str:
        db = SessionLocal()
        try:
            service = BudgetService(db)
            income = service.get_monthly_income(year_month)
            if income:
                result = f"{year_month}의 월 수입: ₩{income.amount:,.0f}"
                if income.description:
                    result += f" (설명: {income.description})"
                return result
            return f"{year_month}에 등록된 수입이 없습니다."
        finally:
            db.close()
