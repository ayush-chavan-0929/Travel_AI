# Agentic AI-Powered Intelligent Travel Planning and Booking Assistant

## 1. Project Overview

### Project Title
**Agentic AI-Powered Intelligent Travel Planning and Booking Assistant**

### Subtitle
*A Multi-Agent System for Personalized Travel Planning, Budget Optimization, Itinerary Generation, and Booking Assistance*

### Objective

Build an AI-powered travel assistant that accepts a user's natural-language travel goal, understands the user's constraints and preferences, researches travel options, creates an optimized itinerary, estimates the budget, recommends transportation, hotels and activities, verifies the plan, and optionally performs booking-related actions through APIs.

The key distinction from a normal chatbot is that the system follows an agentic loop:

```text
User Goal
   ↓
Understand
   ↓
Plan
   ↓
Use Tools
   ↓
Observe Results
   ↓
Verify
   ↓
Re-plan if Required
   ↓
User Approval
   ↓
Execute Booking Actions
   ↓
Verify Booking
   ↓
Final Trip Package
```

---

# 2. Problem Statement

Planning a trip usually requires users to manually:

- Search destinations
- Compare transportation
- Find hotels
- Search tourist attractions
- Check weather
- Estimate costs
- Arrange activities
- Build a day-by-day itinerary
- Check whether the plan fits the budget
- Re-plan when prices, availability, or constraints change
- Manage booking information

Existing travel chatbots generally provide recommendations but do not perform structured planning, constraint checking, tool-based research, verification, and replanning.

This project aims to create an **Agentic AI Travel Planner** that performs these tasks as a coordinated workflow of specialized AI agents.

---

# 3. Example User Request

A user can say:

> "Plan a 5-day trip to Goa from Mumbai for 4 people. My budget is ₹60,000. We want beaches, nightlife and water sports. Prefer 3-star hotels."

The system converts this into structured requirements:

```json
{
  "origin": "Mumbai",
  "destination": "Goa",
  "duration": 5,
  "travellers": 4,
  "budget": 60000,
  "interests": [
    "beaches",
    "nightlife",
    "water sports"
  ],
  "hotel_preference": "3-star"
}
```

---

# 4. Complete End-to-End Architecture

```text
                         USER
                           │
                           ▼
                 ┌───────────────────┐
                 │   Travel Interface│
                 │    Web / Mobile   │
                 └─────────┬─────────┘
                           │
                           ▼
                 ┌───────────────────┐
                 │ AI Travel         │
                 │ Orchestrator      │
                 │    LangGraph      │
                 └─────────┬─────────┘
                           │
             ┌─────────────┼─────────────┐
             │             │             │
             ▼             ▼             ▼
       Intent Agent   Preference     Constraint
                       Agent           Agent
             │             │             │
             └─────────────┼─────────────┘
                           ▼
                  ┌────────────────┐
                  │ Planning Agent │
                  └───────┬────────┘
                          │
            ┌─────────────┼──────────────┐
            ▼             ▼              ▼
      Destination      Transport       Hotel
         Agent           Agent          Agent
            │             │              │
            └─────────────┼──────────────┘
                          ▼
                  Activity Agent
                          │
                          ▼
                  Budget Agent
                          │
                          ▼
                Itinerary Optimizer
                          │
                          ▼
                 Verification Agent
                          │
                          ▼
                  ┌──────────────┐
                  │ User Approval│
                  └──────┬───────┘
                         │
                    Approved?
                    /         \
                  NO           YES
                  │             │
                  ▼             ▼
             Re-plan      Booking Agent
                                │
                   ┌────────────┼────────────┐
                   ▼            ▼            ▼
                Flights       Hotels      Activities
                   │            │            │
                   └────────────┼────────────┘
                                ▼
                       Booking Verification
                                │
                                ▼
                        Final Trip Package
```

---

# 5. Detailed End-to-End Workflow

## Step 1: User Interaction

The user provides the travel requirement through a web interface.

