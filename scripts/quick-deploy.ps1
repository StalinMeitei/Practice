# Quick Deploy - Upload and Restart
# Simple deployment that uploads code and restarts containers

param(
    [string]$ServerIP = "192.168.1.200",
    [string]$Username = "dev",
    [string]$Password = "dev@2025"
)

Write-Host "=== Quick Deploy to $ServerIP ===" -ForegroundColor Cyan
Write-Host ""

# Step 1: Upload frontend source
Write-Host "[1/5] Uploading frontend source..." -ForegroundColor Cyan
pscp -pw $Password -r ../frontend/src ${Username}@${ServerIP}:/home/${Username}/paomi-as2/frontend/
pscp -pw $Password ../frontend/package.json ${Username}@${ServerIP}:/home/${Username}/paomi-as2/frontend/
pscp -pw $Password ../frontend/vite.config.js ${Username}@${ServerIP}:/home/${Username}/paomi-as2/frontend/
pscp -pw $Password ../frontend/index.html ${Username}@${ServerIP}:/home/${Username}/paomi-as2/frontend/

Write-Host "  ✓ Frontend uploaded" -ForegroundColor Green
Write-Host ""

# Step 2: Upload API views
Write-Host "[2/5] Uploading API views..." -ForegroundColor Cyan
pscp -pw $Password ../api_views.py ${Username}@${ServerIP}:/home/${Username}/paomi-as2/
pscp -pw $Password ../P1/urls.py ${Username}@${ServerIP}:/home/${Username}/paomi-as2/P1/

Write-Host "  ✓ API files uploaded" -ForegroundColor Green
Write-Host ""

# Step 3: Rebuild frontend container
Write-Host "[3/5] Rebuilding frontend container..." -ForegroundColor Cyan
Write-Host "  This will take 2-3 minutes..." -ForegroundColor Yellow

$rebuildScript = @'
cd /home/dev/paomi-as2
docker-compose stop frontend nginx
docker-compose build --no-cache frontend
docker-compose up -d frontend nginx
'@

plink -batch -pw $Password ${Username}@${ServerIP} $rebuildScript

Write-Host "  ✓ Frontend rebuilt" -ForegroundColor Green
Write-Host ""

# Step 4: Restart P1 container
Write-Host "[4/5] Restarting P1 container..." -ForegroundColor Cyan
plink -batch -pw $Password ${Username}@${ServerIP} "cd /home/dev/paomi-as2; docker-compose restart p1"

Write-Host "  ✓ P1 restarted" -ForegroundColor Green
Write-Host ""

# Step 5: Wait and verify
Write-Host "[5/5] Waiting for services..." -ForegroundColor Cyan
Start-Sleep -Seconds 10

try {
    $response = Invoke-WebRequest -Uri "http://${ServerIP}:8001/" -TimeoutSec 5 -UseBasicParsing
    Write-Host "  ✓ Dashboard is accessible!" -ForegroundColor Green
} catch {
    Write-Host "  ⚠ Dashboard not yet ready - may need more time" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=== Deployment Complete ===" -ForegroundColor Green
Write-Host ""
Write-Host "Access:" -ForegroundColor Cyan
Write-Host "  Dashboard: http://${ServerIP}:8001/" -ForegroundColor White
Write-Host "  Admin: http://${ServerIP}:8001/admin/" -ForegroundColor White
Write-Host ""
Write-Host "Features:" -ForegroundColor Cyan
Write-Host "  ✓ Real-time data from API" -ForegroundColor White
Write-Host "  ✓ Line chart with sent/received/failed" -ForegroundColor White
Write-Host "  ✓ Heatmap with 5 granularities" -ForegroundColor White
Write-Host "  ✓ Toggle between Line Chart and Heatmap" -ForegroundColor White
Write-Host ""
Write-Host "Clear browser cache with Ctrl+F5 to see latest UI!" -ForegroundColor Yellow
Write-Host ""
