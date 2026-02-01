# Deploy AS2 Servers with pgEdge Agentic AI Toolkit
# PowerShell script for Windows

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan
Write-Host "  AS2 Docker Deployment with pgEdge Agentic AI" -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan
Write-Host ""

# Check if Docker is running
Write-Host "[1/6] Checking Docker..." -ForegroundColor Yellow
try {
    docker ps | Out-Null
    Write-Host "  ✓ Docker is running" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Docker is not running. Please start Docker Desktop." -ForegroundColor Red
    exit 1
}

# Stop existing containers
Write-Host "`n[2/6] Stopping existing containers..." -ForegroundColor Yellow
docker-compose down
Write-Host "  ✓ Containers stopped" -ForegroundColor Green

# Remove old images to force rebuild
Write-Host "`n[3/6] Removing old images..." -ForegroundColor Yellow
docker-compose rm -f
Write-Host "  ✓ Old images removed" -ForegroundColor Green

# Build new images with pgEdge
Write-Host "`n[4/6] Building Docker images with pgEdge Agentic AI..." -ForegroundColor Yellow
docker-compose build --no-cache
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ✗ Build failed" -ForegroundColor Red
    exit 1
}
Write-Host "  ✓ Images built successfully" -ForegroundColor Green

# Start containers
Write-Host "`n[5/6] Starting containers..." -ForegroundColor Yellow
docker-compose up -d
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ✗ Failed to start containers" -ForegroundColor Red
    exit 1
}
Write-Host "  ✓ Containers started" -ForegroundColor Green

# Wait for services to be ready
Write-Host "`n[6/6] Waiting for services to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Check container status
Write-Host "`nContainer Status:" -ForegroundColor Cyan
docker-compose ps

# Display connection information
Write-Host "`n" -NoNewline
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan
Write-Host "  Deployment Complete!" -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan

Write-Host "`nAS2 Server URLs:" -ForegroundColor Yellow
Write-Host "  P1 Admin: http://localhost:8001/admin/" -ForegroundColor White
Write-Host "  P2 Admin: http://localhost:8001/p2/admin/" -ForegroundColor White

Write-Host "`nDBeaver Connection:" -ForegroundColor Yellow
Write-Host "  Host:     localhost" -ForegroundColor White
Write-Host "  Port:     5432" -ForegroundColor White
Write-Host "  User:     postgres" -ForegroundColor White
Write-Host "  Password: postgres" -ForegroundColor White
Write-Host "  Databases:" -ForegroundColor White
Write-Host "    - postgres (default)" -ForegroundColor Gray
Write-Host "    - p1_as2_db (P1 data)" -ForegroundColor Gray
Write-Host "    - p2_as2_db (P2 data)" -ForegroundColor Gray

Write-Host "`nNext Steps:" -ForegroundColor Yellow
Write-Host "  1. Open DBeaver and connect using the credentials above" -ForegroundColor White
Write-Host "  2. See DBEAVER_SETUP.md for detailed connection guide" -ForegroundColor White
Write-Host "  3. Run pgedge_agentic_examples.py to test AI queries" -ForegroundColor White

Write-Host "`nUseful Commands:" -ForegroundColor Yellow
Write-Host "  View logs:    docker-compose logs -f" -ForegroundColor White
Write-Host "  Stop all:     docker-compose down" -ForegroundColor White
Write-Host "  Restart:      docker-compose restart" -ForegroundColor White

Write-Host "`n" -NoNewline
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan
Write-Host ""