### Possible inputs

- Origin
- Destination
- Travel dates
- Duration
- Number of travellers
- Budget
- Interests
- Hotel preference
- Transport preference
- Food preference
- Travel style
- Special requirements

### Example

> "I want to visit Manali for 4 days with my friends. We have a budget of ₹40,000."

The system should identify missing information and ask targeted questions.

---

# 6. Step 2: Intent Agent

The Intent Agent determines what the user wants.

### Responsibilities

- Identify travel planning intent
- Extract destination
- Extract duration
- Extract traveller count
- Extract dates
- Extract budget
- Extract travel preferences
- Detect missing information

### Example

Input:

> "Take me to Jaipur for 3 days with my parents."

Output:

```text
Destination → Jaipur
Duration → 3 days
Travellers → 3
Travel Type → Family
Preference → Comfortable / senior-friendly
```

---

# 7. Step 3: Preference and Constraint Agent

The system separates requirements into **hard constraints** and **soft preferences**.

## Hard Constraints

These must be satisfied whenever possible.

Example:

```text
Budget <= ₹60,000
Duration = 5 days
Travellers = 4
```

## Soft Preferences

These should be optimized.

Example:

```text
3-star hotel
Beach proximity
Nightlife
Water sports
Low travel time
Good ratings
```

This allows the system to make intelligent trade-offs.

---

# 8. Step 4: Destination Research Agent

The Destination Agent researches the destination.

### Information collected

- Tourist attractions
- Popular areas
- Activities
- Local transportation
- Approximate costs
- Opening hours
- Weather
- Distance between locations
- Travel time
- Reviews and ratings
- Destination-specific information

### Example: Goa

```text
North Goa
 ├── Baga Beach
 ├── Calangute
 ├── Anjuna
 └── Vagator

South Goa
 ├── Palolem
 ├── Colva
 └── Benaulim
```

The agent selects destinations and attractions based on user preferences.

---

# 9. Step 5: Transportation Agent

The Transportation Agent researches travel options.

### Possible modes

- Flight
- Train
- Bus
- Car
- Local transport

### Comparison

| Option | Cost | Duration | Comfort |
|---|---:|---:|---|
| Flight | Variable | Low | High |
| Train | Variable | Medium/High | Medium |
| Bus | Variable | High | Medium |
| Car | Variable | High | High |

The agent considers:

```text
Cost
+
Travel Time
+
Comfort
+
User Preference
+
Availability
```

It then ranks the options.

---

# 10. Step 6: Hotel Agent

The Hotel Agent searches for accommodation.

### Parameters

- Destination
- Dates
- Number of guests
- Budget
- Hotel category
- Location
- Rating
- Distance from attractions
- Availability

### Example flow

```text
Budget
   ↓
₹15,000
   ↓
3-star hotels
   ↓
North Goa
   ↓
Near beaches
   ↓
Good ratings
   ↓
Ranked hotel options
```

---

# 11. Step 7: Activity Agent

The Activity Agent recommends activities based on interests.

### Example

```text
Beaches
 ├── Baga
 ├── Anjuna
 └── Palolem

Water Sports
 ├── Parasailing
 ├── Jet Ski
 └── Banana Boat

Nightlife
 ├── Clubs
 ├── Beach parties
 └── Night markets
```

The agent evaluates:

- Cost
- Duration
- Distance
- Opening hours
- Availability
- User interest

---

# 12. Step 8: Budget Agent

The Budget Agent calculates the complete estimated cost.

```text
Transportation
      +
Hotel
      +
Food
      +
Activities
      +
Local Transport
      +
Emergency Buffer
      =
Total Estimated Cost
```

### Example

```text
Flights              ₹20,000
Hotel                ₹15,000
Food                  ₹8,000
Activities            ₹7,000
Local Transport       ₹5,000
Emergency Buffer      ₹3,000
--------------------------------
Total                 ₹58,000
```

User budget:

```text
₹60,000
```

