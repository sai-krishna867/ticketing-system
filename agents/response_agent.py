from integrations.openai_client import run_assistant

# Replace with your Response Assistant ID from Playground
RESPONSE_ASSISTANT_ID = "asst_your_response_id_here"

def generate_response(state: dict) -> str:
    """
    Generate a conversational reply for the user
    based on the final ticket state.
    """
    if state.get("clarification_question"):
        user_message = f"The system needs more info. Ask the user: {state['clarification_question']}"
    else:
        user_message = f"Here is the ticket state: {state}. Reply to the user naturally."

    reply = run_assistant(RESPONSE_ASSISTANT_ID, user_message)
    return reply.strip()
