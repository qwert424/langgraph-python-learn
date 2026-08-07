from dataclasses import dataclass, field
from typing import Any

from langgraph_python.core.config import anthropic_settings
from langgraph_python.core.create_model import Provider


@dataclass
class ModelConfig:
    """模型配置，最终透传给 create_model"""

    model_name: str = anthropic_settings.default_model
    provider: Provider = "anthropic"
    kwargs: dict[str, Any] = field(default_factory=dict)

    def to_kwargs(self) -> dict[str, Any]:
        return {
            "model_name": self.model_name,
            "provider": self.provider,
            **self.kwargs,
        }