Remaining:

```text
₹2,000
```

---

# 13. Step 9: Itinerary Planning Agent

The Itinerary Agent creates the day-by-day plan.

## Example

### Day 1

```text
Mumbai → Goa
↓
Hotel Check-in
↓
Baga Beach
↓
Dinner
```

### Day 2

```text
Calangute
↓
Water Sports
↓
Anjuna
↓
Nightlife
```

### Day 3

```text
Vagator
↓
Chapora Fort
↓
Local Sightseeing
```

### Day 4

```text
South Goa
↓
Palolem
↓
Beach Activities
↓
Dinner
```

### Day 5

```text
Breakfast
↓
Shopping
↓
Hotel Checkout
↓
Goa → Mumbai
```

---

# 14. Step 10: Itinerary Optimization Agent

The optimizer checks whether the itinerary is practical.

## Checks

### Geographic optimization

Bad:

```text
Baga → Palolem → Vagator → Baga
```

Better:

```text
Baga → Anjuna → Vagator
```

### Other checks

- Opening hours
- Travel time
- Activity duration
- Overlapping activities
- Budget
- Hotel location
- Weather
- User preferences
- Available time

If the plan violates constraints, the system automatically replans.

---

# 15. Step 11: Verification Agent

Before showing the final plan, the Verification Agent validates it.

```text
Draft Itinerary
      ↓
Verification Agent
      │
      ├── Budget Check
      ├── Timing Check
      ├── Availability Check
      ├── Location Check
      ├── Preference Check
      └── Conflict Check
      │
      ▼
    Valid?
    /    \
   NO     YES
   │       │
   ▼       ▼
Re-plan   Final Plan
```

This verification loop is a major component that makes the project genuinely agentic.

---

# 16. Step 12: User Approval

The user sees the proposed trip before any booking action.

Example:

```text
YOUR 5-DAY GOA TRIP

Estimated Cost: ₹58,000

Transport:       ₹20,000
Hotel:           ₹15,000
Food:             ₹8,000
Activities:       ₹7,000
Local Transport:  ₹5,000
Buffer:           ₹3,000

[Approve Plan]
[Modify Plan]
[Cancel]
```

The system should require user approval before committing to booking-related actions.

---

# 17. Step 13: Replanning

If the user says:

> "Reduce the budget to ₹50,000."

The system should not simply regenerate text.

It should:

```text
New Constraint
      ↓
Constraint Agent
      ↓
Budget Agent
      ↓
Transport Agent
      ↓
Hotel Agent
      ↓
Activity Agent
      ↓
Itinerary Optimizer
      ↓
Verification
      ↓
New Plan
```

This is a strong demonstration of agentic reasoning.

---

# 18. Step 14: Booking Agent

After approval, the Booking Agent performs booking-related operations.

```text
Approved Itinerary
        ↓
Booking Agent
        ↓
 ┌──────┼────────┐
 ↓      ↓        ↓
Flight Hotel  Activities
```

Possible integrations:

- Flight APIs
- Hotel APIs
- Activity/ticket APIs
- Payment APIs
- Calendar APIs

For a diploma project, real financial transactions are not necessary. **Mock booking APIs** are recommended for the academic prototype.

---

# 19. Step 15: Booking Verification

After each booking action:

```text
Booking Request
      ↓
External API / Mock API
      ↓
Booking Confirmation
      ↓
Verification Agent
      ↓
Check:
 ├── Booking ID / PNR
 ├── Date
 ├── Traveller Count
 ├── Amount
 └── Cancellation Policy
```

If booking fails:

```text
Booking Failed
      ↓
Retry / Find Alternative
      ↓
Inform User
```

---

# 20. Step 16: Final Trip Package

The system generates a complete travel package containing:

## Itinerary

Day-by-day schedule.

## Transport

Tickets, timings, and booking references.

## Hotel

Hotel details and confirmation.

## Activities

Activity timings and booking information.

## Budget

