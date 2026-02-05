import { memo } from 'react';
import type { CategoryAnalysis } from '@/types/dashboard';

interface CategoryBreakdownProps {
  categories: CategoryAnalysis[];
}

function formatCurrency(amount: number): string {
  return new Intl.NumberFormat('ko-KR', {
    style: 'currency',
    currency: 'KRW',
    maximumFractionDigits: 0,
  }).format(amount);
}

const CATEGORY_COLORS = [
  'bg-blue-500',
  'bg-green-500',
  'bg-amber-500',
  'bg-purple-500',
  'bg-pink-500',
  'bg-indigo-500',
  'bg-teal-500',
  'bg-orange-500',
];

export const CategoryBreakdown = memo(function CategoryBreakdown({
  categories,
}: CategoryBreakdownProps) {
  return (
    <div className="bg-white rounded-xl shadow-sm p-5 border border-gray-100">
      <div className="flex items-center gap-3 mb-4">
        <div className="w-10 h-10 bg-indigo-100 rounded-lg flex items-center justify-center">
          <svg
            className="w-5 h-5 text-indigo-600"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z"
            />
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M20.488 9H15V3.512A9.025 9.025 0 0120.488 9z"
            />
          </svg>
        </div>
        <h3 className="text-sm font-medium text-gray-500">카테고리별 지출</h3>
      </div>

      {categories.length > 0 ? (
        <div className="space-y-3">
          {categories.map((category, index) => (
            <div key={category.category} className="space-y-1">
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-700">{category.category}</span>
                <div className="flex items-center gap-2">
                  <span className="text-xs text-gray-400">
                    {category.count}건
                  </span>
                  <span className="text-sm font-medium text-gray-800">
                    {formatCurrency(category.total_amount)}
                  </span>
                </div>
              </div>
              <div className="w-full bg-gray-100 rounded-full h-2 overflow-hidden">
                <div
                  className={`h-full rounded-full transition-all duration-500 ${
                    CATEGORY_COLORS[index % CATEGORY_COLORS.length]
                  }`}
                  style={{ width: `${category.percentage}%` }}
                />
              </div>
              <p className="text-xs text-gray-400 text-right">
                {category.percentage}%
              </p>
            </div>
          ))}
        </div>
      ) : (
        <p className="text-sm text-gray-400 text-center py-4">
          지출 내역이 없습니다
        </p>
      )}
    </div>
  );
});
