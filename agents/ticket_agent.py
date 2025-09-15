from integrations.jira_client import create_jira_ticket, get_jira_ticket_status

def create_ticket(summary: str, description: str, severity: str, priority: str, team: str, issue_type: str) -> str:
    """
    Create a new ticket in JIRA.

    Args:
        summary (str): Short title of the issue
        description (str): Detailed description from the user
        severity (str): Severity classification
        priority (str): Priority level (must match JIRA config, e.g., "Highest", "High", "Medium", "Low")
        team (str): Team assignment
        issue_type (str): JIRA issue type (e.g., "Bug", "Task", "Incident", "Story")

    Returns:
        str: JIRA ticket ID
    """
    ticket_id = create_jira_ticket(summary, description, severity, priority, team, issue_type)
    return ticket_id


def check_ticket_status(ticket_id: str) -> dict:
    """
    Fetch the status of an existing JIRA ticket.

    Args:
        ticket_id (str): JIRA ticket ID

    Returns:
        dict: Ticket status details {status, assignee, last_updated}
    """
    status = get_jira_ticket_status(ticket_id)
    return status
