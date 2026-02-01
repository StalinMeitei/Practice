# Deploy API changes and run real integration test

param(
    [string]$ServerIP = "192.168.1.200",
    [string]$Username = "dev",
    [string]$Password = "dev@2025"
)

Write-Host "=== Deploy and Test AS2 System ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "This will:" -ForegroundColor Yellow
Write-Host "  1. Deploy updated API with send-message endpoint" -ForegroundColor White
Write-Host "  2. Restart Docker containers" -ForegroundColor White
Write-Host "  3. Run real AS2 integration test" -ForegroundColor White
Write-Host "  4. Verify message counts increase" -ForegroundColor White
Write-Host ""

$continue = Read-Host "Continue? (y/n)"
if ($continue -ne 'y') {
    Write-Host "Cancelled" -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "Step 1: Deploying to server..." -ForegroundColor Cyan

# Run the deployment script
.\deploy-to-192.168.1.200.ps1

if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Deployment failed" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Step 2: Waiting for services to start..." -ForegroundColor Cyan
Write-Host "Waiting 10 seconds..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

Write-Host ""
Write-Host "Step 3: Running integration test..." -ForegroundColor Cyan
Write-Host ""

# Run the integration test
python test_real_as2_integration.py
$exitCode = $LASTEXITCODE

Write-Host ""

if ($exitCode -eq 0) {
    Write-Host "=== SUCCESS ===" -ForegroundColor Green
    Write-Host ""
    Write-Host "✓ API deployed successfully" -ForegroundColor Green
    Write-Host "✓ Integration test passed" -ForegroundColor Green
    Write-Host "✓ Messages sent and verified" -ForegroundColor Green
    Write-Host ""
    Write-Host "Check the results:" -ForegroundColor Cyan
    Write-Host "  - Dashboard: http://${ServerIP}:8001/" -ForegroundColor White
    Write-Host "  - Admin: http://${ServerIP}:8001/admin/pyas2/message/" -ForegroundColor White
    Write-Host "  - Messages: http://${ServerIP}:8001/messages" -ForegroundColor White
} else {
    Write-Host "=== FAILED ===" -ForegroundColor Red
    Write-Host ""
    Write-Host "Check the error messages above" -ForegroundColor Yellow
}

Write-Host ""
exit $exitCode
