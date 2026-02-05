import type { ChatRequest, ChatResponse } from '@/types/chat';
import type { DashboardData } from '@/types/dashboard';

const API_BASE_URL = import.meta.env.VITE_API_URL || '';

export const chatApi = {
  sendMessage: async (
    content: string,
    conversationId?: string
  ): Promise<ChatResponse> => {
    const request: ChatRequest = {
      content,
      conversation_id: conversationId,
    };

    const response = await fetch(`${API_BASE_URL}/api/v1/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  },

  resetChat: async (conversationId?: string): Promise<void> => {
    await fetch(`${API_BASE_URL}/api/v1/chat/reset`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ conversation_id: conversationId }),
    });
  },

  healthCheck: async (): Promise<boolean> => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/health`);
      return response.ok;
    } catch {
      return false;
    }
  },
};

export const dashboardApi = {
  getDashboard: async (yearMonth?: string): Promise<DashboardData> => {
    const params = yearMonth ? `?year_month=${yearMonth}` : '';
    const response = await fetch(`${API_BASE_URL}/api/v1/dashboard${params}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  },
};
