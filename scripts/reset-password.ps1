# Reset admin password on remote server
$ErrorActionPreference = "Stop"

$REMOTE_HOST = "dev_192168_rsa"

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Resetting Admin Passwords" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# Copy reset script to remote
Write-Host "`nCopying reset script..." -ForegroundColor Green
scp "reset_admin_password.py" "${REMOTE_HOST}:/home/dev/paomi-as2/"

# Reset P1 password
Write-Host "`nResetting P1 admin password..." -ForegroundColor Green
ssh $REMOTE_HOST "cd /home/dev/paomi-as2 && docker exec p1-as2 python /app/reset_admin_password.py p1"

# Reset P2 password
Write-Host "`nResetting P2 admin password..." -ForegroundColor Green
ssh $REMOTE_HOST "cd /home/dev/paomi-as2 && docker exec p2-as2 python /app/reset_admin_password.py p2"

Write-Host "`n=========================================" -ForegroundColor Cyan
Write-Host "✓ Passwords Reset Successfully!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "`nLogin credentials:" -ForegroundColor Yellow
Write-Host "  Username: admin" -ForegroundColor White
Write-Host "  Password: admin123" -ForegroundColor White
Write-Host "`nAccess:" -ForegroundColor Yellow
Write-Host "  P1: http://192.168.1.200:8001/admin/" -ForegroundColor White
Write-Host "  P2: http://192.168.1.200:8001/p2/admin/" -ForegroundColor White
Write-Host ""
