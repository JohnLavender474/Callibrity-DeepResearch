import os

from pathlib import Path


def load_prompt(filename: str) -> str:
    prompt_dir = Path(__file__).parent.parent / "prompts"
    prompt_path = prompt_dir / filename

    with open(prompt_path, "r") as f:
        return f.read()
