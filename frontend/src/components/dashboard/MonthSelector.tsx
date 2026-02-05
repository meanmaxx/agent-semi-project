import { memo } from 'react';

interface MonthSelectorProps {
  selectedMonth: string;
  onMonthChange: (month: string) => void;
}

export const MonthSelector = memo(function MonthSelector({
  selectedMonth,
  onMonthChange,
}: MonthSelectorProps) {
  const handlePrevMonth = () => {
    const [year, month] = selectedMonth.split('-').map(Number);
    const date = new Date(year, month - 2, 1);
    const newMonth = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
    onMonthChange(newMonth);
  };

  const handleNextMonth = () => {
    const [year, month] = selectedMonth.split('-').map(Number);
    const date = new Date(year, month, 1);
    const newMonth = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
    onMonthChange(newMonth);
  };

  const formatDisplay = (yearMonth: string) => {
    const [year, month] = yearMonth.split('-');
    return `${year}년 ${parseInt(month)}월`;
  };

  return (
    <div className="flex items-center justify-center gap-4 mb-6">
      <button
        onClick={handlePrevMonth}
        className="p-2 hover:bg-gray-200 rounded-full transition-colors"
        aria-label="이전 달"
      >
        <svg
          className="w-5 h-5 text-gray-600"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M15 19l-7-7 7-7"
          />
        </svg>
      </button>
      <h2 className="text-xl font-semibold text-gray-800 min-w-[140px] text-center">
        {formatDisplay(selectedMonth)}
      </h2>
      <button
        onClick={handleNextMonth}
        className="p-2 hover:bg-gray-200 rounded-full transition-colors"
        aria-label="다음 달"
      >
        <svg
          className="w-5 h-5 text-gray-600"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M9 5l7 7-7 7"
          />
        </svg>
      </button>
    </div>
  );
});
