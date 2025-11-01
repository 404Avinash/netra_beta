# 🚀 Quick Start Guide for Judges

## Prerequisites
- Python 3.8 or higher installed
- Git installed (optional, for cloning)

---

## Step 1: Get the Code

### Option A: Download ZIP
1. Click "Code" → "Download ZIP" on GitHub
2. Extract to your desired location
3. Open terminal/PowerShell in the extracted folder

### Option B: Git Clone
```bash
git clone https://github.com/404Avinash/netra_beta.git
cd netra_beta
```

---

## Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

**Wait 1-2 minutes for installation to complete.**

---

## Step 3: Explore the Notebook (Optional - 5 minutes)

**See the algorithm development:**

```bash
# Open in Jupyter
jupyter notebook NETRA_BETA_v2.ipynb

# OR open in VS Code
code NETRA_BETA_v2.ipynb
```

This notebook shows:
- ✅ Complete Bayesian fusion algorithm
- ✅ Multi-sensor data processing
- ✅ Threat classification logic
- ✅ All visualizations and analysis

---

## Step 4: Launch the Dashboard

```bash
streamlit run netra_unified_app.py
```

**The app will automatically open in your browser at:** http://localhost:8501

---

## 📊 What to Explore in the Dashboard

### 1. **Dashboard** (Main Overview)
   - View 500 historical threat analyses
   - See 30-day trend charts
   - Check threat distribution statistics

### 2. **Live Analysis** (Interactive Demo)
   - Adjust 7 sensor sliders
   - Watch real-time threat calculation
   - See confidence scores change
   - View action recommendations

### 3. **Historical Data** (Filter & Analyze)
   - Filter by date, location, threat level
   - See detailed analysis records
   - Understand threat patterns

### 4. **Regional Map** (Geographic View)
   - Interactive map with 50 locations
   - Color-coded threat markers
   - Click markers for details
   - Zoom in/out for better view

### 5. **Batch Analysis** (Multi-Location)
   - Analyze all 50 locations simultaneously
   - See progress bar
   - View aggregate statistics

### 6. **Reports** (Export Data)
   - Download CSV reports
   - Filter by date range
   - Export for further analysis

### 7. **Settings** (Configuration)
   - Adjust AI thresholds
   - Modify sensor weights
   - Customize display

---

## 🎯 Recommended Demo Flow (20 minutes)

### **Part 1: Notebook Overview** (5 min)
1. Open `NETRA_BETA_v2.ipynb`
2. Show the algorithm section
3. Explain Bayesian fusion
4. Highlight data processing

### **Part 2: Live Dashboard** (10 min)
1. Launch Streamlit app
2. Start with Dashboard overview
3. Go to Live Analysis - adjust sliders
4. Show Regional Map - 50 locations
5. Demonstrate Batch Analysis

### **Part 3: Data & Insights** (5 min)
1. Show Historical Data filtering
2. Explain threat classification
3. Display Reports & Export
4. Answer questions

---

## 🔧 Troubleshooting

### Port Already in Use
```bash
streamlit run netra_unified_app.py --server.port 8502
```

### Missing Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Permission Errors (Windows)
Run PowerShell as Administrator:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📦 What's Included

```
✅ NETRA_BETA_v2.ipynb - Complete algorithm development
✅ netra_unified_app.py - Interactive web dashboard
✅ netra_core.py - AI engine with Bayesian fusion
✅ 500 historical threat analyses (CSV)
✅ 50 strategic locations across NE India (CSV)
✅ 100 recent sensor readings (CSV)
✅ Complete documentation
```

---

## 🎓 Key Highlights to Mention

1. **Multi-Sensor Fusion**: 7 different sensors working together
2. **Bayesian AI**: Sophisticated probability-based threat assessment
3. **Real-Time Processing**: Sub-second analysis
4. **Regional Focus**: Designed for NE India terrain
5. **Scalable**: Can handle 50+ locations simultaneously
6. **Interactive**: Live sensor controls and instant feedback
7. **Data-Driven**: 30 days of historical analysis (500 records)

---

## 📞 Support

- **GitHub Issues**: [Report bugs](https://github.com/404Avinash/netra_beta/issues)
- **Documentation**: See `DATA_FLOW_COMPLETE_GUIDE.md`
- **Deployment**: See `DEPLOYMENT_GUIDE.md`

---

<div align="center">

**🛡️ N.E.T.R.A. System**  
*Next-Gen Eye for Threat Recognition and Analysis*

Developed by **Avinash Jha**

</div>
