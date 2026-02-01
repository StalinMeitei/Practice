#!/usr/bin/env pwsh
# Send test messages to populate the dashboard with real data

Write-Host "=== Sending Test Messages ===" -ForegroundColor Cyan
Write-Host ""

$server = "192.168.1.200"
$user = "dev"
$password = "dev@2025"
$projectPath = "/home/dev/paomi-as2"

Write-Host "Running integration test to send messages..." -ForegroundColor Yellow
plink -batch -pw $password ${user}@${server} "cd $projectPath && python3 unittest/test_send_messages_to_server.py"

Write-Host ""
Write-Host "=== Test Messages Sent ===" -ForegroundColor Green
Write-Host ""
Write-Host "Refresh the dashboard to see updated data!" -ForegroundColor Cyan
Write-Host "Dashboard: http://192.168.1.200:8001" -ForegroundColor Cyan
