import { memo } from 'react';
import type { FixedExpensesData } from '@/types/dashboard';

interface FixedExpenseCardProps {
  fixedExpenses: FixedExpensesData;
}

function formatCurrency(amount: number): string {
  return new Intl.NumberFormat('ko-KR', {
    style: 'currency',
    currency: 'KRW',
    maximumFractionDigits: 0,
  }).format(amount);
}

export const FixedExpenseCard = memo(function FixedExpenseCard({
  fixedExpenses,
}: FixedExpenseCardProps) {
  return (
    <div className="bg-white rounded-xl shadow-sm p-5 border border-gray-100">
      <div className="flex items-center gap-3 mb-3">
        <div className="w-10 h-10 bg-red-100 rounded-lg flex items-center justify-center">
          <svg
            className="w-5 h-5 text-red-600"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
            />
          </svg>
        </div>
        <h3 className="text-sm font-medium text-gray-500">고정지출</h3>
      </div>
      <p className="text-2xl font-bold text-gray-800 mb-3">
        {formatCurrency(fixedExpenses.total)}
      </p>
      {fixedExpenses.items.length > 0 ? (
        <ul className="space-y-2 max-h-32 overflow-y-auto">
          {fixedExpenses.items.map((item) => (
            <li
              key={item.id}
              className="flex justify-between items-center text-sm"
            >
              <span className="text-gray-600">
                {item.name}
                {item.category && (
                  <span className="text-xs text-gray-400 ml-1">
                    ({item.category})
                  </span>
                )}
              </span>
              <span className="text-gray-800 font-medium">
                {formatCurrency(item.amount)}
              </span>
            </li>
          ))}
        </ul>
      ) : (
        <p className="text-sm text-gray-400">등록된 고정지출이 없습니다</p>
      )}
    </div>
  );
});
