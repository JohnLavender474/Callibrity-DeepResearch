import json

from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel

from llm.claude_client import claude_client
from model.parallel_synthesis import (
    ParallelSynthesisInput,
    ParallelSynthesisOutput,
)
from model.task_entry import (
    TaskDecomposition,
)
from utils.prompt_loader import load_prompt


async def execute_parallel_synthesis(
    input_data: ParallelSynthesisInput,
) -> ParallelSynthesisOutput:
    prompt = load_prompt(
        "parallel_synthesis_decomposition.md",
    )
    formatted_prompt = prompt.format(
        input_data=json.dumps(
            input_data.model_dump(),
            indent=2,
        ),
    )

    messages = (
        input_data.messages 
        if input_data.messages is not None 
        else []
    )
    messages.extend([
        SystemMessage(content=formatted_prompt),
        HumanMessage(content=input_data.query),
    ])

    decomposition = await claude_client.ainvoke(
        input=messages,
        output_type=TaskDecomposition,
    )

    result = ""

    return ParallelSynthesisOutput(
        overall_result=result,
        task_entries=[],
    )
