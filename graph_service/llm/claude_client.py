from typing import overload, Optional, Type, TypeVar, Any

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import BaseMessage

from config import CLAUDE_API_KEY


# Claude model configuration constants.
# These can be turned into env vars later if needed.
# It may also be worth exposing configurations to the
# invokers so that each graph node can have different settings.

CLAUDE_MODEL = "claude-opus-4-5"
CLAUDE_TEMPERATURE = 0.5
CLAUDE_MAX_TOKENS = 64000


T = TypeVar("T")


class ClaudeClientWrapper:

    def __init__(self):
        self._client = ChatAnthropic(
            model=CLAUDE_MODEL,
            api_key=CLAUDE_API_KEY,
            temperature=CLAUDE_TEMPERATURE,
            max_tokens=CLAUDE_MAX_TOKENS,
        )


    @overload
    async def ainvoke(
        self,
        input: list[BaseMessage],        
        output_type: None = None,
    ) -> Any:
        ...


    @overload
    async def ainvoke(
        self,
        input: list[BaseMessage],
        output_type: Type[T] = ...,
    ) -> T:
        ...


    async def ainvoke(
        self,
        input: list[BaseMessage],        
        output_type: Optional[Type[T]] = None,
    ) -> Any:
        if output_type is not None:
            client = self._client.with_structured_output(output_type)
        else:
            client = self._client

        return await client.ainvoke(input)


claude_client = ClaudeClientWrapper()
