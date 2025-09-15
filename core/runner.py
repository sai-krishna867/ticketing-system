from core.graph import build_graph
from core.state import TicketState

def run_graph(user_input: str) -> TicketState:
    """
    Run the LangGraph pipeline for a given user input.
    """
    state = TicketState(user_input=user_input)
    graph = build_graph()
    app = graph.compile()

    final_state = app.invoke(state)
    return final_state


if __name__ == "__main__":
    # Example: Create a ticket
    result = run_graph("The sales order system is crashing when I submit an order.")
    print("Final State:", result)

    # Example: Check status
    result = run_graph("What is the status of SUP-1001?")
    print("Final State:", result)
