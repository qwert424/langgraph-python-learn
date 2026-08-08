from typing import Literal, Union

from .config import anthropic_settings
from langchain.chat_models import init_chat_model

Provider = Union[Literal["anthropic"], Literal["openai_reasoning"]]


def create_model(
    *,
    model_name: str = anthropic_settings.default_model,
    provider: Provider = "anthropic",
    **kwargs,
):
    if provider == "anthropic":
        kwargs.setdefault("thinking", {"type": "disabled"})
    return init_chat_model(model=model_name, model_provider=provider, **kwargs)
