from model.graph_invocation import (
    GraphInvocation,
)


class GraphInvocationsRepository:    

    def __init__(self):
        self._invocations: dict[str, GraphInvocation] = {}
    

    def get_invocation(
        self,
        invocation_id: str,
    ) -> GraphInvocation | None:
        return self._invocations.get(invocation_id)


    def put_invocation(
        self,
        invocation: GraphInvocation,
    ) -> None:
        self._invocations[invocation.invocation_id] = invocation
    


    

