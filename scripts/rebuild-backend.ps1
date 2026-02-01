#!/usr/bin/env pwsh
# Rebuild backend containers (P1 and P2) with updated api_views.py

Write-Host "=== Backend Rebuild ===" -ForegroundColor Cyan
Write-Host ""

$server = "192.168.1.200"
$user = "dev"
$password = "dev@2025"
$projectPath = "/home/dev/paomi-as2"

Write-Host "Step 1: Stopping P1 and P2 containers..." -ForegroundColor Yellow
plink -batch -pw $password ${user}@${server} "cd $projectPath && docker-compose stop p1 p2"

Write-Host ""
Write-Host "Step 2: Removing P1 and P2 containers..." -ForegroundColor Yellow
plink -batch -pw $password ${user}@${server} "cd $projectPath && docker-compose rm -f p1 p2"

Write-Host ""
Write-Host "Step 3: Removing backend image..." -ForegroundColor Yellow
plink -batch -pw $password ${user}@${server} "docker rmi paomi-as2-p1 paomi-as2-p2 || true"

Write-Host ""
Write-Host "Step 4: Rebuilding backend with --no-cache..." -ForegroundColor Yellow
plink -batch -pw $password ${user}@${server} "cd $projectPath && docker-compose build --no-cache p1 p2"

Write-Host ""
Write-Host "Step 5: Starting P1 and P2 containers..." -ForegroundColor Yellow
plink -batch -pw $password ${user}@${server} "cd $projectPath && docker-compose up -d p1 p2"

Write-Host ""
Write-Host "Step 6: Waiting for containers to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

Write-Host ""
Write-Host "Step 7: Verifying deployment..." -ForegroundColor Yellow
plink -batch -pw $password ${user}@${server} "docker ps | grep 'p1-as2\|p2-as2'"

Write-Host ""
Write-Host "Step 8: Checking P1 logs..." -ForegroundColor Yellow
plink -batch -pw $password ${user}@${server} "docker logs p1-as2 --tail 20"

Write-Host ""
Write-Host "Step 9: Testing API endpoint..." -ForegroundColor Yellow
Start-Sleep -Seconds 5
plink -batch -pw $password ${user}@${server} "curl -s http://localhost:8001/api/stats/"

Write-Host ""
Write-Host "=== Rebuild Complete ===" -ForegroundColor Green
Write-Host ""
Write-Host "API should now be working at: http://192.168.1.200:8001/api/" -ForegroundColor Cyan
