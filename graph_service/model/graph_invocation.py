from enum import Enum
from typing import Optional

from model.graph_state import GraphState


class GraphInvocationState(str, Enum):    
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class GraphInvocation:
    
    def __init__(
        self,
        invocation_id: str,        
        invocation_state: GraphInvocationState = (
            GraphInvocationState.PENDING
        ),
        graph_state: Optional[GraphState] = None,
    ):
        self.invocation_id = invocation_id
        self.invocation_state = invocation_state
        self.graph_state = graph_state        