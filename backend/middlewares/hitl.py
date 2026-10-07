from langchain.agents.middleware import HumanInTheLoopMiddleware

def build_hitl_middleware() -> HumanInTheLoopMiddleware:
    return HumanInTheLoopMiddleware(
        interrupt_on={
            "search_events": False,
            "get_event_details": False,
            "proceed_to_booking": {
                "allowed_decisions": ["approve", "reject"],
                "description": "Provide the official Ticketmaster booking URL for the selected event"
            }
        },
        description_prefix="Human approval required before revealing booking URL"
    )