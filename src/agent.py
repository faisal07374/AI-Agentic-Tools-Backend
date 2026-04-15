from langgraph.graph import StateGraph, END
from .nodes import format_json_node, validate_json_node
from .state import AgentState

def should_continue(state):
    # Stop if valid or if we've tried 3 times
    if not state["errors"] and state["json_output"]:
        return "end"
    if state["iterations"] >= 3:
        return "end"
    return "continue"

workflow = StateGraph(AgentState)

workflow.add_node("formatter", format_json_node)
workflow.add_node("validator", validate_json_node)

workflow.set_entry_point("formatter")

workflow.add_edge("formatter", "validator")

workflow.add_conditional_edges(
    "validator",
    should_continue,
    {
        "continue": "formatter",
        "end": END
    }
)

app = workflow.compile()