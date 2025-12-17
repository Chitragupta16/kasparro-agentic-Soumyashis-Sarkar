from langgraph.graph import StateGraph, END
from src.core.state import AgentState
from src.agents.nodes import analyst_node, strategist_node, publisher_node

def route_strategist(state: AgentState):
    """
    Decides where to go after the Strategist runs.
    """
    questions = state.get("generated_questions", [])
    retries = state.get("retry_count", 0)
    
    if len(questions) < 5 and retries < 3:

        return "retry"
    else:
        return "continue"

def build_graph():
    workflow = StateGraph(AgentState)

    # 1. Add Nodes
    workflow.add_node("analyst", analyst_node)
    workflow.add_node("strategist", strategist_node)
    workflow.add_node("publisher", publisher_node)

    # 2. Add Standard Edges
    workflow.set_entry_point("analyst")
    workflow.add_edge("analyst", "strategist")

    # 3. Add Conditional Edge
    workflow.add_conditional_edges(
        "strategist",
        route_strategist,
        {
            "retry": "strategist",   
            "continue": "publisher" 
        }
    )

    workflow.add_edge("publisher", END)

    return workflow.compile()