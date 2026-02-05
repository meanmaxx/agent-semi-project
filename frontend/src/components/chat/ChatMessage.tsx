import { memo } from 'react';
import type { Message } from '@/types/chat';

interface ChatMessageProps {
  message: Message;
}

export const ChatMessage = memo(function ChatMessage({
  message,
}: ChatMessageProps) {
  const isUser = message.role === 'user';

  return (
    <div
      className={`flex w-full mb-4 ${isUser ? 'justify-end' : 'justify-start'}`}
    >
      <div
        className={`max-w-[80%] rounded-2xl px-4 py-3 ${
          isUser
            ? 'bg-blue-500 text-white rounded-br-md'
            : 'bg-white text-gray-800 shadow-sm rounded-bl-md'
        }`}
      >
        {!isUser && (
          <div className="text-xs text-gray-500 mb-1 font-medium">
            가계부 도우미
          </div>
        )}
        <div className="message-content text-sm leading-relaxed whitespace-pre-wrap">
          {message.content}
        </div>
        <div
          className={`text-xs mt-1 ${
            isUser ? 'text-blue-100' : 'text-gray-400'
          }`}
        >
          {message.timestamp.toLocaleTimeString('ko-KR', {
            hour: '2-digit',
            minute: '2-digit',
          })}
        </div>
      </div>
    </div>
  );
});
