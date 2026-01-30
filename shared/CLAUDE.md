# Shared Resources

## 개요
프론트엔드와 백엔드 간 공유되는 리소스를 관리합니다.

## 디렉토리 구조
```
shared/
└── constants/
    └── tool_definitions.json
```

## 공유 리소스

### Tool Definitions
`constants/tool_definitions.json`에 도구 정의를 저장하여 프론트엔드와 백엔드 간 동기화합니다.

```json
{
  "version": "1.0.0",
  "tools": [
    {
      "name": "calculator",
      "description": "Perform basic mathematical calculations",
      "category": "utility",
      "parameters": [
        {
          "name": "expression",
          "type": "string",
          "description": "Mathematical expression to evaluate (e.g., '2 + 2')",
          "required": true
        }
      ]
    },
    {
      "name": "web_search",
      "description": "Search the web for information",
      "category": "information",
      "parameters": [
        {
          "name": "query",
          "type": "string",
          "description": "Search query",
          "required": true
        },
        {
          "name": "num_results",
          "type": "integer",
          "description": "Number of results to return (default: 5)",
          "required": false
        }
      ]
    }
  ]
}
```

## 동기화 방법

### Backend에서 사용
```python
# backend/app/tools/loader.py
import json
from pathlib import Path

def load_tool_definitions() -> dict:
    """Load tool definitions from shared JSON file."""
    path = Path(__file__).parent.parent.parent.parent / "shared" / "constants" / "tool_definitions.json"
    with open(path) as f:
        return json.load(f)
```

### Frontend에서 사용
```typescript
// frontend/src/utils/tools.ts
import toolDefinitions from '../../../shared/constants/tool_definitions.json';

export function getToolDefinitions() {
  return toolDefinitions.tools;
}

export function getToolByName(name: string) {
  return toolDefinitions.tools.find(t => t.name === name);
}
```

### Vite 설정 (Frontend)
```typescript
// vite.config.ts
import { defineConfig } from 'vite';

export default defineConfig({
  resolve: {
    alias: {
      '@shared': '../shared',
    },
  },
});
```

## 버전 관리

도구 정의가 변경될 때:
1. `tool_definitions.json`의 `version` 업데이트
2. 백엔드와 프론트엔드 양쪽에서 호환성 확인
3. 필요시 마이그레이션 코드 작성

## 타입 정의

### TypeScript (Frontend)
```typescript
// frontend/src/types/tool.ts
export interface ToolParameter {
  name: string;
  type: 'string' | 'integer' | 'boolean' | 'array' | 'object';
  description: string;
  required: boolean;
  enum?: string[];
}

export interface ToolDefinition {
  name: string;
  description: string;
  category: string;
  parameters: ToolParameter[];
}

export interface ToolDefinitionsFile {
  version: string;
  tools: ToolDefinition[];
}
```

### Python (Backend)
```python
# backend/app/schemas/tool.py
from pydantic import BaseModel

class ToolParameter(BaseModel):
    name: str
    type: str
    description: str
    required: bool = True
    enum: list[str] | None = None

class ToolDefinition(BaseModel):
    name: str
    description: str
    category: str
    parameters: list[ToolParameter]
```

## 코딩 규칙

### JSON 파일
- 들여쓰기: 2 spaces
- UTF-8 인코딩
- 후행 쉼표 없음

### 도구 이름
- snake_case 사용
- 명확하고 설명적인 이름
- 동사로 시작 권장 (예: `search_web`, `calculate`)

### 파라미터 타입
JSON Schema 호환 타입만 사용:
- `string`
- `integer`
- `number`
- `boolean`
- `array`
- `object`
