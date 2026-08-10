from typing import Annotated, Any, NotRequired, Required, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class CoreAgentState(TypedDict):
    """核心 Agent 图状态"""

    # 消息列表，使用 add_messages reducer 自动累积
    messages: Required[Annotated[list[BaseMessage], add_messages]]
    # 系统提示词模板名称，选填，默认 system
    system_prompt_template: NotRequired[str]
