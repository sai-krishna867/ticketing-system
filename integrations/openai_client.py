import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def run_assistant(assistant_id: str, user_message: str):
    """
    Call an OpenAI Assistant by ID and run a thread with a user message.

    Args:
        assistant_id (str): The ID of the assistant created in Playground
        user_message (str): The user's query/input

    Returns:
        str: Assistant's reply text
    """
    # Create and run a thread with the assistant
    response = client.beta.threads.create_and_run(
        assistant_id=assistant_id,
        thread={
            "messages": [
                {"role": "user", "content": user_message}
            ]
        }
    )

    # Extract text output (Assistants API can also return tools, JSON, etc.)
    if hasattr(response, "output") and response.output:
        return response.output[0].content[0].text.value
    else:
        return " No response from assistant."
