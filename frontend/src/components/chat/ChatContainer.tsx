import { useCallback, useEffect, useRef } from 'react';
import { useChatStore } from '@/stores/chatStore';
import { useDashboardStore } from '@/stores/dashboardStore';
import { chatApi } from '@/services/api';
import { ChatMessage } from './ChatMessage';
import { ChatInput } from './ChatInput';
import type { Message } from '@/types/chat';

export function ChatContainer() {
  const {
    messages,
    conversationId,
    isLoading,
    error,
    addMessage,
    setConversationId,
    setLoading,
    setError,
    clearMessages,
  } = useChatStore();

  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);

  const handleSend = useCallback(
    async (content: string) => {
      // Add user message
      const userMessage: Message = {
        id: crypto.randomUUID(),
        role: 'user',
        content,
        timestamp: new Date(),
      };
      addMessage(userMessage);
      setLoading(true);
      setError(null);

      try {
        const response = await chatApi.sendMessage(content, conversationId ?? undefined);

        // Update conversation ID if new
        if (response.conversation_id && !conversationId) {
          setConversationId(response.conversation_id);
        }

        // Add assistant message
        const assistantMessage: Message = {
          id: crypto.randomUUID(),
          role: 'assistant',
          content: response.content,
          timestamp: new Date(),
        };
        addMessage(assistantMessage);

        // Trigger dashboard refresh after successful response
        useDashboardStore.getState().triggerRefresh();
      } catch (err) {
        const errorMsg = err instanceof Error ? err.message : '오류가 발생했습니다';
        setError(errorMsg);

        // Add error message as assistant response
        const errorMessage: Message = {
          id: crypto.randomUUID(),
          role: 'assistant',
          content: `오류가 발생했습니다: ${errorMsg}\n\n다시 시도해주세요.`,
          timestamp: new Date(),
        };
        addMessage(errorMessage);
      } finally {
        setLoading(false);
      }
    },
    [conversationId, addMessage, setConversationId, setLoading, setError]
  );

  const handleReset = useCallback(async () => {
    if (conversationId) {
      await chatApi.resetChat(conversationId);
    }
    clearMessages();
  }, [conversationId, clearMessages]);

  return (
    <div className="flex flex-col h-full bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b px-4 py-3 flex items-center justify-between">
        <div>
          <h1 className="text-lg font-semibold text-gray-800">가계부 챗봇</h1>
          <p className="text-xs text-gray-500">
            자연어로 가계부를 관리하세요
          </p>
        </div>
        <button
          onClick={handleReset}
          className="text-sm text-gray-500 hover:text-gray-700 px-3 py-1 rounded hover:bg-gray-100"
        >
          새 대화
        </button>
      </header>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4">
        <div className="max-w-4xl mx-auto">
          {messages.length === 0 && (
            <div className="text-center py-12">
              <div className="text-6xl mb-4">💰</div>
              <h2 className="text-xl font-semibold text-gray-700 mb-2">
                가계부 도우미입니다
              </h2>
              <p className="text-gray-500 mb-6">
                자연어로 가계부를 관리해보세요
              </p>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 max-w-2xl mx-auto text-left">
                {[
                  '이번 달 수입을 350만원으로 설정해줘',
                  '월세 80만원 고정지출로 추가해줘',
                  '오늘 점심으로 15000원 썼어',
                  '이번 달 지출 현황 보여줘',
                ].map((example, i) => (
                  <button
                    key={i}
                    onClick={() => handleSend(example)}
                    disabled={isLoading}
                    className="text-sm text-gray-600 bg-white border rounded-lg px-4 py-3
                               hover:bg-gray-50 hover:border-blue-300 transition-colors text-left
                               disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    "{example}"
                  </button>
                ))}
              </div>
            </div>
          )}

          {messages.map((message) => (
            <ChatMessage key={message.id} message={message} />
          ))}

          {isLoading && (
            <div className="flex justify-start mb-4">
              <div className="bg-white rounded-2xl rounded-bl-md px-4 py-3 shadow-sm">
                <div className="flex items-center gap-2">
                  <span className="inline-block w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                  <span
                    className="inline-block w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                    style={{ animationDelay: '0.1s' }}
                  />
                  <span
                    className="inline-block w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                    style={{ animationDelay: '0.2s' }}
                  />
                </div>
              </div>
            </div>
          )}

          {error && (
            <div className="text-center py-2">
              <span className="text-sm text-red-500">{error}</span>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input */}
      <ChatInput onSend={handleSend} disabled={isLoading} />
    </div>
  );
}
