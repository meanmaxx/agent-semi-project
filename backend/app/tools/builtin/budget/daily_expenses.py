"""Daily expenses tools."""

from typing import Any

from app.db.database import SessionLocal
from app.services.budget_service import BudgetService
from app.tools.base import BaseTool, ToolParameter


class AddDailyExpenseTool(BaseTool):
    """Tool for adding daily expense."""

    @property
    def name(self) -> str:
        return "add_daily_expense"

    @property
    def description(self) -> str:
        return "일별 지출을 기록합니다."

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter(
                name="date",
                type="string",
                description="날짜 (형식: YYYY-MM-DD, 예: 2024-01-15)",
                required=True,
            ),
            ToolParameter(
                name="amount",
                type="number",
                description="지출 금액 (원)",
                required=True,
            ),
            ToolParameter(
                name="category",
                type="string",
                description="카테고리 (예: 식비, 교통, 쇼핑, 문화/여가, 의료, 교육, 기타)",
                required=True,
            ),
            ToolParameter(
                name="description",
                type="string",
                description="지출 내용 설명 (선택사항)",
                required=False,
            ),
        ]

    async def execute(
        self,
        date: str,
        amount: float,
        category: str,
        description: str | None = None,
        **kwargs: Any,
    ) -> str:
        db = SessionLocal()
        try:
            service = BudgetService(db)
            expense = service.add_daily_expense(date, amount, category, description)
            result = f"{date}에 {category} ₩{expense.amount:,.0f} 지출이 기록되었습니다."
            if expense.description:
                result += f" (내용: {expense.description})"
            return result
        finally:
            db.close()


class GetExpensesByDateTool(BaseTool):
    """Tool for getting expenses by date."""

    @property
    def name(self) -> str:
        return "get_expenses_by_date"

    @property
    def description(self) -> str:
        return "특정 날짜의 모든 지출을 조회합니다."

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter(
                name="date",
                type="string",
                description="날짜 (형식: YYYY-MM-DD, 예: 2024-01-15)",
                required=True,
            ),
        ]

    async def execute(self, date: str, **kwargs: Any) -> str:
        db = SessionLocal()
        try:
            service = BudgetService(db)
            expenses = service.get_expenses_by_date(date)

            if not expenses:
                return f"{date}에 기록된 지출이 없습니다."

            total = sum(e.amount for e in expenses)
            lines = [f"📅 {date} 지출 내역:"]

            for e in expenses:
                line = f"  - {e.category}: ₩{e.amount:,.0f}"
                if e.description:
                    line += f" ({e.description})"
                lines.append(line)

            lines.append(f"\n총 지출: ₩{total:,.0f}")
            return "\n".join(lines)
        finally:
            db.close()


class GetExpensesByPeriodTool(BaseTool):
    """Tool for getting expenses by period."""

    @property
    def name(self) -> str:
        return "get_expenses_by_period"

    @property
    def description(self) -> str:
        return "특정 기간의 지출을 조회합니다."

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter(
                name="start_date",
                type="string",
                description="시작 날짜 (형식: YYYY-MM-DD)",
                required=True,
            ),
            ToolParameter(
                name="end_date",
                type="string",
                description="종료 날짜 (형식: YYYY-MM-DD)",
                required=True,
            ),
        ]

    async def execute(
        self,
        start_date: str,
        end_date: str,
        **kwargs: Any,
    ) -> str:
        db = SessionLocal()
        try:
            service = BudgetService(db)
            expenses = service.get_expenses_by_period(start_date, end_date)

            if not expenses:
                return f"{start_date} ~ {end_date} 기간에 기록된 지출이 없습니다."

            total = sum(e.amount for e in expenses)
            lines = [f"📅 {start_date} ~ {end_date} 지출 내역:"]

            # Group by date
            current_date = None
            for e in expenses:
                if e.date != current_date:
                    current_date = e.date
                    lines.append(f"\n[{current_date}]")

                line = f"  - {e.category}: ₩{e.amount:,.0f}"
                if e.description:
                    line += f" ({e.description})"
                lines.append(line)

            lines.append(f"\n총 지출: ₩{total:,.0f} ({len(expenses)}건)")
            return "\n".join(lines)
        finally:
            db.close()
