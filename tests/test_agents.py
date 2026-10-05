import sys
import os

# Add root directory to python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.agents.orchestrator import travel_agent_graph
from app.agents.verification_and_booking_agents import booking_agent, booking_verification_agent

def test_complete_travel_workflow():
    print("==================================================================")
    print("🧪 TEST 1: Running LangGraph Multi-Agent Travel Planner Workflow")
    print("==================================================================")
    
    query = "Plan a 5-day trip to Goa from Mumbai for 4 people. My budget is ₹60,000. We want beaches, nightlife and water sports. Prefer 3-star hotels."
    initial_state = {
        "user_query": query,
        "replan_count": 0,
        "agent_logs": []
    }
    
    result = travel_agent_graph.invoke(initial_state)
    
    assert result["origin"] == "Mumbai"
    assert result["destination"] == "Goa"
    assert result["duration_days"] == 5
    assert result["travellers"] == 4
    assert result["budget"] == 60000.0
    assert result["verification_status"] == "PASS"
    assert len(result["itinerary"]) == 5
    assert result["total_estimated_cost"] <= 60000.0
    
    print(f"✅ Workflow Execution Succeeded!")
    print(f"Origin -> Destination: {result['origin']} -> {result['destination']}")
    print(f"Estimated Cost: ₹{result['total_estimated_cost']:,.0f} (Budget: ₹{result['budget']:,.0f})")
    print(f"Transport: {result['selected_transport']['provider']} ({result['selected_transport']['mode']})")
    print(f"Hotel: {result['selected_hotel']['name']} ({result['selected_hotel']['category']})")
    print(f"Days in Itinerary: {len(result['itinerary'])}")
    print(f"Weather: {result['weather_info']['temperature']} - {result['weather_info']['condition']}")

    print("\n==================================================================")
    print("🧪 TEST 2: Testing Replanning on Reduced Budget (₹50,000)")
    print("==================================================================")
    
    replanned_query = "Actually, my budget is only ₹50,000."
    new_state = dict(result)
    new_state["budget"] = 50000.0
    new_state["user_query"] = replanned_query
    new_state["replan_count"] = 0
    
    replanned_result = travel_agent_graph.invoke(new_state)
    assert replanned_result["total_estimated_cost"] <= 50000.0
    print(f"✅ Re-planning Passed! Cost downscaled to: ₹{replanned_result['total_estimated_cost']:,.0f}")
    print(f"Adjusted Transport: {replanned_result['selected_transport']['provider']} ({replanned_result['selected_transport']['mode']})")

    print("\n==================================================================")
    print("🧪 TEST 3: Testing Human Approval and Booking Execution")
    print("==================================================================")
    
    replanned_result["user_approved"] = True
    bkg_res = booking_agent(replanned_result)
    replanned_result.update(bkg_res)
    verif_res = booking_verification_agent(replanned_result)
    replanned_result.update(verif_res)
    
    pkg = replanned_result["final_package"]
    assert pkg["package_status"] == "READY_FOR_TRAVEL"
    assert len(pkg["confirmed_bookings"]) >= 3
    print(f"✅ Booking Confirmed with {len(pkg['confirmed_bookings'])} items:")
    for b in pkg["confirmed_bookings"]:
        print(f"  - [{b['booking_type']}] Ref: {b['reference_number']} | Amount: ₹{b['amount']:,.0f}")
        
    print("\n🎉 ALL 3 AGENTIC SYSTEM TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    test_complete_travel_workflow()
