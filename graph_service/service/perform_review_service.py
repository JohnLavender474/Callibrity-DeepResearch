import json
import logging

from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
)

from llm.claude_client import claude_client
from model.perform_review import (
    PerformReviewInput,
    PerformReviewOutput,
)
from utils.prompt_loader import load_prompt


logger = logging.getLogger(__name__)


async def execute_perform_review(
    input_data: PerformReviewInput,
) -> PerformReviewOutput:
    logger.debug("Starting task results review")
    review_prompt = load_prompt("perform_review.md")

    review_response = await claude_client.ainvoke(
        input=[
            SystemMessage(content=review_prompt),
            HumanMessage(
                content=json.dumps(
                    [entry.model_dump() for entry in input_data.task_entries],
                    indent=2,
                ),
            ),
        ],
    )

    review_content = review_response.content

    logger.debug("Task review completed")
    return PerformReviewOutput(review=review_content)
