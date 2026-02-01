#!/usr/bin/env pwsh
# Run real AS2 send/receive integration test on the server

Write-Host "=== AS2 Real Send/Receive Integration Test ===" -ForegroundColor Cyan
Write-Host ""

$server = "192.168.1.200"
$user = "dev"
$password = "dev@2025"
$projectPath = "/home/dev/paomi-as2"

Write-Host "Step 1: Uploading test script to server..." -ForegroundColor Yellow
pscp -batch -pw $password ../unittest/test_real_as2_send_receive.py ${user}@${server}:${projectPath}/unittest/test_real_as2_send_receive.py

Write-Host ""
Write-Host "Step 2: Running test inside P1 Docker container..." -ForegroundColor Yellow
Write-Host ""
plink -batch -pw $password ${user}@${server} "cd $projectPath && docker exec -it p1-as2 python3 /app/unittest/test_real_as2_send_receive.py"

Write-Host ""
Write-Host "=== Test Complete ===" -ForegroundColor Green
Write-Host ""
Write-Host "Check the results above and verify in your browser:" -ForegroundColor Cyan
Write-Host "  - Dashboard: http://192.168.1.200:8001/" -ForegroundColor Yellow
Write-Host "  - Admin: http://192.168.1.200:8001/admin/pyas2/message/" -ForegroundColor Yellow
Write-Host "  - Messages: http://192.168.1.200:8001/messages" -ForegroundColor Yellow
