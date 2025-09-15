from integrations.openai_client import run_assistant

# Replace with your real Clarification Assistant ID from Playground
CLARIFICATION_ASSISTANT_ID = "asst_your_clarification_id_here"

def clarify_information(state: dict) -> dict:
    """
    Use the Clarification Assistant to ask follow-up questions
    when classification results are incomplete.

    Args:
        state (dict): Current ticket state (may have missing severity/priority/team/issue_type)

    Returns:
        dict: Updated state with clarifications filled in (or a question to ask user)
    """
    user_message = (
        f"Here is the current ticket state: {state}. "
        "If any key info is missing (severity, priority, team, issue_type), "
        "ask the user a clarifying question. "
        "Otherwise, return the updated state as JSON."
    )

    reply = run_assistant(CLARIFICATION_ASSISTANT_ID, user_message)
    return reply.strip()
