import re
import json
from typing import Dict, Any
from app.models.travel_state import TravelState
from app.tools.llm import get_gemini_llm

def intent_agent(state: TravelState) -> Dict[str, Any]:
    """
    Parses natural language travel requests and extracts core parameters:
    origin, destination, duration, traveller count, and budget.
    Utilizes Gemini LLM if GEMINI_API_KEY is configured, with robust regex fallback.
    """
    query = state.get("user_query", "")
    q_lower = query.lower()
    
    # Defaults
    origin = state.get("origin") or "Mumbai"
    destination = state.get("destination") or "Goa"
    duration = state.get("duration_days") or 5
    travellers = state.get("travellers") or 4
    budget = state.get("budget") or 60000.0

    gemini_used = False
    llm = get_gemini_llm()
    if llm and query:
        try:
            prompt = f"""
            You are the Intent Agent for Travel_AI.
            Extract the following travel parameters from the user's request:
            - origin (city name, e.g. "Mumbai")
            - destination (city/region name, e.g. "Goa")
            - duration_days (integer, default 5)
            - travellers (integer, default 4)
            - budget (float in INR, e.g. 60000)

            Return ONLY valid JSON matching this schema with no markdown formatting:
            {{"origin": "...", "destination": "...", "duration_days": 5, "travellers": 4, "budget": 60000.0}}

            User Request: "{query}"
            """
            response = llm.invoke(prompt)
            content = response.content.strip()
            # Clean possible markdown fence
            if content.startswith("```"):
                content = re.sub(r"^```[a-zA-Z]*\n?", "", content)
                content = re.sub(r"\n?```$", "", content)
            parsed = json.loads(content)
            if parsed.get("origin"):
                origin = parsed["origin"]
            if parsed.get("destination"):
                destination = parsed["destination"]
            if parsed.get("duration_days"):
                duration = int(parsed["duration_days"])
            if parsed.get("travellers"):
                travellers = int(parsed["travellers"])
            if parsed.get("budget"):
                budget = float(parsed["budget"])
            gemini_used = True
        except Exception as e:
            # Fall back smoothly to regex pattern parsing
            pass

    if not gemini_used:
        # Regex extraction
        from_match = re.search(r"from\s+([A-Za-z]+)", query, re.IGNORECASE)
        if from_match:
            origin = from_match.group(1).capitalize()

        to_match = re.search(r"(?:to|visit)\s+([A-Za-z]+)", query, re.IGNORECASE)
        if to_match:
            dest_candidate = to_match.group(1).capitalize()
            if dest_candidate.lower() not in ["the", "a", "an"]:
                destination = dest_candidate

        day_match = re.search(r"(\d+)\s*(?:-| )?days?", query, re.IGNORECASE)
        if day_match:
            duration = int(day_match.group(1))

        traveller_match = re.search(r"(\d+)\s*(?:people|persons|travellers|friends|adults)", query, re.IGNORECASE)
        if traveller_match:
            travellers = int(traveller_match.group(1))
        elif re.search(r"for\s+(\d+)", query, re.IGNORECASE):
            travellers = int(re.search(r"for\s+(\d+)", query, re.IGNORECASE).group(1))

        cleaned_q = query.replace(",", "")
        direct_budget = re.search(r"(?:budget|under|worth)\s*(?:of|is|around)?\s*(?:₹|rs\.?|inr)?\s*(\d+)", cleaned_q, re.IGNORECASE)
        if direct_budget:
            budget = float(direct_budget.group(1))
        elif "50k" in q_lower or "50000" in q_lower:
            budget = 50000.0
        elif "60k" in q_lower or "60000" in q_lower:
            budget = 60000.0

    missing_info = []
    if not origin:
        missing_info.append("origin")
    if not destination:
        missing_info.append("destination")
    if not budget:
        missing_info.append("budget")

    engine_tag = "Gemini 1.5 Flash (Google AI)" if gemini_used else "Heuristic / Rule Engine"
    logs = state.get("agent_logs", [])
    logs.append({
        "agent": "IntentAgent",
        "action": f"[{engine_tag}] Identified trip intent: {origin} -> {destination}, {duration} days, {travellers} travellers, Budget: ₹{budget:,.0f}"
    })

    return {
        "origin": origin,
        "destination": destination,
        "duration_days": duration,
        "travellers": travellers,
        "budget": budget,
        "missing_info": missing_info,
        "agent_logs": logs
    }
