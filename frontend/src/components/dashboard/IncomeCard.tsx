import { memo } from 'react';
import type { IncomeData } from '@/types/dashboard';

interface IncomeCardProps {
  income: IncomeData | null;
}

function formatCurrency(amount: number): string {
  return new Intl.NumberFormat('ko-KR', {
    style: 'currency',
    currency: 'KRW',
    maximumFractionDigits: 0,
  }).format(amount);
}

export const IncomeCard = memo(function IncomeCard({ income }: IncomeCardProps) {
  return (
    <div className="bg-white rounded-xl shadow-sm p-5 border border-gray-100">
      <div className="flex items-center gap-3 mb-3">
        <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
          <svg
            className="w-5 h-5 text-green-600"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
        </div>
        <h3 className="text-sm font-medium text-gray-500">월 수입</h3>
      </div>
      {income ? (
        <>
          <p className="text-2xl font-bold text-gray-800">
            {formatCurrency(income.amount)}
          </p>
          {income.description && (
            <p className="text-xs text-gray-400 mt-1">{income.description}</p>
          )}
        </>
      ) : (
        <p className="text-lg text-gray-400">설정되지 않음</p>
      )}
    </div>
  );
});
