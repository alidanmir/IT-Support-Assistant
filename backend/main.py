import json
import os
import uuid

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from pydantic import BaseModel

from src.agent import support_chat
from src.retrieval import build_policy_index


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


policies = build_policy_index(client)


app = FastAPI(
    title="IT Support Assistant API"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://it-support-assistant-theta.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Stores conversation history for each browser session
sessions = {}


class ChatRequest(BaseModel):
    question: str
    session_id: str | None = None


class ChatResponse(BaseModel):
    response: str
    session_id: str
    source_id: str | None = None
    ticket: dict | None = None


def get_latest_tool_data(history):
    """
    Get any policy source or ticket returned
    by a tool during the current request.
    """

    source_id = None
    ticket = None

    for message in reversed(history):

        if message.get("role") != "tool":
            continue

        try:
            result = json.loads(message["content"])
        except (json.JSONDecodeError, TypeError):
            continue

        if source_id is None and result.get("source_id"):
            source_id = result["source_id"]

        if ticket is None and result.get("ticket_id"):
            ticket = result

        if source_id is not None and ticket is not None:
            break

    return source_id, ticket


@app.get("/")
def root():
    return {
        "message": "IT Support Assistant API is running"
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    session_id = request.session_id or str(uuid.uuid4())

    if session_id not in sessions:
        sessions[session_id] = []

    history = sessions[session_id]

    # Remember where this request starts in the history
    history_start = len(history)

    response = support_chat(
        request.question,
        history,
        client,
        policies
    )

    # Only look at tool results created during this request
    current_turn = history[history_start:]

    source_id, ticket = get_latest_tool_data(current_turn)

    return ChatResponse(
        response=response,
        session_id=session_id,
        source_id=source_id,
        ticket=ticket
    )