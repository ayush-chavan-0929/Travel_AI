import sqlite3
import json
import os
from typing import Dict, Any, Optional

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "travel_ai.db")

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Trips table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trips (
        trip_id TEXT PRIMARY KEY,
        user_query TEXT,
        origin TEXT,
        destination TEXT,
        duration_days INTEGER,
        travellers INTEGER,
        budget REAL,
        total_cost REAL,
        status TEXT,
        state_json TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Bookings table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        booking_id TEXT PRIMARY KEY,
        trip_id TEXT,
        booking_type TEXT,
        provider TEXT,
        reference_number TEXT,
        amount REAL,
        status TEXT,
        details_json TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    conn.commit()
    conn.close()

def save_trip(trip_id: str, state: Dict[str, Any], status: str = "PLANNED"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT OR REPLACE INTO trips (trip_id, user_query, origin, destination, duration_days, travellers, budget, total_cost, status, state_json)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        trip_id,
        state.get("user_query", ""),
        state.get("origin", ""),
        state.get("destination", ""),
        state.get("duration_days", 0),
        state.get("travellers", 0),
        state.get("budget", 0.0),
        state.get("total_estimated_cost", 0.0),
        status,
        json.dumps(state)
    ))
    conn.commit()
    conn.close()

def get_trip(trip_id: str) -> Optional[Dict[str, Any]]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT state_json FROM trips WHERE trip_id = ?", (trip_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return json.loads(row[0])
    return None

def save_booking(trip_id: str, booking: Dict[str, Any]):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT OR REPLACE INTO bookings (booking_id, trip_id, booking_type, provider, reference_number, amount, status, details_json)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        booking.get("booking_id", ""),
        trip_id,
        booking.get("booking_type", ""),
        booking.get("provider", ""),
        booking.get("reference_number", ""),
        booking.get("amount", 0.0),
        booking.get("status", "CONFIRMED"),
        json.dumps(booking.get("details", {}))
    ))
    conn.commit()
    conn.close()

# Initialize DB on module import
init_db()
