# Verify pgEdge Agentic AI Setup
# PowerShell script to check if everything is configured correctly

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan
Write-Host "  pgEdge Agentic AI Setup Verification" -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan
Write-Host ""

$allGood = $true

# Check 1: Docker is running
Write-Host "[1/7] Checking Docker..." -ForegroundColor Yellow
try {
    docker ps | Out-Null
    Write-Host "  ✓ Docker is running" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Docker is not running" -ForegroundColor Red
    $allGood = $false
}

# Check 2: Containers are running
Write-Host "`n[2/7] Checking containers..." -ForegroundColor Yellow
$containers = @("pgedge-as2", "p1-as2", "p2-as2", "nginx-as2")
foreach ($container in $containers) {
    $status = docker ps --filter "name=$container" --format "{{.Status}}"
    if ($status) {
        Write-Host "  ✓ $container is running" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $container is not running" -ForegroundColor Red
        $allGood = $false
    }
}

# Check 3: PostgreSQL is accessible
Write-Host "`n[3/7] Checking PostgreSQL..." -ForegroundColor Yellow
try {
    $pgCheck = docker exec pgedge-as2 pg_isready -U postgres 2>&1
    if ($pgCheck -match "accepting connections") {
        Write-Host "  ✓ PostgreSQL is accepting connections" -ForegroundColor Green
    } else {
        Write-Host "  ✗ PostgreSQL is not ready" -ForegroundColor Red
        $allGood = $false
    }
} catch {
    Write-Host "  ✗ Cannot connect to PostgreSQL" -ForegroundColor Red
    $allGood = $false
}

# Check 4: Databases exist
Write-Host "`n[4/7] Checking databases..." -ForegroundColor Yellow
$databases = @("p1_as2_db", "p2_as2_db")
foreach ($db in $databases) {
    try {
        $dbCheck = docker exec pgedge-as2 psql -U postgres -lqt 2>&1 | Select-String $db
        if ($dbCheck) {
            Write-Host "  ✓ Database $db exists" -ForegroundColor Green
        } else {
            Write-Host "  ✗ Database $db not found" -ForegroundColor Red
            $allGood = $false
        }
    } catch {
        Write-Host "  ✗ Cannot check database $db" -ForegroundColor Red
        $allGood = $false
    }
}

# Check 5: pgEdge package installed
Write-Host "`n[5/7] Checking pgEdge Agentic AI installation..." -ForegroundColor Yellow
try {
    $p1Check = docker exec p1-as2 pip list 2>&1 | Select-String "pgedge"
    $p2Check = docker exec p2-as2 pip list 2>&1 | Select-String "pgedge"
    
    if ($p1Check) {
        Write-Host "  ✓ pgEdge installed in P1 container" -ForegroundColor Green
    } else {
        Write-Host "  ✗ pgEdge not found in P1 container" -ForegroundColor Red
        $allGood = $false
    }
    
    if ($p2Check) {
        Write-Host "  ✓ pgEdge installed in P2 container" -ForegroundColor Green
    } else {
        Write-Host "  ✗ pgEdge not found in P2 container" -ForegroundColor Red
        $allGood = $false
    }
} catch {
    Write-Host "  ✗ Cannot check pgEdge installation" -ForegroundColor Red
    $allGood = $false
}

# Check 6: Port 5432 is accessible
Write-Host "`n[6/7] Checking PostgreSQL port..." -ForegroundColor Yellow
try {
    $portCheck = docker port pgedge-as2 5432 2>&1
    if ($portCheck -match "5432") {
        Write-Host "  ✓ Port 5432 is exposed: $portCheck" -ForegroundColor Green
    } else {
        Write-Host "  ✗ Port 5432 is not exposed" -ForegroundColor Red
        $allGood = $false
    }
} catch {
    Write-Host "  ✗ Cannot check port mapping" -ForegroundColor Red
    $allGood = $false
}

# Check 7: Web interfaces accessible
Write-Host "`n[7/7] Checking web interfaces..." -ForegroundColor Yellow
try {
    $p1Response = Invoke-WebRequest -Uri "http://localhost:8001/admin/" -UseBasicParsing -TimeoutSec 5 -ErrorAction SilentlyContinue
    if ($p1Response.StatusCode -eq 200) {
        Write-Host "  ✓ P1 admin interface is accessible" -ForegroundColor Green
    } else {
        Write-Host "  ⚠ P1 admin interface returned status: $($p1Response.StatusCode)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  ⚠ Cannot reach P1 admin interface (may need login)" -ForegroundColor Yellow
}

# Summary
Write-Host "`n" -NoNewline
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan
if ($allGood) {
    Write-Host "  ✓ All checks passed!" -ForegroundColor Green
    Write-Host "=" -NoNewline -ForegroundColor Cyan
    Write-Host ("=" * 59) -ForegroundColor Cyan
    
    Write-Host "`nYou can now:" -ForegroundColor Yellow
    Write-Host "  1. Connect DBeaver to localhost:5432" -ForegroundColor White
    Write-Host "  2. Run: python pgedge_agentic_examples.py" -ForegroundColor White
    Write-Host "  3. Access P1 Admin: http://localhost:8001/admin/" -ForegroundColor White
    Write-Host "  4. Access P2 Admin: http://localhost:8001/p2/admin/" -ForegroundColor White
} else {
    Write-Host "  ✗ Some checks failed" -ForegroundColor Red
    Write-Host "=" -NoNewline -ForegroundColor Cyan
    Write-Host ("=" * 59) -ForegroundColor Cyan
    
    Write-Host "`nTroubleshooting:" -ForegroundColor Yellow
    Write-Host "  1. Run: docker-compose down" -ForegroundColor White
    Write-Host "  2. Run: .\deploy-pgedge.ps1" -ForegroundColor White
    Write-Host "  3. Check logs: docker-compose logs -f" -ForegroundColor White
}

Write-Host "`nFor detailed setup info, see:" -ForegroundColor Yellow
Write-Host "  - PGEDGE_INTEGRATION.md" -ForegroundColor White
Write-Host "  - DBEAVER_SETUP.md" -ForegroundColor White
Write-Host ""
