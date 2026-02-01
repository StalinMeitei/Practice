#!/usr/bin/env pwsh
# Complete deployment - rebuilds both frontend and backend with latest changes

Write-Host "=== Complete Deployment - Frontend + Backend ===" -ForegroundColor Cyan
Write-Host ""

$server = "192.168.1.200"
$user = "dev"
$password = "dev@2025"
$projectPath = "/home/dev/paomi-as2"

Write-Host "Step 1: Uploading updated files to server..." -ForegroundColor Yellow
Write-Host "  - Uploading api_views.py..." -ForegroundColor Gray
pscp -batch -pw $password ../api_views.py ${user}@${server}:${projectPath}/api_views.py

Write-Host "  - Uploading Dashboard.jsx..." -ForegroundColor Gray
pscp -batch -pw $password ../frontend/src/pages/Dashboard.jsx ${user}@${server}:${projectPath}/frontend/src/pages/Dashboard.jsx

Write-Host ""
Write-Host "Step 2: Stopping all containers..." -ForegroundColor Yellow
plink -batch -pw $password ${user}@${server} "cd $projectPath && docker-compose stop"

Write-Host ""
Write-Host "Step 3: Removing containers..." -ForegroundColor Yellow
plink -batch -pw $password ${user}@${server} "cd $projectPath && docker-compose rm -f p1 p2 frontend"

Write-Host ""
Write-Host "Step 4: Removing old images..." -ForegroundColor Yellow
plink -batch -pw $password ${user}@${server} "docker rmi paomi-as2-p1 paomi-as2-p2 paomi-as2-frontend || true"

Write-Host ""
Write-Host "Step 5: Rebuilding all containers with --no-cache..." -ForegroundColor Yellow
plink -batch -pw $password ${user}@${server} "cd $projectPath && docker-compose build --no-cache p1 p2 frontend"

Write-Host ""
Write-Host "Step 6: Starting all containers..." -ForegroundColor Yellow
plink -batch -pw $password ${user}@${server} "cd $projectPath && docker-compose up -d"

Write-Host ""
Write-Host "Step 7: Waiting for services to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 15

Write-Host ""
Write-Host "Step 8: Verifying deployment..." -ForegroundColor Yellow
plink -batch -pw $password ${user}@${server} "docker ps | grep 'p1-as2\|p2-as2\|as2-frontend'"

Write-Host ""
Write-Host "Step 9: Testing API endpoint..." -ForegroundColor Yellow
Start-Sleep -Seconds 5
$apiTest = plink -batch -pw $password ${user}@${server} "curl -s http://localhost:8001/api/stats/"
Write-Host "API Response: $apiTest" -ForegroundColor Gray

Write-Host ""
Write-Host "Step 10: Verifying frontend bundle..." -ForegroundColor Yellow
$heatmapCheck = plink -batch -pw $password ${user}@${server} "docker exec as2-frontend sh -c 'grep -o heatmap /usr/share/nginx/html/assets/*.js | wc -l'"
Write-Host "Heatmap references in bundle: $heatmapCheck" -ForegroundColor Green

Write-Host ""
Write-Host "=== Deployment Complete ===" -ForegroundColor Green
Write-Host ""
Write-Host "IMPORTANT: Clear your browser cache!" -ForegroundColor Red
Write-Host "  - Press Ctrl+Shift+Delete" -ForegroundColor Yellow
Write-Host "  - Or press Ctrl+F5 to hard refresh" -ForegroundColor Yellow
Write-Host "  - Or open in incognito/private mode" -ForegroundColor Yellow
Write-Host ""
Write-Host "Access the dashboard at: http://192.168.1.200:8001" -ForegroundColor Cyan
Write-Host "API endpoints at: http://192.168.1.200:8001/api/" -ForegroundColor Cyan
