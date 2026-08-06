from dataclasses import dataclass
from typing import TypedDict

from langgraph.graph import StateGraph, START, END


# 图状态
class MyState(TypedDict, total=False):
    node1: str  # node1 channel
    node2: str  # node2 channel


# 创建图
workflow = StateGraph(MyState)


def node1(state: MyState):
    return {"node1": "node1 result"}


def node2(state: MyState):
    return {"node2": "node2 result"}


(
    workflow.add_node(node1)
    .add_node(node2)
    .add_edge(START, "node1")
    .add_edge("node1", "node2")
    .add_edge("node2", END)
)
