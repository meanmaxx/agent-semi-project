"""Fixed expenses tools."""

from typing import Any

from app.db.database import SessionLocal
from app.services.budget_service import BudgetService
from app.tools.base import BaseTool, ToolParameter


class AddFixedExpenseTool(BaseTool):
    """Tool for adding fixed expense."""

    @property
    def name(self) -> str:
        return "add_fixed_expense"

    @property
    def description(self) -> str:
        return "고정지출을 추가합니다 (예: 월세, 통신비, 보험료, 구독료 등)."

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter(
                name="name",
                type="string",
                description="고정지출 이름 (예: 월세, 통신비, 넷플릭스)",
                required=True,
            ),
            ToolParameter(
                name="amount",
                type="number",
                description="금액 (원)",
                required=True,
            ),
            ToolParameter(
                name="category",
                type="string",
                description="카테고리 (예: 주거, 통신, 보험, 구독, 교통, 기타)",
                required=False,
            ),
        ]

    async def execute(
        self,
        name: str,
        amount: float,
        category: str | None = None,
        **kwargs: Any,
    ) -> str:
        db = SessionLocal()
        try:
            service = BudgetService(db)
            expense = service.add_fixed_expense(name, amount, category)
            result = f"고정지출 '{expense.name}'이(가) ₩{expense.amount:,.0f}으로 추가되었습니다."
            if expense.category:
                result += f" (카테고리: {expense.category})"
            result += f" [ID: {expense.id}]"
            return result
        finally:
            db.close()


class ListFixedExpensesTool(BaseTool):
    """Tool for listing fixed expenses."""

    @property
    def name(self) -> str:
        return "list_fixed_expenses"

    @property
    def description(self) -> str:
        return "모든 고정지출 목록을 조회합니다."

    @property
    def parameters(self) -> list[ToolParameter]:
        return []

    async def execute(self, **kwargs: Any) -> str:
        db = SessionLocal()
        try:
            service = BudgetService(db)
            expenses = service.list_fixed_expenses()

            if not expenses:
                return "등록된 고정지출이 없습니다."

            total = sum(e.amount for e in expenses)
            lines = ["📋 고정지출 목록:"]

            for e in expenses:
                line = f"  - [{e.id}] {e.name}: ₩{e.amount:,.0f}"
                if e.category:
                    line += f" ({e.category})"
                lines.append(line)

            lines.append(f"\n총 고정지출: ₩{total:,.0f}")
            return "\n".join(lines)
        finally:
            db.close()


class RemoveFixedExpenseTool(BaseTool):
    """Tool for removing fixed expense."""

    @property
    def name(self) -> str:
        return "remove_fixed_expense"

    @property
    def description(self) -> str:
        return "고정지출을 삭제합니다. list_fixed_expenses로 조회한 ID를 사용하세요."

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter(
                name="expense_id",
                type="integer",
                description="삭제할 고정지출의 ID",
                required=True,
            ),
        ]

    async def execute(self, expense_id: int, **kwargs: Any) -> str:
        db = SessionLocal()
        try:
            service = BudgetService(db)
            success = service.remove_fixed_expense(expense_id)
            if success:
                return f"고정지출 ID {expense_id}이(가) 삭제되었습니다."
            return f"ID {expense_id}에 해당하는 고정지출을 찾을 수 없습니다."
        finally:
            db.close()
