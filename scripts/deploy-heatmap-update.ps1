# Deploy Heatmap Update to Server
# This script deploys the new heatmap visualization feature

Write-Host "=== Deploying Heatmap Update ===" -ForegroundColor Cyan

# Server details
$server = "dev@192.168.1.200"
$remotePath = "/home/dev/paomi-as2"

Write-Host "`n1. Copying backend files..." -ForegroundColor Yellow
scp api_views.py "${server}:${remotePath}/"
scp P1/urls.py "${server}:${remotePath}/P1/"

Write-Host "`n2. Copying frontend build..." -ForegroundColor Yellow
ssh $server "mkdir -p /tmp/frontend-heatmap"
scp -r frontend/dist/* "${server}:/tmp/frontend-heatmap/"

Write-Host "`n3. Restarting backend containers..." -ForegroundColor Yellow
ssh $server "cd $remotePath && docker-compose restart p1 p2"

Write-Host "`n4. Updating frontend container..." -ForegroundColor Yellow
ssh $server "docker cp /tmp/frontend-heatmap/. as2-frontend:/usr/share/nginx/html/ && docker exec as2-frontend nginx -s reload"

Write-Host "`n5. Cleaning up..." -ForegroundColor Yellow
ssh $server "rm -rf /tmp/frontend-heatmap"

Write-Host "`n=== Deployment Complete! ===" -ForegroundColor Green
Write-Host "`nAccess your dashboard at: http://192.168.1.200:8001" -ForegroundColor Cyan
Write-Host "New features:" -ForegroundColor White
Write-Host "  - Toggle between Line Chart and Heatmap" -ForegroundColor White
Write-Host "  - D3.js Heatmap showing success/failure patterns" -ForegroundColor White
Write-Host "  - Real data from database" -ForegroundColor White
