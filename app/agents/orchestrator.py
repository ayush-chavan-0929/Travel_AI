from langgraph.graph import StateGraph, END
from app.models.travel_state import TravelState
from app.agents.intent_agent import intent_agent
from app.agents.preference_agent import preference_agent, constraint_agent
from app.agents.destination_agent import destination_agent
from app.agents.travel_options_agents import transport_agent, hotel_agent, activity_agent
from app.agents.planning_agents import budget_agent, itinerary_agent
from app.agents.verification_and_booking_agents import (
    itinerary_optimizer_agent,
    verification_agent,
    replanning_agent,
    booking_agent,
    booking_verification_agent
)

def should_replan_or_approve(state: TravelState):
    """
    Decides routing based on verification output and replanning count safety.
    """
    status = state.get("verification_status", "PASS")
    replan_count = state.get("replan_count", 0)
    
    if status == "FAIL" and replan_count < 2:
        return "replan"
    return "user_approval"

def should_execute_booking(state: TravelState):
    """
    Checks if human user approved the plan.
    """
    if state.get("user_approved", False):
        return "book"
    return END

def build_travel_graph():
    """
    Constructs the end-to-end multi-agent LangGraph workflow.
    """
    workflow = StateGraph(TravelState)

    # 1. Add nodes for each specialized agent
    workflow.add_node("intent_agent", intent_agent)
    workflow.add_node("preference_agent", preference_agent)
    workflow.add_node("constraint_agent", constraint_agent)
    workflow.add_node("destination_agent", destination_agent)
    workflow.add_node("transport_agent", transport_agent)
    workflow.add_node("hotel_agent", hotel_agent)
    workflow.add_node("activity_agent", activity_agent)
    workflow.add_node("budget_agent", budget_agent)
    workflow.add_node("itinerary_agent", itinerary_agent)
    workflow.add_node("itinerary_optimizer_agent", itinerary_optimizer_agent)
    workflow.add_node("verification_agent", verification_agent)
    workflow.add_node("replanning_agent", replanning_agent)
    workflow.add_node("booking_agent", booking_agent)
    workflow.add_node("booking_verification_agent", booking_verification_agent)

    # 2. Build edges following the specification
    workflow.set_entry_point("intent_agent")
    workflow.add_edge("intent_agent", "preference_agent")
    workflow.add_edge("preference_agent", "constraint_agent")
    workflow.add_edge("constraint_agent", "destination_agent")
    workflow.add_edge("destination_agent", "transport_agent")
    workflow.add_edge("transport_agent", "hotel_agent")
    workflow.add_edge("hotel_agent", "activity_agent")
    workflow.add_edge("activity_agent", "budget_agent")
    workflow.add_edge("budget_agent", "itinerary_agent")
    workflow.add_edge("itinerary_agent", "itinerary_optimizer_agent")
    workflow.add_edge("itinerary_optimizer_agent", "verification_agent")

    # 3. Conditional Verification edge (Verification -> Replan OR Human Approval)
    workflow.add_conditional_edges(
        "verification_agent",
        should_replan_or_approve,
        {
            "replan": "replanning_agent",
            "user_approval": END
        }
    )

    # If replanning occurred, re-evaluate budget & itinerary
    workflow.add_edge("replanning_agent", "budget_agent")

    # Separate branch for booking execution
    workflow.add_edge("booking_agent", "booking_verification_agent")
    workflow.add_edge("booking_verification_agent", END)

    app_graph = workflow.compile()
    return app_graph

# Global compiled graph instance
travel_agent_graph = build_travel_graph()
