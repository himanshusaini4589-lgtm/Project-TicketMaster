import requests
import json
from langchain.tools import tool
from backend.config import TICKETMASTER_API_KEY

BASE_URL = "https://app.ticketmaster.com/discovery/v2/"

@tool
def search_events(keyword: str = "", city: str = "", start_date_time: str = "") -> str:
    """
    Search Ticketmaster for live events matching keyword, city, or date.
    Args:
        keyword: Event name or artist (e.g. 'Coldplay', 'comedy', 'music')
        city: City name (e.g. 'London', 'Manchester')
        start_date_time: ISO date string (e.g. '2026-09-18T00:00:00Z')
    """
    url = f"{BASE_URL}events.json"
    params = {
        "apikey": TICKETMASTER_API_KEY,
        "size": 5
    }
    if keyword:
        params["keyword"] = keyword
    if city:
        params["city"] = city
    if start_date_time:
        params["startDateTime"] = start_date_time

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        events = data.get("_embedded", {}).get("events", [])
        if not events:
            return "No events found matching your criteria."

        results = []
        for item in events:
            venue = item.get("_embedded", {}).get("venues", [{}])[0]
            price_ranges = item.get("priceRanges", [{}])[0]
            
            event_info = {
                "id": item.get("id"),
                "name": item.get("name"),
                "url": item.get("url"),
                "date": item.get("dates", {}).get("start", {}).get("localDate"),
                "time": item.get("dates", {}).get("start", {}).get("localTime"),
                "venue": venue.get("name"),
                "city": venue.get("city", {}).get("name"),
                "price_min": price_ranges.get("min"),
                "price_max": price_ranges.get("max"),
                "currency": price_ranges.get("currency", "GBP")
            }
            results.append(event_info)

        return json.dumps(results, indent=2)
    except Exception as err:
        return f"Error fetching Ticketmaster events: {err}"


@tool
def get_event_details(event_id: str) -> str:
    """
    Get detailed information about a specific event using its Ticketmaster ID.
    Args:
        event_id: The unique Ticketmaster event ID string.
    """
    url = f"{BASE_URL}events/{event_id}.json"
    params = {"apikey": TICKETMASTER_API_KEY}

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        if "id" not in data:
            return f"Event ID {event_id} not found."
            
        venue = data.get("_embedded", {}).get("venues", [{}])[0]
        price_ranges = data.get("priceRanges", [{}])[0]

        details = {
            "id": data.get("id"),
            "name": data.get("name"),
            "url": data.get("url"),
            "date": data.get("dates", {}).get("start", {}).get("localDate"),
            "time": data.get("dates", {}).get("start", {}).get("localTime"),
            "venue": venue.get("name"),
            "address": venue.get("address", {}).get("line1"),
            "city": venue.get("city", {}).get("name"),
            "price_range": f"{price_ranges.get('min')} - {price_ranges.get('max')} {price_ranges.get('currency', 'GBP')}"
        }
        return json.dumps(details, indent=2)
    except Exception as err:
        return f"Error fetching event details: {err}"


@tool
def proceed_to_booking(event_name: str, event_url: str) -> str:
    """
    Generates the official Ticketmaster ticket purchase URL for the selected event.
    THIS OPERATION REQUIRES HUMAN APPROVAL BEFORE EXECUTION.
    Args:
        event_name: Name of the event user wants to book.
        event_url: Direct Ticketmaster purchase URL.
    """
    return f"You have approved this event. Complete your purchase on Ticketmaster here: {event_url}"