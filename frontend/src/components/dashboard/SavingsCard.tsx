import { memo } from 'react';
import type { SavingsData } from '@/types/dashboard';

interface SavingsCardProps {
  savings: SavingsData | null;
}

function formatCurrency(amount: number): string {
  return new Intl.NumberFormat('ko-KR', {
    style: 'currency',
    currency: 'KRW',
    maximumFractionDigits: 0,
  }).format(amount);
}

export const SavingsCard = memo(function SavingsCard({
  savings,
}: SavingsCardProps) {
  const progress = savings?.progress_percentage ?? 0;
  const progressColor =
    progress >= 100 ? 'bg-green-500' : progress >= 50 ? 'bg-blue-500' : 'bg-amber-500';

  return (
    <div className="bg-white rounded-xl shadow-sm p-5 border border-gray-100">
      <div className="flex items-center gap-3 mb-3">
        <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
          <svg
            className="w-5 h-5 text-blue-600"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z"
            />
          </svg>
        </div>
        <h3 className="text-sm font-medium text-gray-500">저축 현황</h3>
      </div>
      {savings ? (
        <>
          <div className="flex justify-between items-baseline mb-2">
            <p className="text-2xl font-bold text-gray-800">
              {formatCurrency(savings.actual)}
            </p>
            <p className="text-sm text-gray-500">
              목표: {formatCurrency(savings.target)}
            </p>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
            <div
              className={`h-full rounded-full transition-all duration-500 ${progressColor}`}
              style={{ width: `${Math.min(progress, 100)}%` }}
            />
          </div>
          <p className="text-xs text-gray-500 mt-2 text-right">
            {progress.toFixed(1)}% 달성
          </p>
        </>
      ) : (
        <p className="text-lg text-gray-400">저축 목표 미설정</p>
      )}
    </div>
  );
});
