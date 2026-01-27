from typing import Literal

from pydantic import BaseModel


ProcessType = Literal[
    "simple_synthesis",
    "exhaustive_synthesis",
    "chain_of_process_synthesis",
]


class ProcessSelectionInput(BaseModel):
    query: str


class ProcessSelectionOutput(BaseModel):
    process: ProcessType