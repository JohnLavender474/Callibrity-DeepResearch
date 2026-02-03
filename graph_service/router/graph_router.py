import json
import asyncio

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from model.graph_input import GraphInput
from service.graph_streamer import (
    consume_graph_to_queue,
    stream_from_queue,
)

import logging


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/graph", tags=["graph"])


@router.post("/execute")
async def invoke_graph(
    input_data: GraphInput,
) -> StreamingResponse:
    logger.debug(
        f"Graph invocation requested for query: " 
        f"{json.dumps(input_data.model_dump(), indent=2)}"
    )
    
    queue: asyncio.Queue = asyncio.Queue()
    
    asyncio.create_task(
        consume_graph_to_queue(
            input_data=input_data,
            queue=queue,
        )
    )
    
    return StreamingResponse(
        stream_from_queue(queue),
        media_type="text/event-stream",
    )
