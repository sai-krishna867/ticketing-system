from typing import Optional, List, Dict
from dataclasses import dataclass, field

@dataclass
class TicketState:
    # User input
    user_input: str

    # Intent (from Intake Agent)
    intent: Optional[str] = None

    # Classification results
    severity: Optional[str] = None
    priority: Optional[str] = None
    team: Optional[str] = None
    issue_type: Optional[str] = None

    # Duplicate detection
    similar_tickets: List[Dict] = field(default_factory=list)

    # JIRA ticket
    ticket_id: Optional[str] = None
    ticket_status: Optional[Dict] = None

    # NEW: Clarification handling
    clarification_question: Optional[str] = None