Estimated vs actual expenditure.

## Maps

Routes and locations.

## Checklist

```text
✓ ID Proof
✓ Clothes
✓ Medicines
✓ Chargers
✓ Travel Documents
```

## Emergency Information

Relevant local emergency and travel information.

---

# 21. Multi-Agent Architecture

Use **one Orchestrator + specialized agents**.

```text
                         USER
                           │
                           ▼
                    Travel Assistant
                           │
                           ▼
                    ORCHESTRATOR
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
  Intent Agent      Preference Agent   Constraint Agent
        │                  │                  │
        └──────────────────┼──────────────────┘
                           ▼
                    Planning Agent
                           │
       ┌───────────────────┼────────────────────┐
       │                   │                    │
       ▼                   ▼                    ▼
 Destination          Transport              Hotel
   Agent                Agent                Agent
       │                   │                    │
       └───────────────────┼────────────────────┘
                           ▼
                     Activity Agent
                           │
                           ▼
                      Budget Agent
                           │
                           ▼
                  Itinerary Optimizer
                           │
                           ▼
                   Verification Agent
                           │
                           ▼
                     USER APPROVAL
                           │
                           ▼
                     Booking Agent
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
          Flights        Hotels       Activities
             │             │             │
             └─────────────┼─────────────┘
                           ▼
                  Booking Verification
                           │
                           ▼
                    FINAL TRIP PACKAGE
```

---

# 22. Technology Stack

| Layer | Recommended Technology |
|---|---|
| Frontend | React.js / Streamlit |
| UI | Tailwind CSS |
| Backend | Python |
| API Framework | FastAPI |
| Agent Framework | LangGraph |
| LLM | GPT / Llama / Mistral / Gemma |
| Embeddings | Sentence Transformers |
| RAG | LangChain/LlamaIndex or custom RAG |
| Vector Database | FAISS / ChromaDB |
| Relational Database | PostgreSQL |
| Simple Prototype DB | SQLite |
| Cache | Redis |
| Maps | Google Maps / OpenStreetMap |
| Weather | Weather API |
| Flight Search | Flight API / Mock API |
| Hotel Search | Hotel API / Mock API |
| Activity Search | Activity API / Mock API |
| Authentication | JWT |
| Background Jobs | Celery / FastAPI Background Tasks |
| Containerization | Docker |
| Testing | Pytest |
| Deployment | Docker + Cloud VM |
| Monitoring | Application Logs + Agent Traces |
| Version Control | Git |

---

# 23. Frontend

## Recommended Option

React.js + Tailwind CSS

### Main screens

1. Login
2. Travel Planning Chat
3. Trip Requirements
4. Destination Recommendations
5. Transport Options
6. Hotel Options
7. Activity Options
8. Budget Dashboard
9. Day-by-Day Itinerary
10. Approval Screen
11. Booking Screen
12. Final Trip Dashboard

### Alternative

For a faster diploma prototype:

**Streamlit**

This reduces frontend development effort.

---

# 24. Backend

Use:

**Python + FastAPI**

Responsibilities:

```text
API Gateway
   ↓
Authentication
   ↓
Travel Request
   ↓
Agent Orchestration
   ↓
External API Integration
   ↓
Database
   ↓
Response
```

Suggested API endpoints:

```text
POST /api/v1/travel/plan
GET  /api/v1/travel/{trip_id}
POST /api/v1/travel/{trip_id}/replan
POST /api/v1/travel/{trip_id}/approve
POST /api/v1/booking/search
POST /api/v1/booking/confirm
GET  /api/v1/booking/{booking_id}
POST /api/v1/travel/{trip_id}/cancel
```

---

# 25. Agent Framework

## Recommended: LangGraph

LangGraph is suitable because the system contains:

- Stateful workflows
- Conditional routing
- Tool calling
- Agent coordination
- Human approval
- Verification
- Replanning
- Error handling

### Alternative frameworks

- LangChain
- CrewAI
- AutoGen

