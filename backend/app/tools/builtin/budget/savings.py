"""Savings-related tools."""

from typing import Any

from app.db.database import SessionLocal
from app.services.budget_service import BudgetService
from app.tools.base import BaseTool, ToolParameter


class SetSavingsPlanTool(BaseTool):
    """Tool for setting savings plan."""

    @property
    def name(self) -> str:
        return "set_savings_plan"

    @property
    def description(self) -> str:
        return "월별 저축 목표를 설정합니다."

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
                name="target_amount",
                type="number",
                description="저축 목표 금액 (원)",
                required=True,
            ),
        ]

    async def execute(
        self,
        year_month: str,
        target_amount: float,
        **kwargs: Any,
    ) -> str:
        db = SessionLocal()
        try:
            service = BudgetService(db)
            plan = service.set_savings_plan(year_month, target_amount)
            return (
                f"{year_month}의 저축 목표가 ₩{plan.target_amount:,.0f}으로 설정되었습니다. "
                f"(현재 저축액: ₩{plan.actual_amount:,.0f})"
            )
        finally:
            db.close()


class UpdateSavingsTool(BaseTool):
    """Tool for updating actual savings."""

    @property
    def name(self) -> str:
        return "update_savings"

    @property
    def description(self) -> str:
        return "실제 저축액을 업데이트합니다."

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
                description="실제 저축 금액 (원)",
                required=True,
            ),
        ]

    async def execute(
        self,
        year_month: str,
        amount: float,
        **kwargs: Any,
    ) -> str:
        db = SessionLocal()
        try:
            service = BudgetService(db)
            plan = service.update_savings(year_month, amount)

            if plan:
                progress = (
                    (plan.actual_amount / plan.target_amount * 100)
                    if plan.target_amount > 0
                    else 0
                )
                return (
                    f"{year_month}의 저축액이 ₩{plan.actual_amount:,.0f}으로 업데이트되었습니다. "
                    f"(목표: ₩{plan.target_amount:,.0f}, 달성률: {progress:.1f}%)"
                )
            return (
                f"{year_month}에 저축 계획이 없습니다. "
                f"먼저 set_savings_plan으로 저축 목표를 설정해주세요."
            )
        finally:
            db.close()
