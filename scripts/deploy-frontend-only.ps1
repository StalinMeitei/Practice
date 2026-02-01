# Deploy Frontend Only - Quick Update
# This script uploads the built frontend and restarts only the frontend container

param(
    [string]$ServerIP = "192.168.1.200",
    [string]$Username = "dev",
    [string]$Password = "dev@2025"
)

Write-Host "=== Deploy Frontend Only ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Server: $ServerIP" -ForegroundColor Yellow
Write-Host ""

# Check if dist folder exists
if (-not (Test-Path "../frontend/dist")) {
    Write-Host "Error: Frontend not built!" -ForegroundColor Red
    Write-Host "Run: cd frontend && npm run build" -ForegroundColor Yellow
    exit 1
}

Write-Host "[1/4] Uploading frontend dist folder..." -ForegroundColor Cyan
pscp -pw $Password -r ../frontend/dist ${Username}@${ServerIP}:/home/${Username}/paomi-as2/frontend/

if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Upload failed" -ForegroundColor Red
    exit 1
}

Write-Host "  ✓ Frontend uploaded" -ForegroundColor Green
Write-Host ""

Write-Host "[2/4] Restarting frontend container..." -ForegroundColor Cyan
plink -pw $Password ${Username}@${ServerIP} "cd /home/${Username}/paomi-as2 && docker-compose restart as2-frontend nginx-as2"

Write-Host "  ✓ Containers restarted" -ForegroundColor Green
Write-Host ""

Write-Host "[3/4] Waiting for services..." -ForegroundColor Cyan
Start-Sleep -Seconds 5
Write-Host "  ✓ Services should be ready" -ForegroundColor Green
Write-Host ""

Write-Host "[4/4] Verifying deployment..." -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri "http://${ServerIP}:8001/" -TimeoutSec 5 -UseBasicParsing
    Write-Host "  ✓ Dashboard is accessible!" -ForegroundColor Green
} catch {
    Write-Host "  ⚠ Dashboard not yet accessible - may need more time" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=== Deployment Complete ===" -ForegroundColor Green
Write-Host ""
Write-Host "Access the dashboard:" -ForegroundColor Cyan
Write-Host "  http://${ServerIP}:8001/" -ForegroundColor White
Write-Host ""
Write-Host "Features available:" -ForegroundColor Cyan
Write-Host "  ✓ Dashboard with statistics" -ForegroundColor White
Write-Host "  ✓ Line chart (sent/received/failed)" -ForegroundColor White
Write-Host "  ✓ Heatmap (hourly/daily/weekly/monthly/yearly)" -ForegroundColor White
Write-Host "  ✓ Messages list" -ForegroundColor White
Write-Host "  ✓ Partners management" -ForegroundColor White
Write-Host "  ✓ Keys management" -ForegroundColor White
Write-Host ""
Write-Host "If you see old UI, try:" -ForegroundColor Yellow
Write-Host "  1. Hard refresh: Ctrl+F5" -ForegroundColor White
Write-Host "  2. Clear browser cache" -ForegroundColor White
Write-Host "  3. Open in incognito/private window" -ForegroundColor White
Write-Host ""
