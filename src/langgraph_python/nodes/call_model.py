import os
import subprocess
from typing import Any

from langchain_core.messages import SystemMessage

from langgraph_python.core.create_model import create_model
from langgraph_python.states.core_agent_state import CoreAgentState
from langgraph_python.states.model_config import ModelConfig
from langgraph_python.templates import prompt_from_filename
from langgraph_python.tools import tools


def _is_git(cwd: str) -> bool:
    result = subprocess.run(
        ["git", "-C", cwd, "rev-parse", "--is-inside-work-tree"],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def _environment_info() -> dict[str, Any]:
    cwd = os.getcwd()
    return {
        "cwd": cwd,
        "os": os.name,
        "is_git": _is_git(cwd),
    }


# 系统提示词名称 -> 需要注入的信息
_SYSTEM_PROMPT_TEMPLATES: dict[str, dict[str, Any]] = {"system": _environment_info()}


def _build_system_message(template_name: str) -> SystemMessage:
    data = _SYSTEM_PROMPT_TEMPLATES[template_name]
    return SystemMessage(
        content=prompt_from_filename(template_name, data),
    )


async def call_model(state: CoreAgentState) -> dict:
    """调用模型节点"""
    messages = state["messages"]  # 取出messages，不包含系统提示词
    model_config = state.get("model_config", ModelConfig())
    template_name = state.get("system_prompt_template", "system")
    system_message = _build_system_message(template_name)
    model = create_model(**model_config.to_kwargs())
    model_with_tools = model.bind_tools(tools)
    response = await model_with_tools.ainvoke([system_message, *messages])
    return {"messages": [response]}
