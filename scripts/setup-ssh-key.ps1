# Setup Passwordless SSH to 192.168.1.200
# This script generates SSH keys and copies them to the server

param(
    [string]$ServerIP = "192.168.1.200",
    [string]$Username = "dev",
    [string]$Password = "dev@2025"
)

Write-Host "=== Setup Passwordless SSH ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Server: $ServerIP" -ForegroundColor Yellow
Write-Host "Username: $Username" -ForegroundColor Yellow
Write-Host ""

# Check if .ssh directory exists
$sshDir = "$env:USERPROFILE\.ssh"
if (-not (Test-Path $sshDir)) {
    Write-Host "[1/4] Creating .ssh directory..." -ForegroundColor Cyan
    New-Item -ItemType Directory -Path $sshDir -Force | Out-Null
    Write-Host "  ✓ Directory created" -ForegroundColor Green
} else {
    Write-Host "[1/4] .ssh directory exists" -ForegroundColor Cyan
    Write-Host "  ✓ Directory found" -ForegroundColor Green
}
Write-Host ""

# Check if SSH key already exists
$keyPath = "$sshDir\id_rsa"
if (Test-Path $keyPath) {
    Write-Host "[2/4] SSH key already exists" -ForegroundColor Cyan
    Write-Host "  ✓ Using existing key: $keyPath" -ForegroundColor Green
    $useExisting = Read-Host "Use existing key? (y/n)"
    if ($useExisting -ne 'y') {
        Write-Host "  Generating new key..." -ForegroundColor Yellow
        ssh-keygen -t rsa -b 4096 -f $keyPath -N '""' -C "paomi-as2-deployment"
    }
} else {
    Write-Host "[2/4] Generating SSH key..." -ForegroundColor Cyan
    ssh-keygen -t rsa -b 4096 -f $keyPath -N '""' -C "paomi-as2-deployment"
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ SSH key generated" -ForegroundColor Green
    } else {
        Write-Host "  ✗ Failed to generate SSH key" -ForegroundColor Red
        exit 1
    }
}
Write-Host ""

# Copy public key to server
Write-Host "[3/4] Copying public key to server..." -ForegroundColor Cyan
Write-Host "  Password will be required one last time: $Password" -ForegroundColor Yellow
Write-Host ""

# Read the public key
$publicKey = Get-Content "$keyPath.pub"

# Create a temporary script to add the key
$tempScript = @"
mkdir -p ~/.ssh
chmod 700 ~/.ssh
echo '$publicKey' >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
echo 'SSH key added successfully'
"@

# Execute the script on the server
$tempScriptPath = "$env:TEMP\add_ssh_key.sh"
$tempScript | Out-File -FilePath $tempScriptPath -Encoding ASCII

# Upload and execute the script
Write-Host "  Uploading key..." -ForegroundColor Yellow
pscp -pw $Password $tempScriptPath ${Username}@${ServerIP}:/tmp/add_ssh_key.sh

if ($LASTEXITCODE -eq 0) {
    Write-Host "  Executing on server..." -ForegroundColor Yellow
    plink -batch -pw $Password ${Username}@${ServerIP} "bash /tmp/add_ssh_key.sh && rm /tmp/add_ssh_key.sh"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ Public key copied to server" -ForegroundColor Green
    } else {
        Write-Host "  ✗ Failed to add key to server" -ForegroundColor Red
        Remove-Item $tempScriptPath
        exit 1
    }
} else {
    Write-Host "  ✗ Failed to upload key" -ForegroundColor Red
    Remove-Item $tempScriptPath
    exit 1
}

Remove-Item $tempScriptPath
Write-Host ""

# Test passwordless connection
Write-Host "[4/4] Testing passwordless connection..." -ForegroundColor Cyan
$testResult = plink -batch ${Username}@${ServerIP} "echo 'Connection successful'"

if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Passwordless SSH is working!" -ForegroundColor Green
} else {
    Write-Host "  ⚠ Connection test failed, but key may be installed" -ForegroundColor Yellow
    Write-Host "  Try manually: ssh ${Username}@${ServerIP}" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=== Setup Complete ===" -ForegroundColor Green
Write-Host ""
Write-Host "SSH Key Location:" -ForegroundColor Cyan
Write-Host "  Private: $keyPath" -ForegroundColor White
Write-Host "  Public: $keyPath.pub" -ForegroundColor White
Write-Host ""
Write-Host "Test Connection:" -ForegroundColor Cyan
Write-Host "  ssh ${Username}@${ServerIP}" -ForegroundColor White
Write-Host "  plink ${Username}@${ServerIP}" -ForegroundColor White
Write-Host ""
Write-Host "Now you can deploy without password:" -ForegroundColor Cyan
Write-Host "  cd scripts" -ForegroundColor White
Write-Host "  .\deploy-to-192.168.1.200.ps1" -ForegroundColor White
Write-Host ""
