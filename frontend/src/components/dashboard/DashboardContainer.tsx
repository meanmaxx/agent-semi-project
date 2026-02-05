import { useEffect, useCallback } from 'react';
import { useDashboardStore } from '@/stores/dashboardStore';
import { dashboardApi } from '@/services/api';
import { MonthSelector } from './MonthSelector';
import { IncomeCard } from './IncomeCard';
import { FixedExpenseCard } from './FixedExpenseCard';
import { SavingsCard } from './SavingsCard';
import { BudgetStatusCard } from './BudgetStatusCard';
import { CategoryBreakdown } from './CategoryBreakdown';

export function DashboardContainer() {
  const {
    data,
    selectedMonth,
    isLoading,
    error,
    refreshCounter,
    setData,
    setSelectedMonth,
    setLoading,
    setError,
  } = useDashboardStore();

  const fetchDashboard = useCallback(async (yearMonth: string) => {
    setLoading(true);
    setError(null);
    try {
      const dashboardData = await dashboardApi.getDashboard(yearMonth);
      setData(dashboardData);
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Failed to load dashboard';
      setError(errorMsg);
    } finally {
      setLoading(false);
    }
  }, [setLoading, setError, setData]);

  useEffect(() => {
    fetchDashboard(selectedMonth);
  }, [selectedMonth, refreshCounter, fetchDashboard]);

  const handleMonthChange = (month: string) => {
    setSelectedMonth(month);
  };

  if (isLoading && !data) {
    return (
      <div className="p-6 h-full flex items-center justify-center">
        <div className="flex flex-col items-center gap-3">
          <div className="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin" />
          <p className="text-sm text-gray-500">불러오는 중...</p>
        </div>
      </div>
    );
  }

  if (error && !data) {
    return (
      <div className="p-6 h-full flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-500 mb-2">{error}</p>
          <button
            onClick={() => fetchDashboard(selectedMonth)}
            className="text-sm text-blue-500 hover:underline"
          >
            다시 시도
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 h-full overflow-y-auto">
      <div className="max-w-4xl mx-auto">
        <header className="mb-6">
          <h1 className="text-2xl font-bold text-gray-800 text-center mb-4">
            가계부 대시보드
          </h1>
          <MonthSelector
            selectedMonth={selectedMonth}
            onMonthChange={handleMonthChange}
          />
        </header>

        {isLoading && (
          <div className="flex justify-center mb-4">
            <span className="text-sm text-gray-400">갱신 중...</span>
          </div>
        )}

        {data && (
          <div className="space-y-6">
            {/* Top row: Income, Fixed Expenses, Savings */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <IncomeCard income={data.income} />
              <FixedExpenseCard fixedExpenses={data.fixed_expenses} />
              <SavingsCard savings={data.savings} />
            </div>

            {/* Budget status */}
            <BudgetStatusCard budgetStatus={data.budget_status} />

            {/* Category breakdown */}
            <CategoryBreakdown categories={data.category_analysis} />
          </div>
        )}
      </div>
    </div>
  );
}
