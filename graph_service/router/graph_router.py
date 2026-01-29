import json

from fastapi import APIRouter

from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    AIMessage,
)

from graph import build_graph
from model.graph_input import GraphInput
from model.graph_state import GraphState

from logging import logger


logger = logger.getLogger(__name__)

router = APIRouter(prefix="/api/graph", tags=["graph"])


@router.post(
    "/execute",
    response_model=GraphState,
)
async def invoke_graph(
    input_data: GraphInput,
) -> GraphState:
    logger.debug(
        f"Graph invocation requested for query: " 
        f"{json.dumps(input_data.user_query, indent=2)}"
    )

    graph_state_messages: list[BaseMessage] = []

    for message in input_data.messages:
        if message.role == "user":
            graph_state_messages.append(
                HumanMessage(content=message.content)
            )
        elif message.role == "ai":
            graph_state_messages.append(
                AIMessage(content=message.content)
            )
        else:
            raise Exception(f"Invalid message: {message}")

    state = GraphState(
        user_query=input_data.user_query,
        profile_id=input_data.profile_id,
        messages=graph_state_messages,
    )
    
    graph = build_graph()

    result = await graph.ainvoke(state)

    logger.debug(
        f"Graph execution completed with result: " 
        f"{json.dumps(result, indent=2)}"
    )
    
    return result
