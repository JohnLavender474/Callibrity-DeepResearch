from langchain_core.messages import (
  BaseMessage, 
  SystemMessage, 
  HumanMessage, 
  AIMessage
)


def copy_messages(
    messages: list[BaseMessage],
    include_system_messages: bool = False,
) -> list[BaseMessage]:
    output: list[BaseMessage] = []

    for message in messages:
        if isinstance(message, SystemMessage) and not include_system_messages:
            continue
        elif isinstance(message, HumanMessage):
            output.append(HumanMessage(content=message.content))
        elif isinstance(message, AIMessage):
            output.append(AIMessage(content=message.content))
        else:
            raise ValueError(f"Unsupported message type: {type(message)}")
    
    return output