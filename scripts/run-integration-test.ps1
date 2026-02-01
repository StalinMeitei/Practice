# Run AS2 Integration Tests
# Tests actual message sending/receiving on 192.168.1.200:8001

param(
    [string]$ServerUrl = "http://192.168.1.200:8001"
)

Write-Host "=== AS2 Integration Test Runner ===" -ForegroundColor Cyan
Write-Host ""

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python version: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Error: Python not found!" -ForegroundColor Red
    Write-Host "Please install Python 3.x" -ForegroundColor Yellow
    exit 1
}

# Set environment variable for server URL
$env:AS2_SERVER_URL = $ServerUrl

Write-Host "Server URL: $ServerUrl" -ForegroundColor Yellow
Write-Host ""

# Check if server is accessible
Write-Host "Checking server connectivity..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri $ServerUrl -TimeoutSec 5 -UseBasicParsing -ErrorAction Stop
    Write-Host "✓ Server is accessible" -ForegroundColor Green
} catch {
    Write-Host "✗ Cannot connect to server at $ServerUrl" -ForegroundColor Red
    Write-Host "  Make sure the server is running and accessible" -ForegroundColor Yellow
    Write-Host "  Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    $continue = Read-Host "Continue anyway? (y/n)"
    if ($continue -ne 'y') {
        exit 1
    }
}

Write-Host ""

# Change to unittest directory
$unittestDir = Join-Path $PSScriptRoot "unittest"
if (-not (Test-Path $unittestDir)) {
    Write-Host "Error: unittest directory not found!" -ForegroundColor Red
    exit 1
}

Set-Location $unittestDir

# Run integration tests
Write-Host "Running integration tests..." -ForegroundColor Cyan
Write-Host ""

python test_as2_integration.py
$exitCode = $LASTEXITCODE

Write-Host ""

# Display result
if ($exitCode -eq 0) {
    Write-Host "=== Integration Tests Passed ===" -ForegroundColor Green
    Write-Host ""
    Write-Host "✓ Messages should now be visible in:" -ForegroundColor Green
    Write-Host "  - Admin panel: $ServerUrl/admin/" -ForegroundColor Cyan
    Write-Host "  - Dashboard UI: $ServerUrl/" -ForegroundColor Cyan
    Write-Host "  - Messages page: $ServerUrl/messages" -ForegroundColor Cyan
} else {
    Write-Host "=== Integration Tests Failed ===" -ForegroundColor Red
    Write-Host ""
    Write-Host "Check the error messages above for details" -ForegroundColor Yellow
}

Write-Host ""

# Return to original directory
Set-Location $PSScriptRoot

exit $exitCode
