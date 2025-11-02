# 🤖 N.E.T.R.A. ML/CV Upgrade & Automation Plan

**Date**: November 2, 2025  
**Current Status**: Bayesian Rule-Based System  
**Goal**: Upgrade to Real ML/CV + Data Automation  

---

## 📋 TABLE OF CONTENTS
1. [Current System Analysis](#current-system-analysis)
2. [ML/CV Questions Answered](#mlcv-questions-answered)
3. [Upgrade Plan - Phase by Phase](#upgrade-plan)
4. [Data Automation Strategy](#data-automation-strategy)
5. [Implementation Roadmap](#implementation-roadmap)

---

## 🔍 CURRENT SYSTEM ANALYSIS

### What We Have Now

**Streamlit App (`netra_unified_app.py`)**:
```python
# Current "AI" is actually weighted formula:
weights = {
    'fume': 0.25,
    'metal': 0.20,
    'gpr': 0.20,
    'ground_cv': 0.10,  # ← Not real computer vision
    'drone_cv': 0.10,   # ← Not real computer vision
    'disturbance': 0.10,
    'thermal': 0.05
}
probability = sum(sensors[k] * weights[k] for k in sensors.keys())
```

**Reality Check**:
- ❌ **No real Machine Learning** - Just weighted averages
- ❌ **No Computer Vision models** - Ground_CV and Drone_CV are just slider values
- ❌ **No trained models** - No .pth, .h5, or .pkl files
- ❌ **No image processing** - No actual images being analyzed
- ✅ **Works well** - But it's rule-based, not AI

---

## 💡 ML/CV QUESTIONS ANSWERED

### Question 1: "Does Streamlit webapp handle ML parts?"

**Current Answer**: ❌ **NO**
- Right now it's just math formulas
- No actual ML models are loaded or running
- "Computer Vision" is simulated as percentage values

**Future Answer**: ✅ **YES, IT CAN!**
- Streamlit can run ML models (TensorFlow, PyTorch, scikit-learn)
- BUT has limitations for heavy models
- Need to consider: Model size, inference time, memory

**Architecture Options**:

```
OPTION A: Streamlit Handles Everything (Simple)
┌─────────────────────────────────────────┐
│  Streamlit App                          │
│  ├── Load sensor data                   │
│  ├── Load ML model (.pkl/.pth)          │
│  ├── Run inference                      │
│  └── Display results                    │
└─────────────────────────────────────────┘
✅ Pros: Simple, one place
❌ Cons: Slow for heavy models, high memory

OPTION B: Hybrid - Backend API (Recommended)
┌──────────────┐         ┌──────────────┐
│  Streamlit   │────────▶│   FastAPI    │
│  (Frontend)  │  HTTP   │  (ML Server) │
└──────────────┘         └──────────────┘
                              │
                         ML Models
                         ├── YOLOv8
                         ├── ResNet
                         └── Random Forest
✅ Pros: Scalable, separate concerns, faster
✅ Cons: More complex setup

OPTION C: Local-First with Fallback (Best for You)
┌─────────────────────────────────────────┐
│  Streamlit App                          │
│  ├── Try load local models              │
│  │   └── If success → ML mode           │
│  └── If fail → Rule-based fallback      │
└─────────────────────────────────────────┘
✅ Pros: Works everywhere, graceful degradation
✅ Perfect for your "local-first" approach
```

---

### Question 2: "Computer Vision flows from v2 beta notebook?"

From `NETRA_BETA_v2.ipynb`, I see references to:
- **YOLOv8**: Object detection (ground rover camera)
- **ResNet**: Image classification (drone aerial view)
- **CV pipelines**: But NOT actually implemented

**What notebook mentions**:
```
"Machine learning models (YOLOv8, ResNet) are referenced 
but not trained here"
```

**Translation**: It's a **concept/architecture** document, not working code.

**What You Need for Real CV**:

1. **Ground Computer Vision (Rover Camera)**:
   ```python
   Input: Image from ground camera
   Model: YOLOv8 or Faster R-CNN
   Output: Detected objects (wires, suspicious packages, disturbed soil)
   Confidence: 0-100%
   ```

2. **Drone Computer Vision (Aerial Camera)**:
   ```python
   Input: Aerial image/video frame
   Model: ResNet + Custom classifier
   Output: Ground anomaly detection (heat signatures, patterns)
   Confidence: 0-100%
   ```

3. **Reality for Your Project**:
   - ❌ You don't have actual camera feeds yet
   - ❌ You don't have trained models yet
   - ✅ You have the architecture planned
   - ✅ You can simulate CV outputs (what you do now)

---

## 🚀 UPGRADE PLAN - PHASE BY PHASE

### 🎯 PHASE 1: Add Real ML for Sensor Fusion (2-3 days)

**Goal**: Replace weighted formula with actual ML model

**Current**:
```python
probability = sum(sensors[k] * weights[k] for k in sensors.keys())
```

**Upgrade to**:
```python
import joblib
model = joblib.load('models/netra_rf_model.pkl')
probability = model.predict_proba([sensor_values])[0][1] * 100
```

**Steps**:
1. ✅ **Train a model** on your 1200 historical records
2. ✅ **Use scikit-learn Random Forest** (fast, lightweight)
3. ✅ **Save model as .pkl file**
4. ✅ **Load in Streamlit** with try-except fallback
5. ✅ **Deploy to Streamlit Cloud** (model file < 100MB works fine)

**Code Changes**:
```python
# File: netra_unified_app.py

# Add at top
try:
    import joblib
    NETRA_ML_MODEL = joblib.load('models/threat_detector.pkl')
    ML_MODE = True
except:
    ML_MODE = False
    print("⚠️ ML model not found, using rule-based mode")

# Modify analyze function
def analyze_threat(sensors):
    if ML_MODE:
        # Real ML prediction
        features = [sensors['fume'], sensors['metal'], sensors['gpr'],
                   sensors['ground_cv'], sensors['drone_cv'], 
                   sensors['disturbance'], sensors['thermal']]
        probability = NETRA_ML_MODEL.predict_proba([features])[0][1] * 100
    else:
        # Fallback to weighted formula
        probability = weighted_calculation(sensors)
    
    return probability
```

**Training Script** (I can create this):
```python
# File: development/train_ml_model.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load your 1200 historical records
df = pd.read_csv('netra_threat_log.csv')

# Features: sensor readings
X = df[['Fume_Detection', 'Metal_Detection', 'GPR_Reading',
        'Ground_CV', 'Drone_CV', 'Disturbance', 'Thermal']]

# Target: threat level (convert to binary or multi-class)
y = (df['Threat_Probability'] > 50).astype(int)

# Train
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Save
joblib.dump(model, 'models/threat_detector.pkl')
print("✅ Model trained and saved!")
```

---

### 🎯 PHASE 2: Add Computer Vision (Simulated) (1 day)

**Goal**: Make CV outputs look more realistic

**Current**: User slides = Ground_CV value
**Problem**: Not realistic, too manual

**Upgrade**: Simulate CV from other sensors + noise
```python
def simulate_ground_cv(sensors, has_explosive_signature):
    """Simulate what a YOLO model might output"""
    base_detection = 0
    
    # If fume + metal high → likely visible anomaly
    if sensors['fume'] > 70 and sensors['metal'] > 60:
        base_detection = np.random.uniform(75, 95)
    elif sensors['disturbance'] > 60:
        base_detection = np.random.uniform(50, 75)
    else:
        base_detection = np.random.uniform(10, 40)
    
    # Add realistic noise
    noise = np.random.normal(0, 5)
    return np.clip(base_detection + noise, 0, 100)

def simulate_drone_cv(ground_cv, thermal):
    """Simulate aerial CV correlation"""
    # Aerial view should somewhat correlate with ground + thermal
    correlation = (ground_cv * 0.6 + thermal * 0.4)
    noise = np.random.normal(0, 8)
    return np.clip(correlation + noise, 0, 100)
```

**Result**: More believable "AI" behavior without actual models

---

### 🎯 PHASE 3: Add Real CV (With Actual Models) (5-7 days)

**Only do this if you have/plan to have**:
- ✅ Camera feeds (images/video)
- ✅ Compute resources (GPU helps)
- ✅ Time to train/fine-tune models

**Architecture**:
```python
# File: netra_cv_engine.py

import torch
from ultralytics import YOLO
import cv2

class NetraComputerVision:
    def __init__(self):
        self.ground_model = YOLO('models/yolov8_ied.pt')
        # Fine-tuned on IED/explosives dataset
        
        self.drone_model = torch.load('models/resnet_aerial.pth')
        # Trained on aerial anomaly detection
    
    def analyze_ground_image(self, image_path):
        """Run YOLOv8 on ground rover camera"""
        results = self.ground_model(image_path)
        
        detections = []
        confidence = 0
        
        for result in results:
            boxes = result.boxes
            for box in boxes:
                if box.cls in [0, 1, 2]:  # IED classes
                    confidence = max(confidence, float(box.conf))
                    detections.append({
                        'class': self.ground_model.names[int(box.cls)],
                        'confidence': float(box.conf),
                        'bbox': box.xyxy[0].tolist()
                    })
        
        return {
            'detection_confidence': confidence * 100,
            'objects_detected': detections,
            'threat_present': confidence > 0.6
        }
    
    def analyze_drone_image(self, image_path):
        """Run ResNet on drone camera"""
        # Preprocessing, inference, postprocessing
        # ...
        return {'anomaly_score': 0-100}
```

**Streamlit Integration**:
```python
# In netra_unified_app.py

# Add upload widget
uploaded_ground = st.file_uploader("📸 Upload Ground Camera Image", 
                                   type=['jpg', 'png'])
uploaded_drone = st.file_uploader("🛸 Upload Drone Camera Image", 
                                  type=['jpg', 'png'])

if uploaded_ground:
    cv_results = netra_cv.analyze_ground_image(uploaded_ground)
    st.write(f"Ground CV Confidence: {cv_results['detection_confidence']:.1f}%")
    
    # Use this instead of slider
    sensors['ground_cv'] = cv_results['detection_confidence']
```

**Challenges**:
- 📦 YOLOv8 model ~100MB (might hit Streamlit Cloud limits)
- 🐌 Inference slow without GPU
- 💾 Need image storage/handling

**Solution**: Use API backend (FastAPI) for CV inference if needed

---

## 📡 DATA AUTOMATION STRATEGY

### Current Problem
- ❌ Data is static CSV file
- ❌ Manually regenerated via script
- ❌ No real sensor connections

### Your Vision (I understand)
> "Automate data refresh to sensors and main sources"
> "If system can access it (locally or on Streamlit), utilize the data"

### 🎯 SOLUTION: Tiered Data Sources

```
┌──────────────────────────────────────────────────────────────┐
│                    N.E.T.R.A. DATA LAYER                     │
└──────────────────────────────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
    [TIER 1]          [TIER 2]          [TIER 3]
  Real Sensors     Simulated API      Static CSV
  (If available)  (Auto-refresh)    (Fallback)
        │                 │                 │
        ▼                 ▼                 ▼
    Hardware       generate_data.py    threat_log.csv
    Interface       (Scheduled)         (Backup)
```

### Implementation: Smart Data Connector

```python
# File: data_connector.py

class NetraDataConnector:
    """Intelligent data source manager"""
    
    def __init__(self):
        self.data_source = self.detect_available_source()
    
    def detect_available_source(self):
        """Auto-detect best available data source"""
        
        # Priority 1: Check for real hardware sensors
        if self.check_hardware_connection():
            print("✅ Connected to hardware sensors")
            return "HARDWARE"
        
        # Priority 2: Check for simulation API
        elif self.check_simulation_api():
            print("✅ Using simulation API")
            return "SIMULATION_API"
        
        # Priority 3: Use static CSV
        else:
            print("⚠️ Using static CSV (no live connection)")
            return "STATIC_CSV"
    
    def check_hardware_connection(self):
        """Try to connect to real sensors"""
        try:
            # Check if serial port available
            import serial
            ports = serial.tools.list_ports.comports()
            
            # Check for Raspberry Pi GPIO
            if os.path.exists('/dev/gpiochip0'):
                return True
            
            # Check for USB devices
            if any('Arduino' in p.description for p in ports):
                return True
            
            return False
        except:
            return False
    
    def check_simulation_api(self):
        """Check if local simulation server running"""
        try:
            import requests
            response = requests.get('http://localhost:5000/health', 
                                   timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def get_sensor_data(self, location):
        """Get data from best available source"""
        
        if self.data_source == "HARDWARE":
            return self.read_hardware_sensors()
        
        elif self.data_source == "SIMULATION_API":
            return self.fetch_simulated_data(location)
        
        else:
            return self.read_csv_data(location)
    
    def read_hardware_sensors(self):
        """Read from actual sensors"""
        # Connect to Arduino/Raspberry Pi
        # Read I2C, serial, GPIO
        pass
    
    def fetch_simulated_data(self, location):
        """Fetch from local API"""
        import requests
        response = requests.get(
            f'http://localhost:5000/sensors/{location}'
        )
        return response.json()
    
    def read_csv_data(self, location):
        """Fallback to CSV"""
        df = pd.read_csv('netra_threat_log.csv')
        latest = df[df['Location'] == location].iloc[-1]
        return latest.to_dict()
```

---

### 🔄 AUTO-REFRESH MECHANISMS

#### Option A: Scheduled Data Generation (Simplest)

```python
# File: auto_refresh.py

import schedule
import time
from generate_enhanced_data import generate_threat_data

def refresh_data():
    """Generate fresh data every hour"""
    print("🔄 Refreshing threat data...")
    generate_threat_data(num_records=100, days=1)
    print("✅ Data refreshed!")

# Run every hour
schedule.every(1).hours.do(refresh_data)

# Or run at specific times
schedule.every().day.at("00:00").do(refresh_data)
schedule.every().day.at("06:00").do(refresh_data)
schedule.every().day.at("12:00").do(refresh_data)
schedule.every().day.at("18:00").do(refresh_data)

while True:
    schedule.run_pending()
    time.sleep(60)
```

**Deploy with**:
- **Local**: Run as background service
- **Linux**: `cron` job
- **Windows**: Task Scheduler
- **Cloud**: GitHub Actions (free!) or AWS Lambda

---

#### Option B: Real-Time Streaming (Advanced)

```python
# File: sensor_stream.py

import asyncio
import websockets

async def sensor_stream():
    """Continuous sensor data streaming"""
    
    connector = NetraDataConnector()
    
    while True:
        # Get fresh readings every 30 seconds
        for location in LOCATIONS:
            data = connector.get_sensor_data(location)
            
            # Save to database (SQLite for local, PostgreSQL for cloud)
            save_to_db(data)
            
            # Broadcast via WebSocket if anyone listening
            await broadcast_to_clients(data)
        
        await asyncio.sleep(30)

# Run continuously
asyncio.run(sensor_stream())
```

---

#### Option C: Hybrid Smart Refresh (Recommended)

```python
# File: smart_refresh.py

class SmartDataRefresh:
    """Intelligent refresh based on context"""
    
    def __init__(self):
        self.connector = NetraDataConnector()
        self.refresh_interval = self.determine_interval()
    
    def determine_interval(self):
        """Adapt refresh rate to data source"""
        
        if self.connector.data_source == "HARDWARE":
            # Real sensors → refresh every 30 seconds
            return 30
        
        elif self.connector.data_source == "SIMULATION_API":
            # Simulation → refresh every 5 minutes
            return 300
        
        else:
            # Static CSV → refresh daily
            return 86400
    
    def start_refresh_loop(self):
        """Run refresh loop"""
        
        while True:
            self.refresh_data()
            time.sleep(self.refresh_interval)
    
    def refresh_data(self):
        """Refresh based on source type"""
        
        if self.connector.data_source == "HARDWARE":
            # Poll hardware sensors
            self.poll_hardware()
        
        elif self.connector.data_source == "SIMULATION_API":
            # Fetch from API
            self.fetch_from_api()
        
        else:
            # Regenerate CSV
            self.regenerate_csv()
```

---

## 📅 IMPLEMENTATION ROADMAP

### ✅ IMMEDIATE (This Week)

**1. Train ML Model (2 hours)**
- [ ] Create `development/train_ml_model.py`
- [ ] Train Random Forest on 1200 records
- [ ] Save to `models/threat_detector.pkl`
- [ ] Test locally

**2. Integrate ML in Streamlit (1 hour)**
- [ ] Add model loading with try-except
- [ ] Replace weighted formula with ML prediction
- [ ] Add "ML Mode" indicator in UI
- [ ] Test on Streamlit Cloud

**3. Add Smart Data Connector (2 hours)**
- [ ] Create `data_connector.py`
- [ ] Implement tier detection
- [ ] Integrate into Streamlit app
- [ ] Test fallback behavior

---

### 🎯 SHORT TERM (Next 2 Weeks)

**4. Improve CV Simulation (1 day)**
- [ ] Add correlated CV outputs
- [ ] Make it more realistic
- [ ] Add confidence intervals

**5. Setup Auto-Refresh (1 day)**
- [ ] Create scheduled data generation
- [ ] Deploy as GitHub Action (free!)
- [ ] Auto-commit to repo → Streamlit auto-deploys

**6. Add Data Source Status Dashboard (0.5 day)**
- [ ] Show which data source is active
- [ ] Display last refresh time
- [ ] Add manual refresh button

---

### 🚀 MEDIUM TERM (Next Month)

**7. Build Simulation API (2-3 days)**
- [ ] Create FastAPI server
- [ ] Endpoints for sensor data
- [ ] Deploy locally (Docker)
- [ ] Connect Streamlit to it

**8. Add Database Layer (2 days)**
- [ ] SQLite for local
- [ ] PostgreSQL for cloud option
- [ ] Store historical data
- [ ] Query optimization

---

### 🔮 LONG TERM (Future)

**9. Real Computer Vision (1-2 weeks)**
- [ ] Train YOLOv8 on IED dataset
- [ ] Add image upload interface
- [ ] Deploy CV API separately
- [ ] Integrate with Streamlit

**10. Hardware Integration (Hardware dependent)**
- [ ] Design sensor interface protocol
- [ ] Create Arduino/RPi driver
- [ ] Test with real sensors
- [ ] Field deployment

---

## 🎬 WHAT TO DO NEXT?

### My Recommendations (In Order)

**1. ✅ START HERE: Train ML Model**
- Easiest upgrade
- Biggest credibility boost
- "AI-powered" becomes real
- **I can create this for you RIGHT NOW**

**2. ✅ ADD: Smart Data Connector**
- Prepares for future hardware
- Makes system production-ready
- **I can create this too**

**3. ⚠️ CONSIDER: Auto-refresh via GitHub Actions**
- Free automation
- Works on Streamlit Cloud
- No server needed

**4. ⏸️ SKIP FOR NOW: Real Computer Vision**
- Needs image dataset
- Needs training time
- Needs GPU
- Do this only when you have cameras

---

## 🤔 QUESTIONS FOR YOU

Before I start creating code, please confirm:

### About ML:
1. **Do you want me to create the ML training script RIGHT NOW?**
   - Uses your 1200 records
   - Creates Random Forest model
   - Replaces weighted formula
   - Takes 30 min for me to write

2. **Model complexity preference?**
   - Option A: Simple (Random Forest, <1MB, fast)
   - Option B: Medium (XGBoost, ~5MB, accurate)
   - Option C: Complex (Neural Network, large, slow)

### About Data Automation:
3. **Where will you deploy?**
   - Option A: Local only (my laptop)
   - Option B: Streamlit Cloud only
   - Option C: Both (with fallback)

4. **Do you plan to connect real hardware sensors?**
   - If YES → When? What sensors?
   - If NO → We focus on simulation quality

5. **Data refresh frequency preference?**
   - Option A: Real-time (30 sec, needs API)
   - Option B: Hourly (good for demo)
   - Option C: Daily (lightweight)

### About Computer Vision:
6. **Do you have camera images/video available?**
   - If YES → I'll add upload feature
   - If NO → Keep simulating for now

7. **Is CV a priority or nice-to-have?**
   - Priority → I'll plan architecture
   - Nice-to-have → We skip for now

---

## 🚀 READY TO START?

**Tell me your priorities**:
1. What's most important to you?
2. What should we build first?
3. Any constraints (time, budget, hardware)?

**I recommend starting with**:
```
Week 1:
✅ Day 1: Train ML model + integrate
✅ Day 2: Add data connector
✅ Day 3: Setup auto-refresh
✅ Day 4: Testing + documentation

Result: Professional ML-powered system with smart data handling
```

**Your thoughts?** 🤔
