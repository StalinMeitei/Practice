# Run AS2 Unit Tests
# This script runs the AS2 unit tests and displays results

param(
    [switch]$Send,
    [switch]$Receive,
    [switch]$Coverage,
    [int]$Verbosity = 2
)

Write-Host "=== AS2 Unit Test Runner ===" -ForegroundColor Cyan
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

# Change to unittest directory
$unittestDir = Join-Path $PSScriptRoot "unittest"
if (-not (Test-Path $unittestDir)) {
    Write-Host "Error: unittest directory not found!" -ForegroundColor Red
    exit 1
}

Set-Location $unittestDir

# Build command
$command = "python run_tests.py"

if ($Send) {
    $command += " --send"
    Write-Host "Running Send tests only..." -ForegroundColor Yellow
} elseif ($Receive) {
    $command += " --receive"
    Write-Host "Running Receive tests only..." -ForegroundColor Yellow
} else {
    Write-Host "Running all tests..." -ForegroundColor Yellow
}

# Note: verbosity is handled by the Python script's default value

Write-Host ""

# Run tests
if ($Coverage) {
    Write-Host "Running with coverage..." -ForegroundColor Yellow
    Write-Host ""
    
    # Check if coverage is installed
    try {
        python -m coverage --version | Out-Null
    } catch {
        Write-Host "Installing coverage..." -ForegroundColor Yellow
        pip install coverage
    }
    
    # Run with coverage
    python -m coverage run run_tests.py
    $exitCode = $LASTEXITCODE
    
    Write-Host ""
    Write-Host "=== Coverage Report ===" -ForegroundColor Cyan
    python -m coverage report
    
    Write-Host ""
    Write-Host "Generating HTML coverage report..." -ForegroundColor Yellow
    python -m coverage html
    Write-Host "HTML report generated in: htmlcov/index.html" -ForegroundColor Green
} else {
    # Run tests normally
    Invoke-Expression $command
    $exitCode = $LASTEXITCODE
}

Write-Host ""

# Display result
if ($exitCode -eq 0) {
    Write-Host "=== Tests Passed ===" -ForegroundColor Green
} else {
    Write-Host "=== Tests Failed ===" -ForegroundColor Red
}

Write-Host ""

# Return to original directory
Set-Location $PSScriptRoot

exit $exitCode
