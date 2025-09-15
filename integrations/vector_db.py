import os
import faiss
import pickle
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# File paths for persistence
VECTOR_STORE_PATH = "data/embeddings/ticket_index.faiss"
METADATA_STORE_PATH = "data/embeddings/ticket_metadata.pkl"

# Dimension of OpenAI embeddings (for text-embedding-3-small it is 1536)
EMBEDDING_DIM = 1536


# --- Persistence Helpers ---
def save_index(index, metadata):
    faiss.write_index(index, VECTOR_STORE_PATH)
    with open(METADATA_STORE_PATH, "wb") as f:
        pickle.dump(metadata, f)


def load_index():
    if os.path.exists(VECTOR_STORE_PATH) and os.path.exists(METADATA_STORE_PATH):
        index = faiss.read_index(VECTOR_STORE_PATH)
        with open(METADATA_STORE_PATH, "rb") as f:
            metadata = pickle.load(f)
        return index, metadata
    else:
        index = faiss.IndexFlatL2(EMBEDDING_DIM)
        return index, []


# --- Embedding Helper ---
def get_embedding(text: str) -> np.ndarray:
    """Get OpenAI embedding vector for given text."""
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return np.array(response.data[0].embedding, dtype="float32")


# --- Core Functions ---
def add_ticket_embedding(ticket_id: str, description: str):
    """Add a ticket description to the FAISS index."""
    index, metadata = load_index()

    embedding = get_embedding(description).reshape(1, -1)
    index.add(embedding)
    metadata.append({"id": ticket_id, "description": description})

    save_index(index, metadata)


def find_similar_tickets(description: str, top_k: int = 3):
    """Find top_k most similar tickets to the given description."""
    index, metadata = load_index()

    if index.ntotal == 0:
        return []

    embedding = get_embedding(description).reshape(1, -1)
    distances, indices = index.search(embedding, top_k)

    results = []
    for dist, idx in zip(distances[0], indices[0]):
        if idx < len(metadata):
            similarity = 1 / (1 + dist)  # Convert L2 distance to similarity (0-1 approx)
            results.append({
                "id": metadata[idx]["id"],
                "description": metadata[idx]["description"],
                "similarity": round(float(similarity), 3)
            })

    return results
