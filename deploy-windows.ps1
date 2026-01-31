# Windows PowerShell Deployment Script
# Uses SSH config (dev_192168_rsa)

$ErrorActionPreference = "Stop"

$REMOTE_HOST = "dev_192168_rsa"
$REMOTE_DIR = "/home/dev/paomi-as2"
$PROJECT_NAME = "paomi-as2"

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Deploying $PROJECT_NAME to remote server" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# Check if we're in the right directory
if (-not (Test-Path "docker-compose.yml")) {
    Write-Host "Error: docker-compose.yml not found. Please run from project root." -ForegroundColor Red
    exit 1
}

# Create deployment package
Write-Host "`nCreating deployment package..." -ForegroundColor Green
$excludeItems = @('.git', '__pycache__', '*.pyc', '*.sqlite3', 'venv', '*.log', 'node_modules')
$tarCommand = "tar -czf $PROJECT_NAME.tar.gz --exclude='.git' --exclude='__pycache__' --exclude='*.pyc' --exclude='*.sqlite3' --exclude='venv' --exclude='*.log' ."

try {
    Invoke-Expression $tarCommand
    Write-Host "✓ Package created: $PROJECT_NAME.tar.gz" -ForegroundColor Green
} catch {
    Write-Host "Error creating package: $_" -ForegroundColor Red
    exit 1
}

# Copy to remote server
Write-Host "`nCopying to remote server..." -ForegroundColor Green
try {
    scp "$PROJECT_NAME.tar.gz" "${REMOTE_HOST}:/tmp/"
    Write-Host "✓ Files copied successfully" -ForegroundColor Green
} catch {
    Write-Host "Error copying files: $_" -ForegroundColor Red
    Remove-Item "$PROJECT_NAME.tar.gz" -Force
    exit 1
}

# Deploy on remote server
Write-Host "`nDeploying on remote server..." -ForegroundColor Green

$deployScript = "set -e && cd /home/dev && mkdir -p paomi-as2 && cd paomi-as2 && if [ -d 'P1' ] || [ -d 'P2' ]; then echo 'Creating backup...' && BACKUP_DIR=`"../paomi-as2-backup-`$(date +%Y%m%d-%H%M%S)`" && mkdir -p `$BACKUP_DIR && cp -r * `$BACKUP_DIR/ 2>/dev/null || true; fi && echo 'Extracting...' && tar -xzf /tmp/paomi-as2.tar.gz && rm /tmp/paomi-as2.tar.gz && echo 'Stopping containers...' && docker-compose down 2>/dev/null || true && echo 'Building...' && docker-compose build && echo 'Starting...' && docker-compose up -d && sleep 15 && docker-compose ps && echo '' && echo 'Deployment complete!' && echo 'Access: http://192.168.1.200:8001/'"

try {
    ssh $REMOTE_HOST $deployScript
    Write-Host "`n✓ Deployment completed successfully!" -ForegroundColor Green
} catch {
    Write-Host "Error during deployment: $_" -ForegroundColor Red
    Remove-Item "$PROJECT_NAME.tar.gz" -Force -ErrorAction SilentlyContinue
    exit 1
}

# Cleanup
Remove-Item "$PROJECT_NAME.tar.gz" -Force

Write-Host "`n=========================================" -ForegroundColor Cyan
Write-Host "Deployment Summary" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "`nYour application is now running at:" -ForegroundColor Yellow
Write-Host "  http://192.168.1.200:8001/" -ForegroundColor White
Write-Host "`nAdmin Interfaces:" -ForegroundColor Yellow
Write-Host "  P1: http://192.168.1.200:8001/admin/" -ForegroundColor White
Write-Host "  P2: http://192.168.1.200:8001/p2/admin/" -ForegroundColor White
Write-Host "`nDefault credentials: admin / admin123" -ForegroundColor Yellow
Write-Host ""
