# src/core/graph.py
from langgraph.graph import StateGraph, END
from src.core.state import AgentState
from src.agents.nodes import analyst_node, strategist_node, publisher_node

def build_graph():
    # 1. Initialize Graph with State
    workflow = StateGraph(AgentState)
    
    # 2. Add Nodes
    workflow.add_node("analyst", analyst_node)
    workflow.add_node("strategist", strategist_node)
    workflow.add_node("publisher", publisher_node)
    
    # 3. Define Edges (The Flow)
    workflow.set_entry_point("analyst")
    workflow.add_edge("analyst", "strategist")
    workflow.add_edge("strategist", "publisher")
    workflow.add_edge("publisher", END)
    
    # 4. Compile
    return workflow.compile()