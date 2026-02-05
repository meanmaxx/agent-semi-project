export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export interface ChatRequest {
  content: string;
  conversation_id?: string;
}

export interface ChatResponse {
  content: string;
  conversation_id?: string;
}
