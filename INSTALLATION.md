# 🚀 N.E.T.R.A. Installation & Testing Guide

## Quick Installation (30 seconds)

```powershell
# Install all dependencies
pip install -r requirements_streamlit.txt
```

Wait for installation to complete, then:

```powershell
# Test the core engine
python netra_core.py

# If successful, launch the app
streamlit run netra_app.py
```

---

## Step-by-Step Installation

### Step 1: Check Python Version
```powershell
python --version
```
**Required:** Python 3.8 or higher

If you don't have Python, download from: https://www.python.org/downloads/

---

### Step 2: Install Dependencies
```powershell
pip install -r requirements_streamlit.txt
```

This will install:
- streamlit (web framework)
- pandas (data processing)
- numpy (numerical computing)
- plotly (visualizations)
- folium (maps)
- streamlit-folium (map integration)
- And more...

**Expected time:** 2-5 minutes depending on internet speed

---

### Step 3: Verify Installation
```powershell
# Test core engine
python netra_core.py
```

**Expected output:**
```
================================================================================
🛡️ N.E.T.R.A. Core Engine Test
================================================================================

📍 Location: Guwahati Airport Road, Assam
🎯 Threat Probability: XX.X%
⚠️ Threat Level: 🔴 CRITICAL (or other level)
💯 Confidence: XX.X%

📋 Recommendations:
  1. ⚠️ EVACUATE 200m radius IMMEDIATELY
  2. 🚫 BLOCK all vehicle and pedestrian traffic
  ... (more recommendations)

✅ Core engine test completed successfully!
```

---

### Step 4: Launch Web Application
```powershell
streamlit run netra_app.py
```

**Expected output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.X.X:8501
```

The app will automatically open in your browser!

---

## Alternative: Use Quick Start Script

### Windows PowerShell
```powershell
.\start_netra.ps1
```

This script will:
1. ✅ Check Python installation
2. ✅ Check dependencies
3. ✅ Install missing packages
4. ✅ Verify core files
5. ✅ Launch the application

---

## Testing Checklist

### ✅ Core Engine Test
```powershell
python netra_core.py
```
**Success indicators:**
- No import errors
- Threat analysis completes
- Probability calculated
- Recommendations generated

### ✅ Web App Test
```powershell
streamlit run netra_app.py
```
**Success indicators:**
- Server starts on port 8501
- Browser opens automatically
- Dashboard loads with header
- No error messages in terminal

### ✅ Interactive Test
In the web app:
1. Go to "🔍 Threat Analysis"
2. Select any location
3. Adjust sliders
4. Click "ANALYZE THREAT NOW"
5. Verify results appear

**Success indicators:**
- Alert box displays
- Charts render
- Map loads
- Recommendations show

### ✅ Batch Analysis Test
1. Go to "📊 Batch Analysis"
2. Click "RUN BATCH ANALYSIS"
3. Wait for progress bar

**Success indicators:**
- Progress bar completes
- Table displays results
- Charts generate
- Map shows markers

---

## Troubleshooting

### Problem: Python not found
**Solution:**
1. Download Python from https://www.python.org
2. During installation, check "Add Python to PATH"
3. Restart PowerShell

### Problem: pip not found
**Solution:**
```powershell
python -m ensurepip --upgrade
```

### Problem: Permission denied
**Solution:**
Run PowerShell as Administrator or use:
```powershell
pip install --user -r requirements_streamlit.txt
```

### Problem: Module not found after installation
**Solution:**
```powershell
pip install --upgrade -r requirements_streamlit.txt
```

### Problem: Streamlit won't start
**Solution:**
```powershell
# Try running with Python module syntax
python -m streamlit run netra_app.py
```

### Problem: Port 8501 already in use
**Solution:**
```powershell
# Use a different port
streamlit run netra_app.py --server.port 8502
```

### Problem: Map tiles don't load
**Issue:** No internet connection or firewall blocking
**Solution:**
- Check internet connection
- Try switching to different map tile (in Settings)
- Maps are optional; other features still work

---

## Verification Commands

### Check all imports
```powershell
python -c "import streamlit, pandas, numpy, plotly, folium; print('✅ All imports successful!')"
```

### Check Streamlit version
```powershell
streamlit --version
```
**Required:** 1.28.0 or higher

### Check package versions
```powershell
pip list | Select-String "streamlit|pandas|numpy|plotly|folium"
```

---

## Expected Package Versions

```
streamlit      >= 1.28.0
pandas         >= 2.0.0
numpy          >= 1.24.0
plotly         >= 5.17.0
folium         >= 0.14.0
streamlit-folium >= 0.15.0
matplotlib     >= 3.7.0
seaborn        >= 0.12.0
Pillow         >= 10.0.0
```

---

## First-Time Setup (Complete Flow)

```powershell
# 1. Navigate to project directory
cd c:\Users\ajha1\Downloads\netra-system\netra-system

