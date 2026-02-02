#!/usr/bin/env pwsh
# Test EDI XML Messages - Send realistic EDI documents via AS2

Write-Host "=== EDI XML AS2 Message Test ===" -ForegroundColor Cyan
Write-Host ""

$server = "192.168.1.200"
$user = "dev"
$password = "dev@2025"
$projectPath = "/home/dev/paomi-as2"

Write-Host "Step 1: Uploading EDI test script..." -ForegroundColor Yellow
pscp -batch -pw $password ../unittest/test_edi_xml_messages.py ${user}@${server}:${projectPath}/unittest/

Write-Host ""
Write-Host "Step 2: Copying to Docker container..." -ForegroundColor Yellow
plink -batch -pw $password ${user}@${server} "docker cp ${projectPath}/unittest/test_edi_xml_messages.py p1-as2:/app/unittest/"

Write-Host ""
Write-Host "Step 3: Running EDI XML test..." -ForegroundColor Yellow
Write-Host ""
Write-Host "----------------------------------------" -ForegroundColor DarkGray

plink -batch -pw $password ${user}@${server} "docker exec p1-as2 python3 /app/unittest/test_edi_xml_messages.py"

Write-Host "----------------------------------------" -ForegroundColor DarkGray
Write-Host ""

Write-Host "Step 4: Checking results..." -ForegroundColor Yellow
$stats = plink -batch -pw $password ${user}@${server} "curl -s http://localhost:8001/api/stats/"
Write-Host "Stats: $stats" -ForegroundColor Green

Write-Host ""
Write-Host "=== Test Complete ===" -ForegroundColor Green
Write-Host ""
Write-Host "Verify in your browser:" -ForegroundColor Cyan
Write-Host "  - Dashboard: http://192.168.1.200:8001/" -ForegroundColor Yellow
Write-Host "  - Messages: http://192.168.1.200:8001/messages" -ForegroundColor Yellow
Write-Host "  - Admin: http://192.168.1.200:8001/admin/pyas2/message/" -ForegroundColor Yellow
Write-Host ""
Write-Host "Click the eye icon (👁️) to view full EDI XML content!" -ForegroundColor Green
