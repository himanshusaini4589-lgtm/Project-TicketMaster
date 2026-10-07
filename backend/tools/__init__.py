from backend.tools.event_tools import search_events, get_event_details, proceed_to_booking

ALL_TOOLS = [
    search_events,
    get_event_details,
    proceed_to_booking,
]

def tool_catalog() -> list[dict[str, str]]:
    return [{"name": tool.name, "description": tool.description} for tool in ALL_TOOLS]