import streamlit as st
import json
import requests
from typing import Dict, Any

# Configure page layout and style
st.set_page_config(
    page_title="Travel_AI | Agentic Travel Assistant",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .agent-card {
        background-color: #F8FAFC;
        border-left: 4px solid #3B82F6;
        padding: 10px 15px;
        margin-bottom: 10px;
        border-radius: 4px;
        font-family: monospace;
        font-size: 0.9rem;
    }
    .cost-badge {
        background-color: #10B981;
        color: white;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: bold;
    }
    .day-box {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# Direct integration fallback (if FastAPI backend is running or local direct import)
from app.agents.orchestrator import travel_agent_graph
from app.agents.verification_and_booking_agents import booking_agent, booking_verification_agent
from app.database.db import save_trip, save_booking

# Initialize session states
if "trip_state" not in st.session_state:
    st.session_state.trip_state = None
if "final_package" not in st.session_state:
    st.session_state.final_package = None
if "trip_id" not in st.session_state:
    st.session_state.trip_id = None

# Sidebar Controls
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=400&q=80", use_container_width=True)
    st.title("Travel_AI Settings")
    st.caption("Powered by LangGraph & Free APIs (Open-Meteo & Gemini)")

    import os
    gemini_key_env = os.getenv("GEMINI_API_KEY", "")
    gemini_input = st.text_input(
        "🔑 Gemini API Key (Optional Free Tier):",
        value=st.session_state.get("gemini_key", gemini_key_env),
        type="password",
        help="Get a free key at https://aistudio.google.com/app/apikey"
    )
    if gemini_input:
        os.environ["GEMINI_API_KEY"] = gemini_input
        st.session_state["gemini_key"] = gemini_input
        st.success("Gemini Key Active! 🤖", icon="✨")
    else:
        st.info("No key set: using smart heuristic agent fallback.", icon="💡")
    
    st.markdown("---")
    st.subheader("💡 Example Queries")
    ex1 = "Plan a 5-day trip to Goa from Mumbai for 4 people. My budget is ₹60,000. We want beaches, nightlife and water sports. Prefer 3-star hotels."
    ex2 = "Plan a 4-day trip to Goa from Delhi for 2 people with ₹40,000 budget focusing on beaches and relaxation."
    
    if st.button("Load Goa 5-Day Plan (₹60,000)"):
        st.session_state.query_input = ex1
    if st.button("Load Goa 4-Day Plan (₹40,000)"):
        st.session_state.query_input = ex2

    st.markdown("---")
    st.markdown("**Core Agent System**:")
    st.markdown("""
    - 🔍 `Intent Agent`
    - 🎯 `Preference & Constraint Agent`
    - 🌦️ `Destination Agent (Open-Meteo)`
    - 🚆 `Transport & Hotel Agent`
    - 🏄 `Activity Agent`
    - 💰 `Budget Agent`
    - 📅 `Itinerary Optimizer`
    - 🛡️ `Verification & Replanning`
    - 🎫 `Booking & Verification Agent`
    """)

# Main UI Header
st.markdown('<div class="main-header">✈️ Travel_AI: Agentic Travel Planner & Booking Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Autonomous multi-agent trip design with constraint validation, budget optimization, and live booking simulation.</div>', unsafe_allow_html=True)

# User Query Input
default_q = st.session_state.get("query_input", "Plan a 5-day trip to Goa from Mumbai for 4 people. My budget is ₹60,000. We want beaches, nightlife and water sports. Prefer 3-star hotels.")
user_query = st.text_area("Enter your travel goal in natural language:", value=default_q, height=90)

col_plan, col_reset = st.columns([1, 5])
with col_plan:
    plan_button = st.button("🚀 Plan My Trip", type="primary", use_container_width=True)
with col_reset:
    if st.button("Clear / Reset"):
        st.session_state.trip_state = None
        st.session_state.final_package = None
        st.session_state.trip_id = None
        st.rerun()

# Execution Flow
if plan_button and user_query:
    with st.spinner("🤖 Coordinated AI agents are researching, estimating budgets, and optimizing itinerary..."):
        initial_state = {
            "user_query": user_query,
            "replan_count": 0,
            "agent_logs": []
        }
        
        # Run LangGraph Orchestrator
        result_state = travel_agent_graph.invoke(initial_state)
        st.session_state.trip_state = result_state
        st.session_state.trip_id = f"TRIP-{hash(user_query) % 1000000:06d}"
        st.session_state.final_package = None
        
        # Save to DB
        save_trip(st.session_state.trip_id, result_state, status="AWAITING_APPROVAL")

# Display Results
if st.session_state.trip_state:
    state = st.session_state.trip_state
    
    # Overview Metrics
    st.markdown("### 📊 Trip Requirements & Strategy")
    m1, m2, m3, m4, m5 = st.columns(5)
    with m1:
        st.metric("Route", f"{state.get('origin')} ➔ {state.get('destination')}")
    with m2:
        st.metric("Duration", f"{state.get('duration_days')} Days")
    with m3:
        st.metric("Travellers", f"{state.get('travellers')} Pax")
    with m4:
        st.metric("Budget Ceiling", f"₹{state.get('budget', 0):,.0f}")
    with m5:
        cost = state.get("total_estimated_cost", 0)
        st.metric("Est. Total Cost", f"₹{cost:,.0f}", delta=f"₹{state.get('budget', 0) - cost:,.0f} Saved")

    # Tabs for structured viewing
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📅 Day-by-Day Itinerary",
        "🏨 Transport & Hotels",
        "💵 Budget Breakdown",
        "🤖 Agent Trace Logs",
        "🎫 Human Approval & Booking"
    ])
    
    # TAB 1: Itinerary
    with tab1:
        st.subheader("Geographically Optimized Day-by-Day Plan")
        weather = state.get("weather_info", {})
        if weather:
            st.info(f"🌤️ **Live Destination Weather ({weather.get('destination')}):** {weather.get('temperature')} | {weather.get('condition')} | Wind: {weather.get('windspeed')} (Source: {weather.get('source')})")

        itinerary = state.get("itinerary", [])
        for day in itinerary:
            with st.container():
                st.markdown(f"""
                <div class="day-box">
                    <h4 style="margin: 0; color: #1E3A8A;">Day {day.get('day')}: {day.get('title')}</h4>
                    <p style="color: #6B7280; font-size: 0.85rem; margin-bottom: 8px;">📍 <b>Area:</b> {day.get('area')}</p>
                    <ul style="margin-bottom: 0;">
                        <li><b>Morning:</b> {day.get('morning')}</li>
                        <li><b>Afternoon:</b> {day.get('afternoon')}</li>
                        <li><b>Evening:</b> {day.get('evening')}</li>
                        <li><b>Night:</b> {day.get('night')}</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

    # TAB 2: Transport & Hotels
    with tab2:
        c_tr, c_ht = st.columns(2)
        with c_tr:
            st.subheader("Selected Transportation")
            tr = state.get("selected_transport", {})
            if tr:
                st.success(f"**{tr.get('mode')}** via **{tr.get('provider')}**")
                st.write(f"- Departure: {tr.get('departure_time')} | Arrival: {tr.get('arrival_time')}")
                st.write(f"- Duration: {tr.get('duration')} | Comfort: {tr.get('comfort_rating')}/5.0")
                st.write(f"- Total Fare: **₹{tr.get('total_price'):,.0f}** for {state.get('travellers')} people")

        with c_ht:
            st.subheader("Selected Hotel")
            ht = state.get("selected_hotel", {})
            if ht:
                st.success(f"**{ht.get('name')}** ({ht.get('category')})")
                st.write(f"- Location: {ht.get('location')} (Rating: ⭐ {ht.get('rating')})")
                st.write(f"- Amenities: {', '.join(ht.get('amenities', []))}")
                st.write(f"- Total Stay Cost: **₹{ht.get('total_price'):,.0f}**")

        st.markdown("---")
        st.subheader("Curated Activities")
        acts = state.get("selected_activities", [])
        for a in acts:
            st.markdown(f"- **{a.get('name')}** ({a.get('timing_slot')}) at *{a.get('location')}* — ₹{a.get('total_cost'):,.0f}")

    # TAB 3: Budget Breakdown
    with tab3:
        st.subheader("Financial Optimization & Breakdown")
        b_break = state.get("budget_breakdown", {})
        col_b1, col_b2 = st.columns([2, 1])
        with col_b1:
            st.table([{"Category": k, "Estimated Cost (INR)": f"₹{v:,.0f}"} for k, v in b_break.items()])
        with col_b2:
            st.metric("Total Trip Cost", f"₹{state.get('total_estimated_cost', 0):,.0f}")
            st.metric("User Budget", f"₹{state.get('budget', 0):,.0f}")
            st.success("✅ Verification Passed: Within Budget Constraints!")

    # TAB 4: Agent Logs
    with tab4:
        st.subheader("Transparent Agentic Trace Logs")
        logs = state.get("agent_logs", [])
        for log in logs:
            st.markdown(f"""
            <div class="agent-card">
                <b>[{log.get('agent')}]</b> {log.get('action')}
            </div>
            """, unsafe_allow_html=True)

    # TAB 5: Human Approval & Re-planning
    with tab5:
        st.subheader("Human-In-The-Loop Approval & Booking Simulation")
        st.write("Review the proposed trip plan above. You can either approve the package or test the replanning loop with stricter constraints.")

        c_app, c_rep = st.columns(2)
        
        with c_app:
            st.markdown("#### Option A: Approve & Book")
            if st.button("✅ Approve Plan & Generate Booking Package", type="primary", use_container_width=True):
                with st.spinner("Executing bookings with mock API provider and validating PNRs..."):
                    state["user_approved"] = True
                    bkg_res = booking_agent(state)
                    state.update(bkg_res)
                    verif_res = booking_verification_agent(state)
                    state.update(verif_res)
                    st.session_state.final_package = state.get("final_package")
                    
                    # Save bookings in SQLite
                    for b in state.get("bookings", []):
                        save_booking(st.session_state.trip_id, b)
                    save_trip(st.session_state.trip_id, state, status="CONFIRMED")
                    st.success("🎉 Trip successfully booked and confirmed!")

        with c_rep:
            st.markdown("#### Option B: Test Re-planning (Dynamic Budget Change)")
            new_budget_val = st.number_input("Adjust Budget to (e.g. ₹50,000):", min_value=20000, max_value=100000, value=50000, step=5000)
            if st.button("🔄 Trigger Re-planning Loop", use_container_width=True):
                with st.spinner(f"Agentic loop re-evaluating options for new budget ₹{new_budget_val:,.0f}..."):
                    new_state = dict(state)
                    new_state["budget"] = float(new_budget_val)
                    new_state["user_query"] += f" (Reduced budget to ₹{new_budget_val})"
                    new_state["replan_count"] = 0
                    
                    updated = travel_agent_graph.invoke(new_state)
                    st.session_state.trip_state = updated
                    st.session_state.final_package = None
                    save_trip(st.session_state.trip_id, updated, status="REPLANNED")
                    st.rerun()

# Display Final Trip Package if Booked
if st.session_state.final_package:
    pkg = st.session_state.final_package
    st.markdown("---")
    st.markdown("## 🎒 Confirmed Trip Package")
    st.success(f"Trip Ref: **{st.session_state.trip_id}** — Status: **{pkg.get('package_status')}**")
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.markdown("### 🎫 Confirmed Bookings")
        for b in pkg.get("confirmed_bookings", []):
            st.markdown(f"""
            - **{b.get('booking_type')}**: {b.get('provider')}
              - **Reference / PNR:** `{b.get('reference_number')}`
              - **Status:** `{b.get('status')}` | **Amount:** ₹{b.get('amount'):,.0f}
            """)
            
    with col_p2:
        st.markdown("### 🧳 Smart Travel Checklist")
        for item in pkg.get("checklist", []):
            st.markdown(f"- [x] {item}")
            
        st.markdown("### 🚨 Emergency Contacts")
        for k, v in pkg.get("emergency_contacts", {}).items():
            st.markdown(f"- **{k}:** `{v}`")
