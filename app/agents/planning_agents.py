from typing import Dict, Any, List
from app.models.travel_state import TravelState

def budget_agent(state: TravelState) -> Dict[str, Any]:
    """
    Computes total estimated expenditure across transport, accommodation,
    food, activities, local transit, and safety contingency buffer.
    """
    duration = state.get("duration_days", 5)
    travellers = state.get("travellers", 4)
    user_budget = state.get("budget", 60000.0)
    
    selected_transport = state.get("selected_transport", {})
    selected_hotel = state.get("selected_hotel", {})
    selected_activities = state.get("selected_activities", [])

    transport_cost = selected_transport.get("total_price", 16800.0)
    hotel_cost = selected_hotel.get("total_price", 14400.0)
    
    activities_cost = sum(act.get("total_cost", 0.0) for act in selected_activities)
    
    # Food estimate: ~₹400-500 per person per day (budget-friendly beach shacks & local dining)
    food_cost = (500.0 if user_budget >= 55000 else 400.0) * travellers * duration
    
    # Local transport (scooter / car rental / cabs)
    local_transport_cost = (800.0 if user_budget >= 55000 else 600.0) * duration
    
    # Contingency buffer
    emergency_buffer = 3000.0 if user_budget >= 55000 else 2000.0

    total_cost = transport_cost + hotel_cost + activities_cost + food_cost + local_transport_cost + emergency_buffer

    breakdown = {
        "Transportation": transport_cost,
        "Hotel": hotel_cost,
        "Activities": activities_cost,
        "Food & Dining": food_cost,
        "Local Transport": local_transport_cost,
        "Contingency Buffer": emergency_buffer
    }

    budget_status = "WITHIN_BUDGET" if total_cost <= user_budget else "EXCEEDED"

    logs = state.get("agent_logs", [])
    logs.append({
        "agent": "BudgetAgent",
        "action": f"Calculated Total Cost: ₹{total_cost:,.0f} vs Budget ₹{user_budget:,.0f} ({budget_status})"
    })

    return {
        "budget_breakdown": breakdown,
        "total_estimated_cost": total_cost,
        "budget_status": budget_status,
        "agent_logs": logs
    }


def itinerary_agent(state: TravelState) -> Dict[str, Any]:
    """
    Constructs a geographically-clustered, day-by-day travel itinerary.
    """
    origin = state.get("origin", "Mumbai")
    destination = state.get("destination", "Goa")
    duration = state.get("duration_days", 5)
    selected_transport = state.get("selected_transport", {})
    selected_hotel = state.get("selected_hotel", {})

    hotel_name = selected_hotel.get("name", "Beach Resort")
    transport_mode = selected_transport.get("mode", "Flight")
    rag_context = state.get("rag_context", "")
    weather = state.get("weather_info", {})

    from app.tools.llm import get_gemini_llm
    llm = get_gemini_llm()
    custom_gemini_title = None
    if llm:
        try:
            p = f"Write a catchy 5-word trip title for a {duration}-day trip to {destination} for {travellers} people with {weather.get('temperature', '28C')} weather. Output ONLY the title."
            resp = llm.invoke(p)
            custom_gemini_title = resp.content.strip().replace('"', '')
        except Exception:
            pass

    # Template day schedule optimized by area
    itinerary = []
    
    # Day 1: Arrival & North Goa Beaches
    itinerary.append({
        "day": 1,
        "title": f"Arrival & Relaxed Sunset by the Shore",
        "area": "North Goa (Candolim / Baga)",
        "morning": f"Depart from {origin} to {destination} via {transport_mode}. Land and transfer to hotel.",
        "afternoon": f"Check-in at {hotel_name}. Unpack, freshen up, and enjoy resort amenities.",
        "evening": "Stroll along Baga Beach. Witness the vibrant beach shacks and sunset.",
        "night": "Dinner at Britto's or beachside seafood shack with acoustic live music.",
        "estimated_day_cost": 2500.0
    })

    # Day 2: Water Sports & Epic Nightlife
    itinerary.append({
        "day": 2,
        "title": "Thrilling Water Sports & Nightlife",
        "area": "Baga & Calangute",
        "morning": "Parasailing, Jet Skiing, and Banana boat rides at Baga Beach.",
        "afternoon": "Lunch at Souza Lobo, followed by beach relaxation and swimming.",
        "evening": "Visit Calangute market for souvenirs and beachwear shopping.",
        "night": "Party night at Tito's Lane and Club Cabana (Arpora hill).",
        "estimated_day_cost": 4500.0
    })

    # Day 3: Heritage & Sunset Viewpoints
    itinerary.append({
        "day": 3,
        "title": "Iconic Forts, Cliffs & Beach Vibes",
        "area": "Vagator & Anjuna",
        "morning": "Visit Chapora Fort ('Dil Chahta Hai' spot) and admire the Ozran cliff views.",
        "afternoon": "Lunch at Thalassa Greek taverna or Curlies Shack on Anjuna Beach.",
        "evening": "Sunset cocktails at Little Vagator rocky beach.",
        "night": "Trance beach lounge or quiet dinner at German Bakery Anjuna.",
        "estimated_day_cost": 3000.0
    })

    if duration >= 4:
        # Day 4: South Goa or Serene Escapes
        itinerary.append({
            "day": 4,
            "title": "Heritage & Scenic South Goa Discovery",
            "area": "Old Goa & South Beaches",
            "morning": "Visit Old Goa Churches (Basilica of Bom Jesus, Se Cathedral).",
            "afternoon": "Scenic coastal drive down to Palolem Beach; lunch by the bay.",
            "evening": "Boat ride for dolphin spotting or kayak at Palolem.",
            "night": "Traditional Goan fish-curry-thali dinner in Panaji Latin Quarter (Fontainhas).",
            "estimated_day_cost": 3200.0
        })

    if duration >= 5:
        # Day 5: Farewell & Departure
        itinerary.append({
            "day": 5,
            "title": "Souvenir Shopping & Return Journey",
            "area": "Panaji & Airport/Station",
            "morning": "Leisurely breakfast at hotel, pack luggage and complete check-out.",
            "afternoon": "Quick shopping for Goan feni, cashews, and handicrafts in Panjim.",
            "evening": f"Transfer to airport/railway station for departure return to {origin}.",
            "night": f"Safe arrival back in {origin} with unforgettable memories.",
            "estimated_day_cost": 1500.0
        })

    logs = state.get("agent_logs", [])
    logs.append({
        "agent": "ItineraryAgent",
        "action": f"Generated cohesive {duration}-day schedule clustered geographically by North/South Goa"
    })

    return {
        "itinerary": itinerary,
        "agent_logs": logs
    }
