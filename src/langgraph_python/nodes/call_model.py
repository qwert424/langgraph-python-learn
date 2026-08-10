from langchain_core.messages import SystemMessage
from langchain_core.runnables import RunnableConfig, ensure_config

from langgraph_python.core.create_model import create_model
from langgraph_python.core.mock_model import mock_model
from langgraph_python.states.core_agent_state import CoreAgentState
from langgraph_python.tools import get_tools, tools


def _get_system_prompts(config: RunnableConfig):
    "根据配置获取系统提示词"
    system_msgs = []
    configurable = config.get("configurable") or {}
    system_prompt = configurable.get("system_prompt")
    if system_prompt:
        system_msgs.append(SystemMessage(system_prompt))
    return system_msgs


def _get_model(config: RunnableConfig):
    "根据配置获取模型对象"
    configurable = config.get("configurable") or {}
    model = configurable.get("model")
    if model == "fake":
        return mock_model()
    else:
        return create_model()


def _get_tools(config: RunnableConfig):
    "根据配置获取工具列表，未配置时返回全部工具"
    configurable = config.get("configurable") or {}
    tool_names = configurable.get("tools")
    if tool_names:
        return get_tools(tool_names)
    return tools


async def call_model(state: CoreAgentState, config: RunnableConfig) -> dict:
    """调用模型节点"""
    messages = state["messages"]
    # 根据配置获取模型对象
    model = _get_model(config)
    # 根据配置读取系统提示词
    system_prompts = _get_system_prompts(config)
    # 根据配置获取工具列表
    active_tools = _get_tools(config)
    model_with_tools = model.bind_tools(active_tools)

    # 调用模型
    response = await model_with_tools.ainvoke([*system_prompts, *messages])
    return {"messages": [response]}
