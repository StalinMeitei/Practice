# Quick Deploy to 192.168.1.200
# PowerShell script

$ServerIP = "192.168.1.200"
$Username = "dev"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Deploy AS2 Dashboard to $ServerIP" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "This script will:" -ForegroundColor Yellow
Write-Host "  1. Create a deployment package" -ForegroundColor White
Write-Host "  2. Upload to server via SCP" -ForegroundColor White
Write-Host "  3. Deploy using Docker Compose" -ForegroundColor White
Write-Host "  4. Verify deployment" -ForegroundColor White
Write-Host ""

# Check for SSH
Write-Host "[1/7] Checking SSH client..." -ForegroundColor Yellow
try {
    $null = Get-Command ssh -ErrorAction Stop
    $null = Get-Command scp -ErrorAction Stop
    Write-Host "  ✓ SSH client found" -ForegroundColor Green
} catch {
    Write-Host "  ✗ SSH client not found" -ForegroundColor Red
    Write-Host "  Please install OpenSSH or use Git Bash" -ForegroundColor Yellow
    exit 1
}

# Create package
Write-Host "`n[2/7] Creating deployment package..." -ForegroundColor Yellow
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$packageName = "as2-deploy-$timestamp.tar.gz"

# Use tar if available, otherwise use 7zip or zip
if (Get-Command tar -ErrorAction SilentlyContinue) {
    tar -czf $packageName `
        docker-compose.yml `
        Dockerfile `
        nginx.conf `
        init-db.sh `
        init_as2_config.py `
        init_pgedge_agentic.py `
        api_views.py `
        generate_certificates.py `
        P1 `
        P2 `
        frontend `
        *.pem 2>$null
    Write-Host "  ✓ Package created: $packageName" -ForegroundColor Green
} else {
    Write-Host "  ✗ tar command not found" -ForegroundColor Red
    Write-Host "  Please install Git Bash or WSL" -ForegroundColor Yellow
    exit 1
}

# Upload package
Write-Host "`n[3/7] Uploading to server..." -ForegroundColor Yellow
Write-Host "  Enter password when prompted: dev@2025" -ForegroundColor Cyan
scp $packageName "${Username}@${ServerIP}:/home/dev/"

if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Upload complete" -ForegroundColor Green
} else {
    Write-Host "  ✗ Upload failed" -ForegroundColor Red
    exit 1
}

# Create deployment script
Write-Host "`n[4/7] Creating deployment script..." -ForegroundColor Yellow
$deployScript = @"
#!/bin/bash
cd /home/dev
echo '=== Extracting package ==='
mkdir -p paomi-as2-new
tar -xzf $packageName -C paomi-as2-new

echo '=== Stopping existing containers ==='
cd paomi-as2 2>/dev/null && docker-compose down || true

echo '=== Backing up old deployment ==='
cd /home/dev
mv paomi-as2 paomi-as2-backup-$timestamp 2>/dev/null || true
mv paomi-as2-new paomi-as2

echo '=== Building containers ==='
cd /home/dev/paomi-as2
docker-compose build --no-cache

echo '=== Starting containers ==='
docker-compose up -d

echo '=== Waiting for services ==='
sleep 20

echo '=== Container status ==='
docker-compose ps

echo '=== Deployment complete ==='
"@

$deployScript | Out-File -FilePath "deploy_script.sh" -Encoding ASCII -NoNewline

# Upload deployment script
Write-Host "`n[5/7] Uploading deployment script..." -ForegroundColor Yellow
scp deploy_script.sh "${Username}@${ServerIP}:/home/dev/"

# Execute deployment
Write-Host "`n[6/7] Executing deployment on server..." -ForegroundColor Yellow
Write-Host "  This may take several minutes..." -ForegroundColor Cyan
ssh "${Username}@${ServerIP}" "bash /home/dev/deploy_script.sh"

# Verify
Write-Host "`n[7/7] Verifying deployment..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

$services = @{
    "Dashboard" = "http://${ServerIP}:3000"
    "P1 Admin" = "http://${ServerIP}:8001/admin/"
    "API" = "http://${ServerIP}:8001/api/stats/"
}

foreach ($name in $services.Keys) {
    $url = $services[$name]
    try {
        $response = Invoke-WebRequest -Uri $url -TimeoutSec 10 -UseBasicParsing -ErrorAction SilentlyContinue
        Write-Host "  ✓ $name is accessible ($url)" -ForegroundColor Green
    } catch {
        Write-Host "  ⚠ $name not yet accessible - may need more time" -ForegroundColor Yellow
    }
}

# Cleanup
Write-Host "`nCleaning up..." -ForegroundColor Yellow
Remove-Item $packageName -Force -ErrorAction SilentlyContinue
Remove-Item deploy_script.sh -Force -ErrorAction SilentlyContinue

Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "  Deployment Complete!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Access Points:" -ForegroundColor Yellow
Write-Host "  Dashboard:    http://${ServerIP}:3000" -ForegroundColor White
Write-Host "  P1 Admin:     http://${ServerIP}:8001/admin/" -ForegroundColor White
Write-Host "  P2 Admin:     http://${ServerIP}:8001/p2/admin/" -ForegroundColor White
Write-Host "  API:          http://${ServerIP}:8001/api/" -ForegroundColor White
Write-Host ""
Write-Host "Credentials:" -ForegroundColor Yellow
Write-Host "  Admin:        admin / admin123" -ForegroundColor White
Write-Host "  Database:     postgres / postgres" -ForegroundColor White
Write-Host ""
Write-Host "Check Status:" -ForegroundColor Yellow
Write-Host "  ssh ${Username}@${ServerIP}" -ForegroundColor White
Write-Host "  cd /home/dev/paomi-as2" -ForegroundColor White
Write-Host "  docker-compose ps" -ForegroundColor White
Write-Host "  docker-compose logs -f" -ForegroundColor White
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
