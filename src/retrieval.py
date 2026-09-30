# Loads IT policies, creates embeddings, compares them with the user question,
# and returns the policy with the closest semantic match.

import json
from pathlib import Path
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent
POLICY_FILE = BASE_DIR / "data" / "policies.json"

def load_policies():
    return json.loads(
        POLICY_FILE.read_text(encoding="utf-8")
    )

def cosine_similarity(vector_a, vector_b):
    a = np.array(vector_a)
    b = np.array(vector_b)

    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )

def build_policy_index(client): # The OpenAI client is passed in when this function is called.
    policies = load_policies()

    policy_texts = [
        policy["title"] + "\n" + policy["content"]
        for policy in policies
    ]

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=policy_texts
    )

    for item in response.data:
        policies[item.index]["embedding"] = item.embedding

    return policies


# Find the policy that best matches the query

def search_it_policy(client, policies, query):
    """
    Find the policy that is most semantically similar to the user's question.

    Parameters:
        client:
            OpenAI client used to create the query embedding.
        
        policies:
            Policy list returned by build_policy_index().
            Each policy should already contain an embedding.
        
        query:
            The user's natural-language question.

    Returns:
        A dictionary containing:
        - source_id
        - title
        - content
        - similarity score
    """

    # Embed the user question with the same model used for the policies.
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )

    query_embedding = response.data[0].embedding

    # Start with no match and keep the highest score we find.
    best_policy = None
    best_score = -float("inf")

    # Compare the query embedding with every policy embedding.
    for policy in policies:
        score = cosine_similarity(
            query_embedding,
            policy["embedding"]
        )

        # Replace the current match when this policy scores higher.
        if score > best_score:
            best_score = score
            best_policy = policy


    # Handle the case where there are no policies to search.
    if best_policy is None:
        return {
            "error": "No policy document was found."
        }

    # Return the useful policy fields, not the full embedding vector.
    return {
        "source_id": best_policy["id"],
        "title": best_policy["title"],
        "content": best_policy["content"],
        "similarity": round(float(best_score), 3)
    }