from typing import Optional

from client import database_client

import logging


logger = logging.getLogger(__name__)


async def create_invocation(
    profile_id: str,
    invocation_id: str,
    user_query: str,
    status: str = "running",
    graph_state: Optional[dict] = None,
):
    return await database_client.create_invocation(
        profile_id=profile_id,
        invocation_id=invocation_id,
        user_query=user_query,
        status=status,
        graph_state=graph_state,
    )


async def update_invocation(
    profile_id: str,
    invocation_id: str,
    status: Optional[str] = None,
    graph_state: Optional[dict] = None,
):
    return await database_client.update_invocation(
        profile_id=profile_id,
        invocation_id=invocation_id,
        status=status,
        graph_state=graph_state,
    )


async def check_stop_request_exists(
    invocation_id: str,
) -> bool:
    return await database_client.check_stop_request_exists(
        invocation_id=invocation_id,
    )


async def delete_stop_request(
    invocation_id: str,
):
    return await database_client.delete_stop_request(
        invocation_id=invocation_id,
    )
