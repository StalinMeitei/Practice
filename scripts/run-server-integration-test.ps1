# Run Integration Test on Server
# This script copies the test to the server and runs it there

param(
    [string]$ServerIP = "192.168.1.200",
    [string]$Username = "dev",
    [string]$Password = "dev@2025",
    [int]$MessageCount = 5
)

Write-Host "=== AS2 Server Integration Test ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Server: $ServerIP" -ForegroundColor Yellow
Write-Host "This will send $MessageCount real AS2 messages on the server" -ForegroundColor Yellow
Write-Host ""

# Check if plink is available (PuTTY)
$plinkPath = "plink"
$pscpPath = "pscp"

try {
    & $plinkPath -V 2>&1 | Out-Null
} catch {
    Write-Host "Error: plink (PuTTY) not found!" -ForegroundColor Red
    Write-Host "Please install PuTTY or use manual deployment" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Manual steps:" -ForegroundColor Cyan
    Write-Host "1. Copy test_send_messages_to_server.py to server" -ForegroundColor White
    Write-Host "2. SSH to server: ssh $Username@$ServerIP" -ForegroundColor White
    Write-Host "3. cd /home/$Username/paomi-as2" -ForegroundColor White
    Write-Host "4. python test_send_messages_to_server.py" -ForegroundColor White
    exit 1
}

Write-Host "Step 1: Copying test script to server..." -ForegroundColor Cyan

# Copy test script to server
$testScript = "test_send_messages_to_server.py"
$remotePath = "/home/$Username/paomi-as2/"

try {
    & $pscpPath -pw $Password $testScript "${Username}@${ServerIP}:${remotePath}"
    Write-Host "✓ Test script copied to server" -ForegroundColor Green
} catch {
    Write-Host "✗ Failed to copy script: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Step 2: Running test on server..." -ForegroundColor Cyan
Write-Host ""

# Run test on server
$command = "cd /home/$Username/paomi-as2 && python test_send_messages_to_server.py"

try {
    & $plinkPath -pw $Password "${Username}@${ServerIP}" $command
    $exitCode = $LASTEXITCODE
    
    Write-Host ""
    if ($exitCode -eq 0) {
        Write-Host "=== Integration Test Completed Successfully ===" -ForegroundColor Green
        Write-Host ""
        Write-Host "✓ Messages sent to server" -ForegroundColor Green
        Write-Host "✓ Message counts should now be increased" -ForegroundColor Green
        Write-Host ""
        Write-Host "Verify at:" -ForegroundColor Cyan
        Write-Host "  - Dashboard: http://${ServerIP}:8001/" -ForegroundColor White
        Write-Host "  - Admin: http://${ServerIP}:8001/admin/pyas2/message/" -ForegroundColor White
        Write-Host "  - Messages: http://${ServerIP}:8001/messages" -ForegroundColor White
    } else {
        Write-Host "=== Integration Test Failed ===" -ForegroundColor Red
        Write-Host "Check the error messages above" -ForegroundColor Yellow
    }
} catch {
    Write-Host "✗ Failed to run test: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
exit $exitCode
