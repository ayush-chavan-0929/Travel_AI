from typing import TypedDict, List, Dict, Any, Optional
from pydantic import BaseModel, Field

class HotelOption(BaseModel):
    id: str
    name: str
    location: str
    category: str
    rating: float
    price_per_night: float
    total_price: float
    amenities: List[str] = []
    selected: bool = False

class TransportOption(BaseModel):
    id: str
    mode: str  # Flight, Train, Bus, Cab
    provider: str
    origin: str
    destination: str
    departure_time: str
    arrival_time: str
    duration: str
    price_per_person: float
    total_price: float
    comfort_rating: float
    selected: bool = False

class ActivityItem(BaseModel):
    id: str
    name: str
    category: str  # beach, adventure, cultural, nightlife, food
    location: str
    duration_hours: float
    cost_per_person: float
    total_cost: float
    timing_slot: str  # Morning, Afternoon, Evening, Night
    best_time: str = ""

class ItineraryDay(BaseModel):
    day: int
    title: str
    area: str
    morning: str
    afternoon: str
    evening: str
    night: str
    estimated_day_cost: float

class BookingConfirmation(BaseModel):
    booking_id: str
    booking_type: str  # Transport, Hotel, Activity
    provider: str
    reference_number: str
    status: str
    amount: float
    details: Dict[str, Any]

class TravelState(TypedDict, total=False):
    # User Input & Intent
    user_query: str
    origin: str
    destination: str
    duration_days: int
    travellers: int
    budget: float
    start_date: str
    
    # Preferences & Constraints
    preferences: Dict[str, Any]
    hard_constraints: Dict[str, Any]
    soft_preferences: List[str]
    missing_info: List[str]
    
    # Research Data (from tools)
    weather_info: Dict[str, Any]
    destination_info: Dict[str, Any]
    rag_context: str
    
    # Options Found
    transport_options: List[Dict[str, Any]]
    hotel_options: List[Dict[str, Any]]
    activity_options: List[Dict[str, Any]]
    
    # Selection & Optimization
    selected_transport: Optional[Dict[str, Any]]
    selected_hotel: Optional[Dict[str, Any]]
    selected_activities: List[Dict[str, Any]]
    
    # Budget breakdown
    budget_breakdown: Dict[str, float]
    total_estimated_cost: float
    budget_status: str  # "WITHIN_BUDGET" or "EXCEEDED"
    
    # Itinerary
    itinerary: List[Dict[str, Any]]
    
    # Verification & Re-planning
    verification_status: str  # "PASS", "FAIL"
    verification_issues: List[str]
    replan_count: int
    replan_reason: str
    
    # Human-in-the-loop Approval & Booking
    user_approved: bool
    booking_status: str  # "PENDING", "CONFIRMED", "FAILED"
    bookings: List[Dict[str, Any]]
    
    # Final Package & Execution Logs
    final_package: Dict[str, Any]
    agent_logs: List[Dict[str, str]]
