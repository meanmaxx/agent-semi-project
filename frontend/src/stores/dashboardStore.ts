import { create } from 'zustand';
import type { DashboardData } from '@/types/dashboard';

function getCurrentYearMonth(): string {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  return `${year}-${month}`;
}

interface DashboardState {
  data: DashboardData | null;
  selectedMonth: string;
  isLoading: boolean;
  error: string | null;
  refreshCounter: number;

  setData: (data: DashboardData | null) => void;
  setSelectedMonth: (month: string) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  triggerRefresh: () => void;
}

export const useDashboardStore = create<DashboardState>((set) => ({
  data: null,
  selectedMonth: getCurrentYearMonth(),
  isLoading: false,
  error: null,
  refreshCounter: 0,

  setData: (data) => set({ data }),

  setSelectedMonth: (month) => set({ selectedMonth: month }),

  setLoading: (loading) => set({ isLoading: loading }),

  setError: (error) => set({ error }),

  triggerRefresh: () =>
    set((state) => ({ refreshCounter: state.refreshCounter + 1 })),
}));
