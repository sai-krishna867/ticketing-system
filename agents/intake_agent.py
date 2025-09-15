from integrations.openai_client import run_assistant


INTAKE_ASSISTANT_ID = "asst_your_intake_id_here" # add here 

def detect_intent(user_input: str) -> str:
    """
    Detect user intent using the Intake Assistant.
    Possible outputs: 'create_ticket' or 'check_status'.

    Args:
        user_input (str): The user's query

    Returns:
        str: The detected intent
    """
    reply = run_assistant(INTAKE_ASSISTANT_ID, user_input)
    return reply.strip().lower()
