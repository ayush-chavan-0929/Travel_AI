import uuid
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional

from app.models.travel_state import TravelState
from app.agents.orchestrator import travel_agent_graph
from app.agents.verification_and_booking_agents import booking_agent, booking_verification_agent
from app.database.db import save_trip, get_trip, save_booking

app = FastAPI(
    title="Travel_AI Multi-Agent API",
    description="Agentic AI-Powered Intelligent Travel Planning and Booking Assistant built with LangGraph & Free APIs",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PlanTripRequest(BaseModel):
    query: str

class ReplanRequest(BaseModel):
    new_budget: Optional[float] = None
    new_duration: Optional[int] = None

class ApproveBookingRequest(BaseModel):
    approved: bool

@app.get("/")
def health_check():
    return {
        "status": "online",
        "service": "Travel_AI Multi-Agent Platform",
        "framework": "LangGraph",
        "version": "1.0.0"
    }

@app.post("/api/v1/travel/plan")
def plan_trip(req: PlanTripRequest):
    trip_id = f"TRIP-{uuid.uuid4().hex[:8].upper()}"
    
    initial_state: TravelState = {
        "user_query": req.query,
        "replan_count": 0,
        "agent_logs": []
    }
    
    final_state = travel_agent_graph.invoke(initial_state)
    save_trip(trip_id, final_state, status="AWAITING_APPROVAL")
    
    return {
        "trip_id": trip_id,
        "status": "PLANNED",
        "state": final_state
    }

@app.get("/api/v1/travel/{trip_id}")
def get_trip_details(trip_id: str):
    state = get_trip(trip_id)
    if not state:
        raise HTTPException(status_code=404, detail="Trip not found")
    return {
        "trip_id": trip_id,
        "state": state
    }

@app.post("/api/v1/travel/{trip_id}/replan")
def replan_trip(trip_id: str, req: ReplanRequest):
    state = get_trip(trip_id)
    if not state:
        raise HTTPException(status_code=404, detail="Trip not found")
        
    if req.new_budget is not None:
        state["budget"] = req.new_budget
    if req.new_duration is not None:
        state["duration_days"] = req.new_duration
        
    state["user_query"] += f" (Adjusted: budget={req.new_budget})"
    state["replan_count"] = 0
    
    # Re-run through workflow
    updated_state = travel_agent_graph.invoke(state)
    save_trip(trip_id, updated_state, status="REPLANNED_AWAITING_APPROVAL")
    
    return {
        "trip_id": trip_id,
        "status": "REPLANNED",
        "state": updated_state
    }

@app.post("/api/v1/travel/{trip_id}/approve")
def approve_and_book(trip_id: str, req: ApproveBookingRequest):
    state = get_trip(trip_id)
    if not state:
        raise HTTPException(status_code=404, detail="Trip not found")
        
    if not req.approved:
        return {"trip_id": trip_id, "status": "REJECTED_OR_CANCELLED"}
        
    state["user_approved"] = True
    
    # Trigger Booking Agent & Verification Agent
    bkg_res = booking_agent(state)
    state.update(bkg_res)
    
    verif_res = booking_verification_agent(state)
    state.update(verif_res)
    
    # Save bookings into database
    for b in state.get("bookings", []):
        save_booking(trip_id, b)
        
    save_trip(trip_id, state, status="CONFIRMED")
    
    return {
        "trip_id": trip_id,
        "status": "CONFIRMED",
        "final_package": state.get("final_package")
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
