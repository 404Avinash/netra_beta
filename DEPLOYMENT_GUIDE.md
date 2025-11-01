# 🚀 N.E.T.R.A. Deployment Guide
## GitHub + Streamlit Cloud Deployment

This guide will walk you through deploying N.E.T.R.A. to GitHub and Streamlit Cloud.

---

## 📋 Pre-Deployment Checklist

✅ **Phase 1-3 Complete**:
- [x] Project cleaned (__pycache__, .ipynb_checkpoints removed)
- [x] Datasets generated (50 locations, 500 analyses, 30 days)
- [x] Data flow tested (Streamlit app runs successfully)

✅ **Phase 4 Complete**:
- [x] README.md created (professional, hackathon-ready)
- [x] .gitignore configured for GitHub
- [x] requirements.txt present
- [x] All CSV datasets ready

---

## 🎯 Phase 5: GitHub Deployment

### Step 1: Configure Git (YOU NEED TO DO THIS)

```bash
# Set your name and email
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Verify configuration
git config --list
```

### Step 2: Initialize Git Repository

```bash
# Navigate to project directory
cd "c:\Users\ajha1\Downloads\netra-system\netra-system"

# Initialize git (if not already done)
git init

# Check status
git status
```

### Step 3: Add Remote Repository

```bash
# Add your GitHub repository as remote
git remote add origin https://github.com/404Avinash/netra_beta.git

# Verify remote
git remote -v
```

### Step 4: Stage All Files

```bash
# Add all files to staging
git add .

# Verify staged files
git status
```

### Step 5: Create Initial Commit

```bash
# Commit with descriptive message
git commit -m "Initial deployment: Complete N.E.T.R.A. system with datasets"

# Verify commit
git log --oneline
```

### Step 6: Push to GitHub

```bash
# Push to main branch (force overwrite if repository exists)
git push -u origin main --force

# If main doesn't exist, try master:
# git branch -M main
# git push -u origin main --force
```

### Step 7: Verify on GitHub

1. Go to: https://github.com/404Avinash/netra_beta
2. Verify all files are present:
   - ✅ README.md
   - ✅ netra_streamlit_app.py
   - ✅ requirements.txt
   - ✅ netra_threat_log.csv (500 records)
   - ✅ locations_northeast_india.csv (50 locations)
   - ✅ sensor_readings_live.csv (100 readings)
   - ✅ DATA_FLOW_COMPLETE_GUIDE.md
   - ✅ DATA_FLOW_VISUAL_DIAGRAMS.txt

---

## ☁️ Phase 6: Streamlit Cloud Deployment

### Step 1: Prepare Streamlit Configuration

Create `.streamlit` directory with configuration:

```bash
# Create directory
mkdir .streamlit

# Create config.toml
# (See config.toml content below)
```

**File: `.streamlit/config.toml`**
```toml
[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#0E1117"
secondaryBackgroundColor = "#262730"
textColor = "#FAFAFA"
font = "sans serif"

[server]
headless = true
port = 8501

[browser]
gatherUsageStats = false
```

### Step 2: Verify Requirements

**File: `requirements.txt`** (should already exist)
```
streamlit==1.51.0
pandas>=1.5.0
numpy>=1.24.0
plotly>=5.14.0
folium>=0.14.0
streamlit-folium>=0.12.0
```

### Step 3: Deploy to Streamlit Cloud

1. **Go to Streamlit Cloud**:
   - Visit: https://share.streamlit.io
   - Click "Sign in" → Use GitHub account

2. **Create New App**:
   - Click "New app"
   - Select repository: `404Avinash/netra_beta`
   - Branch: `main` (or `master`)
   - Main file path: `netra_unified_app.py`
   - Click "Deploy"

3. **Wait for Deployment** (2-3 minutes):
   - Streamlit Cloud will:
     * Clone your repository
     * Install dependencies from requirements.txt
     * Start the app
     * Assign a URL

4. **Access Your App**:
   - URL format: `https://404avinash-netra-beta-netra-streamlit-app-xyz123.streamlit.app`
   - **Bookmark this URL!**

### Step 4: Test Deployed App

1. **Dashboard**: Verify 500 analyses displayed
2. **Live Analysis**: Test sensor controls
3. **Regional Map**: Check 50 locations render
4. **Batch Analysis**: Run all locations test
5. **Historical Reports**: Generate date-range analytics

---

## 🔧 Troubleshooting

### GitHub Push Failed

**Error**: `authentication failed`
```bash
# Solution: Use Personal Access Token (PAT)
# 1. Go to GitHub.com → Settings → Developer settings → Personal access tokens
# 2. Generate new token (classic) with 'repo' scope
# 3. Use token as password when pushing
```

**Error**: `remote origin already exists`
```bash
# Solution: Remove and re-add remote
git remote remove origin
git remote add origin https://github.com/404Avinash/netra_beta.git
```