For this project, **LangGraph is the preferred choice**.

---

# 26. LLM

Possible choices:

```text
Cloud:
- GPT model
- Other commercial LLM APIs

Local:
- Llama
- Mistral
- Gemma
```

For local/offline experimentation:

```text
Ollama
   ↓
Local LLM
```

The LLM handles:

- Natural-language understanding
- Planning
- Structured extraction
- Reasoning
- Tool selection
- Explanation generation

---

# 27. RAG Layer

RAG can provide destination-specific knowledge.

### Knowledge sources

- Destination guides
- Tourist attraction information
- Hotel information
- Travel policies
- Cancellation policies
- Activity descriptions
- FAQs
- Local travel information

### RAG pipeline

```text
Travel Documents
       ↓
Document Loader
       ↓
Text Cleaning
       ↓
Chunking
       ↓
Embeddings
       ↓
Vector Database
       ↓
Retriever
       ↓
Relevant Context
       ↓
Travel Agent
       ↓
LLM Response
```

---

# 28. Vector Database

Recommended options:

### FAISS

Good for:

- Simple prototypes
- Local development
- Low complexity

### ChromaDB

Good for:

- Easy development
- Metadata filtering
- Local projects

### Qdrant

Good for:

- More production-like architecture
- Filtering
- Scalable vector search

For diploma students:

> **FAISS or ChromaDB is sufficient.**

---

# 29. Database Design

Recommended database:

**PostgreSQL**

## Main tables

### users

```text
id
name
email
password_hash
created_at
```

### user_preferences

```text
id
user_id
budget_preference
hotel_preference
transport_preference
food_preference
travel_style
```

### trips

```text
id
user_id
origin
destination
start_date
end_date
traveller_count
budget
status
created_at
```

### itineraries

```text
id
trip_id
day_number
date
location
activity
start_time
end_time
estimated_cost
```

### hotels

```text
id
trip_id
name
location
rating
price
availability
booking_status
```

### transport_options

```text
id
trip_id
mode
provider
departure
arrival
duration
price
availability
```

### activities

```text
id
trip_id
name
location
duration
price
availability
```

### bookings

```text
id
trip_id
booking_type
provider
booking_reference
amount
status
created_at
```

### agent_logs

```text
id
trip_id
agent_name
input
output
tool_used
status
timestamp
```

---

# 30. Shared Agent State

The Orchestrator should maintain a shared state.

Example:

```python
TravelState = {
    "origin": "Mumbai",
    "destination": "Goa",
    "dates": [],
    "travellers": 4,
    "budget": 60000,
    "preferences": {},
    "transport_options": [],
    "hotel_options": [],
    "activities": [],
    "itinerary": [],
    "total_cost": 0,
    "validation_status": None,
    "user_approved": False
}
```

Each agent reads and updates only the relevant state.

---

# 31. Tool Layer

Agents should use controlled tools rather than directly accessing every external system.

```text
                    AGENTS
                       │
                       ▼
                  TOOL MANAGER
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
   Maps Tool       Weather Tool    Search Tool
        │              │              │
        ▼              ▼              ▼
    Maps API       Weather API    Search/API
```

### Tools

```text
Flight Search Tool
Hotel Search Tool
Activity Search Tool
Maps Tool
Weather Tool
Currency Tool
Calendar Tool
Notification Tool
Booking Tool
```

---

# 32. Memory

## Short-Term Memory

Stores information for the current trip:

```text
Destination
Dates
Budget
Travellers
Current itinerary
Current booking status
```

## Long-Term Memory

Stores user preferences:

```text
Preferred hotel category → 3-star
Preferred transport → Train
Food preference → Vegetarian
Travel style → Budget
```

This enables:

> "Plan another trip like my previous Goa trip."

The system can reuse previous preferences.

---

# 33. Agentic Decision Loop

The core loop is:

