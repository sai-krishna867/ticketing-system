from integrations.vector_db import add_ticket_embedding, find_similar_tickets

def check_duplicates(ticket_id: str, description: str, top_k: int = 3, threshold: float = 0.8):
    """
    Check if a new ticket description is similar to existing ones.

    Args:
        ticket_id (str): Temporary/new ticket ID
        description (str): The issue description from the user
        top_k (int): Number of similar tickets to fetch
        threshold (float): Similarity threshold (0-1, higher = stricter)

    Returns:
        list[dict]: List of similar tickets with {id, description, similarity}
    """
    # Search vector DB for similar tickets
    matches = find_similar_tickets(description, top_k=top_k)

    # Filter by similarity threshold
    similar_tickets = [m for m in matches if m["similarity"] >= threshold]

    # Store embedding for the new ticket after search
    add_ticket_embedding(ticket_id, description)

    return similar_tickets
