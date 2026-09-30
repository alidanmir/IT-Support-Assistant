import json
from pathlib import Path


# Find the project root from the location of this file.

# __file__ points to tickets.py; going up two folders reaches the project root.
BASE_DIR = Path(__file__).resolve().parent.parent

# Local JSON file used as the demo ticket database.
TICKET_FILE = BASE_DIR / "data" / "demo_tickets.json"


# Read the saved tickets

def load_tickets():
    """
    Read all existing demo tickets from the JSON file.

    Returns:
        A list of ticket dictionaries.

    If the file does not exist yet, return an empty list.
    """

    if TICKET_FILE.exists():

        # read_text() returns text, and json.loads() turns it into Python data.
        return json.loads(
            TICKET_FILE.read_text(encoding="utf-8")
        )

    return []


# Create a new ticket

def create_dock_ticket(
    laptop_model,
    docking_station_model,
    issue_description,
    troubleshooting_steps
):
    """
    Create a new local demo support ticket.

    The AI agent will eventually call this function after it has
    collected all four required pieces of information from the user.
    """

    # Put the required ticket details together.
    details = {
        "laptop_model": laptop_model,
        "docking_station_model": docking_station_model,
        "issue_description": issue_description,
        "troubleshooting_steps": troubleshooting_steps
    }

    # Reject missing, empty, or non-text values.
    for field, value in details.items():

        if not isinstance(value, str) or not value.strip():
            return {
                "error": f"Please provide {field}."
            }

    # Load the tickets that are already saved.
    saved_tickets = load_tickets()

    # Use the highest existing ticket number to create the next ID.
    # Example: "DEMO-0007" -> "0007" -> 7, so the next number is 8.
    next_number = max(
        (
            int(ticket["ticket_id"].split("-")[1])
            for ticket in saved_tickets
        ),
        default=0
    ) + 1

    # Build the new ticket record.
    ticket = {
        "ticket_id": f"DEMO-{next_number:04d}",
        "status": "open",
        **details
    }

    # Add it to the current ticket list.
    saved_tickets.append(ticket)

    # Save the updated list back to demo_tickets.json.
    TICKET_FILE.write_text(
        json.dumps(saved_tickets, indent=2),
        encoding="utf-8"
    )

    # Return the ticket so the agent can show the new ID and status.
    return ticket


# Look up a ticket

def get_ticket(ticket_id):
    """
    Find a saved ticket using its ticket ID.
    """

    # Reload the file so the lookup uses the latest saved data.
    tickets = load_tickets()

    # Normalize IDs such as " demo-0007 " to "DEMO-0007".
    normalized_id = ticket_id.strip().upper()

    # Check each saved ticket for the requested ID.
    for ticket in tickets:

        if ticket["ticket_id"] == normalized_id:
            return ticket

    # If nothing matches, return an error.
    return {
        "error": f"Ticket {normalized_id} was not found."
    }