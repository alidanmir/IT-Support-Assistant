# Agent integration tests

# These tests run through the full agent flow and make real API calls.
import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from src.agent import support_chat
from src.retrieval import build_policy_index


# Test setup

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError(
        "OPENAI_API_KEY was not found in the .env file."
    )


client = OpenAI(
    api_key=api_key,
    default_headers={"Accept-Encoding": "identity"}
)


# Build the policy embeddings once before the tests run.
policies = build_policy_index(client)


# Helpers for reading tool calls and tool results from the saved history.

def get_tool_names(history):
    """
    Extract the names of tools requested by the LLM
    from the saved conversation history.
    """

    tool_names = []

    for message in history:

        for tool_call in message.get("tool_calls", []):
            tool_names.append(
                tool_call["function"]["name"]
            )

    return tool_names

def get_tool_results(history):
    """
    Extract the results returned by tools
    from the conversation history.
    """

    results = []

    for message in history:

        if message.get("role") == "tool":

            results.append(
                json.loads(message["content"])
            )

    return results


# Policy questions should use policy search.

def test_agent_uses_policy_search():
    history = []

    response = support_chat(
        "Can I buy a replacement docking station myself?",
        history,
        client,
        policies
    )

    tool_names = get_tool_names(history)
    tool_results = get_tool_results(history)

    # Make sure the agent chose the policy search tool.
    assert "search_it_policy" in tool_names

    # Make sure the retrieved policy was IT-001.
    assert any(
        result.get("source_id") == "IT-001"
        for result in tool_results
    )

# Ticket status questions should use ticket lookup.

def test_agent_uses_ticket_lookup():
    history = []

    response = support_chat(
        "What is the status of ticket DEMO-0007?",
        history,
        client,
        policies
    )

    tool_names = get_tool_names(history)

    assert "get_ticket" in tool_names
    assert "open" in response.lower()


# Without a ticket ID, the agent should ask for one.

def test_agent_asks_for_missing_ticket_id():
    history = []

    response = support_chat(
        "What is the status of my support ticket?",
        history,
        client,
        policies
    )

    tool_names = get_tool_names(history)

    # Do not let the model guess a ticket ID.
    assert "get_ticket" not in tool_names

    # The response should ask the user for the ID.
    assert "ticket" in response.lower()
    assert "id" in response.lower()