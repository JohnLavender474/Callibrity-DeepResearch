import asyncio
import json

from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
    AIMessage,
    BaseMessage,
)

from llm.claude_client import claude_client
from model.parallel_synthesis import (
    ParallelSynthesisInput,
    ParallelSynthesisOutput,
)
from graph_service.model.task import (
    TaskDecomposition,
    TaskResult,
    TaskEntry,
)
from utils.prompt_loader import load_prompt


async def execute_parallel_synthesis(
    input_data: ParallelSynthesisInput,
) -> ParallelSynthesisOutput:
    decomposition_prompt = load_prompt(
        "parallel_synthesis_decomposition.md",
    )
    formatted_decomposition_prompt = (
        decomposition_prompt.format(
            input_data=json.dumps(
                input_data.model_dump(),
                indent=2,
            ),
        )
    )

    messages = (
        input_data.messages
        if input_data.messages is not None
        else []
    )
    messages.extend([
        SystemMessage(
            content=formatted_decomposition_prompt,
        ),
        HumanMessage(content=input_data.query),
    ])

    decomposition = await claude_client.ainvoke(
        input=messages,
        output_type=TaskDecomposition,
    )

    task_execution_prompt = load_prompt(
        "task_execution.md",
    )

    task_coroutines = [
        _execute_task(
            task,
            task_execution_prompt,
            input_data.messages or [],
        )
        for task in decomposition.tasks
    ]

    task_entries = await asyncio.gather(
        *task_coroutines,
    )

    for entry in task_entries:
        messages.append(
            HumanMessage(content=entry.task),
        )
        if entry.success:
            content = (
                f"Result: {entry.result}\n"
                f"Reasoning: {entry.reasoning}"
            )
        else:
            content = (
                f"Error: {entry.result}"
            )
        messages.append(
            AIMessage(content=content),
        )

    result = ""

    return ParallelSynthesisOutput(
        overall_result=result,
        task_entries=task_entries,
    )


async def _execute_task(
    task: str,
    prompt: str,
    messages: list[BaseMessage],
) -> TaskEntry:
    try:
        formatted_prompt = prompt.format(task=task)

        task_messages = messages.copy()
        task_messages.append(
            SystemMessage(content=formatted_prompt),
        )
        task_messages.append(
            HumanMessage(content=task),
        )

        result = await claude_client.ainvoke(
            input=task_messages,
            output_type=TaskResult,
        )

        return TaskEntry(
            task=task,
            success=True,
            result=result.result,
            reasoning=result.reasoning,
        )
    except Exception as e:
        return TaskEntry(
            task=task,
            success=False,
            result=str(e),
        )
