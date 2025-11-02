# N.E.T.R.A. FastAPI Backend

## 🚀 Quick Start

### Local Development

1. **Install Dependencies**
   ```powershell
   cd api
   pip install -r requirements.txt
   ```

2. **Run the Server**
   ```powershell
   # From project root
   uvicorn api.main:app --reload --port 8000
   
   # Or from api directory
   cd api
   python main.py
   ```

3. **Access API Documentation**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc
   - Health Check: http://localhost:8000/api/health

---

## 📡 API Endpoints

### Core Endpoints

#### 1. **POST /api/analyze** - Threat Analysis
Perform ML-powered threat analysis on sensor data.

**Request:**
```json
{
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
```

**Response:**
```json
{
  "scan_id": "SCAN_20251102_143052",
  "timestamp": "2025-11-02T14:30:52.123456",
  "location": "Guwahati, Assam",
  "threat_level": "HIGH",
  "probability": 78.45,
  "confidence": 78.45,
  "all_probabilities": {
    "CRITICAL": 12.5,
    "HIGH": 78.45,
    "MODERATE": 7.8,
    "LOW": 1.25
  },
  "feature_contributions": [
    {"name": "Multiple_Indicators", "importance": 49.8, "value": 4},
    {"name": "Fume_Detection", "importance": 11.8, "value": 75.5}
  ],
  "ml_powered": true,
  "model_version": "1.0"
}
```

#### 2. **GET /api/health** - Health Check
Check API and model status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-02T14:30:52.123456",
  "model_loaded": true,
  "uptime_seconds": 12345.67
}
```

#### 3. **GET /api/model/info** - Model Information
Get ML model details and capabilities.

**Response:**
```json
{
  "model_type": "XGBoost",
  "version": "1.0",
  "accuracy": 0.831,
  "training_samples": 10000,
  "features": ["Fume_Detection", "Metal_Detection", ...],
  "classes": ["CRITICAL", "HIGH", "MODERATE", "LOW"],
  "loaded": true
}
```

#### 4. **GET /api/sensors/live** - Live Sensor Data
Get real-time sensor readings (currently simulated).

**Response:**
```json
{
  "timestamp": "2025-11-02T14:30:52.123456",
  "sensors": {
    "fume": 45.67,
    "metal": 52.34,
    "gpr": 38.90,
    "ground_cv": 65.12,
    "drone_cv": 70.45,
    "disturbance": 42.10,
    "thermal": 35.80
  },
  "status": "simulated"
}
```

#### 5. **POST /api/data/refresh** - Refresh Dataset
Trigger background data regeneration.

**Response:**
```json
{
  "status": "Data refresh initiated",
  "timestamp": "2025-11-02T14:30:52.123456"
}
```

#### 6. **WebSocket /api/stream** - Real-time Streaming
WebSocket connection for live threat analysis streaming.

**Usage:**
```javascript
const ws = new WebSocket('ws://localhost:8000/api/stream');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received:', data);
};

ws.send(JSON.stringify({type: 'subscribe', location: 'Guwahati'}));
```

---

## 🔗 Streamlit Integration

### Option 1: Direct API Calls (Python)

```python
import requests

# Configure API endpoint
API_BASE_URL = "http://localhost:8000"

def analyze_via_api(sensors, location):
    """Call FastAPI for threat analysis"""
    response = requests.post(
        f"{API_BASE_URL}/api/analyze",
        json={
            "sensors": sensors,
            "location": location
        }
    )
    return response.json()

# Usage in Streamlit
analysis = analyze_via_api(sensor_data, location)
st.write(analysis['threat_level'])
```

### Option 2: Streamlit + FastAPI Hybrid

Keep current Streamlit with local ML, but add API fallback:

```python
try:
    # Try local ML first (fast)
    if ML_MODEL:
        analysis = local_ml_predict(sensors)
except:
    # Fallback to FastAPI (scalable)
    analysis = requests.post(f"{API_URL}/api/analyze", json=data).json()
