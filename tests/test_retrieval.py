import os

from dotenv import load_dotenv
from openai import OpenAI

from src.retrieval import (
    build_policy_index,
    search_it_policy
)


# Retrieval test setup

# Load the API key from .env.
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError(
        "OPENAI_API_KEY was not found in the .env file."
    )


# Client used for the embedding calls.
client = OpenAI(
    api_key=api_key,
    default_headers={"Accept-Encoding": "identity"}
)


# Build the policy embeddings once before the tests run.
policies = build_policy_index(client)


# Check that common questions return the expected policy.

def test_docking_station_policy():
    result = search_it_policy(
        client,
        policies,
        "Can I buy a replacement docking station myself?"
    )

    assert result["source_id"] == "IT-001"


def test_password_policy():
    result = search_it_policy(
        client,
        policies,
        "I forgot my password. How do I reset it?"
    )

    assert result["source_id"] == "IT-002"


def test_vpn_policy():
    result = search_it_policy(
        client,
        policies,
        "My VPN connection failed. What should I do?"
    )

    assert result["source_id"] == "IT-003"