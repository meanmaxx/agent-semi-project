"""Analysis tools."""

from typing import Any

from app.db.database import SessionLocal
from app.services.budget_service import BudgetService
from app.tools.base import BaseTool, ToolParameter


class GetMonthlySummaryTool(BaseTool):
    """Tool for getting monthly summary."""

    @property
    def name(self) -> str:
        return "get_monthly_summary"

    @property
    def description(self) -> str:
        return "월별 수입/지출/저축 요약을 보여줍니다."

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
            summary = service.get_monthly_summary(year_month)

            lines = [
                f"📊 {year_month} 월간 요약",
                "=" * 30,
                f"💰 총 수입: ₩{summary['total_income']:,.0f}",
                "",
                "📤 지출 내역:",
                f"  - 고정지출: ₩{summary['total_fixed_expenses']:,.0f}",
                f"  - 변동지출: ₩{summary['total_daily_expenses']:,.0f}",
                f"  - 총 지출: ₩{summary['total_expenses']:,.0f}",
                "",
                "💎 저축:",
                f"  - 목표: ₩{summary['savings_target']:,.0f}",
                f"  - 실제: ₩{summary['savings_actual']:,.0f}",
                "",
                "=" * 30,
                f"💵 남은 예산: ₩{summary['remaining_budget']:,.0f}",
            ]

            return "\n".join(lines)
        finally:
            db.close()


class GetCategoryAnalysisTool(BaseTool):
    """Tool for category analysis."""

    @property
    def name(self) -> str:
        return "get_category_analysis"

    @property
    def description(self) -> str:
        return "카테고리별 지출 분석을 제공합니다."

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
            analysis = service.get_category_analysis(year_month)

            if not analysis:
                return f"{year_month}에 기록된 지출이 없습니다."

            lines = [
                f"📈 {year_month} 카테고리별 지출 분석",
                "=" * 35,
            ]

            total = sum(item["total_amount"] for item in analysis)

            for item in analysis:
                bar_length = int(item["percentage"] / 5)  # Max 20 chars for 100%
                bar = "█" * bar_length
                lines.append(
                    f"{item['category']}: ₩{item['total_amount']:,.0f} ({item['count']}건)"
                )
                lines.append(f"  {bar} {item['percentage']}%")

            lines.append("=" * 35)
            lines.append(f"총 지출: ₩{total:,.0f}")

            return "\n".join(lines)
        finally:
            db.close()


class GetBudgetStatusTool(BaseTool):
    """Tool for budget status."""

    @property
    def name(self) -> str:
        return "get_budget_status"

    @property
    def description(self) -> str:
        return "예산 대비 현황을 확인합니다."

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
            status = service.get_budget_status(year_month)

            status_emoji = {
                "good": "✅",
                "warning": "⚠️",
                "over_budget": "🚨",
            }

            status_text = {
                "good": "양호",
                "warning": "주의 필요",
                "over_budget": "예산 초과",
            }

            emoji = status_emoji.get(status["status"], "❓")
            text = status_text.get(status["status"], "알 수 없음")

            lines = [
                f"💰 {year_month} 예산 현황 {emoji}",
                "=" * 30,
                f"수입: ₩{status['total_income']:,.0f}",
                f"지출: ₩{status['total_expenses']:,.0f}",
                f"남은 금액: ₩{status['remaining']:,.0f}",
                "",
                f"저축 달성률: {status['savings_progress']:.1f}%",
                "",
                f"상태: {text}",
            ]

            # Add recommendations based on status
            if status["status"] == "over_budget":
                lines.append("\n💡 추천: 지출을 줄이거나 저축 목표를 조정해보세요.")
            elif status["status"] == "warning":
                lines.append("\n💡 추천: 남은 예산이 적습니다. 지출에 주의하세요.")

            return "\n".join(lines)
        finally:
            db.close()
