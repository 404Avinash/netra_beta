# 🚀 N.E.T.R.A. FastAPI Deployment Guide

## Free Deployment Options (No Credit Card Required!)

---

## Option 1: Railway.app ⭐ RECOMMENDED

**Why:** Easiest, automatic HTTPS, good free tier

### Steps:

1. **Sign up at [railway.app](https://railway.app)** with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `netra_beta` repository

3. **Configure Service**
   - Root Directory: `/api`
   - Start Command: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
   - Build Command: `pip install -r requirements.txt`

4. **Environment Variables** (Optional)
   ```
   PYTHON_VERSION=3.11
   ```

5. **Deploy!**
   - Railway auto-deploys on every push to `develop` branch
   - Get your URL: `https://netra-api-production.up.railway.app`

6. **Update Streamlit**
   - Add API URL to Streamlit secrets:
   ```toml
   # .streamlit/secrets.toml
   API_BASE_URL = "https://netra-api-production.up.railway.app"
   ```

**Free Tier:**
- 500 hours/month
- 1GB RAM
- Auto-sleep after inactivity
- $5 free credits/month

---

## Option 2: Render.com 🎨

**Why:** Good for APIs, automatic deployments

### Steps:

1. **Sign up at [render.com](https://render.com)**

2. **Create Web Service**
   - "New" → "Web Service"
   - Connect GitHub repo
   - Select `netra_beta`

3. **Configure**
   ```
   Name: netra-api
   Region: Oregon (US West)
   Branch: develop
   Root Directory: api
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

4. **Create Service** (takes ~5 minutes)

5. **Get URL**: `https://netra-api.onrender.com`

**Free Tier:**
- 750 hours/month
- Sleeps after 15min inactivity
- 512MB RAM
- Auto-deploy on push

**⚠️ Note:** First request after sleep takes ~30s to wake up

---

## Option 3: Fly.io 🪰

**Why:** Edge deployment, WebSocket support, better performance

### Steps:

1. **Install Fly CLI**
   ```powershell
   irm https://fly.io/install.ps1 | iex
   ```

2. **Login**
   ```powershell
   fly auth login
   ```

3. **Launch App**
   ```powershell
   cd c:\Users\ajha1\Downloads\netra-system\netra-system
   fly launch
   ```
   
   Answer prompts:
   - Name: `netra-api`
   - Region: Choose closest to you
   - Database: No
   - Deploy: Yes

4. **Configure** (auto-created `fly.toml`):
   ```toml
   app = "netra-api"
   primary_region = "ord"

   [build]
     dockerfile = "Dockerfile"

   [http_service]
     internal_port = 8000
     force_https = true
     auto_stop_machines = true
     auto_start_machines = true

   [[vm]]
     cpu_kind = "shared"
     cpus = 1
     memory_mb = 256
   ```

5. **Deploy**
   ```powershell
   fly deploy
   ```

6. **Get URL**: `https://netra-api.fly.dev`

**Free Tier:**
- 3 shared VMs (256MB each)
- 160GB bandwidth/month
- Auto-scale to zero when idle

---

## Option 4: Deta Space 🌌 SIMPLEST

**Why:** Zero config, instant deploy, unlimited free tier!

### Steps:

1. **Install Deta CLI**
   ```powershell
   iwr https://get.deta.dev/cli.ps1 -useb | iex
   ```

2. **Login**
   ```powershell
   deta login
   ```

3. **Create Space**
   ```powershell
   cd api
   deta new --python
   ```

4. **Deploy**
   ```powershell
   deta deploy
   ```

5. **Get URL**: Auto-generated (e.g., `https://abc123.deta.dev`)

**Free Tier:**
- **UNLIMITED** (yes, really!)
- No credit card required
- Auto-sleep, instant wake
- WebSocket support

---

## Option 5: Vercel (API Routes) 🔺

**Why:** Same platform as Streamlit alternatives, global CDN

### Steps:

1. **Install Vercel CLI**
   ```powershell
   npm install -g vercel
   ```

2. **Create `vercel.json`**
   ```json
   {
     "builds": [
       {
         "src": "api/main.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "api/main.py"
       }
     ]
   }
   ```

3. **Deploy**
   ```powershell
   vercel --prod
   ```

**Free Tier:**
- Unlimited deployments
- 100GB bandwidth/month
- Global CDN

**⚠️ Limitation:** Serverless functions have 10s timeout

---

## 🏆 Comparison Table

| Platform | Free Tier | Best For | Limitations | Setup Difficulty |
|----------|-----------|----------|-------------|------------------|
| **Railway** | 500h/month, $5 credits | Full apps | Sleeps after idle | ⭐ Easy |
| **Render** | 750h/month | APIs | 15min sleep | ⭐ Easy |
| **Fly.io** | 3 VMs, 160GB | Performance | Requires CLI | ⭐⭐ Medium |
| **Deta** | **Unlimited** | Quick tests | Beta platform | ⭐ Easiest |
| **Vercel** | 100GB/month | Static + API | 10s timeout | ⭐⭐ Medium |

---

## 🔗 Connect to Streamlit Cloud

After deploying API, update your Streamlit app:

### 1. **Create `.streamlit/secrets.toml`** (local only)
```toml
API_BASE_URL = "https://your-api-url.railway.app"
API_ENABLED = true
```

### 2. **Add to Streamlit Cloud Secrets**
- Go to Streamlit Cloud dashboard
- Select your app
- Settings → Secrets
- Add:
  ```toml
  API_BASE_URL = "https://your-api-url.railway.app"
  API_ENABLED = true
  ```

### 3. **Update `netra_unified_app.py`**

Add at the top:
```python
import requests
import streamlit as st

# Try to get API URL from secrets
try:
    API_BASE_URL = st.secrets.get("API_BASE_URL", None)
    API_ENABLED = st.secrets.get("API_ENABLED", False)
except:
    API_BASE_URL = None
    API_ENABLED = False

def analyze_threat_via_api(sensors, location):
    """Use FastAPI for analysis"""
    if not API_ENABLED or not API_BASE_URL:
        return None
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/analyze",
            json={
                "sensors": sensors,
                "location": location
            },
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
    except:
        pass
    
    return None

# In analyze_threat() function:
def analyze_threat(sensors, location):
    # Priority 1: Try FastAPI (if available)
    if API_ENABLED:
        api_result = analyze_threat_via_api(sensors, location)
        if api_result:
            return api_result
    
    # Priority 2: Try local ML model
    if ML_MODE:
        return ml_analysis(sensors, location)
    
    # Priority 3: Fallback to rule-based
    return fallback_rule_based_analysis(sensors, location)
```

---

## 🧪 Test Your Deployment

### 1. **Health Check**
```powershell
curl https://your-api-url.railway.app/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2025-11-02T14:30:52.123456",
  "model_loaded": true,
  "uptime_seconds": 12345.67
}
```

### 2. **Test Analysis**
```powershell
curl -X POST https://your-api-url.railway.app/api/analyze `
  -H "Content-Type: application/json" `
  -d '{
    "sensors": {
      "fume": 75,
      "metal": 80,
      "gpr": 65,
      "ground_cv": 70,
      "drone_cv": 68,
      "disturbance": 55,
      "thermal": 45
    },
    "location": "Test Location"
  }'
```

### 3. **Check API Docs**
Visit: `https://your-api-url.railway.app/docs`

---

## 📊 Monitor Your Deployment

### Railway.app
- Dashboard: https://railway.app/dashboard
- View logs in real-time
- See metrics (CPU, RAM, requests)

### Render.com
- Dashboard: https://dashboard.render.com
- Logs tab shows all output
- Metrics tab for performance

### Fly.io
```powershell
fly logs          # View logs
fly status        # Check status
fly scale count 1 # Scale instances
```

---

## 🐛 Troubleshooting

### Model not loading
- Check model files are in `models/` directory
- Verify file sizes (should be ~2.37 MB)
- Check logs for "ML Model loaded successfully"

### API timeout
- Increase timeout in Streamlit: `timeout=30`
- Check if API is sleeping (free tiers)
- Use Railway/Fly.io for better performance

### CORS errors
- Add your Streamlit URL to allowed origins in `api/main.py`:
  ```python
  allow_origins=[
      "https://netra-unified-bet-001.streamlit.app",
      "https://your-streamlit-url.streamlit.app"
  ]
  ```

### Out of memory
- ML model needs ~512MB RAM minimum
- Use Railway (1GB) or Fly.io
- Optimize model (reduce n_estimators if needed)

---

## 🎯 Recommended Setup for Hackathon

**Best combo for FREE:**

1. **FastAPI Backend:** Railway.app (500h free)
2. **Streamlit Frontend:** Streamlit Cloud (already deployed)
3. **Fallback:** Keep local ML in Streamlit (works without API)

**Architecture:**
```
User → Streamlit Cloud → Railway FastAPI → XGBoost Model
          ↓ (if API fails)
       Local ML Model
```

This gives you:
- ✅ Scalable backend (Railway)
- ✅ Free hosting (both platforms)
- ✅ Redundancy (local ML fallback)
- ✅ Fast response times
- ✅ WebSocket support for streaming

---

## 📝 Next Steps

1. **Deploy FastAPI to Railway** (5 minutes)
2. **Test API endpoints** (2 minutes)
3. **Update Streamlit secrets** (3 minutes)
4. **Test end-to-end** (5 minutes)
5. **Push to develop branch** ✅

**Total time:** ~15 minutes for full deployment!

---

**Questions?** Check API docs at `/docs` or GitHub issues!
