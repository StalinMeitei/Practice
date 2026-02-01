#!/usr/bin/env pwsh
# Complete frontend rebuild script - stops, removes, rebuilds, and restarts frontend

Write-Host "=== Complete Frontend Rebuild ===" -ForegroundColor Cyan
Write-Host ""

$server = "192.168.1.200"
$user = "dev"
$password = "dev@2025"
$projectPath = "/home/dev/paomi-as2"

Write-Host "Step 1: Stopping frontend container..." -ForegroundColor Yellow
plink -batch -pw $password ${user}@${server} "cd $projectPath && docker-compose stop frontend"

Write-Host ""
Write-Host "Step 2: Removing frontend container..." -ForegroundColor Yellow
plink -batch -pw $password ${user}@${server} "cd $projectPath && docker-compose rm -f frontend"

Write-Host ""
Write-Host "Step 3: Removing frontend image..." -ForegroundColor Yellow
plink -batch -pw $password ${user}@${server} "docker rmi paomi-as2-frontend || true"

Write-Host ""
Write-Host "Step 4: Rebuilding frontend with --no-cache..." -ForegroundColor Yellow
plink -batch -pw $password ${user}@${server} "cd $projectPath && docker-compose build --no-cache frontend"

Write-Host ""
Write-Host "Step 5: Starting frontend container..." -ForegroundColor Yellow
plink -batch -pw $password ${user}@${server} "cd $projectPath && docker-compose up -d frontend"

Write-Host ""
Write-Host "Step 6: Waiting for container to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

Write-Host ""
Write-Host "Step 7: Verifying deployment..." -ForegroundColor Yellow
plink -batch -pw $password ${user}@${server} "docker ps | grep as2-frontend"

Write-Host ""
Write-Host "Step 8: Checking built files..." -ForegroundColor Yellow
plink -batch -pw $password ${user}@${server} "docker exec as2-frontend ls -lh /usr/share/nginx/html/"
plink -batch -pw $password ${user}@${server} "docker exec as2-frontend ls -lh /usr/share/nginx/html/assets/"

Write-Host ""
Write-Host "Step 9: Verifying MessageHeatmap in bundle..." -ForegroundColor Yellow
$heatmapCheck = plink -batch -pw $password ${user}@${server} "docker exec as2-frontend grep -o 'heatmap' /usr/share/nginx/html/assets/*.js | wc -l"
Write-Host "Heatmap references found: $heatmapCheck" -ForegroundColor Green

Write-Host ""
Write-Host "=== Rebuild Complete ===" -ForegroundColor Green
Write-Host ""
Write-Host "IMPORTANT: Clear your browser cache!" -ForegroundColor Red
Write-Host "  - Press Ctrl+Shift+Delete" -ForegroundColor Yellow
Write-Host "  - Or press Ctrl+F5 to hard refresh" -ForegroundColor Yellow
Write-Host "  - Or open in incognito/private mode" -ForegroundColor Yellow
Write-Host ""
Write-Host "Access the dashboard at: http://192.168.1.200:8001" -ForegroundColor Cyan
