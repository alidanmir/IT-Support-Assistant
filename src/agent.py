# Handles the conversation between the user, the model, and our Python tools.

# This file sends the chat history to the model, lets it choose tools,
# runs the matching Python function, and returns the final reply.

# The model only requests a tool. Python is what actually runs the function.

import json


from src.retrieval import search_it_policy
from src.tickets import create_dock_ticket, get_ticket
from src.tools import assistant_tools


# Instructions the model follows
SYSTEM_PROMPT = """
You are an IT support assistant.

POLICY QUESTIONS:
For company IT policy questions, use search_it_policy.
Base policy claims only on information returned by that tool.
Cite the returned source_id when using policy information.
If the returned policy does not contain the answer, say so.
Do not invent policies, links, procedures, timelines, or approvals.
Similarity is a retrieval score, not proof that the answer exists.

DEMO TICKETS:
Use create_dock_ticket when the user asks to create a
docking-station support ticket and all required information is known.

Required information:
- laptop model
- docking-station model
- issue description
- troubleshooting steps already attempted

Use information already provided earlier in the conversation.
Ask only for information that is still missing.
Do not invent missing details.

Only confirm ticket creation after create_dock_ticket returns
a ticket_id.

Clearly state that created tickets are local demos and are not
submitted to real IT.

TICKET LOOKUP:
Use get_ticket whenever the user asks for the status or details
of an existing ticket.

Use a ticket ID supplied by the user or clearly identifiable
from conversation history.

If no ticket ID can be determined, ask the user for it.
Never invent a ticket ID or ticket status.
"""

# Run the Python function chosen by the model

def execute_tool(
        tool_name,
        arguments,
        client,
        policies
):

    """
    Connect a tool name selected by the LLM
    to the real Python function that performs the action.
    """

    if tool_name == "search_it_policy":
        return search_it_policy(
            client,
            policies,
            **arguments
        )

    if tool_name == "create_dock_ticket":
        return create_dock_ticket(
            **arguments
        )

    if tool_name == "get_ticket":
        return get_ticket(
            **arguments
        )

    return {
        "error": f"Unknown tool requested: {tool_name}"
    }


# Main chat loop
def support_chat(
    question,
    history,
    client,
    policies,
    max_tool_rounds=3
):
    """
    Process one user message through the AI agent.

    The function:
    1. Sends the user's message and conversation history to the LLM.
    2. Gives the LLM access to our available tools.
    3. Executes any tool the LLM requests.
    4. Sends the tool result back to the LLM.
    5. Returns the final assistant response.

    Parameters:
        question:
            The newest message from the user.

        history:
            Previous conversation messages.

        client:
            The OpenAI client created elsewhere.

        policies:
            Indexed policies containing embeddings.

        max_tool_rounds:
            Maximum number of tool-use cycles allowed
            during one user request.
    """

    
    # Build the messages sent to the model

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ] + history + [
        {
            "role": "user",
            "content": question
        }
    ]


    # Let the model use tools if needed

    # A request may need more than one tool step.

    for _ in range(max_tool_rounds):
        # Send the current conversation to the model.
        # assistant_tools is the list of tools the model can choose from.
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages,
            tools=assistant_tools,
            parallel_tool_calls=False
        )

        message = response.choices[0].message


        # Keep the model response in the conversation history.

        # If it requested a tool, the tool result has to come after this message.

        messages.append(
            message.model_dump(exclude_none=True)
        )

        # No tool call means the model is ready to give its final answer.

        if not message.tool_calls:

            # Save the updated history without the system prompt.
            history[:] = messages[1:]

            # Return the final text response.
            return message.content

        # If a tool was requested, run it.

        # Handle each tool call from the model.
        for tool_call in message.tool_calls:

            # Tool arguments arrive as JSON text.

            # Example:
            # {"ticket_id": "DEMO-0007"}

            # json.loads() turns that JSON text into a Python dictionary.
            arguments = json.loads(
                tool_call.function.arguments
            )

            # Run the Python function that matches the requested tool.
            tool_result = execute_tool(
                tool_call.function.name,
                arguments,
                client,
                policies
            )

            # Give the tool result back to the model so it can use it in the reply.

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(tool_result)
            })

    # Stop if the model reaches the tool-use limit.

    history[:] = messages[1:]

    return (
        "I could not complete the request because "
        "too many tool actions were required."
    )