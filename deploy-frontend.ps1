# Deploy AS2 Dashboard Frontend
# PowerShell script for Windows

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan
Write-Host "  AS2 Dashboard Frontend Deployment" -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan
Write-Host ""

# Check if Docker is running
Write-Host "[1/5] Checking Docker..." -ForegroundColor Yellow
try {
    docker ps | Out-Null
    Write-Host "  ✓ Docker is running" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Docker is not running. Please start Docker Desktop." -ForegroundColor Red
    exit 1
}

# Check if Node.js is installed
Write-Host "`n[2/5] Checking Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "  ✓ Node.js $nodeVersion installed" -ForegroundColor Green
} catch {
    Write-Host "  ⚠ Node.js not found (optional for Docker build)" -ForegroundColor Yellow
}

# Build frontend Docker image
Write-Host "`n[3/5] Building frontend Docker image..." -ForegroundColor Yellow
docker-compose build frontend
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ✗ Build failed" -ForegroundColor Red
    exit 1
}
Write-Host "  ✓ Frontend image built successfully" -ForegroundColor Green

# Start frontend container
Write-Host "`n[4/5] Starting frontend container..." -ForegroundColor Yellow
docker-compose up -d frontend
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ✗ Failed to start container" -ForegroundColor Red
    exit 1
}
Write-Host "  ✓ Frontend container started" -ForegroundColor Green

# Wait for frontend to be ready
Write-Host "`n[5/5] Waiting for frontend to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Check container status
$status = docker ps --filter "name=as2-frontend" --format "{{.Status}}"
if ($status) {
    Write-Host "  ✓ Frontend is running" -ForegroundColor Green
} else {
    Write-Host "  ✗ Frontend container not running" -ForegroundColor Red
    Write-Host "`nChecking logs..." -ForegroundColor Yellow
    docker logs as2-frontend
    exit 1
}

Write-Host "`n" -NoNewline
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan
Write-Host "  Deployment Complete!" -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan

Write-Host "`nAccess Points:" -ForegroundColor Yellow
Write-Host "  Dashboard:    http://localhost:3000" -ForegroundColor White
Write-Host "  P1 Admin:     http://localhost:8001/admin/" -ForegroundColor White
Write-Host "  P2 Admin:     http://localhost:8001/p2/admin/" -ForegroundColor White

Write-Host "`nAPI Endpoints:" -ForegroundColor Yellow
Write-Host "  Partners:     http://localhost:8001/api/partners/" -ForegroundColor White
Write-Host "  Keys:         http://localhost:8001/api/keys/" -ForegroundColor White
Write-Host "  Messages:     http://localhost:8001/api/messages/" -ForegroundColor White
Write-Host "  Stats:        http://localhost:8001/api/stats/" -ForegroundColor White

Write-Host "`nUseful Commands:" -ForegroundColor Yellow
Write-Host "  View logs:    docker logs as2-frontend -f" -ForegroundColor White
Write-Host "  Restart:      docker-compose restart frontend" -ForegroundColor White
Write-Host "  Stop:         docker-compose stop frontend" -ForegroundColor White
Write-Host "  Rebuild:      docker-compose build --no-cache frontend" -ForegroundColor White

Write-Host "`n" -NoNewline
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan
Write-Host ""
