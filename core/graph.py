from langgraph.graph import StateGraph, END
from core.state import TicketState
from agents.intake_agent import detect_intent
from agents.classification_agent import classify_ticket
from agents.clarification_agent import clarify_information
from agents.duplicate_agent import check_duplicates
from agents.ticket_agent import create_ticket, check_ticket_status


# ---- Node Functions ----
def intake_node(state: TicketState) -> TicketState:
    state.intent = detect_intent(state.user_input)
    return state

def classification_node(state: TicketState) -> TicketState:
    result = classify_ticket(state.user_input)
    state.severity = result.get("severity")
    state.priority = result.get("priority")
    state.team = result.get("team")
    state.issue_type = result.get("issue_type")
    return state

def clarification_node(state: TicketState) -> TicketState:
    reply = clarify_information(state.__dict__)

    # If AI asks a question instead of returning JSON
    if reply and not reply.strip().startswith("{"):
        state.clarification_question = reply.strip()
    else:
        try:
            data = eval(reply)
            state.severity = data.get("severity", state.severity)
            state.priority = data.get("priority", state.priority)
            state.team = data.get("team", state.team)
            state.issue_type = data.get("issue_type", state.issue_type)
        except:
            pass

    return state

def duplicate_node(state: TicketState) -> TicketState:
    state.similar_tickets = check_duplicates("TEMP-NEW", state.user_input)
    return state

def create_ticket_node(state: TicketState) -> TicketState:
    state.ticket_id = create_ticket(
        summary=state.user_input[:50],
        description=state.user_input,
        severity=state.severity,
        priority=state.priority,
        team=state.team,
        issue_type=state.issue_type,
    )
    return state

def status_node(state: TicketState) -> TicketState:
    state.ticket_status = check_ticket_status(state.user_input)
    return state


# ---- Graph Definition ----
def build_graph():
    workflow = StateGraph(TicketState)

    workflow.add_node("intake", intake_node)
    workflow.add_node("classification", classification_node)
    workflow.add_node("clarification", clarification_node)
    workflow.add_node("duplicate", duplicate_node)
    workflow.add_node("create_ticket", create_ticket_node)
    workflow.add_node("check_status", status_node)

    workflow.set_entry_point("intake")

    # Branch: ticket creation
    workflow.add_edge("intake", "classification", condition=lambda s: s.intent == "create_ticket")
    workflow.add_edge("classification", "duplicate", condition=lambda s: all([s.severity, s.priority, s.team, s.issue_type]))
    workflow.add_edge("classification", "clarification", condition=lambda s: not all([s.severity, s.priority, s.team, s.issue_type]))
    workflow.add_edge("clarification", "duplicate")

    # Branch: check status
    workflow.add_edge("intake", "check_status", condition=lambda s: s.intent == "check_status")

    # Endpoints
    workflow.add_edge("duplicate", "create_ticket")
    workflow.add_edge("create_ticket", END)
    workflow.add_edge("check_status", END)

    return workflow
