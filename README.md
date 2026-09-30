# IT Support Assistant

An AI-powered IT support application that can answer company policy questions, look up support tickets, and create new demo tickets through a conversational interface.

The project uses a React frontend, FastAPI backend, OpenAI tool calling, semantic search with embeddings, and persistent local ticket storage.


## Live Demo

Frontend & Live UI:
https://it-support-assistant-theta.vercel.app

Backend API:
https://it-support-assistant-kmkm.onrender.com

API Documentation:
https://it-support-assistant-kmkm.onrender.com/docs


## Demo

The assistant supports three main workflows:

### IT Policy Questions

Users can ask questions such as:

> Can I buy my own replacement docking station?

The assistant searches the company policy knowledge base using embeddings and returns the most relevant policy.

Policy sources are displayed separately in the interface, such as:

`IT-001`

### Ticket Lookup

Users can retrieve an existing support ticket by ID:

> What is the status of ticket DEMO-0010?

The application returns the ticket status and displays the saved details in a structured ticket card.

### Ticket Creation

Users can create a support ticket conversationally:

> Create a support ticket. My external monitor keeps disconnecting.

If information is missing, the assistant asks for the remaining details before creating the ticket.

Required information includes:

- Laptop model
- Docking station model
- Issue description
- Troubleshooting already attempted

Once complete, the ticket is stored locally and assigned an ID such as:

`DEMO-0011`

---

## Features

- AI-powered IT support chat
- OpenAI tool calling
- Semantic IT policy search
- Embedding-based retrieval
- Multi-turn conversation memory
- Support ticket creation
- Support ticket lookup
- Persistent JSON ticket storage
- Structured policy source metadata
- Structured ticket cards
- React frontend
- FastAPI REST API
- Automated testing with pytest

---

## Tech Stack

### Frontend

- React
- TypeScript
- Vite
- CSS

### Backend

- Python
- FastAPI
- Pydantic
- Uvicorn

### AI

- OpenAI API
- `gpt-4.1-mini`
- `text-embedding-3-small`
- Tool calling
- Retrieval using cosine similarity

### Data and Testing

- JSON
- NumPy
- pytest

---

## Architecture

```text
React Frontend
      |
      | HTTP / JSON
      v
FastAPI Backend
      |
      v
AI Agent
      |
      +----------------------+
      |                      |
      v                      v
Policy Retrieval         Ticket Tools
      |                      |
      v                      v
policies.json       demo_tickets.json