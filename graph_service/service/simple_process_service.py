from langchain_core.messages import HumanMessage, BaseMessage

from llm.claude_client import claude_client
from model.simple_process import (
    SimpleProcessInput,
    SimpleProcessOutput,
)


async def execute_simple_process(
    input_data: SimpleProcessInput,
) -> SimpleProcessOutput:
    message_list = (
        input_data.messages.copy()
        if input_data.messages else []
    )
    message_list.append(
        HumanMessage(content=input_data.query),
    )

    response = await claude_client.ainvoke(
        message_list,
    )

    return SimpleProcessOutput(result=response.content)
