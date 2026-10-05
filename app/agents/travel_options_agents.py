from typing import Dict, Any, List
from app.models.travel_state import TravelState
from app.tools.apis import MockTravelAPI

def transport_agent(state: TravelState) -> Dict[str, Any]:
    """
    Finds and ranks transportation options considering group size and budget.
    """
    origin = state.get("origin", "Mumbai")
    destination = state.get("destination", "Goa")
    travellers = state.get("travellers", 4)
    budget = state.get("budget", 60000.0)
    preferences = state.get("preferences", {})
    preferred_mode = preferences.get("transport_preference", "Flight")

    transports = MockTravelAPI.search_transports(origin, destination, travellers)
    
    # Selection logic based on budget headroom
    selected = None
    if budget < 55000.0:
        # Pick high comfort train or sleeper bus for budget efficiency
        for t in transports:
            if t["mode"] == "Train":
                selected = t
                break
    else:
        # Pick flight or user preferred mode
        for t in transports:
            if t["mode"].lower() == preferred_mode.lower():
                selected = t
                break
                
    if not selected and transports:
        selected = transports[0]

    logs = state.get("agent_logs", [])
    logs.append({
        "agent": "TransportAgent",
        "action": f"Selected {selected['mode']} via {selected['provider']} for ₹{selected['total_price']:,.0f} ({travellers} pax)"
    })

    return {
        "transport_options": transports,
        "selected_transport": selected,
        "agent_logs": logs
    }


def hotel_agent(state: TravelState) -> Dict[str, Any]:
    """
    Searches and selects accommodations based on user preference and budget.
    """
    destination = state.get("destination", "Goa")
    duration = state.get("duration_days", 5)
    nights = max(1, duration - 1)
    travellers = state.get("travellers", 4)
    budget = state.get("budget", 60000.0)
    preferences = state.get("preferences", {})
    hotel_pref = preferences.get("hotel_preference", "3-star")

    hotels = MockTravelAPI.search_hotels(destination, nights, travellers, hotel_pref)
    
    # Dynamic selection: If budget <= 50,000, choose economical hotel
    selected = None
    if budget <= 50000.0:
        for h in hotels:
            if "BloomSuites" in h["name"] or "Oceanic" in h["name"]:
                selected = h
                break
    else:
        for h in hotels:
            if hotel_pref.lower() in h["category"].lower():
                selected = h
                break

    if not selected and hotels:
        selected = hotels[0]

    logs = state.get("agent_logs", [])
    logs.append({
        "agent": "HotelAgent",
        "action": f"Selected '{selected['name']}' ({selected['category']}) in {selected['location']} for ₹{selected['total_price']:,.0f} ({nights} nights)"
    })

    return {
        "hotel_options": hotels,
        "selected_hotel": selected,
        "agent_logs": logs
    }


def activity_agent(state: TravelState) -> Dict[str, Any]:
    """
    Recommends activities matching user interests (beaches, nightlife, water sports).
    """
    destination = state.get("destination", "Goa")
    travellers = state.get("travellers", 4)
    budget = state.get("budget", 60000.0)
    preferences = state.get("preferences", {})
    interests = preferences.get("interests", ["beaches", "nightlife", "water sports"])

    all_activities = MockTravelAPI.search_activities(destination, interests, travellers)
    
    # Filter/Select activities
    selected_acts = []
    for act in all_activities:
        if any(cat in act["category"].lower() for cat in interests):
            selected_acts.append(act)

    # If budget is tight, prune expensive activities or trim extras
    if budget <= 50000.0 and len(selected_acts) > 3:
        selected_acts = selected_acts[:3]

    logs = state.get("agent_logs", [])
    logs.append({
        "agent": "ActivityAgent",
        "action": f"Curated {len(selected_acts)} activities tailored to {interests}"
    })

    return {
        "activity_options": all_activities,
        "selected_activities": selected_acts,
        "agent_logs": logs
    }
