# GitHub Deployment Script
# Run this to deploy N.E.T.R.A. to GitHub

Write-Host "🛡️ N.E.T.R.A. GitHub Deployment" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Check if git is configured
$gitUser = git config --global user.name
$gitEmail = git config --global user.email

if (-not $gitUser -or -not $gitEmail) {
    Write-Host "⚠️  Git not configured. Please configure first:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  git config --global user.name 'Your Name'" -ForegroundColor White
    Write-Host "  git config --global user.email 'your.email@example.com'" -ForegroundColor White
    Write-Host ""
    exit 1
}

Write-Host "✅ Git configured as: $gitUser <$gitEmail>" -ForegroundColor Green
Write-Host ""

# Initialize git if needed
if (-not (Test-Path ".git")) {
    Write-Host "📦 Initializing Git repository..." -ForegroundColor Yellow
    git init
    Write-Host "✅ Repository initialized" -ForegroundColor Green
} else {
    Write-Host "✅ Git repository already exists" -ForegroundColor Green
}

# Add remote if not exists
$remoteUrl = "https://github.com/404Avinash/netra_beta.git"
$existingRemote = git remote get-url origin 2>$null

if (-not $existingRemote) {
    Write-Host "🔗 Adding remote repository..." -ForegroundColor Yellow
    git remote add origin $remoteUrl
    Write-Host "✅ Remote added: $remoteUrl" -ForegroundColor Green
} elseif ($existingRemote -ne $remoteUrl) {
    Write-Host "🔄 Updating remote URL..." -ForegroundColor Yellow
    git remote set-url origin $remoteUrl
    Write-Host "✅ Remote updated: $remoteUrl" -ForegroundColor Green
} else {
    Write-Host "✅ Remote already configured correctly" -ForegroundColor Green
}

Write-Host ""
Write-Host "📝 Staging files..." -ForegroundColor Yellow

# Add all files
git add .

Write-Host "✅ Files staged" -ForegroundColor Green
Write-Host ""

# Show what will be committed
Write-Host "📋 Files to be deployed:" -ForegroundColor Cyan
git status --short

Write-Host ""
Write-Host "💾 Creating commit..." -ForegroundColor Yellow

# Commit
git commit -m "🛡️ Complete N.E.T.R.A. System - Production Ready

- ✅ NETRA_BETA_v2.ipynb: Complete algorithm development
- ✅ netra_unified_app.py: Interactive web dashboard (7 pages)
- ✅ netra_core.py: Bayesian AI engine
- ✅ 500 historical threat analyses (30 days)
- ✅ 50 strategic locations across NE India
- ✅ 100 sensor readings dataset
- ✅ Complete documentation (README, guides)
- ✅ Streamlit Cloud deployment ready

Author: Avinash Jha
Version: 2.0 (Production)
Status: ✅ Hackathon Ready"

Write-Host "✅ Commit created" -ForegroundColor Green
Write-Host ""

# Push to GitHub
Write-Host "🚀 Pushing to GitHub..." -ForegroundColor Yellow
Write-Host "   Repository: $remoteUrl" -ForegroundColor Cyan
Write-Host ""

# Push with force to ensure clean deployment
git push -u origin main --force

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Green
    Write-Host "✅ DEPLOYMENT SUCCESSFUL!" -ForegroundColor Green
    Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Green
    Write-Host ""
    Write-Host "🌐 Your repository is live at:" -ForegroundColor Cyan
    Write-Host "   https://github.com/404Avinash/netra_beta" -ForegroundColor White
    Write-Host ""
    Write-Host "📋 Next Steps:" -ForegroundColor Yellow
    Write-Host "   1. Visit the repository URL above" -ForegroundColor White
    Write-Host "   2. Verify all files are present" -ForegroundColor White
    Write-Host "   3. Check README displays correctly" -ForegroundColor White
    Write-Host "   4. Deploy to Streamlit Cloud:" -ForegroundColor White
    Write-Host "      → https://share.streamlit.io" -ForegroundColor Cyan
    Write-Host "      → Main file: netra_unified_app.py" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "🎉 Ready to share with judges!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "❌ DEPLOYMENT FAILED" -ForegroundColor Red
    Write-Host ""
    Write-Host "Common issues:" -ForegroundColor Yellow
    Write-Host "  1. Authentication required - you may need to enter GitHub credentials" -ForegroundColor White
    Write-Host "  2. Repository doesn't exist - create it on GitHub first" -ForegroundColor White
    Write-Host "  3. Network issues - check your internet connection" -ForegroundColor White
    Write-Host ""
}
