# N.E.T.R.A. Development Tools

This folder contains LOCAL development tools for data generation and deployment. **These files are NOT pushed to GitHub** to keep sensitive explosive data and development workflows private.

## 📁 Files Overview

### Data Generation
- **`generate_enhanced_data.py`** - Generate 1000+ threat analyses with 47 explosive types
- **`integrate_explosives.py`** - Parse Excel file and create explosive_database.csv
- **`DOC-20251102-WA0083.xlsx`** - Source data (47 explosive types) [NOT IN GIT]

### Quality Assurance
- **`validate_data.py`** - Validate CSV data quality before deployment

### Deployment
- **`update_and_deploy.ps1`** - One-click script to generate, validate, and deploy

## 🚀 Quick Start

### Generate New Data (1000+ records)

```powershell
cd development
python generate_enhanced_data.py
```

This creates updated `netra_threat_log.csv` in the root directory with:
- 1000 threat analyses
- 60-day date range
- 47 explosive types
- Realistic sensor correlations
- Proper threat level distribution

### Integrate Explosive Database

```powershell
python integrate_explosives.py
```

**Requirements:**
- Place `DOC-20251102-WA0083.xlsx` in this folder
- Creates `explosive_database.csv` in root directory

### Validate Data Quality

```powershell
python validate_data.py
```

Checks:
- Required columns present
- No duplicates
- Sensor readings in valid range (0-100)
- Proper date ranges
- Threat level distribution
- Null value detection

### One-Click Update & Deploy

```powershell
.\update_and_deploy.ps1
```

**What it does:**
1. ✅ Generates enhanced data (1000+ records)
2. ✅ Integrates explosive database (if Excel present)
3. ✅ Validates data quality
4. ✅ Commits CSV files to Git
5. ✅ Pushes to GitHub
6. ✅ Triggers Streamlit Cloud auto-deploy

**Result:** Your app updates in 2-3 minutes at https://netra-unified-bet-001.streamlit.app

## 📊 Data Specifications

### Current Production Data
- **Threat Log**: 500 analyses, 30 days
- **Locations**: 50 strategic locations, 7 NE states
- **Sensor Readings**: 100 live readings

### Enhanced Data (Generated)
- **Threat Log**: 1000+ analyses, 60 days
- **Explosive Types**: 47 types from Excel
- **Fume Signatures**: Realistic colors (Black, Orange/Brown, White, etc.)
- **Threat Distribution**: CRITICAL 21%, HIGH 26%, MODERATE 32%, LOW 20%

## 🔒 Security Notes

### Files NOT in Git
- `DOC-20251102-WA0083.xlsx` (sensitive explosive data)
- `generate_enhanced_data.py` (development tool)
- `integrate_explosives.py` (development tool)
- `validate_data.py` (development tool)
- `update_and_deploy.ps1` (deployment script)

### Files Pushed to Git
- `netra_threat_log.csv` (threat analyses - safe for public)
- `locations_northeast_india.csv` (locations - public info)
- `sensor_readings_live.csv` (sensor data - safe)
- `explosive_database.csv` (processed data without sensitive notes)

## 🛠️ Customization

### Generate Custom Dataset

```python
# In generate_enhanced_data.py
df = generate_enhanced_threats(
    num_records=1500,  # Change record count
    days_back=90       # Change date range
)
```

### Add New Explosive Types

1. Edit `DOC-20251102-WA0083.xlsx`
2. Add new rows with: Name, Composition, Fume Color, etc.
3. Run `python integrate_explosives.py`

## 📝 Workflow Example

```powershell
# 1. Generate new data
cd development
python generate_enhanced_data.py

# 2. Check quality
python validate_data.py

# 3. If validation passes, deploy
.\update_and_deploy.ps1

# 4. Wait 2-3 minutes
# 5. Check https://netra-unified-bet-001.streamlit.app
```

## 🐛 Troubleshooting

### "Excel file not found"
- Place `DOC-20251102-WA0083.xlsx` in `development/` folder
- Or skip explosive integration (data will still generate)

### "Validation failed"
- Check the validation output for specific errors
- Common issues: sensor readings out of range, missing columns
- Fix data generation parameters and retry

### "Git push failed"
- Check your Git credentials
- Ensure you have push access to the repository
- Try manual push: `git push origin main`

### "No changes detected"
- CSV files are already up to date
- Generate new data with different parameters
- No deployment needed

## 📚 Additional Resources

- **Main App**: https://netra-unified-bet-001.streamlit.app
- **GitHub**: https://github.com/404Avinash/netra_beta
- **Auto-Deploy**: Happens automatically on Git push (2-3 min)

## 🎯 Best Practices

1. **Always validate** before deployment
2. **Keep Excel file LOCAL** (never push to Git)
3. **Test locally** before pushing to production
4. **Use one-click script** for consistent deployments
5. **Check app** 2-3 minutes after deployment

---

**Note:** This development folder is for LOCAL use only. Keep sensitive explosive data private and never commit it to GitHub.
