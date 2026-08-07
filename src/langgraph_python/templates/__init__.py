from pathlib import Path
from typing import Any
from langchain_core.utils.mustache import render


def prompt(template: str, data: dict[str, Any]):
    return render(template, data)


def prompt_from_filename(filename: str, data: dict[str, Any]):
    template_path = Path(__file__).parent / f"{filename}.mst"
    template = template_path.read_text()
    return prompt(template, data)
