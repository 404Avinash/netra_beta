"""
N.E.T.R.A. FastAPI Backend
Handles ML inference, data streaming, and API endpoints
"""

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
import joblib
import json
import numpy as np
import pandas as pd
from datetime import datetime
import asyncio
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

# Initialize FastAPI app
app = FastAPI(
    title="N.E.T.R.A. API",
    description="Neural Explosive Threat Recognition Algorithm - ML Backend",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for Streamlit integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify Streamlit Cloud URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for ML model
ML_MODEL = None
ML_ENCODERS = None
ML_FEATURES = None
ML_METADATA = None
MODEL_LOADED = False

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass

manager = ConnectionManager()

# Pydantic models for request/response
class SensorData(BaseModel):
    fume: float = Field(..., ge=0, le=100, description="Fume detection percentage")
    metal: float = Field(..., ge=0, le=100, description="Metal detection percentage")
    gpr: float = Field(..., ge=0, le=100, description="Ground Penetrating Radar reading")
    ground_cv: float = Field(..., ge=0, le=100, description="Ground Computer Vision score")
    drone_cv: float = Field(..., ge=0, le=100, description="Drone Computer Vision score")
    disturbance: float = Field(..., ge=0, le=100, description="Ground disturbance level")
    thermal: float = Field(..., ge=0, le=100, description="Thermal signature reading")

class ThreatAnalysisRequest(BaseModel):
    sensors: SensorData
    location: str = Field(..., description="Location name or coordinates")
    danger_level: Optional[str] = Field(default="Medium", description="Known danger level")
    explosive_class: Optional[str] = Field(default="Low Explosive", description="Expected explosive type")

class ThreatAnalysisResponse(BaseModel):
    scan_id: str
    timestamp: str
    location: str
    threat_level: str
    probability: float
    confidence: float
    all_probabilities: Dict[str, float]
    feature_contributions: List[Dict[str, Any]]
    ml_powered: bool
    model_version: str

class ModelInfoResponse(BaseModel):
    model_type: str
    version: str
    accuracy: float
    training_samples: int
    features: List[str]
    classes: List[str]
    loaded: bool

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    model_loaded: bool
    uptime_seconds: float

# Startup event - Load ML model
@app.on_event("startup")
async def load_ml_model():
    """Load ML model on startup"""
    global ML_MODEL, ML_ENCODERS, ML_FEATURES, ML_METADATA, MODEL_LOADED
    
    try:
        base_path = Path(__file__).parent.parent / "models"
        
        ML_MODEL = joblib.load(base_path / 'netra_xgboost_model.pkl')
        ML_ENCODERS = joblib.load(base_path / 'netra_encoders.pkl')
        
        with open(base_path / 'netra_features.json', 'r') as f:
            ML_FEATURES = json.load(f)
        
        with open(base_path / 'netra_model_metadata.json', 'r') as f:
            ML_METADATA = json.load(f)
        
        MODEL_LOADED = True
        print("✅ ML Model loaded successfully!")
        print(f"📊 Model: {ML_METADATA.get('model_type', 'XGBoost')}")
        print(f"🎯 Test Accuracy: {ML_METADATA.get('test_accuracy', 0)*100:.2f}%")
        
    except Exception as e:
        print(f"❌ Failed to load ML model: {e}")
        MODEL_LOADED = False

# Root endpoint
@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "N.E.T.R.A. API is running",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/health"
    }