```text
              ┌──────────────┐
              │     Goal     │
              └──────┬───────┘
                     ↓
              ┌──────────────┐
              │    PLAN      │
              └──────┬───────┘
                     ↓
              ┌──────────────┐
              │     ACT      │
              │    / TOOL    │
              └──────┬───────┘
                     ↓
              ┌──────────────┐
              │   OBSERVE    │
              └──────┬───────┘
                     ↓
              ┌──────────────┐
              │   VERIFY     │
              └──────┬───────┘
                     ↓
                 Satisfied?
                /         \
              NO           YES
              │             │
              ↓             ↓
           REPLAN         RESULT
              │
              └──────→ ACT
```

---

# 34. Project Folder Structure

```text
ai-travel-agent/
│
├── app/
│   ├── main.py
│   │
│   ├── agents/
│   │   ├── orchestrator.py
│   │   ├── intent_agent.py
│   │   ├── preference_agent.py
│   │   ├── constraint_agent.py
│   │   ├── destination_agent.py
│   │   ├── transport_agent.py
│   │   ├── hotel_agent.py
│   │   ├── activity_agent.py
│   │   ├── budget_agent.py
│   │   ├── itinerary_agent.py
│   │   ├── booking_agent.py
│   │   └── verification_agent.py
│   │
│   ├── tools/
│   │   ├── maps.py
│   │   ├── weather.py
│   │   ├── flights.py
│   │   ├── hotels.py
│   │   ├── activities.py
│   │   └── currency.py
│   │
│   ├── rag/
│   │   ├── ingestion.py
│   │   ├── embeddings.py
│   │   └── retriever.py
│   │
│   ├── models/
│   │   ├── travel_state.py
│   │   └── schemas.py
│   │
│   ├── database/
│   │   ├── models.py
│   │   └── database.py
│   │
│   └── api/
│       ├── travel.py
│       ├── booking.py
│       └── users.py
│
├── frontend/
│
├── tests/
│
├── data/
│   └── travel_knowledge/
│
├── requirements.txt
├── .env.example
├── Dockerfile
└── README.md
```

---

# 35. MVP Scope

Do not implement every feature initially.

## Phase 1 — Basic MVP

Implement:

```text
User
 ↓
Intent Agent
 ↓
Destination Agent
 ↓
Hotel Agent
 ↓
Activity Agent
 ↓
Budget Agent
 ↓
Itinerary Agent
 ↓
Final Plan
```

Use mock APIs where necessary.

---

# 36. Phase 2 — Agentic Capabilities

Add:

```text
Tool Calling
↓
Shared State
↓
Memory
↓
RAG
↓
Planning
↓
Verification
↓
Replanning
```

---

# 37. Phase 3 — Advanced Features

Add:

```text
Weather Awareness
↓
Real-Time API Data
↓
Transport Optimization
↓
Booking Simulation
↓
Notifications
↓
Voice Interface
```

---

# 38. Suggested Development Timeline

## Week 1 — Requirement Analysis

- Define project scope
- Define user journeys
- Define agents
- Define APIs
- Define database

## Week 2 — UI + Backend

- Create React/Streamlit interface
- Create FastAPI backend
- Create database
- Implement authentication

## Week 3 — LLM + Intent

- Integrate LLM
- Implement structured extraction
- Implement Intent Agent
- Implement Preference Agent

## Week 4 — Travel Agents

- Destination Agent
- Transport Agent
- Hotel Agent
- Activity Agent

## Week 5 — Planning

- Budget Agent
- Itinerary Agent
- Optimization logic
- Shared state

## Week 6 — RAG + Tools

- Build travel knowledge base
- Create embeddings
- Implement vector search
- Add maps/weather/search tools

## Week 7 — Verification + Replanning

- Verification Agent
- Constraint validation
- Replanning
- Error handling

## Week 8 — Booking Simulation

- Mock flight API
- Mock hotel API
- Booking Agent
- Booking verification

## Week 9 — Testing

- Unit testing
- Integration testing
- Agent workflow testing
- Failure scenarios

