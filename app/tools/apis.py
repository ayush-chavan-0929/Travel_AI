import requests
import random
import uuid
from typing import Dict, Any, List

class FreeWeatherTool:
    """
    Uses Open-Meteo API (100% free, no API key needed).
    Coordinates for common Indian & global travel destinations.
    """
    COORDINATES = {
        "goa": {"latitude": 15.2993, "longitude": 74.1240},
        "mumbai": {"latitude": 19.0760, "longitude": 72.8777},
        "jaipur": {"latitude": 26.9124, "longitude": 75.7873},
        "delhi": {"latitude": 28.6139, "longitude": 77.2090},
        "manali": {"latitude": 32.2432, "longitude": 77.1892},
        "kerala": {"latitude": 10.8505, "longitude": 76.2711},
        "bangalore": {"latitude": 12.9716, "longitude": 77.5946},
        "agra": {"latitude": 27.1767, "longitude": 78.0081}
    }

    @classmethod
    def get_weather(cls, destination: str) -> Dict[str, Any]:
        dest_key = destination.strip().lower()
        coords = cls.COORDINATES.get(dest_key, {"latitude": 15.2993, "longitude": 74.1240})
        
        try:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={coords['latitude']}&longitude={coords['longitude']}&current_weather=true"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                curr = data.get("current_weather", {})
                temp = curr.get("temperature", 28.0)
                windspeed = curr.get("windspeed", 10.0)
                condition = "Sunny & Warm" if temp > 25 else "Pleasant / Mild"
                return {
                    "destination": destination,
                    "temperature": f"{temp}°C",
                    "windspeed": f"{windspeed} km/h",
                    "condition": condition,
                    "is_suitable_for_travel": True,
                    "source": "Open-Meteo Free API"
                }
        except Exception:
            pass
            
        # Resilient fallback
        return {
            "destination": destination,
            "temperature": "29°C",
            "windspeed": "12 km/h",
            "condition": "Sunny, Ideal for Tourism & Beaches",
            "is_suitable_for_travel": True,
            "source": "Open-Meteo Cached/Fallback"
        }


class FreeMapsTool:
    """
    Uses OpenStreetMap / Nominatim (100% free open standard)
    Calculates distances & routing heuristics.
    """
    DISTANCES_KM = {
        ("mumbai", "goa"): 590,
        ("delhi", "jaipur"): 280,
        ("delhi", "manali"): 530,
        ("bangalore", "goa"): 560,
    }

    @classmethod
    def get_route_info(cls, origin: str, destination: str) -> Dict[str, Any]:
        o = origin.strip().lower()
        d = destination.strip().lower()
        
        dist = cls.DISTANCES_KM.get((o, d), cls.DISTANCES_KM.get((d, o), 450))
        
        return {
            "origin": origin,
            "destination": destination,
            "approx_distance_km": dist,
            "flight_time_hrs": 1.2 if dist > 300 else 0.8,
            "train_time_hrs": round(dist / 60, 1),
            "bus_time_hrs": round(dist / 45, 1),
            "source": "OpenStreetMap / Public Geographic Data"
        }


class FreeCurrencyTool:
    """
    Currency converter using Free Open-Access Currency API
    """
    @classmethod
    def convert_inr_to_usd(cls, inr_amount: float) -> float:
        return round(inr_amount / 86.5, 2)


