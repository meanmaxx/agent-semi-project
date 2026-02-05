import { memo } from 'react';
import type { BudgetStatus } from '@/types/dashboard';

interface BudgetStatusCardProps {
  budgetStatus: BudgetStatus;
}

function formatCurrency(amount: number): string {
  return new Intl.NumberFormat('ko-KR', {
    style: 'currency',
    currency: 'KRW',
    maximumFractionDigits: 0,
  }).format(amount);
}

const STATUS_CONFIG = {
  good: {
    label: '양호',
    bgColor: 'bg-green-100',
    textColor: 'text-green-700',
    borderColor: 'border-green-200',
  },
  warning: {
    label: '주의',
    bgColor: 'bg-amber-100',
    textColor: 'text-amber-700',
    borderColor: 'border-amber-200',
  },
  over_budget: {
    label: '초과',
    bgColor: 'bg-red-100',
    textColor: 'text-red-700',
    borderColor: 'border-red-200',
  },
};

export const BudgetStatusCard = memo(function BudgetStatusCard({
  budgetStatus,
}: BudgetStatusCardProps) {
  const config = STATUS_CONFIG[budgetStatus.status];
  const usedPercentage =
    budgetStatus.total_income > 0
      ? (budgetStatus.total_expenses / budgetStatus.total_income) * 100
      : 0;

  return (
    <div
      className={`bg-white rounded-xl shadow-sm p-5 border ${config.borderColor}`}
    >
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
            <svg
              className="w-5 h-5 text-purple-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
              />
            </svg>
          </div>
          <h3 className="text-sm font-medium text-gray-500">예산 현황</h3>
        </div>
        <span
          className={`px-3 py-1 rounded-full text-xs font-medium ${config.bgColor} ${config.textColor}`}
        >
          {config.label}
        </span>
      </div>

      <div className="space-y-3">
        <div className="flex justify-between">
          <span className="text-sm text-gray-500">총 수입</span>
          <span className="text-sm font-medium text-gray-800">
            {formatCurrency(budgetStatus.total_income)}
          </span>
        </div>
        <div className="flex justify-between">
          <span className="text-sm text-gray-500">총 지출</span>
          <span className="text-sm font-medium text-gray-800">
            {formatCurrency(budgetStatus.total_expenses)}
          </span>
        </div>
        <div className="border-t pt-3">
          <div className="flex justify-between">
            <span className="text-sm font-medium text-gray-700">남은 예산</span>
            <span
              className={`text-lg font-bold ${
                budgetStatus.remaining >= 0 ? 'text-green-600' : 'text-red-600'
              }`}
            >
              {formatCurrency(budgetStatus.remaining)}
            </span>
          </div>
        </div>
      </div>

      <div className="mt-4">
        <div className="flex justify-between text-xs text-gray-500 mb-1">
          <span>지출 비율</span>
          <span>{usedPercentage.toFixed(1)}%</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
          <div
            className={`h-full rounded-full transition-all duration-500 ${
              usedPercentage > 100
                ? 'bg-red-500'
                : usedPercentage > 80
                ? 'bg-amber-500'
                : 'bg-green-500'
            }`}
            style={{ width: `${Math.min(usedPercentage, 100)}%` }}
          />
        </div>
      </div>
    </div>
  );
});
