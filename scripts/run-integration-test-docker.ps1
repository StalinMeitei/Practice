#!/usr/bin/env pwsh
# Run AS2 integration test inside Docker container

Write-Host "=== AS2 Integration Test (Docker) ===" -ForegroundColor Cyan
Write-Host ""

$server = "192.168.1.200"
$user = "dev"
$password = "dev@2025"
$projectPath = "/home/dev/paomi-as2"

Write-Host "Step 1: Uploading test scripts to server..." -ForegroundColor Yellow
pscp -batch -pw $password ../unittest/test_send_messages_to_server.py ${user}@${server}:${projectPath}/unittest/test_send_messages_to_server.py
pscp -batch -pw $password ../unittest/test_real_as2_send_receive.py ${user}@${server}:${projectPath}/unittest/test_real_as2_send_receive.py

Write-Host ""
Write-Host "Step 2: Checking Docker containers..." -ForegroundColor Yellow
plink -batch -pw $password ${user}@${server} "docker ps | grep 'p1-as2\|p2-as2'"

Write-Host ""
Write-Host "Step 3: Getting initial message count..." -ForegroundColor Yellow
$initialStats = plink -batch -pw $password ${user}@${server} "curl -s http://localhost:8001/api/stats/"
Write-Host "Initial stats: $initialStats" -ForegroundColor Gray

Write-Host ""
Write-Host "Step 4: Running integration test inside P1 container..." -ForegroundColor Yellow
Write-Host ""
Write-Host "----------------------------------------" -ForegroundColor DarkGray

plink -batch -pw $password ${user}@${server} "cd $projectPath && docker exec p1-as2 python3 /app/unittest/test_send_messages_to_server.py"

Write-Host "----------------------------------------" -ForegroundColor DarkGray
Write-Host ""

Write-Host "Step 5: Waiting for messages to be processed..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "Step 6: Getting final message count..." -ForegroundColor Yellow
$finalStats = plink -batch -pw $password ${user}@${server} "curl -s http://localhost:8001/api/stats/"
Write-Host "Final stats: $finalStats" -ForegroundColor Gray

Write-Host ""
Write-Host "Step 7: Checking recent messages..." -ForegroundColor Yellow
$messages = plink -batch -pw $password ${user}@${server} "curl -s http://localhost:8001/api/messages/ | head -50"
Write-Host "Recent messages retrieved" -ForegroundColor Gray

Write-Host ""
Write-Host "=== Test Complete ===" -ForegroundColor Green
Write-Host ""
Write-Host "Verify the results in your browser:" -ForegroundColor Cyan
Write-Host "  - Dashboard: http://192.168.1.200:8001/" -ForegroundColor Yellow
Write-Host "  - Admin: http://192.168.1.200:8001/admin/pyas2/message/" -ForegroundColor Yellow
Write-Host "  - Messages: http://192.168.1.200:8001/messages" -ForegroundColor Yellow
Write-Host ""
Write-Host "The message counts should have increased!" -ForegroundColor Green
