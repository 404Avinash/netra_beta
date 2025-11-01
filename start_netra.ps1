# N.E.T.R.A. System Quick Start Script
# This script will set up and launch the Streamlit application

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   N.E.T.R.A. System Quick Start" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "[1/5] Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found! Please install Python 3.8 or higher." -ForegroundColor Red
    exit 1
}

# Check if requirements are installed
Write-Host ""
Write-Host "[2/5] Checking dependencies..." -ForegroundColor Yellow
$packages = @("streamlit", "pandas", "numpy", "plotly", "folium")
$missingPackages = @()

foreach ($package in $packages) {
    $installed = python -c "import $package" 2>&1
    if ($LASTEXITCODE -ne 0) {
        $missingPackages += $package
    }
}

if ($missingPackages.Count -gt 0) {
    Write-Host "✗ Missing packages detected: $($missingPackages -join ', ')" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "[3/5] Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements_streamlit.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "✗ Installation failed!" -ForegroundColor Red
        exit 1
    }
    Write-Host "✓ All dependencies installed successfully!" -ForegroundColor Green
} else {
    Write-Host "✓ All dependencies are already installed!" -ForegroundColor Green
    Write-Host ""
    Write-Host "[3/5] Skipping installation..." -ForegroundColor Yellow
}

# Check if core files exist
Write-Host ""
Write-Host "[4/5] Verifying core files..." -ForegroundColor Yellow
$requiredFiles = @("netra_core.py", "netra_app.py")
$allFilesExist = $true

foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "✓ Found: $file" -ForegroundColor Green
    } else {
        Write-Host "✗ Missing: $file" -ForegroundColor Red
        $allFilesExist = $false
    }
}

if (-not $allFilesExist) {
    Write-Host ""
    Write-Host "✗ Some required files are missing!" -ForegroundColor Red
    exit 1
}

# Launch Streamlit
Write-Host ""
Write-Host "[5/5] Launching N.E.T.R.A. Command Center..." -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🛡️  NETRA System Starting..." -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📍 Local URL: http://localhost:8501" -ForegroundColor Cyan
Write-Host "🌐 Network URL: Check terminal output below" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Run Streamlit
streamlit run netra_app.py

# If Streamlit exits
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "N.E.T.R.A. System Stopped" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