# Health check endpoint
@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Check API health status"""
    return HealthResponse(
        status="healthy" if MODEL_LOADED else "degraded",
        timestamp=datetime.now().isoformat(),
        model_loaded=MODEL_LOADED,
        uptime_seconds=0.0  # TODO: Implement uptime tracking
    )

# Model info endpoint
@app.get("/api/model/info", response_model=ModelInfoResponse)
async def get_model_info():
    """Get ML model information"""
    if not MODEL_LOADED:
        raise HTTPException(status_code=503, detail="ML model not loaded")
    
    return ModelInfoResponse(
        model_type=ML_METADATA.get('model_type', 'XGBoost'),
        version=ML_METADATA.get('version', '1.0'),
        accuracy=ML_METADATA.get('test_accuracy', 0.831),
        training_samples=ML_METADATA.get('training_samples', 10000),
        features=ML_FEATURES.get('all_features', []),
        classes=list(ML_ENCODERS['target_encoder'].classes_),
        loaded=True
    )

# Main threat analysis endpoint
@app.post("/api/analyze", response_model=ThreatAnalysisResponse)
async def analyze_threat(request: ThreatAnalysisRequest):
    """Perform ML-powered threat analysis"""
    if not MODEL_LOADED:
        raise HTTPException(status_code=503, detail="ML model not loaded")
    
    try:
        # Convert sensor data to dict
        sensors = request.sensors.dict()
        
        # Prepare features for ML model
        features = {
            'Fume_Detection': sensors['fume'],
            'Metal_Detection': sensors['metal'],
            'GPR_Reading': sensors['gpr'],
            'Ground_CV': sensors['ground_cv'],
            'Drone_CV': sensors['drone_cv'],
            'Disturbance': sensors['disturbance'],
            'Thermal': sensors['thermal']
        }
        
        # Add derived features
        features['Fume_Metal_Product'] = sensors['fume'] * sensors['metal'] / 100
        features['CV_Average'] = (sensors['ground_cv'] + sensors['drone_cv']) / 2
        features['Surface_Anomaly'] = (sensors['disturbance'] + sensors['thermal']) / 2
        features['High_Fume_Metal'] = int(sensors['fume'] > 70 and sensors['metal'] > 70)
        features['High_CV_Detection'] = int(sensors['ground_cv'] > 70 or sensors['drone_cv'] > 70)
        features['Multiple_Indicators'] = sum([
            int(sensors['fume'] > 60),
            int(sensors['metal'] > 60),
            int(sensors['gpr'] > 60),
            int(sensors['disturbance'] > 60)
        ])
        
        # Encode explosive characteristics
        try:
            features['Danger_Level_Encoded'] = ML_ENCODERS['danger_encoder'].transform([request.danger_level])[0]
            features['Explosive_Class_Encoded'] = ML_ENCODERS['class_encoder'].transform([request.explosive_class])[0]
        except:
            features['Danger_Level_Encoded'] = 0
            features['Explosive_Class_Encoded'] = 0
        
        # Create feature array in correct order
        X_new = np.array([[features[f] for f in ML_FEATURES['all_features']]])
        
        # ML PREDICTION
        prediction = ML_MODEL.predict(X_new)[0]
        probabilities = ML_MODEL.predict_proba(X_new)[0]
        
        threat_level = ML_ENCODERS['target_encoder'].inverse_transform([prediction])[0]
        probability = float(probabilities[prediction] * 100)
        
        # Get all class probabilities
        all_classes = ML_ENCODERS['target_encoder'].classes_
        all_probabilities = {
            str(cls): float(prob * 100) 
            for cls, prob in zip(all_classes, probabilities)
        }
        
        # Get feature importance
        feature_importance = ML_MODEL.feature_importances_
        feature_names = ML_FEATURES['all_features']
        importance_dict = dict(zip(feature_names, feature_importance))
        top_features = sorted(importance_dict.items(), key=lambda x: x[1], reverse=True)[:5]
        
        feature_contributions = [
            {
                'name': name,
                'importance': float(imp * 100),
                'value': float(features.get(name, 0))
            }
            for name, imp in top_features
        ]
        
        # Generate scan ID
        scan_id = f"SCAN_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        response = ThreatAnalysisResponse(
            scan_id=scan_id,
            timestamp=datetime.now().isoformat(),
            location=request.location,
            threat_level=threat_level,
            probability=probability,
            confidence=probability,
            all_probabilities=all_probabilities,
            feature_contributions=feature_contributions,
            ml_powered=True,
            model_version=ML_METADATA.get('version', '1.0')
        )
        
        # Broadcast to WebSocket clients
        await manager.broadcast({
            "type": "threat_analysis",
            "data": response.dict()
        })
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

# Live sensor data endpoint (simulated for now)
@app.get("/api/sensors/live")
async def get_live_sensors():
    """Get live sensor data (simulated)"""
    # In production, this would connect to actual hardware
    import random
    
    return {
        "timestamp": datetime.now().isoformat(),
        "sensors": {
            "fume": round(random.uniform(10, 90), 2),
            "metal": round(random.uniform(10, 90), 2),
            "gpr": round(random.uniform(10, 90), 2),
            "ground_cv": round(random.uniform(10, 90), 2),
            "drone_cv": round(random.uniform(10, 90), 2),
            "disturbance": round(random.uniform(10, 90), 2),
            "thermal": round(random.uniform(10, 90), 2)
        },
        "status": "simulated"
    }

# Data refresh endpoint
@app.post("/api/data/refresh")
async def refresh_data(background_tasks: BackgroundTasks):
    """Trigger data refresh/regeneration"""
    def regenerate_data():
        try:
            # Run data generation script
            import subprocess
            subprocess.run([
                sys.executable,
                str(Path(__file__).parent.parent / "development" / "generate_large_dataset.py")
            ])
        except Exception as e:
            print(f"Error regenerating data: {e}")
    
    background_tasks.add_task(regenerate_data)
    
    return {
        "status": "Data refresh initiated",
        "timestamp": datetime.now().isoformat()
    }

# WebSocket endpoint for real-time streaming
@app.websocket("/api/stream")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for real-time threat streaming"""
    await manager.connect(websocket)
    
    try:
        while True:
            # Wait for client messages
            data = await websocket.receive_json()
            
            # Echo back with timestamp
            response = {
                "type": "ack",
                "timestamp": datetime.now().isoformat(),
                "received": data
            }
            await websocket.send_json(response)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("WebSocket client disconnected")

# Run with: uvicorn api.main:app --reload --port 8000
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
