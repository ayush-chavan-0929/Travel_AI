from typing import Dict, Any, List
from app.models.travel_state import TravelState

def preference_agent(state: TravelState) -> Dict[str, Any]:
    """
    Extracts user soft preferences (interests, accommodation style, transport style).
    """
    query = state.get("user_query", "").lower()
    
    interests = []
    if "beach" in query:
        interests.append("beaches")
    if "nightlife" in query or "party" in query or "club" in query:
        interests.append("nightlife")
    if "water sport" in query or "watersport" in query or "parasailing" in query or "scuba" in query:
        interests.append("water sports")
    if "sightseeing" in query or "fort" in query or "history" in query:
        interests.append("sightseeing")
    if "food" in query or "culinary" in query or "seafood" in query:
        interests.append("culinary")
        
    if not interests:
        interests = ["beaches", "nightlife", "water sports"]

    hotel_pref = "3-star"
    if "4-star" in query or "luxury" in query or "resort" in query:
        hotel_pref = "4-star"
    elif "2-star" in query or "budget hotel" in query or "hostel" in query:
        hotel_pref = "2-star"

    transport_pref = "Flight"
    if "train" in query:
        transport_pref = "Train"
    elif "bus" in query:
        transport_pref = "Bus"

    preferences = {
        "interests": interests,
        "hotel_preference": hotel_pref,
        "transport_preference": transport_pref
    }

    logs = state.get("agent_logs", [])
    logs.append({
        "agent": "PreferenceAgent",
        "action": f"Identified interests: {interests}, Hotel: {hotel_pref}, Transport: {transport_pref}"
    })

    return {
        "preferences": preferences,
        "soft_preferences": interests,
        "agent_logs": logs
    }


def constraint_agent(state: TravelState) -> Dict[str, Any]:
    """
    Formulates and locks hard boundaries: maximum budget, duration, and group count.
    """
    budget = state.get("budget", 60000.0)
    duration = state.get("duration_days", 5)
    travellers = state.get("travellers", 4)

    hard_constraints = {
        "max_budget": budget,
        "duration_days": duration,
        "travellers_count": travellers,
        "must_include_safety_buffer": True
    }

    logs = state.get("agent_logs", [])
    logs.append({
        "agent": "ConstraintAgent",
        "action": f"Configured hard constraints: Max Budget ₹{budget:,.0f}, {duration} days, {travellers} pax"
    })

    return {
        "hard_constraints": hard_constraints,
        "agent_logs": logs
    }
