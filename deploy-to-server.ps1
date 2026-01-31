# Deploy AS2 Dashboard to Remote Server (192.168.1.200)
# PowerShell script for Windows

param(
    [string]$ServerIP = "192.168.1.200",
    [string]$Username = "dev",
    [string]$Password = "dev@2025"
)

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan
Write-Host "  Deploy AS2 Dashboard to $ServerIP" -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan
Write-Host ""

# Check if plink and pscp are available (PuTTY tools)
$plinkPath = "plink"
$pscpPath = "pscp"

Write-Host "[1/8] Checking deployment tools..." -ForegroundColor Yellow
try {
    $null = Get-Command $plinkPath -ErrorAction Stop
    $null = Get-Command $pscpPath -ErrorAction Stop
    Write-Host "  ✓ PuTTY tools found" -ForegroundColor Green
} catch {
    Write-Host "  ⚠ PuTTY tools not found. Installing..." -ForegroundColor Yellow
    Write-Host "  Please install PuTTY from: https://www.putty.org/" -ForegroundColor Yellow
    Write-Host "  Or use: winget install PuTTY.PuTTY" -ForegroundColor Yellow
    
    # Try alternative: use ssh/scp if available
    try {
        $null = Get-Command ssh -ErrorAction Stop
        $null = Get-Command scp -ErrorAction Stop
        Write-Host "  ✓ Using OpenSSH instead" -ForegroundColor Green
        $plinkPath = "ssh"
        $pscpPath = "scp"
    } catch {
        Write-Host "  ✗ No SSH tools available" -ForegroundColor Red
        exit 1
    }
}

# Create deployment package
Write-Host "`n[2/8] Creating deployment package..." -ForegroundColor Yellow
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$packageName = "as2-dashboard-$timestamp.zip"

# Files to include
$filesToInclude = @(
    "docker-compose.yml",
    "Dockerfile",
    "nginx.conf",
    "init-db.sh",
    "init_as2_config.py",
    "init_pgedge_agentic.py",
    "api_views.py",
    "generate_certificates.py",
    "P1",
    "P2",
    "frontend"
)

# Create zip package
Compress-Archive -Path $filesToInclude -DestinationPath $packageName -Force
Write-Host "  ✓ Package created: $packageName" -ForegroundColor Green

# Upload package to server
Write-Host "`n[3/8] Uploading package to server..." -ForegroundColor Yellow
if ($pscpPath -eq "scp") {
    scp -o StrictHostKeyChecking=no $packageName "${Username}@${ServerIP}:/home/dev/"
} else {
    & $pscpPath -pw $Password $packageName "${Username}@${ServerIP}:/home/dev/"
}

if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Package uploaded" -ForegroundColor Green
} else {
    Write-Host "  ✗ Upload failed" -ForegroundColor Red
    exit 1
}

# Execute deployment on server
Write-Host "`n[4/8] Connecting to server..." -ForegroundColor Yellow

$deployScript = @"
cd /home/dev
echo '=== Extracting package ==='
unzip -o $packageName -d paomi-as2-new
cd paomi-as2-new

echo '=== Stopping existing containers ==='
cd /home/dev/paomi-as2 2>/dev/null && docker-compose down || true

echo '=== Backing up old deployment ==='
cd /home/dev
mv paomi-as2 paomi-as2-backup-$timestamp 2>/dev/null || true
mv paomi-as2-new paomi-as2

echo '=== Building and starting containers ==='
cd /home/dev/paomi-as2
docker-compose build --no-cache
docker-compose up -d

echo '=== Waiting for services to start ==='
sleep 15

echo '=== Checking container status ==='
docker-compose ps

echo '=== Deployment complete ==='
"@

# Save script to temp file
$tempScript = "deploy_script_$timestamp.sh"
$deployScript | Out-File -FilePath $tempScript -Encoding ASCII

# Upload and execute script
Write-Host "`n[5/8] Uploading deployment script..." -ForegroundColor Yellow
if ($pscpPath -eq "scp") {
    scp -o StrictHostKeyChecking=no $tempScript "${Username}@${ServerIP}:/home/dev/"
} else {
    & $pscpPath -pw $Password $tempScript "${Username}@${ServerIP}:/home/dev/"
}

Write-Host "`n[6/8] Executing deployment on server..." -ForegroundColor Yellow
if ($plinkPath -eq "ssh") {
    ssh -o StrictHostKeyChecking=no "${Username}@${ServerIP}" "bash /home/dev/$tempScript"
} else {
    & $plinkPath -pw $Password "${Username}@${ServerIP}" "bash /home/dev/$tempScript"
}

# Verify deployment
Write-Host "`n[7/8] Verifying deployment..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Test endpoints
$endpoints = @{
    "Dashboard" = "http://${ServerIP}:3000"
    "P1 Admin" = "http://${ServerIP}:8001/admin/"
    "P2 Admin" = "http://${ServerIP}:8001/p2/admin/"
    "API Stats" = "http://${ServerIP}:8001/api/stats/"
}

foreach ($name in $endpoints.Keys) {
    $url = $endpoints[$name]
    try {
        $response = Invoke-WebRequest -Uri $url -TimeoutSec 5 -UseBasicParsing -ErrorAction SilentlyContinue
        if ($response.StatusCode -eq 200) {
            Write-Host "  ✓ $name is accessible" -ForegroundColor Green
        } else {
            Write-Host "  ⚠ $name returned status: $($response.StatusCode)" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "  ⚠ $name not yet accessible (may need time to start)" -ForegroundColor Yellow
    }
}

# Cleanup
Write-Host "`n[8/8] Cleaning up..." -ForegroundColor Yellow
Remove-Item $packageName -Force
Remove-Item $tempScript -Force
Write-Host "  ✓ Cleanup complete" -ForegroundColor Green

Write-Host "`n" -NoNewline
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan
Write-Host "  Deployment Complete!" -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan

Write-Host "`nAccess Points:" -ForegroundColor Yellow
Write-Host "  Dashboard:    http://${ServerIP}:3000" -ForegroundColor White
Write-Host "  P1 Admin:     http://${ServerIP}:8001/admin/" -ForegroundColor White
Write-Host "  P2 Admin:     http://${ServerIP}:8001/p2/admin/" -ForegroundColor White
Write-Host "  API:          http://${ServerIP}:8001/api/" -ForegroundColor White

Write-Host "`nCredentials:" -ForegroundColor Yellow
Write-Host "  Admin:        admin / admin123" -ForegroundColor White
Write-Host "  Database:     postgres / postgres" -ForegroundColor White

Write-Host "`nSSH Access:" -ForegroundColor Yellow
Write-Host "  ssh ${Username}@${ServerIP}" -ForegroundColor White
Write-Host "  Password: ${Password}" -ForegroundColor White

Write-Host "`nUseful Commands (on server):" -ForegroundColor Yellow
Write-Host "  cd /home/dev/paomi-as2" -ForegroundColor White
Write-Host "  docker-compose ps" -ForegroundColor White
Write-Host "  docker-compose logs -f" -ForegroundColor White
Write-Host "  docker-compose restart frontend" -ForegroundColor White

Write-Host "`nBackup Location:" -ForegroundColor Yellow
Write-Host "  /home/dev/paomi-as2-backup-$timestamp" -ForegroundColor White

Write-Host "`n" -NoNewline
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan
Write-Host ""
