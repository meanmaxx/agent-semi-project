# Frontend - React + TypeScript + Vite

## 개요
vLLM 에이전트와 상호작용하는 채팅 인터페이스입니다.

## 기술 스택
- React 18+
- TypeScript 5+
- Vite
- Zustand (상태관리)
- TailwindCSS (스타일링)

## 디렉토리 구조
```
src/
├── components/       # UI 컴포넌트
│   ├── chat/        # 채팅 관련 컴포넌트
│   ├── common/      # 공통 컴포넌트 (Button, Input 등)
│   └── layout/      # 레이아웃 컴포넌트 (Header, Sidebar 등)
├── hooks/           # 커스텀 훅
├── services/        # API 통신 레이어
├── stores/          # Zustand 스토어
├── types/           # TypeScript 타입 정의
└── utils/           # 유틸리티 함수
```

## 컴포넌트 패턴

### 컴포넌트 구조
```tsx
// components/chat/ChatMessage.tsx
import { memo } from 'react';
import type { Message } from '@/types';

interface ChatMessageProps {
  message: Message;
  isLoading?: boolean;
}

export const ChatMessage = memo(function ChatMessage({
  message,
  isLoading = false,
}: ChatMessageProps) {
  return (
    <div className="chat-message">
      {/* ... */}
    </div>
  );
});
```

### 훅 패턴
```tsx
// hooks/useChat.ts
export function useChat() {
  const { messages, addMessage } = useChatStore();

  const sendMessage = useCallback(async (content: string) => {
    // API 호출 로직
  }, []);

  return { messages, sendMessage };
}
```

## 상태관리 (Zustand)

### 스토어 정의
```tsx
// stores/chatStore.ts
import { create } from 'zustand';

interface ChatState {
  messages: Message[];
  isLoading: boolean;
  addMessage: (message: Message) => void;
  setLoading: (loading: boolean) => void;
}

export const useChatStore = create<ChatState>((set) => ({
  messages: [],
  isLoading: false,
  addMessage: (message) =>
    set((state) => ({ messages: [...state.messages, message] })),
  setLoading: (loading) => set({ isLoading: loading }),
}));
```

## API 통신

### 서비스 레이어
```tsx
// services/api.ts
const API_BASE_URL = import.meta.env.VITE_API_URL;

export const chatApi = {
  sendMessage: async (content: string): Promise<Response> => {
    return fetch(`${API_BASE_URL}/api/v1/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content }),
    });
  },
};
```

### 스트리밍 응답 처리
```tsx
// services/stream.ts
export async function* streamChat(content: string) {
  const response = await chatApi.sendMessage(content);
  const reader = response.body?.getReader();

  while (reader) {
    const { done, value } = await reader.read();
    if (done) break;
    yield new TextDecoder().decode(value);
  }
}
```

## 코딩 규칙

### Import 순서
1. React/외부 라이브러리
2. 내부 컴포넌트
3. 훅/유틸리티
4. 타입
5. 스타일

### 명명 규칙
- 컴포넌트: PascalCase (`ChatMessage.tsx`)
- 훅: camelCase with `use` prefix (`useChat.ts`)
- 유틸리티: camelCase (`formatDate.ts`)
- 타입: PascalCase (`Message`, `ChatState`)

### 타입 정의
```tsx
// types/chat.ts
export interface Message {
  id: string;
  role: 'user' | 'assistant' | 'tool';
  content: string;
  toolCalls?: ToolCall[];
  timestamp: Date;
}

export interface ToolCall {
  id: string;
  name: string;
  arguments: Record<string, unknown>;
  result?: string;
}
```

## 실행 방법
```bash
npm install
npm run dev      # 개발 서버
npm run build    # 프로덕션 빌드
npm run preview  # 빌드 미리보기
```
