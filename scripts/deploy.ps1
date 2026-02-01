# PowerShell Deployment script for paomi-as2 to remote server
# Usage: .\deploy.ps1

$ErrorActionPreference = "Stop"

# Configuration
$REMOTE_HOST = "192.168.1.200"
$REMOTE_USER = "dev"
$REMOTE_PASSWORD = "dev@2025"
$REMOTE_DIR = "/home/dev/paomi-as2"
$PROJECT_NAME = "paomi-as2"

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Deploying $PROJECT_NAME to $REMOTE_HOST" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# Check if plink and pscp are available (PuTTY tools)
$plinkPath = Get-Command plink -ErrorAction SilentlyContinue
$pscpPath = Get-Command pscp -ErrorAction SilentlyContinue

if (-not $plinkPath -or -not $pscpPath) {
    Write-Host "Error: PuTTY tools (plink, pscp) not found in PATH" -ForegroundColor Red
    Write-Host "Please install PuTTY or use WSL to run deploy.sh" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Alternative: Use SSH from PowerShell (requires OpenSSH)" -ForegroundColor Yellow
    Write-Host "Or run: wsl ./deploy.sh" -ForegroundColor Yellow
    exit 1
}

# Create deployment package
Write-Host "Creating deployment package..." -ForegroundColor Green
$excludeFiles = @('.git', '__pycache__', '*.pyc', '*.sqlite3', 'venv', '*.log')
tar -czf "$PROJECT_NAME.tar.gz" --exclude='.git' --exclude='__pycache__' --exclude='*.pyc' --exclude='*.sqlite3' --exclude='venv' --exclude='*.log' .

Write-Host "Package created: $PROJECT_NAME.tar.gz" -ForegroundColor Green

# Copy to remote server
Write-Host "Copying files to remote server..." -ForegroundColor Green
echo y | pscp -pw $REMOTE_PASSWORD "$PROJECT_NAME.tar.gz" "${REMOTE_USER}@${REMOTE_HOST}:/tmp/"

# Execute deployment on remote server
Write-Host "Executing deployment on remote server..." -ForegroundColor Green

$deployScript = @'
set -e
mkdir -p /home/dev/paomi-as2
cd /home/dev/paomi-as2

if [ -d "P1" ] || [ -d "P2" ]; then
    echo "Backing up existing deployment..."
    BACKUP_DIR="/home/dev/paomi-as2-backup-$(date +%Y%m%d-%H%M%S)"
    mkdir -p $BACKUP_DIR
    cp -r * $BACKUP_DIR/ 2>/dev/null || true
    echo "Backup created at: $BACKUP_DIR"
fi

echo "Extracting deployment package..."
tar -xzf /tmp/paomi-as2.tar.gz -C /home/dev/paomi-as2/
rm /tmp/paomi-as2.tar.gz

echo "Stopping existing containers..."
docker-compose down || true

echo "Building Docker images..."
docker-compose build

echo "Starting containers..."
docker-compose up -d

echo "Waiting for services to start..."
sleep 10

echo "Checking container status..."
docker-compose ps

echo "Deployment completed successfully!"
echo ""
echo "Access points:"
echo "  - P1 Admin: http://192.168.1.200/admin/ (admin/admin123)"
echo "  - P2 Admin: http://192.168.1.200/p2/admin/ (admin/admin123)"
'@

echo y | plink -pw $REMOTE_PASSWORD "${REMOTE_USER}@${REMOTE_HOST}" $deployScript

# Cleanup local package
Remove-Item "$PROJECT_NAME.tar.gz" -Force

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Deployment completed successfully!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Access your application at:" -ForegroundColor Yellow
Write-Host "  - http://192.168.1.200/" -ForegroundColor White
Write-Host "  - P1 Admin: http://192.168.1.200/admin/" -ForegroundColor White
Write-Host "  - P2 Admin: http://192.168.1.200/p2/admin/" -ForegroundColor White
