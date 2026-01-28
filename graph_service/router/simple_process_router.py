from fastapi import APIRouter

from model.simple_process import (
    SimpleProcessInput,
    SimpleProcessOutput,
)
from service.simple_process_service import (
    execute_simple_process,
)


simple_process_router = APIRouter(
    prefix="/api/graph/simple-process",
    tags=["simple-process"],
)


@simple_process_router.post(
    "/execute",
    response_model=SimpleProcessOutput,
)
async def simple_process_endpoint(
    request: SimpleProcessInput,
) -> SimpleProcessOutput:
    output = await execute_simple_process(request)
    return output
