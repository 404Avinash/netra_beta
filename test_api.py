"""
Quick test script for FastAPI endpoints
Run after starting the API: python test_api.py
"""

import requests
import json
from datetime import datetime

API_BASE = "http://localhost:8000"

def test_endpoint(name, method, endpoint, data=None):
    """Test an API endpoint"""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"{'='*60}")
    
    try:
        url = f"{API_BASE}{endpoint}"
        
        if method == "GET":
            response = requests.get(url, timeout=5)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=5)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success!")
            print(f"Response: {json.dumps(result, indent=2)[:500]}")
        else:
            print(f"❌ Failed: {response.text}")
    
    except requests.exceptions.ConnectionError:
        print(f"❌ Connection failed - Is the API running on {API_BASE}?")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    print("🧪 N.E.T.R.A. API Testing")
    print(f"API Base URL: {API_BASE}")
    
    # Test 1: Root endpoint
    test_endpoint("Root Endpoint", "GET", "/")
    
    # Test 2: Health check
    test_endpoint("Health Check", "GET", "/api/health")
    
    # Test 3: Model info
    test_endpoint("Model Info", "GET", "/api/model/info")
    
    # Test 4: Live sensors
    test_endpoint("Live Sensor Data", "GET", "/api/sensors/live")
    
    # Test 5: Threat analysis
    test_data = {
        "sensors": {
            "fume": 75.5,
            "metal": 80.2,
            "gpr": 65.0,
            "ground_cv": 70.5,
            "drone_cv": 68.3,
            "disturbance": 55.0,
            "thermal": 45.0
        },
        "location": "Guwahati, Assam",
        "danger_level": "High",
        "explosive_class": "High Explosive"
    }
    test_endpoint("Threat Analysis", "POST", "/api/analyze", test_data)
    
    print(f"\n{'='*60}")
    print("✅ Testing Complete!")
    print(f"{'='*60}")
    print("\n📚 Visit API documentation at: http://localhost:8000/docs")

if __name__ == "__main__":
    main()
