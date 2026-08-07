from langgraph.graph import END, START, StateGraph

from langgraph_python.nodes.call_model import call_model
from langgraph_python.states.core_agent_state import CoreAgentState


def build_graph():
    """生成核心 Agent 图（未编译）"""
    workflow = StateGraph(CoreAgentState)
    workflow.add_node("call_model", call_model)
    workflow.add_edge(START, "call_model")
    workflow.add_edge("call_model", END)
    return workflow
