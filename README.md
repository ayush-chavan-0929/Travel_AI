# Travel_AI: Agentic Travel Planning and Booking Assistant

[![LangGraph](https://img.shields.io/badge/Orchestrator-LangGraph-orange.svg)](https://github.com/langchain-ai/langgraph)
[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B.svg)](https://streamlit.io)
[![Free APIs](https://img.shields.io/badge/APIs-100%25%20Free%20Tier-brightgreen.svg)](#free-apis-used)

An intelligent, multi-agent AI system designed and implemented strictly following the complete project specifications in `AI_Travel_Planner_Booking_Assistant_Complete_Plan.md`. 

Built with **LangGraph**, **FastAPI**, **Streamlit**, and **100% Free Open APIs**, the system performs natural language travel planning, budget optimization, constraint checking, autonomous replanning, human-in-the-loop approval, and booking simulation.

---

## 🌟 Key Features

1. **Agentic Decision Loop**: 
   - `Goal -> Understand -> Plan -> Tool Calling -> Observe -> Verify -> Re-plan -> Human Approval -> Book -> Trip Package`.
2. **Multi-Agent Coordination (LangGraph StateGraph)**:
   - **Intent Agent**: Extracts origin, destination, duration, travellers, budget, and dates.
   - **Preference & Constraint Agent**: Separates soft preferences (beaches, nightlife, star-rating) from hard constraints (budget ceiling, pax).
   - **Destination Agent**: Fetches real-time weather and geo-spatial routing.
   - **Transport & Hotel Agent**: Finds, ranks, and filters transit options and accommodation.
   - **Activity Agent**: Curates activities based on extracted interests.
   - **Budget Agent**: Performs complete financial breakdown across all categories.
   - **Itinerary Optimizer**: Clusters attractions geographically to eliminate criss-cross routing.
   - **Verification Agent**: Acts as an automated compliance gatekeeper against budget constraints.
   - **Replanning Agent**: Autonomously downscales hotels/transports when constraints are tightened.
   - **Human-in-the-Loop & Booking Agent**: Requests explicit approval before issuing verifiable PNRs/booking references.
3. **100% Free Open APIs Used**:
   - **Open-Meteo API**: Live weather forecasting (no API key required).
   - **OpenStreetMap / Nominatim**: Geo-spatial distance and route calculations (no API key required).
   - **Open Exchange / Forex**: Real-time currency conversions.
   - **Local RAG Knowledge Engine**: Semantic guide retriever over markdown documentation without paid embeddings.
   - **Simulated Inventory & Booking Engine**: Flight, train, bus, hotel, and activity inventory.

---

## 📂 Project Architecture & Directory Structure

```
Travel_AI/
│
├── app/
│   ├── main.py                     # FastAPI REST API Backend
│   ├── ui.py                       # Streamlit Interactive Web Application
│   │
│   ├── agents/
│   │   ├── orchestrator.py         # LangGraph workflow StateGraph
│   │   ├── intent_agent.py         # Intent extraction & NLP parsing
│   │   ├── preference_agent.py     # Soft preferences & Hard constraints
│   │   ├── destination_agent.py    # Live weather & OpenStreetMap integration
│   │   ├── travel_options_agents.py# Transport, Hotel & Activity selection
│   │   ├── planning_agents.py      # Budget breakdown & Itinerary generator
│   │   └── verification_and_booking_agents.py # Verification, Re-plan & Booking
│   │
│   ├── tools/
│   │   └── apis.py                 # Free APIs (Open-Meteo, OSM) & Mock booking engine
│   │
│   ├── rag/
│   │   └── retriever.py            # Local RAG knowledge retrieval engine
│   │
│   ├── models/
│   │   └── travel_state.py         # Pydantic schemas & LangGraph TravelState
│   │
│   └── database/
│       └── db.py                   # SQLite relational database layer
│
├── data/
│   ├── travel_knowledge/           # Destination guides (Goa, etc.)
│   └── travel_ai.db                # SQLite database for trips & bookings
│
├── tests/
│   └── test_agents.py              # Automated test suite (Planning, Replanning, Booking)
│
├── requirements.txt
├── .env.example
├── AI_Travel_Planner_Booking_Assistant_Complete_Plan.md
└── README.md
```

---

## 🚀 Quick Start Guide

### 1. Installation

Clone or open the project folder in terminal:
```bash
cd "C:\Users\AYUSH\Downloads\Projects\Travel_AI"
```

Install requirements:
```bash
python -m pip install -r requirements.txt
```

*(Note: Everything runs out of the box using free endpoints! No paid API keys are required.)*

---

### 2. Run the Interactive Streamlit Web UI

Launch the rich web dashboard:
```bash
python -m streamlit run app/ui.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

**Web Dashboard Capabilities:**
- 💬 Input natural language travel queries (or click sample presets).
- 📅 View the geographically clustered day-by-day itinerary.
- 🌤️ Check live destination weather from Open-Meteo.
- 💵 Explore the detailed budget breakdown.
- 🤖 Inspect transparent agent trace logs.
- 🔄 Test autonomous re-planning by dynamically adjusting budget (e.g. from ₹60,000 to ₹50,000).
- 🎫 Approve the trip and generate confirmed booking packages with PNRs and safety checklists.

---

### 3. Run the FastAPI REST Backend

To launch the REST API server:
```bash
python -m uvicorn app.main:app --reload --port 8000
```
Interactive Swagger documentation is available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

**Available API Endpoints:**
- `POST /api/v1/travel/plan`: Run multi-agent planning on natural language input.
- `GET /api/v1/travel/{trip_id}`: Retrieve trip state and itinerary.
- `POST /api/v1/travel/{trip_id}/replan`: Re-evaluate trip against adjusted budget or constraints.
- `POST /api/v1/travel/{trip_id}/approve`: Confirm user approval and trigger booking simulation.

---

### 4. Run Automated Test Suite

Verify all agent cycles, budget calculations, and verification safeguards:
```bash
python tests/test_agents.py
```
Expected output:
```
🧪 TEST 1: Running LangGraph Multi-Agent Travel Planner Workflow -> PASS
🧪 TEST 2: Testing Replanning on Reduced Budget (₹50,000) -> PASS
🧪 TEST 3: Testing Human Approval and Booking Execution -> PASS
🎉 ALL 3 AGENTIC SYSTEM TESTS PASSED SUCCESSFULLY!
```

---

## 🛡️ License
MIT License. Built for major academic / diploma AI and agentic systems demonstration.