```

---

## 🌐 Free Deployment Options

### Option 1: Railway.app (Recommended) ⭐

**Why:** Free tier, automatic HTTPS, easy deployment

1. **Create `Procfile`**:
   ```
   web: uvicorn api.main:app --host 0.0.0.0 --port $PORT
   ```

2. **Deploy**:
   - Connect GitHub repo to Railway
   - Set root directory to `/api`
   - Deploy automatically on push

**Free Tier:** 500 hours/month, auto-sleep after inactivity

### Option 2: Render.com

**Why:** Generous free tier, good for APIs

1. **Create `render.yaml`**:
   ```yaml
   services:
     - type: web
       name: netra-api
       env: python
       buildCommand: pip install -r api/requirements.txt
       startCommand: uvicorn api.main:app --host 0.0.0.0 --port $PORT
   ```

2. **Deploy**: Connect repo, auto-deploy on push

**Free Tier:** Auto-sleep after 15min inactivity, wakes on request

### Option 3: Fly.io

**Why:** Edge deployment, WebSocket support

1. **Install Fly CLI**:
   ```powershell
   irm https://fly.io/install.ps1 | iex
   ```

2. **Deploy**:
   ```powershell
   fly launch
   fly deploy
   ```

**Free Tier:** 3 shared VMs, 160GB bandwidth/month

### Option 4: Deta Space (Simplest)

**Why:** Easiest deployment, no config needed

1. **Install Deta CLI**
2. **Deploy**:
   ```powershell
   deta new --python
   deta deploy
   ```

**Free Tier:** Unlimited, no credit card required

---

## 🏗️ Architecture

```
┌─────────────────────┐         ┌──────────────────────┐
│   Streamlit Cloud   │◄───────►│   FastAPI Backend    │
│   (netra-*.app)     │  HTTPS  │   (Railway/Render)   │
│   Port: 8501        │         │   Port: 8000         │
└─────────────────────┘         └──────────────────────┘
         │                                  │
         │                                  │
    [User Browser]                 [ML Model (2.37MB)]
         │                         [XGBoost Inference]
         │                         [WebSocket Stream]
         │                                  │
         └──────────────────────────────────┘
              Real-time Updates via WS

```

### Data Flow:

1. **User** enters sensor data in Streamlit
2. **Streamlit** calls FastAPI `/api/analyze`
3. **FastAPI** runs ML inference
4. **Response** sent back to Streamlit
5. **WebSocket** broadcasts to all connected clients

---

## 🛠️ Configuration

### Environment Variables

Create `.env` file in `api/` directory:

```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Model Paths
MODEL_PATH=../models/netra_xgboost_model.pkl
ENCODERS_PATH=../models/netra_encoders.pkl

# CORS (for production)
ALLOWED_ORIGINS=https://netra-unified-bet-001.streamlit.app

# Logging
LOG_LEVEL=INFO
```

### CORS Configuration

For production, update `main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://netra-unified-bet-001.streamlit.app",
        "http://localhost:8501"  # Local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🧪 Testing

### Run Tests

```powershell
# Install test dependencies
pip install pytest httpx

# Run tests
pytest api/tests/
```

### Manual Testing

```powershell
# Test health endpoint
curl http://localhost:8000/api/health

# Test analysis endpoint
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "sensors": {"fume": 75, "metal": 80, "gpr": 65, "ground_cv": 70, "drone_cv": 68, "disturbance": 55, "thermal": 45},
    "location": "Test Location"
  }'
```

---

## 📊 Performance

- **Average Response Time**: ~50ms (local), ~200ms (cloud)
- **Model Inference**: ~5ms per prediction
- **Concurrent Requests**: 100+ (with uvicorn workers)
- **WebSocket Connections**: 1000+ simultaneous

---

## 🔒 Security (TODO for Production)

1. **API Key Authentication**
   ```python
   from fastapi.security import APIKeyHeader
   api_key_header = APIKeyHeader(name="X-API-Key")
   ```

2. **Rate Limiting**
   ```python
   from slowapi import Limiter
   limiter = Limiter(key_func=get_remote_address)
   ```

3. **HTTPS Only** (handled by deployment platform)

---

## 📈 Monitoring

### Add Prometheus Metrics

```python
from prometheus_client import Counter, Histogram

predictions_total = Counter('predictions_total', 'Total predictions')
prediction_duration = Histogram('prediction_duration_seconds', 'Prediction duration')
```

---

## 🤝 Support

For issues or questions:
- GitHub Issues: https://github.com/404Avinash/netra_beta/issues
- Deployment Docs: See this README

---

**Built with ❤️ for Hackathon**
