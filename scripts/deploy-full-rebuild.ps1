# Full Rebuild and Deploy
# Uploads source code and rebuilds everything on the server

param(
    [string]$ServerIP = "192.168.1.200",
    [string]$Username = "dev",
    [string]$Password = "dev@2025"
)

Write-Host "=== Full Rebuild and Deploy ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "This will:" -ForegroundColor Yellow
Write-Host "  1. Upload all source code to server" -ForegroundColor White
Write-Host "  2. Rebuild Docker images on server" -ForegroundColor White
Write-Host "  3. Restart all containers" -ForegroundColor White
Write-Host ""

$continue = Read-Host "Continue? (y/n)"
if ($continue -ne 'y') {
    Write-Host "Cancelled" -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "[1/5] Creating deployment package..." -ForegroundColor Cyan

# Create tar.gz excluding unnecessary files
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$packageName = "as2-full-$timestamp.tar.gz"

tar -czf $packageName `
    --exclude=node_modules `
    --exclude=dist `
    --exclude=.git `
    --exclude=__pycache__ `
    --exclude=*.pyc `
    --exclude=*.tar.gz `
    -C .. `
    paomi-as2

if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Failed to create package" -ForegroundColor Red
    exit 1
}

Write-Host "  ✓ Package created: $packageName" -ForegroundColor Green
Write-Host ""

Write-Host "[2/5] Uploading to server..." -ForegroundColor Cyan
pscp -pw $Password $packageName ${Username}@${ServerIP}:/home/${Username}/

if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Upload failed" -ForegroundColor Red
    Remove-Item $packageName
    exit 1
}

Write-Host "  ✓ Upload complete" -ForegroundColor Green
Write-Host ""

Write-Host "[3/5] Extracting and preparing..." -ForegroundColor Cyan
plink -batch -pw $Password ${Username}@${ServerIP} @"
cd /home/${Username}
tar -xzf $packageName
cd paomi-as2
"@

Write-Host "  ✓ Files extracted" -ForegroundColor Green
Write-Host ""

Write-Host "[4/5] Rebuilding containers (this may take 5-10 minutes)..." -ForegroundColor Cyan
plink -batch -pw $Password ${Username}@${ServerIP} @"
cd /home/${Username}/paomi-as2
docker-compose down
docker-compose build --no-cache
docker-compose up -d
"@

Write-Host "  ✓ Containers rebuilt and started" -ForegroundColor Green
Write-Host ""

Write-Host "[5/5] Waiting for services to start..." -ForegroundColor Cyan
Start-Sleep -Seconds 15
Write-Host "  ✓ Services should be ready" -ForegroundColor Green
Write-Host ""

# Cleanup
Remove-Item $packageName

Write-Host "=== Deployment Complete ===" -ForegroundColor Green
Write-Host ""
Write-Host "Access the dashboard:" -ForegroundColor Cyan
Write-Host "  http://${ServerIP}:8001/" -ForegroundColor White
Write-Host ""
Write-Host "Features:" -ForegroundColor Cyan
Write-Host "  ✓ Real-time data from API" -ForegroundColor White
Write-Host "  ✓ Line chart (sent/received/failed)" -ForegroundColor White
Write-Host "  ✓ Heatmap with 5 granularities" -ForegroundColor White
Write-Host "  ✓ Messages, Partners, Keys pages" -ForegroundColor White
Write-Host ""
Write-Host "If you see old UI:" -ForegroundColor Yellow
Write-Host "  1. Hard refresh: Ctrl+F5" -ForegroundColor White
Write-Host "  2. Clear browser cache" -ForegroundColor White
Write-Host "  3. Open in incognito window" -ForegroundColor White
Write-Host ""
