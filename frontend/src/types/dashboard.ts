export interface IncomeData {
  amount: number;
  description: string | null;
}

export interface FixedExpenseItem {
  id: number;
  name: string;
  amount: number;
  category: string | null;
}

export interface FixedExpensesData {
  items: FixedExpenseItem[];
  total: number;
}

export interface SavingsData {
  target: number;
  actual: number;
  progress_percentage: number;
}

export interface BudgetStatus {
  year_month: string;
  total_income: number;
  total_expenses: number;
  remaining: number;
  savings_progress: number;
  status: 'good' | 'warning' | 'over_budget';
}

export interface CategoryAnalysis {
  category: string;
  total_amount: number;
  count: number;
  percentage: number;
}

export interface DashboardData {
  year_month: string;
  income: IncomeData | null;
  fixed_expenses: FixedExpensesData;
  savings: SavingsData | null;
  budget_status: BudgetStatus;
  category_analysis: CategoryAnalysis[];
}
