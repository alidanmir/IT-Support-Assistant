import { useState } from "react";
import type { FormEvent } from "react";

import "./App.css";

type Ticket = {
  ticket_id: string;
  status: string;
  laptop_model: string;
  docking_station_model: string;
  issue_description: string;
  troubleshooting_steps: string;
};

type Message = {
  role: "user" | "assistant";
  content: string;
  sourceId?: string | null;
  ticket?: Ticket | null;
};

type ChatResponse = {
  response: string;
  session_id: string;
  source_id: string | null;
  ticket: Ticket | null;
};

const API_URL = "http://127.0.0.1:8000/chat";

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  async function sendMessage(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const question = input.trim();

    if (!question || isLoading) {
      return;
    }

    setMessages((currentMessages) => [
      ...currentMessages,
      {
        role: "user",
        content: question,
      },
    ]);

    setInput("");
    setIsLoading(true);

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question,
          session_id: sessionId,
        }),
      });

      if (!response.ok) {
        throw new Error("The server returned an error.");
      }

      const data: ChatResponse = await response.json();

      setSessionId(data.session_id);

      setMessages((currentMessages) => [
        ...currentMessages,
        {
          role: "assistant",
          content: data.response,
          sourceId: data.source_id,
          ticket: data.ticket,
        },
      ]);
    } catch (error) {
      console.error(error);

      setMessages((currentMessages) => [
        ...currentMessages,
        {
          role: "assistant",
          content:
            "I couldn't connect to the IT support server. Please try again.",
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  }

  function startNewChat() {
    setMessages([]);
    setSessionId(null);
    setInput("");
  }

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">IT</div>

          <div>
            <h1>IT Support</h1>
            <p>AI Assistant</p>
          </div>
        </div>

        <button className="new-chat-button" onClick={startNewChat}>
          + New conversation
        </button>

        <div className="sidebar-section">
          <p className="sidebar-label">Capabilities</p>

          <div className="capability">
            <span>📘</span>
            <p>IT policy questions</p>
          </div>

          <div className="capability">
            <span>🎫</span>
            <p>Ticket lookup</p>
          </div>

          <div className="capability">
            <span>🛠️</span>
            <p>Create support tickets</p>
          </div>
        </div>

        <div className="sidebar-footer">
          <span className="status-dot"></span>
          Demo environment
        </div>
      </aside>

      <main className="main">
        <header className="topbar">
          <div>
            <h2>Support Assistant</h2>
            <p>Company IT help desk</p>
          </div>
        </header>

        <section className="chat-area">
          {messages.length === 0 ? (
            <div className="welcome">
              <div className="welcome-icon">✦</div>

              <h2>How can I help?</h2>

              <p>
                Ask about company IT policies, check an existing ticket,
                or report a docking station issue.
              </p>

              <div className="suggestions">
                <button
                  onClick={() =>
                    setInput(
                      "Can I buy my own replacement docking station?"
                    )
                  }
                >
                  Can I buy my own replacement dock?
                </button>

                <button
                  onClick={() =>
                    setInput("What is the status of ticket DEMO-0010?")
                  }
                >
                  Check DEMO-0010
                </button>

                <button
                  onClick={() =>
                    setInput(
                      "Create a support ticket. My external monitor keeps disconnecting."
                    )
                  }
                >
                  Report a monitor issue
                </button>
              </div>
            </div>
          ) : (
            <div className="messages">
              {messages.map((message, index) => (
                <div
                  className={`message-row ${message.role}`}
                  key={index}
                >
                  <div className="message-avatar">
                    {message.role === "user" ? "U" : "IT"}
                  </div>

                  <div className="message-content">
                    <span className="message-name">
                      {message.role === "user"
                        ? "You"
                        : "IT Support Assistant"}
                    </span>

                    <div className="message-bubble">
                      {message.content}

                      {message.sourceId && (
                        <div className="source-section">
                          <span className="source-label">
                            Policy source
                          </span>

                          <span className="source-badge">
                            {message.sourceId}
                          </span>
                        </div>
                      )}
                    </div>

                    {message.ticket && (
                      <div className="ticket-card">
                        <div className="ticket-header">
                          <div>
                            <span className="ticket-label">
                              Support ticket
                            </span>

                            <h3>{message.ticket.ticket_id}</h3>
                          </div>

                          <span
                            className={`ticket-status ${message.ticket.status.toLowerCase()}`}
                          >
                            {message.ticket.status}
                          </span>
                        </div>

                        <div className="ticket-grid">
                          <div className="ticket-field">
                            <span>Laptop</span>
                            <strong>
                              {message.ticket.laptop_model}
                            </strong>
                          </div>

                          <div className="ticket-field">
                            <span>Docking station</span>
                            <strong>
                              {message.ticket.docking_station_model}
                            </strong>
                          </div>

                          <div className="ticket-field full-width">
                            <span>Issue</span>
                            <strong>
                              {message.ticket.issue_description}
                            </strong>
                          </div>

                          <div className="ticket-field full-width">
                            <span>Troubleshooting</span>
                            <strong>
                              {message.ticket.troubleshooting_steps}
                            </strong>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              ))}

              {isLoading && (
                <div className="message-row assistant">
                  <div className="message-avatar">IT</div>

                  <div className="message-content">
                    <span className="message-name">
                      IT Support Assistant
                    </span>

                    <div className="message-bubble loading">
                      <span className="loading-dot"></span>
                      <span className="loading-dot"></span>
                      <span className="loading-dot"></span>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </section>

        <div className="input-container">
          <form className="chat-form" onSubmit={sendMessage}>
            <input
              value={input}
              onChange={(event) => setInput(event.target.value)}
              placeholder="Ask an IT support question..."
              disabled={isLoading}
            />

            <button
              type="submit"
              disabled={isLoading || !input.trim()}
            >
              Send
            </button>
          </form>

          <p className="disclaimer">
            Demo assistant — tickets are stored locally and are not sent
            to a real IT department.
          </p>
        </div>
      </main>
    </div>
  );
}

export default App;