# 2. Install dependencies
pip install -r requirements_streamlit.txt

# 3. Test core engine (optional)
python netra_core.py

# 4. Launch web app
streamlit run netra_app.py

# 5. Open browser to http://localhost:8501

# 6. Test the application
# - Try Threat Analysis page
# - Run a threat analysis
# - Check Regional Map
# - Run Batch Analysis
```

---

## Performance Optimization

### For Faster Loading
```powershell
# Install with pre-built binaries
pip install -r requirements_streamlit.txt --prefer-binary
```

### For Offline Demo
If you need to demo without internet:
1. All features work except map tiles
2. Consider using local tile server
3. Or explain architecture with diagrams

---

## Docker Alternative (Advanced)

If you prefer Docker:
```powershell
# Build image
docker build -t netra-system .

# Run container
docker run -p 8501:8501 netra-system
```

*Note: Dockerfile not included yet, but can be created if needed*

---

## Virtual Environment Setup (Recommended)

### Create Virtual Environment
```powershell
# Create venv
python -m venv venv

# Activate (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements_streamlit.txt

# Run application
streamlit run netra_app.py

# Deactivate when done
deactivate
```

### Benefits
- ✅ Isolated dependencies
- ✅ No conflicts with other projects
- ✅ Easy to clean up
- ✅ Reproducible environment

---

## Jupyter Notebook Setup (Alternative)

If you want to run the notebook instead:

```powershell
# Install Jupyter
pip install jupyter ipywidgets

# Enable widgets
jupyter nbextension enable --py widgetsnbextension

# Launch notebook
jupyter notebook NETRA_BETA_v2.ipynb
```

Then:
1. Run all cells sequentially
2. Use interactive widgets for demo
3. Show visualizations

---

## System Requirements

### Minimum
- **OS:** Windows 10, macOS 10.14+, Linux
- **Python:** 3.8+
- **RAM:** 4GB
- **Storage:** 500MB
- **Internet:** Required for map tiles

### Recommended
- **OS:** Windows 11, macOS 12+, Ubuntu 20.04+
- **Python:** 3.10+
- **RAM:** 8GB+
- **Storage:** 1GB
- **Internet:** Stable broadband

---

## Demo Preparation Checklist

### 1 Day Before
- [ ] Install all dependencies
- [ ] Test core engine
- [ ] Test web app
- [ ] Run through all pages
- [ ] Test 2-3 demo scenarios
- [ ] Check internet connection

### 1 Hour Before
- [ ] Restart computer (fresh start)
- [ ] Close unnecessary applications
- [ ] Disable notifications
- [ ] Test app one more time
- [ ] Have backup notebook ready
- [ ] Charge laptop

### 5 Minutes Before
- [ ] Start the app
- [ ] Navigate to Dashboard
- [ ] Verify everything loads
- [ ] Keep terminal window visible (shows activity)
- [ ] Have SETUP_SUMMARY.md open for reference

---

## Success Metrics

After installation, you should be able to:

✅ Import netra_core without errors  
✅ Run threat analysis programmatically  
✅ Launch Streamlit app  
✅ Navigate all 6 pages  
✅ Analyze threats with interactive sliders  
✅ View interactive maps  
✅ Run batch analysis  
✅ Export data to CSV  
✅ View analytics and charts  

---

## Getting Help

### During Installation
1. Read error messages carefully
2. Try troubleshooting steps above
3. Google specific error messages
4. Check Streamlit documentation

### During Hackathon
1. Stay calm
2. Use backup notebook if needed
3. Explain architecture if demo fails
4. Judges value problem-solving

---

## Quick Reference

### Essential Commands
```powershell
# Install
pip install -r requirements_streamlit.txt

# Test
python netra_core.py

# Run
streamlit run netra_app.py

# Stop
Ctrl + C
```

### Essential URLs
- **App:** http://localhost:8501
- **Terminal:** Shows live activity
- **Browser:** Auto-opens or paste URL

### Essential Files
- **netra_core.py** - Engine
- **netra_app.py** - Web app
- **NETRA_BETA_v2.ipynb** - Notebook backup
- **requirements_streamlit.txt** - Dependencies

---

## Post-Installation

Once everything works:

1. ✅ Practice your demo 2-3 times
2. ✅ Time your presentation (aim for 10-12 minutes)
3. ✅ Prepare for Q&A (see HACKATHON_GUIDE.md)
4. ✅ Take screenshots as backup
5. ✅ Record a demo video (optional but useful)

---

## You're Ready! 🚀

If you've completed all steps above, your system is **hackathon ready**!

**Next steps:**
1. Read HACKATHON_GUIDE.md for presentation strategy
2. Read SETUP_SUMMARY.md for complete overview
3. Practice your demo
4. Win the hackathon! 🏆

---

**Good luck!** 🛡️

*N.E.T.R.A. - Building Safer Communities Through Technology*
