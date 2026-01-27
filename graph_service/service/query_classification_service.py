from langchain_core.messages import HumanMessage, SystemMessage

from llm.claude_client import claude_client

from graph_service.model.query_classification import (
    ProcessSelectionInput,
    ProcessSelectionOutput,
)
from graph_service.utils.prompt_loader import load_prompt


async def classify_query(
    input_data: ProcessSelectionInput,
) -> ProcessSelectionOutput:
    system_prompt = load_prompt("process_selection.md")

    output = await claude_client.ainvoke(
        [
            SystemMessage(content=system_prompt),
            HumanMessage(content=input_data.query),
        ],        
        output_type=ProcessSelectionOutput,
    )

    return output
