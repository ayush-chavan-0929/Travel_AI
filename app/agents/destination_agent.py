from typing import Dict, Any
from app.models.travel_state import TravelState
from app.tools.apis import FreeWeatherTool, FreeMapsTool
from app.rag.retriever import TravelRAGRetriever

retriever = TravelRAGRetriever()

def destination_agent(state: TravelState) -> Dict[str, Any]:
    """
    Researches destination weather using the free Open-Meteo API,
    retrieves geographic distances from OpenStreetMap, and pulls RAG travel knowledge.
    """
    origin = state.get("origin", "Mumbai")
    destination = state.get("destination", "Goa")
    
    # 1. Free live weather call
    weather = FreeWeatherTool.get_weather(destination)
    
    # 2. Free distance calculation
    route_info = FreeMapsTool.get_route_info(origin, destination)
    
    # 3. RAG Retrieval from local knowledge base
    rag_query = f"{destination} beaches nightlife water sports budget"
    rag_context = retriever.retrieve(rag_query, top_k=2)

    destination_info = {
        "destination": destination,
        "region_focus": "North Goa (Optimal for nightlife, water sports, and beach shacks)",
        "weather": weather,
        "route_info": route_info
    }

    logs = state.get("agent_logs", [])
    logs.append({
        "agent": "DestinationAgent",
        "action": f"Researched {destination}: Weather is {weather['temperature']} ({weather['condition']}). Distance: {route_info['approx_distance_km']} km."
    })

    return {
        "weather_info": weather,
        "destination_info": destination_info,
        "rag_context": rag_context,
        "agent_logs": logs
    }
