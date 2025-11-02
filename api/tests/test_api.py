"""
Test FastAPI endpoints
Run with: pytest api/tests/
"""

import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from api.main import app

client = TestClient(app)

def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "N.E.T.R.A." in response.json()["message"]

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "model_loaded" in data

def test_model_info():
    """Test model info endpoint"""
    response = client.get("/api/model/info")
    
    # Model might not be loaded in test environment
    if response.status_code == 200:
        data = response.json()
        assert "model_type" in data
        assert "accuracy" in data
    else:
        assert response.status_code == 503  # Service unavailable

def test_live_sensors():
    """Test live sensor data endpoint"""
    response = client.get("/api/sensors/live")
    assert response.status_code == 200
    data = response.json()
    assert "sensors" in data
    assert "timestamp" in data
    
    # Check all sensor types present
    sensors = data["sensors"]
    required_sensors = ["fume", "metal", "gpr", "ground_cv", "drone_cv", "disturbance", "thermal"]
    for sensor in required_sensors:
        assert sensor in sensors
        assert 0 <= sensors[sensor] <= 100

def test_analyze_threat():
    """Test threat analysis endpoint"""
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
        "location": "Test Location",
        "danger_level": "High",
        "explosive_class": "High Explosive"
    }
    
    response = client.post("/api/analyze", json=test_data)
    
    # Model might not be loaded in test environment
    if response.status_code == 200:
        data = response.json()
        assert "scan_id" in data
        assert "threat_level" in data
        assert "probability" in data
        assert data["threat_level"] in ["CRITICAL", "HIGH", "MODERATE", "LOW"]
        assert 0 <= data["probability"] <= 100
    else:
        assert response.status_code == 503  # Service unavailable

def test_analyze_invalid_sensors():
    """Test threat analysis with invalid sensor data"""
    invalid_data = {
        "sensors": {
            "fume": 150,  # Invalid: > 100
            "metal": 80.2,
            "gpr": 65.0,
            "ground_cv": 70.5,
            "drone_cv": 68.3,
            "disturbance": 55.0,
            "thermal": 45.0
        },
        "location": "Test Location"
    }
    
    response = client.post("/api/analyze", json=invalid_data)
    assert response.status_code == 422  # Validation error

def test_data_refresh():
    """Test data refresh endpoint"""
    response = client.post("/api/data/refresh")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data

def test_websocket_connection():
    """Test WebSocket connection"""
    with client.websocket_connect("/api/stream") as websocket:
        # Send test message
        websocket.send_json({"type": "test", "message": "hello"})
        
        # Receive acknowledgment
        data = websocket.receive_json()
        assert data["type"] == "ack"
        assert "timestamp" in data

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
