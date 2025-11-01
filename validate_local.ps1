# Local Pre-Deployment Validation Script
Write-Host ""
Write-Host "N.E.T.R.A. PRE-DEPLOYMENT VALIDATION" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

$allPassed = $true

# Check required CSV files
Write-Host "Checking required CSV files..." -ForegroundColor Yellow
$csvFiles = @("netra_threat_log.csv", "locations_northeast_india.csv", "sensor_readings_live.csv")

foreach ($file in $csvFiles) {
    if (Test-Path $file) {
        $lines = (Get-Content $file).Count
        Write-Host "  [OK] $file - $lines lines" -ForegroundColor Green
    } else {
        Write-Host "  [FAIL] $file NOT FOUND" -ForegroundColor Red
        $allPassed = $false
    }
}

# Check Python files
Write-Host ""
Write-Host "Checking Python files..." -ForegroundColor Yellow
$pyFiles = @("netra_core.py", "netra_unified_app.py")

foreach ($file in $pyFiles) {
    if (Test-Path $file) {
        $lines = (Get-Content $file).Count
        Write-Host "  [OK] $file - $lines lines" -ForegroundColor Green
    } else {
        Write-Host "  [FAIL] $file NOT FOUND" -ForegroundColor Red
        $allPassed = $false
    }
}

# Check requirements
Write-Host ""
Write-Host "Checking requirements.txt..." -ForegroundColor Yellow
if (Test-Path "requirements.txt") {
    $packages = (Get-Content "requirements.txt" | Where-Object {$_ -and $_ -notmatch "^#"}).Count
    Write-Host "  [OK] requirements.txt - $packages packages" -ForegroundColor Green
} else {
    Write-Host "  [FAIL] requirements.txt NOT FOUND" -ForegroundColor Red
    $allPassed = $false
}

# Data quality check
Write-Host ""
Write-Host "Quick data quality check..." -ForegroundColor Yellow

if (Test-Path "netra_threat_log.csv") {
    $threatData = Import-Csv "netra_threat_log.csv"
    $totalRecords = $threatData.Count
    
    Write-Host "  Total records: $totalRecords" -ForegroundColor Cyan
    
    # Threat distribution
    $threatCounts = $threatData | Group-Object Threat_Level | Select-Object Name, Count
    foreach ($item in $threatCounts | Sort-Object Count -Descending) {
        $pct = [math]::Round(($item.Count / $totalRecords) * 100, 1)
        Write-Host "    $($item.Name): $($item.Count) records ($pct%)" -ForegroundColor Gray
    }
    
    # Check for explosive types
    $explosiveCount = ($threatData | Select-Object -Unique Explosive_Type).Count
    if ($explosiveCount -gt 0) {
        Write-Host "  [OK] $explosiveCount unique explosive types detected" -ForegroundColor Green
    }
}

# Git status
Write-Host ""
Write-Host "Checking git status..." -ForegroundColor Yellow
$gitStatus = git status --short
if ($gitStatus) {
    $changeCount = ($gitStatus | Measure-Object).Count
    Write-Host "  Changes detected: $changeCount files" -ForegroundColor Cyan
} else {
    Write-Host "  No changes to commit" -ForegroundColor Gray
}

# Final result
Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan

if ($allPassed) {
    Write-Host ""
    Write-Host "SUCCESS - ALL VALIDATION CHECKS PASSED!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Ready to deploy to GitHub!" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "  1. git add netra_threat_log.csv" -ForegroundColor White
    Write-Host "  2. git commit -m 'Data: 1200 analyses with 188 explosive types'" -ForegroundColor White
    Write-Host "  3. git push origin main" -ForegroundColor White
    Write-Host "  4. Wait 2-3 minutes for Streamlit auto-deploy" -ForegroundColor White
    Write-Host ""
    Write-Host "App URL: https://netra-unified-bet-001.streamlit.app" -ForegroundColor Cyan
    Write-Host ""
    exit 0
} else {
    Write-Host ""
    Write-Host "VALIDATION FAILED!" -ForegroundColor Red
    Write-Host "Please fix the issues above before deployment." -ForegroundColor Red
    Write-Host ""
    exit 1
}
