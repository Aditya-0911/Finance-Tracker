from langgraph.graph import StateGraph, END
from models import AgentState
from llm_nodes import model_node, add_expense_node, summarize_node

def router(state):
    if state.action == "add_expense":
        return "add_node"
    elif state.action == "summarize":
        return "summarize_node"

def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("model", model_node)
    graph.add_node("add_node", add_expense_node)
    graph.add_node("summarize_node", summarize_node)
    graph.add_node("Router", lambda state: state)
    
    graph.set_entry_point("model")
    graph.add_edge("model", "Router")
    graph.add_conditional_edges("Router", router, {
        "add_node": "add_node",
        "summarize_node": "summarize_node"
    })

    graph.add_edge("add_node", END)
    graph.add_edge("summarize_node", END)

    return graph.compile()