## Week 10 — Deployment + Documentation

- Dockerize
- Deploy
- Create screenshots
- Prepare report
- Prepare presentation
- Prepare demo

---

# 39. Testing Strategy

## Functional Tests

Test:

- Valid destination
- Invalid destination
- Missing dates
- Missing budget
- Multiple travellers
- Different preferences

## Constraint Tests

Example:

```text
Budget = ₹50,000
Generated cost = ₹65,000

Expected:
Replanning
```

## Failure Tests

Example:

```text
Hotel API unavailable
↓
Agent should use alternative source/mock data
```

## Booking Tests

```text
Booking successful
Booking failed
Booking partially successful
Payment failure
Availability changed
```

## Agent Tests

Verify:

- Correct agent routing
- Correct tool selection
- Correct state updates
- Correct replanning
- No unauthorized booking

---

# 40. Important Safety and Control Design

The system should use **human-in-the-loop approval** for consequential actions.

Recommended flow:

```text
Search
  ↓
Recommend
  ↓
Plan
  ↓
Verify
  ↓
USER APPROVAL
  ↓
Book
```

Do not automatically make real purchases without explicit confirmation.

For an academic project, mock booking APIs are preferable.

---

# 41. Key Agentic AI Features to Demonstrate

The final project should demonstrate these capabilities:

### 1. Planning

The system decomposes a travel goal into subtasks.

### 2. Tool Calling

Agents use external tools/APIs.

### 3. Multi-Agent Collaboration

Different agents specialize in different travel tasks.

### 4. Memory

The system remembers user preferences.

### 5. RAG

The system retrieves destination-specific knowledge.

### 6. Constraint Handling

The system respects budget, time, traveller count, and preferences.

### 7. Verification

The system validates its own generated itinerary.

### 8. Replanning

The system changes the plan when constraints change.

### 9. Human-in-the-Loop

The user approves consequential actions.

### 10. Execution

The system performs booking simulations or API actions.

---

# 42. Example Final Demonstration

Use this scenario for the college/project presentation.

### User

> "Plan a 5-day Goa trip from Mumbai for 4 people under ₹60,000. We like beaches, nightlife and water sports."

### Agent 1 — Intent

Extracts:

```text
Mumbai → Goa
5 days
4 travellers
₹60,000
Beach
Nightlife
Water Sports
```

### Agent 2 — Research

Finds:

```text
Transport options
Hotels
Beaches
Activities
Nightlife
```

### Agent 3 — Planning

Creates the itinerary.

### Agent 4 — Budget

Calculates:

```text
Total = ₹58,000
```

### Agent 5 — Verification

Checks:

```text
Budget → PASS
Timing → PASS
Location → PASS
Activities → PASS
```

### User changes requirement

> "Actually, my budget is only ₹50,000."

### Agentic response

```text
New Constraint
      ↓
Recalculate
      ↓
Replace expensive transport
      ↓
Select cheaper hotel
      ↓
Remove low-priority activity
      ↓
Optimize itinerary
      ↓
Verify
```

New result:

```text
Estimated Cost = ₹49,000
```

### User

> "Approve."

### Booking Agent

Runs mock bookings:

```text
Transport → CONFIRMED
Hotel → CONFIRMED
Activity → CONFIRMED
```

### Final Output

```text
Trip Confirmed

5 Days / 4 People
Mumbai → Goa

Transport: Confirmed
Hotel: Confirmed
Activities: Confirmed

Total: ₹49,000

Booking IDs:
FL12345
HT56789
AC98765
```

---

# 43. What Makes the Project Different from a Chatbot?

## Normal Travel Chatbot

```text
User Question
     ↓
LLM
     ↓
Text Response
```

## This Project

