# N.E.T.R.A. One-Click Update and Deploy Script
# Generates data, validates, and auto-deploys to GitHub/Streamlit Cloud

Write-Host "🚀 N.E.T.R.A. One-Click Update and Deploy" -ForegroundColor Cyan
Write-Host ("=" * 60) -ForegroundColor Cyan

# Change to development directory
Set-Location -Path $PSScriptRoot

# Step 1: Generate enhanced data
Write-Host "`n📊 Step 1: Generating enhanced threat data..." -ForegroundColor Yellow
python generate_enhanced_data.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Data generation failed!" -ForegroundColor Red
    exit 1
}

# Step 2: Integrate explosive database (if Excel file exists)
if (Test-Path "DOC-20251102-WA0083.xlsx") {
    Write-Host "`n💣 Step 2: Integrating explosive database..." -ForegroundColor Yellow
    python integrate_explosives.py
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "⚠️ Warning: Explosive integration failed (continuing anyway)" -ForegroundColor Yellow
    }
} else {
    Write-Host "`n⚠️ Step 2: Skipping explosive integration (Excel file not found)" -ForegroundColor Yellow
}

# Step 3: Validate data
Write-Host "`n🔍 Step 3: Validating data quality..." -ForegroundColor Yellow
python validate_data.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "`n❌ Validation failed! Please fix errors before deployment." -ForegroundColor Red
    Write-Host "   Check the validation output above for details." -ForegroundColor Red
    exit 1
}

# Step 4: Git operations
Write-Host "`n📦 Step 4: Preparing Git commit..." -ForegroundColor Yellow

# Change to root directory
Set-Location ..

# Check git status
Write-Host "   Checking for changes..." -ForegroundColor Gray
$gitStatus = git status --porcelain

if (-not $gitStatus) {
    Write-Host "   ℹ️ No changes detected. Nothing to deploy." -ForegroundColor Cyan
    exit 0
}

# Show what will be committed
Write-Host "`n   Files to be committed:" -ForegroundColor Gray
git status --short

# Ask for confirmation
Write-Host "`n⚠️ Ready to deploy to GitHub?" -ForegroundColor Yellow
Write-Host "   This will:" -ForegroundColor Gray
Write-Host "   1. Commit all CSV changes" -ForegroundColor Gray
Write-Host "   2. Push to GitHub" -ForegroundColor Gray
Write-Host "   3. Trigger Streamlit Cloud auto-deploy (2-3 min)" -ForegroundColor Gray
Write-Host ""

$confirmation = Read-Host "Continue? (y/n)"

if ($confirmation -ne 'y') {
    Write-Host "`n❌ Deployment cancelled by user." -ForegroundColor Red
    exit 1
}

# Step 5: Add CSV files only
Write-Host "`n📤 Step 5: Committing and pushing to GitHub..." -ForegroundColor Yellow

git add *.csv

# Create commit message with timestamp
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$commitMessage = "Data update: Enhanced dataset - $timestamp"

git commit -m $commitMessage

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Git commit failed!" -ForegroundColor Red
    exit 1
}

# Push to GitHub
git push origin main

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Git push failed!" -ForegroundColor Red
    exit 1
}

# Step 6: Success message
Write-Host "`n✅ Deployment successful!" -ForegroundColor Green
Write-Host ("=" * 60) -ForegroundColor Green
Write-Host ""
Write-Host "📈 What happens next:" -ForegroundColor Cyan
Write-Host "   1. GitHub updated with new data ✅" -ForegroundColor Gray
Write-Host "   2. Streamlit Cloud detected changes 🔄" -ForegroundColor Gray
Write-Host "   3. Auto-deployment in progress (~2-3 minutes) ⏳" -ForegroundColor Gray
Write-Host ""
Write-Host "🌐 Your app: https://netra-unified-bet-001.streamlit.app" -ForegroundColor Cyan
Write-Host "📦 GitHub: https://github.com/404Avinash/netra_beta" -ForegroundColor Cyan
Write-Host ""
Write-Host "⏰ Check your app in 2-3 minutes to see the updated data!" -ForegroundColor Yellow
Write-Host ""

exit 0
