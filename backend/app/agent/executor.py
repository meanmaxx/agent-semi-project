"""Agent executor for running the tool-using agent."""

import logging
from typing import Any

from app.agent.memory import ConversationMemory
from app.agent.prompts.system import BUDGET_SYSTEM_PROMPT
from app.llm.client import VLLMClient, vllm_client
from app.llm.parser import ParsedResponse, parse_response
from app.tools.registry import ToolRegistry, tool_registry

logger = logging.getLogger(__name__)


class AgentExecutor:
    """Executes the agent loop with tool calling."""

    def __init__(
        self,
        llm_client: VLLMClient | None = None,
        tools: ToolRegistry | None = None,
        system_prompt: str | None = None,
        max_iterations: int = 10,
    ) -> None:
        """Initialize the executor."""
        self.llm_client = llm_client or vllm_client
        self.tools = tools or tool_registry
        self.system_prompt = system_prompt or BUDGET_SYSTEM_PROMPT
        self.max_iterations = max_iterations
        self.memory = ConversationMemory(system_prompt=self.system_prompt)

    async def run(self, user_input: str) -> str:
        """Run the agent with user input."""
        self.memory.add_user_message(user_input)

        for iteration in range(self.max_iterations):
            logger.info(f"Agent iteration {iteration + 1}")

            # Get LLM response
            response = await self.llm_client.chat_completion(
                messages=self.memory.get_messages(),
                tools=self.tools.get_openai_tools(),
            )

            parsed = parse_response(response)
            logger.info(f"Parsed response: content={parsed.content}, tool_calls={len(parsed.tool_calls)}")

            # No tool calls - return the response
            if not parsed.tool_calls:
                self.memory.add_assistant_message(content=parsed.content)
                return parsed.content or "응답을 생성할 수 없습니다."

            # Process tool calls
            tool_calls_for_memory = self._format_tool_calls(parsed)
            self.memory.add_assistant_message(
                content=parsed.content,
                tool_calls=tool_calls_for_memory,
            )

            # Execute each tool and add results
            for tc in parsed.tool_calls:
                logger.info(f"Executing tool: {tc.name} with args: {tc.arguments}")
                result = await self.tools.execute(tc.name, **tc.arguments)
                logger.info(f"Tool result: {result}")
                self.memory.add_tool_result(
                    tool_call_id=tc.id,
                    name=tc.name,
                    content=result,
                )

        # Max iterations reached
        return "처리 중 최대 반복 횟수에 도달했습니다. 다시 시도해주세요."

    def _format_tool_calls(self, parsed: ParsedResponse) -> list[dict[str, Any]]:
        """Format tool calls for memory storage."""
        return [
            {
                "id": tc.id,
                "type": "function",
                "function": {
                    "name": tc.name,
                    "arguments": str(tc.arguments),
                },
            }
            for tc in parsed.tool_calls
        ]

    def reset(self) -> None:
        """Reset the conversation memory."""
        self.memory.clear()

    def get_conversation_history(self) -> list[dict[str, Any]]:
        """Get the current conversation history."""
        return self.memory.get_messages()
