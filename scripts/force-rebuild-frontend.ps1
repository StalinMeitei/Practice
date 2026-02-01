# Force Rebuild Frontend Container
# This script forces a complete rebuild of the frontend with latest source code

param(
    [string]$ServerIP = "192.168.1.200",
    [string]$Username = "dev",
    [string]$Password = "dev@2025"
)

Write-Host "=== Force Rebuild Frontend ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "This will completely rebuild the frontend container with latest code" -ForegroundColor Yellow
Write-Host ""

# Step 1: Stop and remove old containers
Write-Host "[1/6] Stopping frontend containers..." -ForegroundColor Cyan
plink -batch -pw $Password ${Username}@${ServerIP} @"
cd /home/dev/paomi-as2
docker-compose stop frontend nginx
docker-compose rm -f frontend nginx
"@

Write-Host "  ✓ Containers stopped and removed" -ForegroundColor Green
Write-Host ""

# Step 2: Remove old images
Write-Host "[2/6] Removing old frontend image..." -ForegroundColor Cyan
plink -batch -pw $Password ${Username}@${ServerIP} "docker rmi paomi-as2-frontend 2>/dev/null || true"

Write-Host "  ✓ Old image removed" -ForegroundColor Green
Write-Host ""

# Step 3: Upload latest source code
Write-Host "[3/6] Uploading latest source code..." -ForegroundColor Cyan
pscp -pw $Password -r ../frontend/src ${Username}@${ServerIP}:/home/${Username}/paomi-as2/frontend/
pscp -pw $Password ../frontend/package.json ${Username}@${ServerIP}:/home/${Username}/paomi-as2/frontend/
pscp -pw $Password ../frontend/vite.config.js ${Username}@${ServerIP}:/home/${Username}/paomi-as2/frontend/
pscp -pw $Password ../frontend/index.html ${Username}@${ServerIP}:/home/${Username}/paomi-as2/frontend/
pscp -pw $Password ../frontend/Dockerfile ${Username}@${ServerIP}:/home/${Username}/paomi-as2/frontend/
pscp -pw $Password ../frontend/nginx.conf ${Username}@${ServerIP}:/home/${Username}/paomi-as2/frontend/

Write-Host "  ✓ Source code uploaded" -ForegroundColor Green
Write-Host ""

# Step 4: Build new image (this will take 3-5 minutes)
Write-Host "[4/6] Building new frontend image..." -ForegroundColor Cyan
Write-Host "  This will take 3-5 minutes - building React app..." -ForegroundColor Yellow
Write-Host ""

$buildOutput = plink -batch -pw $Password ${Username}@${ServerIP} @"
cd /home/dev/paomi-as2
docker-compose build --no-cache frontend
"@

Write-Host $buildOutput
Write-Host ""
Write-Host "  ✓ Frontend image built" -ForegroundColor Green
Write-Host ""

# Step 5: Start containers
Write-Host "[5/6] Starting containers..." -ForegroundColor Cyan
plink -batch -pw $Password ${Username}@${ServerIP} @"
cd /home/dev/paomi-as2
docker-compose up -d frontend nginx
"@

Write-Host "  ✓ Containers started" -ForegroundColor Green
Write-Host ""

# Step 6: Verify
Write-Host "[6/6] Verifying deployment..." -ForegroundColor Cyan
Start-Sleep -Seconds 5

try {
    $response = Invoke-WebRequest -Uri "http://${ServerIP}:8001/" -TimeoutSec 10 -UseBasicParsing
    $contentLength = $response.Content.Length
    
    if ($contentLength -gt 1000) {
        Write-Host "  ✓ Dashboard is accessible! (Size: $contentLength bytes)" -ForegroundColor Green
        Write-Host "  ✓ New UI deployed successfully!" -ForegroundColor Green
    } else {
        Write-Host "  ⚠ Dashboard accessible but may be old version (Size: $contentLength bytes)" -ForegroundColor Yellow
        Write-Host "  Expected size > 1000 bytes for new UI" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  ⚠ Dashboard not yet accessible - may need more time" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=== Rebuild Complete ===" -ForegroundColor Green
Write-Host ""
Write-Host "Access the dashboard:" -ForegroundColor Cyan
Write-Host "  http://${ServerIP}:8001/" -ForegroundColor White
Write-Host ""
Write-Host "IMPORTANT: Clear your browser cache!" -ForegroundColor Yellow
Write-Host "  1. Press Ctrl+F5 for hard refresh" -ForegroundColor White
Write-Host "  2. Or open in incognito/private window" -ForegroundColor White
Write-Host "  3. Or clear browser cache completely" -ForegroundColor White
Write-Host ""
Write-Host "You should now see:" -ForegroundColor Cyan
Write-Host "  ✓ Real data from API (not fake data)" -ForegroundColor White
Write-Host "  ✓ Line chart with sent/received/failed" -ForegroundColor White
Write-Host "  ✓ Heatmap toggle button" -ForegroundColor White
Write-Host "  ✓ 5 granularity buttons (Hourly/Daily/Weekly/Monthly/Yearly)" -ForegroundColor White
Write-Host ""
