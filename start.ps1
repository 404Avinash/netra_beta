# N.E.T.R.A. System Startup Script
# Runs both FastAPI backend and Streamlit frontend

Write-Host "🚀 Starting N.E.T.R.A. System..." -ForegroundColor Cyan
Write-Host ""

# Check if models exist
if (-Not (Test-Path "models\netra_xgboost_model.pkl")) {
    Write-Host "⚠️  ML Model not found!" -ForegroundColor Yellow
    Write-Host "   Run: python development\train_ml_model.py --large" -ForegroundColor Yellow
    Write-Host ""
    $response = Read-Host "Continue anyway? (y/n)"
    if ($response -ne "y") {
        exit
    }
}

# Start FastAPI in background
Write-Host "🔧 Starting FastAPI Backend (Port 8000)..." -ForegroundColor Green
$fastapi = Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; uvicorn api.main:app --reload --port 8000" -PassThru

Start-Sleep -Seconds 3

# Start Streamlit in background
Write-Host "🎨 Starting Streamlit Frontend (Port 8501)..." -ForegroundColor Green
$streamlit = Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; streamlit run netra_unified_app.py" -PassThru

Start-Sleep -Seconds 2

Write-Host ""
Write-Host "✅ N.E.T.R.A. System is running!" -ForegroundColor Cyan
Write-Host ""
Write-Host "📡 FastAPI Backend:  http://localhost:8000" -ForegroundColor White
Write-Host "   API Docs:         http://localhost:8000/docs" -ForegroundColor Gray
Write-Host "   Health Check:     http://localhost:8000/api/health" -ForegroundColor Gray
Write-Host ""
Write-Host "🎨 Streamlit App:    http://localhost:8501" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C in each window to stop services" -ForegroundColor Yellow
Write-Host ""

# Wait for user input
Write-Host "Press any key to stop all services..." -ForegroundColor Red
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Cleanup
Write-Host ""
Write-Host "🛑 Stopping services..." -ForegroundColor Yellow
Stop-Process -Id $fastapi.Id -Force -ErrorAction SilentlyContinue
Stop-Process -Id $streamlit.Id -Force -ErrorAction SilentlyContinue
Write-Host "✅ All services stopped." -ForegroundColor Green
