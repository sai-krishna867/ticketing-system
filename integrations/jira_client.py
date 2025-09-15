import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Load JIRA config from .env
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")   # e.g., "https://yourcompany.atlassian.net"
JIRA_EMAIL = os.getenv("JIRA_EMAIL")         # Atlassian email
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN") # API token from Atlassian

HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

AUTH = (JIRA_EMAIL, JIRA_API_TOKEN)

def create_jira_ticket(summary: str, description: str, severity: str, priority: str, team: str, issue_type: str) -> str:
    """
    Create a ticket in JIRA with dynamic issue type.

    Args:
        summary (str): Ticket title
        description (str): Detailed issue description
        severity (str): Severity classification
        priority (str): Priority name in JIRA ("Highest", "High", "Medium", "Low")
        team (str): Team assignment (label, component, or custom field)
        issue_type (str): JIRA issue type (e.g., "Bug", "Task", "Incident", "Story")

    Returns:
        str: JIRA ticket ID
    """
    url = f"{JIRA_BASE_URL}/rest/api/3/issue"

    payload = {
        "fields": {
            "project": {"key": "SUP"},   # Replace with your JIRA project key
            "summary": summary,
            "description": description,
            "issuetype": {"name": issue_type},  # Dynamic issue type
            "priority": {"name": priority},     # Must match exact JIRA priority name
            "labels": [severity, team]          # Simple way to tag
        }
    }

    response = requests.post(url, json=payload, headers=HEADERS, auth=AUTH)
    response.raise_for_status()
    data = response.json()

    return data.get("key", "UNKNOWN-TICKET")


def get_jira_ticket_status(ticket_id: str) -> dict:
    """
    Fetch the status of a JIRA ticket.

    Args:
        ticket_id (str): JIRA issue key (e.g., "SUP-123")

    Returns:
        dict: Ticket status info
    """
    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{ticket_id}"

    response = requests.get(url, headers=HEADERS, auth=AUTH)
    response.raise_for_status()
    data = response.json()

    return {
        "status": data["fields"]["status"]["name"],
        "assignee": data["fields"]["assignee"]["displayName"] if data["fields"]["assignee"] else None,
        "last_updated": data["fields"]["updated"]
    }
