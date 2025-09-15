from integrations.openai_client import run_assistant

# Replace with your real Classification Assistant ID from Playground
CLASSIFICATION_ASSISTANT_ID = "asst_your_classification_id_here"

def classify_ticket(user_input: str) -> dict:
    """
    Use the Classification Assistant to assign severity, priority, team, and issue_type.

    Args:
        user_input (str): The user's ticket description

    Returns:
        dict: Classification results with severity, priority, team, issue_type
    """
    reply = run_assistant(CLASSIFICATION_ASSISTANT_ID, user_input)

    # The assistant in Playground should be instructed to return JSON like:
    # {
    #   "severity": "high",
    #   "priority": "P1",
    #   "team": "ERP Support",
    #   "issue_type": "Bug"
    # }

    try:
        result = eval(reply)  # quick parsing if assistant returns JSON-like string
        if isinstance(result, dict):
            return result
        else:
            return {"severity": None, "priority": None, "team": None, "issue_type": None}
    except Exception:
        return {"severity": None, "priority": None, "team": None, "issue_type": None}