```text
User Goal
     ↓
Intent Understanding
     ↓
Constraint Extraction
     ↓
Planning
     ↓
Multiple Specialized Agents
     ↓
Tool Calling
     ↓
External Data
     ↓
Budget Optimization
     ↓
Itinerary Generation
     ↓
Verification
     ↓
Replanning
     ↓
Human Approval
     ↓
Booking Execution
     ↓
Booking Verification
     ↓
Final Trip Package
```

That distinction should be clearly explained during the project viva.

---

# 44. Final Recommended Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                         USER                               │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND / UI                            │
│              React.js / Streamlit                          │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                     FASTAPI BACKEND                         │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                 LANGGRAPH ORCHESTRATOR                      │
└──────────────────────────┬──────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
   Intent Agent       Preference Agent   Constraint Agent
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
                           ▼
                    Planning Agent
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
 Destination           Transport            Hotel
 Agent                  Agent               Agent
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
                           ▼
                     Activity Agent
                           │
                           ▼
                      Budget Agent
                           │
                           ▼
                 Itinerary Optimizer
                           │
                           ▼
                  Verification Agent
                           │
                     ┌─────┴─────┐
                     │           │
                  Invalid       Valid
                     │           │
                     ▼           ▼
                   Replan    User Approval
                                 │
                                 ▼
                          Booking Agent
                                 │
                    ┌────────────┼────────────┐
                    ▼            ▼            ▼
                 Flight        Hotel       Activity
                    │            │            │
                    └────────────┼────────────┘
                                 │
                                 ▼
                        Booking Verification
                                 │
                                 ▼
                         FINAL TRIP PACKAGE


┌─────────────────────────────────────────────────────────────┐
│                    SUPPORTING SERVICES                      │
│                                                             │
│ LLM │ RAG │ Vector DB │ PostgreSQL │ Redis │ Memory        │
│                                                             │
│ Maps │ Weather │ Flight │ Hotel │ Activity │ Currency APIs │
└─────────────────────────────────────────────────────────────┘
```

---

# 45. Recommended Final Technology Stack

```text
Frontend
    React.js + Tailwind CSS
          │
          ▼
Backend
    Python + FastAPI
          │
          ▼
Agent Orchestration
    LangGraph
          │
          ▼
LLM
    GPT / Llama / Mistral / Gemma
          │
          ├── Tool Calling
          ├── Structured Output
          └── Planning
          │
          ▼
RAG
    Sentence Transformers
          +
    FAISS / ChromaDB
          │
          ▼
Database
    PostgreSQL
          │
          ▼
External Tools
    Maps
    Weather
    Flight Search
    Hotel Search
    Activity Search
    Currency
          │
          ▼
Deployment
    Docker
          │
          ▼
Cloud VM / Local Server
```

---

# 46. Final Project Deliverables

The completed major project should contain:

1. Working web application
2. Multi-agent orchestration
3. Travel planning workflow
4. RAG knowledge base
5. External/mock tool integrations
6. Budget optimization
7. Itinerary generation
8. Verification and replanning
9. Booking simulation
10. PostgreSQL database
11. Agent execution logs
12. Test cases
13. Docker deployment
14. Project report
15. Architecture diagrams
16. Project presentation
17. Final demonstration

---

# 47. Final Project Outcome

The final system should be able to take a request such as:

> "Plan a 5-day trip to Goa for four people from Mumbai under ₹60,000, with beaches, water sports and nightlife."

and autonomously perform:

```text
Understand Request
       ↓
Extract Requirements
       ↓
Research Destination
       ↓
Search Transport
       ↓
Search Hotels
       ↓
Find Activities
       ↓
Calculate Budget
       ↓
Create Itinerary
       ↓
Optimize Itinerary
       ↓
Verify Constraints
       ↓
Ask User Approval
       ↓
Replan if User Changes Requirements
       ↓
Execute Mock/Real API Booking
       ↓
Verify Bookings
       ↓
Generate Final Travel Package
```

This gives the project a clear **Agentic AI + Generative AI + RAG + API Integration + Optimization + Software Engineering** component, making it appropriate for a Diploma AIML major project.
