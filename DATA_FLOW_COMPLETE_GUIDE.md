# 🔄 N.E.T.R.A. SYSTEM - COMPLETE DATA FLOW DOCUMENTATION
## Understanding Data Journey: From Raw Sensors to Beautiful Dashboards

---

## 📋 TABLE OF CONTENTS

1. [Data Flow Overview](#overview)
2. [Stage 1: Raw Sensor Data](#stage1)
3. [Stage 2: Data Collection & Validation](#stage2)
4. [Stage 3: AI Processing & Analysis](#stage3)
5. [Stage 4: Data Storage & Export](#stage4)
6. [Stage 5: Data Bridge (Jupyter ↔ Streamlit)](#stage5)
7. [Stage 6: Streamlit Consumption](#stage6)
8. [Stage 7: User Presentation](#stage7)
9. [Data Formats & Schemas](#formats)
10. [Alternative Data Paths](#alternatives)
11. [Troubleshooting Data Flow](#troubleshooting)

---

<a name="overview"></a>
## 🌊 DATA FLOW OVERVIEW

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        N.E.T.R.A. DATA PIPELINE                              │
└─────────────────────────────────────────────────────────────────────────────┘

STAGE 1: RAW SENSOR DATA
    │
    ├─► Fume Detector          → Chemical signature (0-100%)
    ├─► Metal Detector         → Metallic objects (0-100%)
    ├─► GPR (Ground Radar)     → Subsurface anomalies (0-100%)
    ├─► Ground Computer Vision → Visual patterns (0-100%)
    ├─► Drone Computer Vision  → Aerial view (0-100%)
    ├─► Disturbance Sensor     → Soil changes (0-100%)
    └─► Thermal Camera         → Heat signatures (0-100%)
    │
    ▼
STAGE 2: DATA COLLECTION & VALIDATION
    │
    ├─► netra_data_connector.py  → Multi-source ingestion
    │   ├── CSV Files (File system)
    │   ├── REST APIs (HTTP)
    │   ├── MQTT Streams (IoT)
    │   ├── Database (SQL)
    │   └── Local Network (Sensors)
    │
    ▼
STAGE 3: AI PROCESSING
    │
    ├─► netra_core.py (NetraAI class)
    │   ├── validate_sensors()     → Check data quality
    │   ├── calculate_threat_probability() → Bayesian fusion
    │   │   ├── Weighted scoring (sensor weights)
    │   │   └── Correlation analysis (5 rules)
    │   ├── get_threat_level()     → Classification
    │   └── get_recommendations()  → Action items
    │
    ▼
STAGE 4: DATA STORAGE
    │
    ├─► CSV Export (netra_threat_log.csv)
    │   ├── Single analysis results
    │   └── Batch analysis results
    │
    ├─► Memory (threat_history[])
    │   └── Runtime cache
    │
    └─► Export Files (timestamped)
        └── netra_batch_analysis_YYYYMMDD_HHMMSS.csv
    │
    ▼
STAGE 5: DATA BRIDGE
    │
    ├─► netra_data_bridge.py
    │   ├── Monitors: netra_threat_log.csv
    │   ├── Auto-detects: File modifications
    │   └── Provides: Read interface for Streamlit
    │
    ▼
STAGE 6: STREAMLIT CONSUMPTION
    │
    ├─► netra_app.py
    │   ├── Loads data via NetraAI or DataBridge
    │   ├── Caches in st.session_state
    │   └── Processes for visualization
    │
    ▼
STAGE 7: USER PRESENTATION
    │
    └─► Interactive Dashboard
        ├── Real-time Metrics (st.metric)
        ├── Interactive Maps (Folium)
        ├── Charts (Plotly)
        └── Data Tables (st.dataframe)
```

---

<a name="stage1"></a>
## 🎯 STAGE 1: RAW SENSOR DATA

### Data Sources (7 Sensors)

**1. ROVER PLATFORM (Ground-based)**
```python
Fume Sensor:
  • Type: Chemical vapor detector
  • Output: 0-100% (concentration)
  • Location: On rover chassis
  • Update: Every 1 second
  • Weight in AI: 0.20 (highest)

Metal Detector:
  • Type: Electromagnetic sensor
  • Output: 0-100% (signal strength)
  • Location: Rover front
  • Update: Every 0.5 seconds
  • Weight in AI: 0.18

GPR (Ground Penetrating Radar):
  • Type: Radio wave subsurface imaging
  • Output: 0-100% (anomaly confidence)
  • Location: Rover bottom
  • Update: Every 2 seconds
  • Weight in AI: 0.15

Ground Computer Vision:
  • Type: Camera + AI object detection
  • Output: 0-100% (detection confidence)
  • Location: Rover camera
  • Update: Every 1 second
  • Weight in AI: 0.12
```

**2. DRONE PLATFORM (Aerial)**
```python
Drone Computer Vision:
  • Type: Aerial camera + AI
  • Output: 0-100% (detection confidence)
  • Location: Drone mounted camera
  • Update: Every 1 second
  • Weight in AI: 0.15

Disturbance Sensor:
  • Type: Soil pattern analysis (visual + IR)
  • Output: 0-100% (disturbance level)
  • Location: Drone sensors
  • Update: Every 2 seconds
  • Weight in AI: 0.10

Thermal Camera:
  • Type: Infrared imaging
  • Output: 0-100% (heat signature)
  • Location: Drone mounted
  • Update: Every 1 second
  • Weight in AI: 0.10
```

### Raw Data Format (Before Processing)

**Example: Live Sensor Reading (JSON)**
```json
{
  "timestamp": "2025-11-02T02:15:30Z",
  "location": {
    "name": "Imphal Checkpost",
    "latitude": 24.8170,
    "longitude": 93.9368,
    "state": "Manipur"
  },
  "sensors": {
    "fume": 78.5,
    "metal": 85.2,
    "gpr": 72.0,
    "ground_cv": 68.3,
    "drone_cv": 71.8,
    "disturbance": 65.9,
    "thermal": 58.4
  },
  "metadata": {
    "rover_id": "ROVER_001",
    "drone_id": "DRONE_003",
    "operator": "Field_Team_Alpha"
  }
}
```

**Alternative: CSV Stream**
```csv
timestamp,location,lat,lon,fume,metal,gpr,ground_cv,drone_cv,disturbance,thermal
2025-11-02T02:15:30Z,Imphal Checkpost,24.817,93.937,78.5,85.2,72.0,68.3,71.8,65.9,58.4
2025-11-02T02:15:31Z,Imphal Checkpost,24.817,93.937,79.1,84.8,71.5,67.9,72.1,66.2,58.1
```

---

<a name="stage2"></a>
## 📥 STAGE 2: DATA COLLECTION & VALIDATION

### Module: `netra_data_connector.py`

**Purpose**: Ingest data from ANY source and standardize format

### Data Collection Methods

**METHOD 1: CSV File Monitoring**
```python
# Location: netra_data_connector.py
# Usage: Read from local/network file

connector = SensorDataConnector(source_type="csv", config={
    "file_path": "./sensor_data.csv",
    "refresh_interval": 5  # Re-read every 5 seconds
})

# What happens:
1. Opens sensor_data.csv
2. Reads latest row
3. Validates all 7 sensor values (0-100 range)
4. Returns standardized dict
5. Auto-refreshes every 5 seconds
```

**File Format Expected**:
```csv
timestamp,location,fume,metal,gpr,ground_cv,drone_cv,disturbance,thermal
2025-11-02T02:15:30Z,Imphal,78.5,85.2,72.0,68.3,71.8,65.9,58.4
```

**METHOD 2: REST API Polling**
```python
connector = SensorDataConnector(source_type="api", config={
    "endpoint": "http://192.168.1.100:8000/sensors",
    "refresh_interval": 2
})

# What happens:
1. HTTP GET to http://192.168.1.100:8000/sensors
2. Expects JSON response with sensor data
3. Parses and validates
4. Returns standardized format
5. Polls every 2 seconds
```

**METHOD 3: MQTT Stream (IoT)**
```python
connector = SensorDataConnector(source_type="mqtt", config={
    "broker": "mqtt.netra.local",
    "topics": ["netra/sensors/rover", "netra/sensors/drone"]
})

# What happens:
1. Connects to MQTT broker
2. Subscribes to sensor topics
3. Real-time message reception
4. Validates incoming data
5. Updates latest_data on every message
```

**METHOD 4: Database Query**
```python
connector = SensorDataConnector(source_type="database", config={
    "type": "mysql",
    "host": "192.168.1.50",
    "database": "netra_sensors",
    "table": "sensor_readings"
})

# What happens:
1. Connects to MySQL database
2. Queries: SELECT * FROM sensor_readings ORDER BY timestamp DESC LIMIT 1
3. Converts to dict
4. Validates and standardizes
5. Refreshes every 3 seconds (configurable)
```

**METHOD 5: Simulated Data (Demo Mode)**
```python
connector = SensorDataConnector(source_type="simulated")

# What happens:
1. Generates realistic fake data
2. Random values with patterns (spikes for threats)
3. Used for demos when no real sensors available
4. Updates every 1 second
```

### Data Validation

**Validation Rules** (Applied to ALL sources):
```python
# File: netra_core.py → validate_sensors()

CHECKS:
1. All 7 sensors present?
   ✓ fume, metal, gpr, ground_cv, drone_cv, disturbance, thermal

2. Data types correct?
   ✓ All values must be numbers (int or float)

3. Range validation?
   ✓ Each value: 0 ≤ value ≤ 100

4. Missing data handling?
   ✓ Reject if any sensor missing
   ✓ Log error with details

5. Timestamp valid?
   ✓ Check format: ISO 8601
   ✓ Not too old (< 5 minutes)
```

**Example Validation Code**:
```python
def validate_sensors(sensors: Dict[str, float]) -> bool:
    required_sensors = {'fume', 'metal', 'gpr', 'ground_cv', 
                       'drone_cv', 'disturbance', 'thermal'}
    
    # Check all present
    if set(sensors.keys()) != required_sensors:
        raise ValueError(f"Missing sensors: {required_sensors - set(sensors.keys())}")
    
    # Check ranges
    for sensor, value in sensors.items():
        if not isinstance(value, (int, float)):
            raise TypeError(f"Sensor {sensor} must be numeric")
        if not 0 <= value <= 100:
            raise ValueError(f"Sensor {sensor} out of range: {value}")
    
    return True
```

### Standardized Output Format

**After validation, ALL sources produce**:
```python
{
    'location': 'Imphal Checkpost',
    'timestamp': '2025-11-02T02:15:30Z',
    'sensors': {
        'fume': 78.5,
        'metal': 85.2,
        'gpr': 72.0,
        'ground_cv': 68.3,
        'drone_cv': 71.8,
        'disturbance': 65.9,
        'thermal': 58.4
    },
    'metadata': {
        'source': 'csv',  # or 'api', 'mqtt', etc.
        'validated': True
    }
}
```

---

<a name="stage3"></a>
## 🧠 STAGE 3: AI PROCESSING & ANALYSIS

### Module: `netra_core.py` (NetraAI class)

**Purpose**: Transform validated sensor data into threat assessment

### Processing Pipeline

**STEP 3.1: Weighted Scoring**
```python
# File: netra_core.py → calculate_threat_probability()

# Apply sensor weights
weighted_score = (
    sensors['fume']        * 0.20 +  # Highest weight
    sensors['metal']       * 0.18 +
    sensors['gpr']         * 0.15 +
    sensors['drone_cv']    * 0.15 +
    sensors['ground_cv']   * 0.12 +
    sensors['disturbance'] * 0.10 +
    sensors['thermal']     * 0.10
)

# Example calculation:
# Input: {fume: 80, metal: 75, gpr: 70, ground_cv: 65, 
#         drone_cv: 68, disturbance: 60, thermal: 55}
# 
# Calculation:
# = 80*0.20 + 75*0.18 + 70*0.15 + 68*0.15 + 65*0.12 + 60*0.10 + 55*0.10
# = 16.0 + 13.5 + 10.5 + 10.2 + 7.8 + 6.0 + 5.5
# = 69.5%
```

**STEP 3.2: Correlation Analysis (Bayesian Boost)**
```python
# Detects patterns that indicate higher threat

correlation_boost = 0

# Rule 1: Chemical + Metal (IED signature)
if sensors['fume'] > 70 AND sensors['metal'] > 70:
    correlation_boost += 12
    # Reasoning: Explosives + detonator often found together

# Rule 2: Visual agreement (Ground + Drone see same thing)
if abs(sensors['drone_cv'] - sensors['ground_cv']) < 15:
    correlation_boost += 8
    # Reasoning: Multiple angles confirm detection

# Rule 3: Thermal + Chemical (Explosive heat signature)
if sensors['thermal'] > 60 AND sensors['fume'] > 60:
    correlation_boost += 7
    # Reasoning: Some explosives emit heat + chemicals

# Rule 4: Ground disturbance + GPR (Buried device)
if sensors['disturbance'] > 65 AND sensors['gpr'] > 65:
    correlation_boost += 6
    # Reasoning: Fresh digging + subsurface object

# Rule 5: Multi-sensor high alert
high_sensors = count(sensors where value > 75)
if high_sensors >= 4:
    correlation_boost += 5
    # Reasoning: Multiple independent detections = high confidence

# Example:
# If fume=80, metal=78 → Rule 1 adds +12%
# If thermal=62, fume=80 → Rule 3 adds +7%
# Total boost: +19%
```

**STEP 3.3: Final Probability**
```python
final_probability = min(100, weighted_score + correlation_boost)

# Example:
# weighted_score = 69.5%
# correlation_boost = 19%
# final_probability = 69.5 + 19 = 88.5%
```

**STEP 3.4: Threat Classification**
```python
# File: netra_core.py → get_threat_level()

if probability >= 75:
    level = "🔴 CRITICAL"
    color = "#dc2626"
    description = "Immediate Action Required"
    
elif probability >= 50:
    level = "🟡 HIGH"
    color = "#f59e0b"
    description = "Enhanced Monitoring"
    
elif probability >= 25:
    level = "🟢 MODERATE"
    color = "#10b981"
    description = "Routine Monitoring"
    
else:
    level = "⚪ LOW"
    color = "#3b82f6"
    description = "Area Cleared"

# Example: 88.5% → 🔴 CRITICAL
```

**STEP 3.5: Recommendations**
```python
# File: netra_core.py → get_recommendations()

if probability >= 75:
    recommendations = [
        "⚠️ EVACUATE 200m radius IMMEDIATELY",
        "🚫 BLOCK all vehicle and pedestrian traffic",
        "⚡ DEPLOY bomb disposal unit",
        "📡 ALERT military and civilian authorities",
        "🚁 MAINTAIN continuous aerial surveillance",
        "📸 CAPTURE high-resolution evidence",
        "🔒 SECURE perimeter with armed forces"
    ]
```

### Processed Data Output

**After AI processing**:
```python
{
    'Scan_ID': 'SCAN_20251102_021530_001',
    'Timestamp': '2025-11-02T02:15:30Z',
    'Location': 'Imphal Checkpost',
    'State': 'Manipur',
    'Type': 'Checkpoint Scan',
    'Latitude': 24.8170,
    'Longitude': 93.9368,
    
    # AI Results
    'Threat_Probability': 88.5,
    'Threat_Level': '🔴 CRITICAL',
    'Classification': 'Immediate Action Required',
    'Confidence': 95.2,
    
    # Original Sensor Data (preserved)
    'fume': 80.0,
    'metal': 78.0,
    'gpr': 70.0,
    'ground_cv': 65.0,
    'drone_cv': 68.0,
    'disturbance': 60.0,
    'thermal': 62.0,
    
    # Recommendations
    'recommendations': [
        "⚠️ EVACUATE 200m radius IMMEDIATELY",
        "🚫 BLOCK all vehicle and pedestrian traffic",
        # ... more actions
    ]
}
```

---

<a name="stage4"></a>
## 💾 STAGE 4: DATA STORAGE & EXPORT

### Storage Mechanisms

**STORAGE 1: CSV File Export**

**File: `netra_threat_log.csv`** (Main log file)
```python
# Created by: Both Jupyter notebook AND Streamlit app
# Location: Project root directory
# Format: CSV with headers

# File structure:
Scan_ID,Timestamp,Location,State,Type,Latitude,Longitude,Threat_Probability,Threat_Level,Classification,fume,metal,gpr,ground_cv,drone_cv,disturbance,thermal
SCAN_20251102_021530_001,2025-11-02T02:15:30Z,Imphal Checkpost,Manipur,Checkpoint,24.817,93.937,88.5,CRITICAL,Immediate Action Required,80.0,78.0,70.0,65.0,68.0,60.0,62.0
SCAN_20251102_021545_002,2025-11-02T02:15:45Z,Dimapur Border,Nagaland,Border,25.917,93.733,45.2,MODERATE,Routine Monitoring,35.0,40.0,38.0,42.0,41.0,30.0,28.0

# Writing code (in netra_core.py):
def export_history_to_csv(self, filename='netra_threat_log.csv'):
    df = pd.DataFrame(self.threat_history)
    df.to_csv(filename, index=False)
    return filename
```

**STORAGE 2: In-Memory Cache**
```python
# Location: netra_core.py → NetraAI class

class NetraAI:
    def __init__(self):
        self.threat_history = []  # List of all analyzed threats
        
    def log_threat(self, location, probability, sensors):
        self.threat_history.append({
            'timestamp': datetime.now(),
            'location': location,
            'probability': probability,
            'sensors': sensors
        })
        
# Used for:
# - Quick access during session
# - Bulk export at end
# - Cleared when app restarts
```

**STORAGE 3: Batch Analysis Files**
```python
# Created by: Batch analysis function
# Naming: netra_batch_analysis_YYYYMMDD_HHMMSS.csv
# Example: netra_batch_analysis_20251102_021530.csv

# When created:
# - User clicks "RUN BATCH ANALYSIS" button
# - System analyzes 10 locations
# - Results saved to timestamped file
# - File kept for historical records

# Export code (in netra_app.py):
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
filename = f'netra_batch_analysis_{timestamp}.csv'
results_df.to_csv(filename, index=False)
```

### Export Formats

**FORMAT 1: Standard CSV (Most Common)**
```csv
Scan_ID,Timestamp,Location,Threat_Probability,Threat_Level
SCAN_001,2025-11-02T02:15:30Z,Imphal,88.5,CRITICAL
SCAN_002,2025-11-02T02:15:45Z,Dimapur,45.2,MODERATE
```

**FORMAT 2: Detailed CSV (With All Sensors)**
```csv
Scan_ID,Timestamp,Location,State,Latitude,Longitude,Threat_Probability,Threat_Level,fume,metal,gpr,ground_cv,drone_cv,disturbance,thermal
SCAN_001,2025-11-02T02:15:30Z,Imphal,Manipur,24.817,93.937,88.5,CRITICAL,80,78,70,65,68,60,62
```

**FORMAT 3: JSON (For API Integration)**
```json
{
  "scan_id": "SCAN_001",
  "timestamp": "2025-11-02T02:15:30Z",
  "location": "Imphal Checkpost",
  "threat": {
    "probability": 88.5,
    "level": "CRITICAL",
    "classification": "Immediate Action Required"
  },
  "sensors": {
    "fume": 80.0,
    "metal": 78.0,
    "gpr": 70.0,
    "ground_cv": 65.0,
    "drone_cv": 68.0,
    "disturbance": 60.0,
    "thermal": 62.0
  }
}
```

---

<a name="stage5"></a>
## 🌉 STAGE 5: DATA BRIDGE (Jupyter ↔ Streamlit)

### Module: `netra_data_bridge.py`

**Purpose**: Connect Jupyter notebook output to Streamlit dashboard

### The Bridge Concept

```
┌─────────────────────────────────────────────────────────────┐
│  JUPYTER NOTEBOOK (Research/Analysis)                       │
│  ┌────────────────────────────────────────────────────┐     │
│  │ 1. Run threat analysis                             │     │
│  │ 2. Calculate probabilities                         │     │
│  │ 3. Save to: netra_threat_log.csv                   │     │
│  └────────────────────┬───────────────────────────────┘     │
└────────────────────────┼─────────────────────────────────────┘
                         │
                         │ SHARED FILE
                         │ netra_threat_log.csv
                         │
┌────────────────────────▼─────────────────────────────────────┐
│  STREAMLIT APP (Production/Demo)                            │
│  ┌────────────────────────────────────────────────────┐     │
│  │ 1. Monitor: netra_threat_log.csv                   │     │
│  │ 2. Auto-detect changes                             │     │
│  │ 3. Load latest data                                │     │
│  │ 4. Display in dashboard                            │     │
│  └────────────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────────┘
```

### Bridge Implementation

**Jupyter Notebook Side** (Data Producer):
```python
# File: NETRA_BETA_v2.ipynb

# After analysis, save to CSV
netra_ai = NetraAI()
probability = netra_ai.calculate_threat_probability(sensors)

# Create result dataframe
result_df = pd.DataFrame([{
    'Scan_ID': scan_id,
    'Timestamp': datetime.now(),
    'Location': location,
    'Threat_Probability': probability,
    # ... other fields
}])

# CRITICAL: Save to shared file
csv_filename = 'netra_threat_log.csv'

# Append if file exists, create if not
if os.path.exists(csv_filename):
    result_df.to_csv(csv_filename, mode='a', header=False, index=False)
else:
    result_df.to_csv(csv_filename, mode='w', header=True, index=False)

print(f"✅ Saved to {csv_filename}")
```

**Streamlit Side** (Data Consumer):
```python
# File: netra_app.py (using netra_data_bridge.py)

from netra_data_bridge import NetraDataBridge

# Initialize bridge
bridge = NetraDataBridge(log_file='netra_threat_log.csv')

# Get all threats
all_threats = bridge.get_all_threats()

# Get latest threat
latest = bridge.get_latest_threat()

# Get by location
imphal_threats = bridge.get_threats_by_location('Imphal')

# Get by level
critical_threats = bridge.get_threats_by_level('CRITICAL')
```

### Auto-Refresh Mechanism

**How Streamlit detects new data**:
```python
# File: netra_data_bridge.py

class NetraDataBridge:
    def __init__(self):
        self.last_modified = 0  # Track file modification time
        
    def get_all_threats(self):
        # Check if file was modified
        current_modified = os.path.getmtime(self.log_file)
        
        if current_modified > self.last_modified:
            # File updated! Reload data
            self.last_modified = current_modified
            print(f"🔄 New data detected: {datetime.now()}")
            df = pd.read_csv(self.log_file)
            return df
        else:
            # No changes, use cached data
            return cached_df
```

### Data Synchronization

**Real-time updates**:
```python
# Scenario 1: Single analysis
# ---------------------------
# Time 0:00 - Jupyter analyzes Location A → Saves to CSV
# Time 0:02 - Streamlit auto-refreshes → Shows Location A
# Result: 2-second delay

# Scenario 2: Batch analysis  
# ---------------------------
# Time 0:00 - Jupyter starts batch (10 locations)
# Time 0:30 - Batch complete → Saves all to CSV
# Time 0:32 - Streamlit refreshes → Shows all 10
# Result: ~2-second delay after batch completion

# Scenario 3: Manual export
# ---------------------------
# Time 0:00 - User exports in Streamlit
# Time 0:01 - netra_app.py saves to CSV
# Time 0:03 - Jupyter can read the file
# Result: Bidirectional data flow!
```

---

<a name="stage6"></a>
## 📊 STAGE 6: STREAMLIT DATA CONSUMPTION

### Module: `netra_app.py`

**Purpose**: Load, process, and prepare data for visualization

### Data Loading Strategies

**STRATEGY 1: Direct AI Engine Use**
```python
# File: netra_app.py → show_single_analysis()

# Initialize AI engine
if 'netra_ai' not in st.session_state:
    st.session_state.netra_ai = NetraAI()

# Get user input (sensor values from sliders)
sensors = {
    'fume': st.slider("💨 Fume Sensor", 0, 100, 50),
    'metal': st.slider("🔩 Metal Detector", 0, 100, 50),
    # ... other sensors
}

# Real-time analysis (happens immediately)
probability = st.session_state.netra_ai.calculate_threat_probability(sensors)
level, color, desc = st.session_state.netra_ai.get_threat_level(probability)

# Display result immediately (no file I/O)
st.metric("Threat Probability", f"{probability}%")
```

**STRATEGY 2: Load from CSV (Historical Data)**
```python
# File: netra_app.py → show_dashboard()

from netra_data_bridge import NetraDataBridge

# Load historical analysis
bridge = NetraDataBridge()
all_threats = bridge.get_all_threats()

# Calculate statistics
total_scans = len(all_threats)
critical_threats = len(all_threats[all_threats['Threat_Level'] == 'CRITICAL'])
avg_probability = all_threats['Threat_Probability'].mean()

# Display metrics
st.metric("Total Scans", total_scans)
st.metric("Critical Threats", critical_threats)
st.metric("Avg Threat Level", f"{avg_probability:.1f}%")
```

**STRATEGY 3: Session State Caching**
```python
# File: netra_app.py

# Initialize session state
if 'batch_results' not in st.session_state:
    st.session_state.batch_results = None

if st.button("RUN BATCH ANALYSIS"):
    # Run analysis
    results_df = run_batch_analysis(locations)
    
    # CRITICAL: Save to session state
    st.session_state.batch_results = results_df
    
    # Also save to CSV for persistence
    results_df.to_csv('netra_batch_analysis.csv', index=False)
    
    st.rerun()  # Reload page to display results

# Display results (persists across reruns)
if st.session_state.batch_results is not None:
    st.dataframe(st.session_state.batch_results)
```

### Data Processing for Visualization

**PROCESSING 1: Map Data Preparation**
```python
# File: netra_app.py → show_regional_map()

# Load location data
locations = NE_LOCATIONS  # Predefined dict of locations

# Generate/load threat data
if 'map_threats' not in st.session_state:
    # First load: generate random threats for demo
    st.session_state.map_threats = {
        key: np.random.randint(20, 80) for key in locations
    }

# Create map markers
for key, info in locations.items():
    threat = st.session_state.map_threats[key]
    
    # Determine color based on threat
    color = 'red' if threat >= 75 else 'orange' if threat >= 50 else 'green'
    
    # Add to map
    folium.CircleMarker(
        location=[info['lat'], info['lon']],
        radius=threat/5,
        popup=f"{info['name']}<br>Threat: {threat}%",
        color=color
    ).add_to(map)
```

**PROCESSING 2: Chart Data Transformation**
```python
# File: netra_app.py → show_batch_analysis()

# Raw data from CSV
results_df = pd.read_csv('netra_batch_analysis.csv')

# Transform for bar chart
top5 = results_df.nlargest(5, 'Threat_Probability')

# Create Plotly figure
fig = px.bar(
    top5,
    x='Location',
    y='Threat_Probability',
    color='Threat_Probability',
    color_continuous_scale='Reds',
    title="Top 5 High-Risk Locations"
)

# Display
st.plotly_chart(fig)
```

**PROCESSING 3: Table Formatting**
```python
# Raw data has many columns
raw_df = pd.read_csv('netra_threat_log.csv')

# Select and rename for display
display_df = raw_df[[
    'Location', 'State', 'Threat_Probability', 'Threat_Level', 'Confidence'
]]

# Format probability column
display_df['Threat_Probability'] = display_df['Threat_Probability'].apply(
    lambda x: f"{x:.1f}%"
)

# Display with custom styling
st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)
```

---

<a name="stage7"></a>
## 🎨 STAGE 7: USER PRESENTATION

### Visual Components

**COMPONENT 1: Metrics (st.metric)**
```python
# Data source: Calculated statistics or CSV aggregation
# Display: Colored metric cards with delta

total_scans = 125
critical = 8
delta_critical = +2  # Change from last hour

st.metric(
    label="Critical Threats",
    value=critical,
    delta=f"+{delta_critical} from last hour",
    delta_color="inverse"  # Red for increase
)
```

**COMPONENT 2: Interactive Maps (Folium)**
```python
# Data source: Location coordinates + threat levels
# Display: Zoomable map with markers

map = folium.Map(location=[26.0, 92.5], zoom_start=6)

for location, data in threat_data.items():
    folium.CircleMarker(
        location=[data['lat'], data['lon']],
        radius=data['threat']/5,
        popup=f"{location}<br>{data['threat']}%",
        color='red' if data['threat'] >= 75 else 'orange'
    ).add_to(map)

st_folium(map, width=1400, height=600)
```

**COMPONENT 3: Charts (Plotly)**
```python
# Data source: DataFrame from analysis
# Display: Interactive bar/pie/line charts

# Bar chart
fig = px.bar(df, x='Location', y='Threat_Probability')
st.plotly_chart(fig)

# Pie chart
fig = px.pie(df, values='Threat_Probability', names='State')
st.plotly_chart(fig)
```

**COMPONENT 4: Data Tables (st.dataframe)**
```python
# Data source: CSV or DataFrame
# Display: Sortable, filterable table

st.dataframe(
    results_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Threat_Probability": st.column_config.ProgressColumn(
            "Threat %",
            format="%d%%",
            min_value=0,
            max_value=100
        )
    }
)
```

### User Interaction Flow

```
USER OPENS APP (http://localhost:8501)
    │
    ├─► DASHBOARD PAGE (Default)
    │   ├── Load: netra_threat_log.csv
    │   ├── Calculate: Statistics (total, average, etc.)
    │   ├── Display: 6 metric cards
    │   └── Update: Every auto-refresh (Streamlit native)
    │
    ├─► SINGLE ANALYSIS PAGE
    │   ├── User: Adjusts 7 sensor sliders
    │   ├── Process: Real-time calculation (netra_core.py)
    │   ├── Display: Threat probability, level, gauge
    │   └── Export: Option to save to CSV
    │
    ├─► REGIONAL MAP PAGE
    │   ├── Load: Session state (map_threats)
    │   ├── Generate: Folium map with markers
    │   ├── Display: Interactive map
    │   └── Interaction: Click markers for details
    │
    ├─► BATCH ANALYSIS PAGE
    │   ├── User: Clicks "RUN BATCH ANALYSIS"
    │   ├── Process: Analyze 10 locations (netra_core.py)
    │   ├── Save: results_df → session_state + CSV
    │   ├── Display: Table, charts, heatmap
    │   └── Export: Download CSV button
    │
    ├─► SENSOR CONFIG PAGE
    │   ├── Display: Current sensor weights
    │   ├── User: Adjust weight sliders
    │   ├── Validate: Sum = 1.0
    │   └── Update: AI engine weights
    │
    └─► ABOUT PAGE
        └── Display: System info (static content)
```

---

<a name="formats"></a>
## 📁 DATA FORMATS & SCHEMAS

### Schema 1: Raw Sensor Data
```python
{
    'timestamp': str,        # ISO 8601 format
    'location': str,         # Human-readable name
    'latitude': float,       # GPS coordinate
    'longitude': float,      # GPS coordinate
    'sensors': {
        'fume': float,       # 0-100
        'metal': float,      # 0-100
        'gpr': float,        # 0-100
        'ground_cv': float,  # 0-100
        'drone_cv': float,   # 0-100
        'disturbance': float,# 0-100
        'thermal': float     # 0-100
    }
}
```

### Schema 2: Processed Threat Data
```python
{
    'Scan_ID': str,                    # Unique identifier
    'Timestamp': datetime,             # When analyzed
    'Location': str,                   # Place name
    'State': str,                      # State/region
    'Type': str,                       # 'Checkpoint', 'Border', etc.
    'Latitude': float,                 # GPS
    'Longitude': float,                # GPS
    'Threat_Probability': float,       # 0-100 (AI output)
    'Threat_Level': str,               # CRITICAL/HIGH/MODERATE/LOW
    'Classification': str,             # Description
    'Confidence': float,               # 0-100 (algorithm confidence)
    'fume': float,                     # Original sensor values
    'metal': float,                    # (preserved for audit)
    'gpr': float,
    'ground_cv': float,
    'drone_cv': float,
    'disturbance': float,
    'thermal': float,
    'recommendations': List[str]       # Action items
}
```

### CSV File Schemas

**netra_threat_log.csv** (Main Log):
```csv
Scan_ID,Timestamp,Location,State,Type,Latitude,Longitude,Threat_Probability,Threat_Level,Classification,fume,metal,gpr,ground_cv,drone_cv,disturbance,thermal,Confidence
```

**netra_batch_analysis_TIMESTAMP.csv** (Batch Results):
```csv
Location,State,Latitude,Longitude,Threat_Probability,Threat_Level,Classification,fume,metal,gpr,ground_cv,drone_cv,disturbance,thermal
```

---

<a name="alternatives"></a>
## 🔀 ALTERNATIVE DATA PATHS

### Path 1: Direct Sensor → Streamlit (No Jupyter)
```
Sensors → netra_data_connector.py → netra_core.py → netra_app.py → Display
                                                           ↓
                                                          CSV (optional export)
```

### Path 2: Simulated Data (Demo Mode)
```
netra_app.py → Generate random sensors → netra_core.py → Display
(No external data source needed)
```

### Path 3: API Integration
```
External System API → netra_data_connector.py → netra_core.py → netra_app.py
                                                       ↓
                                                    Database
                                                       ↓
                                            External Dashboard
```

### Path 4: Database-First Architecture
```
Sensors → Database (INSERT) → netra_data_connector.py (SELECT) → Processing → Display
                    ↑
              (All apps query same DB)
```

---

<a name="troubleshooting"></a>
## 🔧 TROUBLESHOOTING DATA FLOW

### Issue 1: Streamlit Not Showing Jupyter Data

**Problem**: Ran analysis in Jupyter, but Streamlit shows nothing

**Diagnosis**:
```bash
# Check if CSV was created
ls -la netra_threat_log.csv

# Check file contents
cat netra_threat_log.csv

# Check file permissions
ls -l netra_threat_log.csv
```

**Solutions**:
1. Verify Jupyter actually saved the file
2. Check both apps use SAME filename
3. Check file path (relative vs absolute)
4. Restart Streamlit to clear cache

---

### Issue 2: Data Not Updating in Real-Time

**Problem**: New Jupyter analysis doesn't show in Streamlit

**Diagnosis**:
```python
# In netra_data_bridge.py, add debug:
def get_all_threats(self):
    print(f"Last modified: {self.last_modified}")
    current = os.path.getmtime(self.log_file)
    print(f"Current modified: {current}")
    print(f"File changed: {current > self.last_modified}")
```

**Solutions**:
1. Check file modification time updates
2. Force Streamlit refresh (press R in browser)
3. Verify auto_refresh=True in bridge
4. Clear browser cache

---

### Issue 3: Session State Data Lost

**Problem**: Batch analysis results disappear on page reload

**Diagnosis**:
```python
# Check session state
print(st.session_state.keys())
print(st.session_state.batch_results)
```

**Solutions**:
1. Ensure data saved to st.session_state
2. Call st.rerun() after saving
3. Also save to CSV for persistence
4. Check for typos in session_state keys

---

## 📊 DATA FLOW SUMMARY TABLE

| Stage | Input | Processing | Output | Storage | Access |
|-------|-------|------------|--------|---------|--------|
| 1. Raw Sensors | Physical sensors | Analog → Digital | 0-100% values | Sensor memory | Data connector |
| 2. Collection | Sensor outputs | Validate, standardize | Sensor dict | Connector cache | AI engine |
| 3. AI Processing | Sensor dict | Bayesian fusion | Threat probability | threat_history[] | Export function |
| 4. Storage | Threat analysis | Format, write | CSV files | File system | Data bridge |
| 5. Bridge | CSV files | Monitor, read | DataFrames | Bridge cache | Streamlit |
| 6. Consumption | DataFrames | Transform, prepare | Display data | Session state | UI components |
| 7. Presentation | Display data | Render | Visual UI | Browser | User |

---

## 🎯 KEY TAKEAWAYS

1. **Data flows in ONE direction**: Sensors → Processing → Storage → Display
2. **Shared files enable integration**: Jupyter and Streamlit share CSV files
3. **Caching improves performance**: Session state and file modification tracking
4. **Validation happens early**: Sensor data validated before AI processing
5. **Multiple storage layers**: Memory (fast) + CSV (persistent) + Session (UI)
6. **Real-time updates via file monitoring**: Bridge detects new data automatically
7. **Export options at every stage**: Can save data at any point in pipeline

---

**Generated**: November 2, 2025  
**N.E.T.R.A. System** - Complete Data Flow Documentation  
**Version**: 1.0 - Production Ready

---
