# Tool schemas used by the agent
# They describe the available Python functions and their required arguments.
# The schemas do not run the functions themselves.



policy_tool = {
    "type": "function",
    "function": {
        "name": "search_it_policy",

        "description": (
            "Search the company IT policy knowledge base. "
            "Use this for questions about IT rules, procedures, "
            "VPN access, password resets, docking-station support, "
            "equipment replacement, or other IT policy information. "
            "Do not use this for looking up an existing support ticket."
        ),

        "parameters": {
            "type": "object",

            "properties": {
                "query": {
                    "type": "string",

                    "description": (
                        "A concise search query describing the "
                        "IT policy information the user needs."
                    )
                }
            },

            "required": [
                "query"
            ],

            "additionalProperties": False
        },

        "strict": True
    }
}

# Ticket creation tool

create_ticket_tool = {
    "type": "function",
    "function": {
        "name": "create_dock_ticket",

        "description": (
            "Create a local demo support ticket for a docking-station issue. "
            "Use this only when the user wants a ticket created and all "
            "required details are known. "
            "Ask for missing details before using this tool. "
            "Do not invent device models, issue details, or troubleshooting steps."
        ),

        "parameters": {
            "type": "object",

            "properties": {
                "laptop_model": {
                    "type": "string",
                    "description": (
                        "The laptop model provided by the user."
                    )
                },

                "docking_station_model": {
                    "type": "string",
                    "description": (
                        "The docking-station model provided by the user."
                    )
                },

                "issue_description": {
                    "type": "string",
                    "description": (
                        "A description of the issue reported by the user."
                    )
                },

                "troubleshooting_steps": {
                    "type": "string",
                    "description": (
                        "Troubleshooting steps already attempted by the user "
                        "and the result of those steps."
                    )
                }
            },

            "required": [
                "laptop_model",
                "docking_station_model",
                "issue_description",
                "troubleshooting_steps"
            ],

            "additionalProperties": False
        },

        "strict": True
    }
}

# Ticket lookup tool

lookup_ticket_tool = {
    "type": "function",
    "function": {
        "name": "get_ticket",

        "description": (
            "Look up a local demo support ticket by its ticket ID. "
            "Use this when the user asks for the status or details "
            "of an existing ticket. "
            "Ask for the ticket ID if it cannot be determined "
            "from the conversation."
        ),

        "parameters": {
            "type": "object",

            "properties": {
                "ticket_id": {
                    "type": "string",
                    "description": (
                        "The ticket ID, such as DEMO-0007."
                    )
                }
            },

            "required": [
                "ticket_id"
            ],

            "additionalProperties": False
        },

        "strict": True
    }
}

# Tools the model can choose from

assistant_tools = [
    policy_tool,
    create_ticket_tool,
    lookup_ticket_tool
]