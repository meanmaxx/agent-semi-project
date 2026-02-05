import { create } from 'zustand';
import type { Message } from '@/types/chat';

interface ChatState {
  messages: Message[];
  conversationId: string | null;
  isLoading: boolean;
  error: string | null;
  addMessage: (message: Message) => void;
  setConversationId: (id: string | null) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  clearMessages: () => void;
}

export const useChatStore = create<ChatState>((set) => ({
  messages: [],
  conversationId: null,
  isLoading: false,
  error: null,

  addMessage: (message) =>
    set((state) => ({
      messages: [...state.messages, message],
    })),

  setConversationId: (id) =>
    set({ conversationId: id }),

  setLoading: (loading) =>
    set({ isLoading: loading }),

  setError: (error) =>
    set({ error }),

  clearMessages: () =>
    set({ messages: [], conversationId: null, error: null }),
}));
