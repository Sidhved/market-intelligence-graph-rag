import requests
import json

def test_api():
    base_url = "http://localhost:8000"
    
    # Test adding a car
    car_data = {
        "name": "Tesla Model 3",
        "manufacturer": "Tesla",
        "segment": "Electric Sedan",
        "features": ["Autopilot", "Over-the-air updates", "Minimalist interior"],
        "price_range": "$40,000-$60,000",
        "competitors": ["BMW i4", "Polestar 2"],
        "market_position": "Premium Electric Vehicle"
    }
    
    response = requests.post(
        f"{base_url}/api/add_car",
        json=car_data
    )
    print("Add car response:", response.json())
    
    # Test market query
    query_data = {
        "query": "Compare charging infrastructure between Tesla and other EV manufacturers",
        "top_k": 3
    }
    
    response = requests.post(
        f"{base_url}/api/query_market",
        json=query_data
    )
    print("Query response:", json.dumps(response.json(), indent=2))
    
    # Test status
    response = requests.get(f"{base_url}/api/status")
    print("Status:", response.json())

# In tests/test_api.py

def test_multiple_cars():
    base_url = "http://localhost:8000"
    
    cars = [
        {
            "name": "BMW i4",
            "manufacturer": "BMW",
            "segment": "Electric Sedan",
            "features": ["BMW iDrive", "DC Fast Charging", "Premium Audio"],
            "price_range": "$45,000-$65,000",
            "competitors": ["Tesla Model 3", "Polestar 2"],
            "market_position": "Luxury Electric Vehicle"
        },
        {
            "name": "Polestar 2",
            "manufacturer": "Polestar",
            "segment": "Electric Fastback",
            "features": ["Google Android Automotive", "Over-the-air updates", "Pilot Assist"],
            "price_range": "$40,000-$55,000",
            "competitors": ["Tesla Model 3", "BMW i4"],
            "market_position": "Premium Electric Vehicle"
        }
    ]
    
    for car in cars:
        response = requests.post(f"{base_url}/api/add_car", json=car)
        print(f"Added {car['name']}: {response.json()}")
    
    # Test different queries
    queries = [
        "Compare performance features between these electric vehicles",
        "Which car offers the best value for money?",
        "Compare the technology features across these vehicles"
    ]
    
    for query in queries:
        response = requests.post(
            f"{base_url}/api/query_market",
            json={"query": query, "top_k": 3}
        )
        print(f"\nQuery: {query}")
        print(json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    test_multiple_cars()