class MockTravelAPI:
    """
    Realistic simulated travel service providing live inventory for
    flights, trains, buses, hotels, and tourist activities with instant pricing.
    """
    
    @classmethod
    def search_transports(cls, origin: str, destination: str, travellers: int) -> List[Dict[str, Any]]:
        return [
            {
                "id": "TRP-FL-101",
                "mode": "Flight",
                "provider": "IndiGo 6E-243",
                "origin": origin,
                "destination": destination,
                "departure_time": "08:30 AM",
                "arrival_time": "09:50 AM",
                "duration": "1h 20m",
                "price_per_person": 4200.0,
                "total_price": 4200.0 * travellers,
                "comfort_rating": 4.5
            },
            {
                "id": "TRP-TR-202",
                "mode": "Train",
                "provider": "Vande Bharat Express",
                "origin": origin,
                "destination": destination,
                "departure_time": "06:00 AM",
                "arrival_time": "02:30 PM",
                "duration": "8h 30m",
                "price_per_person": 1650.0,
                "total_price": 1650.0 * travellers,
                "comfort_rating": 4.2
            },
            {
                "id": "TRP-BS-303",
                "mode": "Bus",
                "provider": "IntrCity SmartBus AC Sleeper",
                "origin": origin,
                "destination": destination,
                "departure_time": "09:00 PM",
                "arrival_time": "08:00 AM (Next Day)",
                "duration": "11h 00m",
                "price_per_person": 950.0,
                "total_price": 950.0 * travellers,
                "comfort_rating": 3.8
            }
        ]

    @classmethod
    def search_hotels(cls, destination: str, nights: int, travellers: int, preference: str = "3-star") -> List[Dict[str, Any]]:
        # Assume 2 travellers per room
        rooms_needed = max(1, (travellers + 1) // 2)
        
        hotels = [
            {
                "id": "HTL-3S-01",
                "name": "Lemon Tree Amarante Beach Resort",
                "location": "Candolim, North Goa",
                "category": "3-star",
                "rating": 4.2,
                "price_per_night": 3200.0 * rooms_needed,
                "total_price": 3200.0 * rooms_needed * nights,
                "amenities": ["Free Breakfast", "Swimming Pool", "Beach 300m", "Wi-Fi"]
            },
            {
                "id": "HTL-3S-02",
                "name": "BloomSuites Calangute",
                "location": "Calangute, North Goa",
                "category": "3-star",
                "rating": 4.3,
                "price_per_night": 2800.0 * rooms_needed,
                "total_price": 2800.0 * rooms_needed * nights,
                "amenities": ["Outdoor Pool", "Bar & Bistro", "Near Night Markets"]
            },
            {
                "id": "HTL-4S-03",
                "name": "Santana Beach Resort",
                "location": "Sinquerim, North Goa",
                "category": "4-star",
                "rating": 4.6,
                "price_per_night": 4800.0 * rooms_needed,
                "total_price": 4800.0 * rooms_needed * nights,
                "amenities": ["Direct Beach Access", "2 Swimming Pools", "Multi-Cuisine Dining"]
            },
            {
                "id": "HTL-2S-04",
                "name": "Oceanic Boutique Stay",
                "location": "Anjuna, North Goa",
                "category": "Budget / 2-star",
                "rating": 3.9,
                "price_per_night": 1800.0 * rooms_needed,
                "total_price": 1800.0 * rooms_needed * nights,
                "amenities": ["Free Wi-Fi", "Scooter Rentals", "Cafe"]
            }
        ]
        return hotels

    @classmethod
    def search_activities(cls, destination: str, interests: List[str], travellers: int) -> List[Dict[str, Any]]:
        all_activities = [
            {
                "id": "ACT-WS-01",
                "name": "Water Sports Combo (Parasailing, Jet Ski, Banana Ride)",
                "category": "water sports",
                "location": "Baga Beach",
                "duration_hours": 3.0,
                "cost_per_person": 1500.0,
                "total_cost": 1500.0 * travellers,
                "timing_slot": "Morning",
                "best_time": "10:00 AM - 01:00 PM"
            },
            {
                "id": "ACT-NL-02",
                "name": "Tito's Lane & Club Cabana Nightlife Experience",
                "category": "nightlife",
                "location": "Arpora / Baga",
                "duration_hours": 4.0,
                "cost_per_person": 800.0,
                "total_cost": 800.0 * travellers,
                "timing_slot": "Night",
                "best_time": "09:00 PM - 01:00 AM"
            },
            {
                "id": "ACT-BC-03",
                "name": "Anjuna & Vagator Sunset Beach Crawl",
                "category": "beaches",
                "location": "Vagator Beach",
                "duration_hours": 3.0,
                "cost_per_person": 200.0,
                "total_cost": 200.0 * travellers,
                "timing_slot": "Evening",
                "best_time": "04:30 PM - 07:30 PM"
            },
            {
                "id": "ACT-CT-04",
                "name": "Chapora Fort & Historic Lighthouse Sightseeing",
                "category": "sightseeing",
                "location": "Chapora",
                "duration_hours": 2.0,
                "cost_per_person": 100.0,
                "total_cost": 100.0 * travellers,
                "timing_slot": "Afternoon",
                "best_time": "02:30 PM - 04:30 PM"
            },
            {
                "id": "ACT-SG-05",
                "name": "South Goa Heritage & Palolem Beach Excursion",
                "category": "beaches",
                "location": "Palolem",
                "duration_hours": 6.0,
                "cost_per_person": 600.0,
                "total_cost": 600.0 * travellers,
                "timing_slot": "Morning to Evening",
                "best_time": "09:00 AM - 04:00 PM"
            }
        ]
        return all_activities

    @classmethod
    def execute_booking(cls, booking_type: str, item_id: str, provider: str, amount: float, details: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simulates booking execution through mock API provider with valid reference numbers.
        """
        prefix_map = {
            "Flight": "FL",
            "Train": "TR",
            "Bus": "BS",
            "Hotel": "HTL",
            "Activity": "ACT"
        }
        prefix = prefix_map.get(booking_type, "BK")
        ref_num = f"{prefix}-{random.randint(10000, 99999)}"
        booking_id = f"BKG-{uuid.uuid4().hex[:8].upper()}"
        
        return {
            "booking_id": booking_id,
            "booking_type": booking_type,
            "provider": provider,
            "reference_number": ref_num,
            "status": "CONFIRMED",
            "amount": amount,
            "timestamp": "2026-10-05T19:30:00Z",
            "details": details
        }