**Error**: `rejected due to existing commits`
```bash
# Solution: Force push (CAUTION: overwrites remote)
git push -u origin main --force
```

### Streamlit Cloud Issues

**Error**: `ModuleNotFoundError: No module named 'X'`
```
Solution: Add missing module to requirements.txt
```

**Error**: `File not found: netra_threat_log.csv`
```
Solution: Verify CSV files are committed to GitHub
git add *.csv
git commit -m "Add dataset files"
git push
```

**Error**: `App crashes on startup`
```
Solution: Check logs in Streamlit Cloud dashboard
- Look for Python version mismatch
- Verify all imports work
- Check file paths (use relative paths)
```

---

## 📊 Deployment Verification Checklist

### GitHub Repository

- [ ] README.md displays correctly with badges
- [ ] All CSV files present (check file sizes):
  * netra_threat_log.csv (~84 KB)
  * locations_northeast_india.csv (~3.4 KB)
  * sensor_readings_live.csv (~10 KB)
- [ ] Main app file: netra_streamlit_app.py
- [ ] requirements.txt with all dependencies
- [ ] Documentation files present
- [ ] .gitignore excludes unnecessary files
- [ ] LICENSE file present (MIT)

### Streamlit Cloud App

- [ ] App loads without errors
- [ ] Dashboard shows 500 historical analyses
- [ ] Threat distribution chart displays correctly
- [ ] Live Analysis page works (sensor sliders)
- [ ] Regional Map renders 50 locations
- [ ] Batch Analysis processes all locations
- [ ] Historical Reports generate correctly
- [ ] No console errors in browser DevTools
- [ ] App responsive on mobile devices

---

## 🎨 Optional: Custom Domain

Want a professional URL? Use Streamlit Cloud custom domains:

1. **Go to App Settings** (Streamlit Cloud dashboard)
2. **Click "Domains"**
3. **Add custom domain**: `netra.yourdomain.com`
4. **Update DNS** (add CNAME record to your domain registrar)
5. **Wait for SSL** (automatic via Let's Encrypt)

---

## 🔄 Updating Deployment

### Update Code

```bash
# Make changes to code
# ...

# Stage and commit
git add .
git commit -m "Update: description of changes"

# Push to GitHub
git push origin main
```

Streamlit Cloud will **auto-deploy** within ~30 seconds!

### Update Datasets

```bash
# Regenerate datasets
python generate_datasets.py

# Stage and commit new CSVs
git add *.csv
git commit -m "Update datasets: new threat analyses"
git push origin main
```

---

## 📈 Post-Deployment

### Monitor App

- **Streamlit Cloud Dashboard**: https://share.streamlit.io
  * View app logs
  * Check resource usage
  * Monitor uptime

- **GitHub Insights**:
  * Track traffic (if public repository)
  * Monitor stars/forks
  * Check Issues tab for bug reports

### Share with Judges

1. **GitHub Repository URL**:
   ```
   https://github.com/404Avinash/netra_beta
   ```

2. **Live Demo URL**:
   ```
   https://[your-app-name].streamlit.app
   ```

3. **Quick Demo Path**:
   - Dashboard → View 500 analyses
   - Live Analysis → Select Moreh Border, set high threat
   - Regional Map → Explore 50 locations
   - Batch Analysis → Run all locations

---

## 🎯 Success Metrics

Your deployment is successful when:

✅ **GitHub repository is public** (or accessible to judges)  
✅ **Streamlit app loads in < 5 seconds**  
✅ **All 500 historical analyses displayed**  
✅ **Interactive maps render correctly**  
✅ **Batch analysis completes in < 10 seconds**  
✅ **No errors in browser console**  
✅ **Mobile responsive** (test on phone)

---

## 🆘 Need Help?

### Resources

- **Streamlit Docs**: https://docs.streamlit.io/streamlit-community-cloud
- **GitHub Docs**: https://docs.github.com/en/get-started
- **Streamlit Forum**: https://discuss.streamlit.io

### Common Commands Reference

```bash
# Git basics
git status              # Check current state
git add .               # Stage all files
git commit -m "msg"     # Commit with message
git push origin main    # Push to GitHub
git pull origin main    # Pull latest changes

# View history
git log --oneline       # Commit history
git diff                # View changes

# Undo changes
git restore <file>      # Discard local changes
git reset HEAD~1        # Undo last commit (keep changes)
```

---

## 🎉 Congratulations!

Once deployed successfully, you'll have:

✅ **Professional GitHub repository** with full documentation  
✅ **Live Streamlit Cloud app** accessible worldwide  
✅ **500 realistic datasets** for demonstration  
✅ **Production-ready system** for hackathon judges  

**Your N.E.T.R.A. system is now live and ready to impress! 🛡️**

---

<div align="center">

**Questions? Check [README.md](README.md) for more details**

</div>
