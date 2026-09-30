from src.tickets import load_tickets, get_ticket


# Basic tests for the local ticket functions.

def test_load_tickets_returns_list():
    # load_tickets() should return a list even when no tickets are saved.
    tickets = load_tickets()

    assert isinstance(tickets, list)


def test_existing_ticket_lookup():
    # Use a known demo ticket for the lookup test.
    result = get_ticket("DEMO-0007")

    assert result["ticket_id"] == "DEMO-0007"
    assert result["status"] == "open"


def test_missing_ticket_lookup():
    # A missing ticket ID should return an error instead of crashing.
    result = get_ticket("DEMO-9999")

    assert "error" in result
    assert result["error"] == "Ticket DEMO-9999 was not found."