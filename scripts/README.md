# Scripts Directory

All PowerShell and shell scripts for deployment, testing, and utilities.

## 📁 Script Categories

### 🚀 Deployment Scripts

#### Main Deployment
- **`deploy-to-192.168.1.200.ps1`** - Deploy entire system to production server
  ```powershell
  .\deploy-to-192.168.1.200.ps1
  ```

- **`deploy-and-test.ps1`** - Deploy and run integration tests
  ```powershell
  .\deploy-and-test.ps1
  ```

#### Specialized Deployment
- **`deploy-frontend.ps1`** - Deploy frontend only
- **`deploy-windows.ps1`** - Deploy from Windows
- **`deploy-pgedge.ps1`** - Deploy with pgEdge database
- **`deploy-heatmap-update.ps1`** - Deploy heatmap updates

#### Shell Scripts (Linux/Mac)
- **`deploy.sh`** - Main deployment script
- **`deploy-remote.sh`** - Remote deployment
- **`deploy-simple.sh`** - Simple deployment
- **`deploy-final.sh`** - Final deployment
- **`quick-redeploy.sh`** - Quick redeploy

---

### 🧪 Testing Scripts

- **`run-unittest.ps1`** - Run unit tests (mock-based)
  ```powershell
  .\run-unittest.ps1
  
  # Options
  .\run-unittest.ps1 -Send      # Send tests only
  .\run-unittest.ps1 -Receive   # Receive tests only
  ```

- **`run-integration-test.ps1`** - Run integration tests (remote API)
  ```powershell
  .\run-integration-test.ps1
  ```

- **`run-server-integration-test.ps1`** - Run integration tests on server
  ```powershell
  .\run-server-integration-test.ps1
  ```

---

### 🔧 Utility Scripts

#### Password Management
- **`reset-password.ps1`** - Reset admin password
  ```powershell
  .\reset-password.ps1
  ```

#### Database
- **`verify_pgedge_setup.ps1`** - Verify pgEdge database setup
  ```powershell
  .\verify_pgedge_setup.ps1
  ```

- **`init-db.sh`** - Initialize database (Linux/Mac)

#### Certificates
- **`show-key-upload-guide.ps1`** - Show certificate upload guide
  ```powershell
  .\show-key-upload-guide.ps1
  ```

#### Server Management
- **`start-local.sh`** - Start local servers (Linux/Mac)

---

## 📝 Usage Examples

### Deploy to Production
```powershell
# Full deployment
.\deploy-to-192.168.1.200.ps1

# Deploy and verify with tests
.\deploy-and-test.ps1
```

### Run Tests
```powershell
# Unit tests (fast, mock-based)
.\run-unittest.ps1

# Integration tests (real messages)
.\deploy-and-test.ps1
```

### Manage System
```powershell
# Reset admin password
.\reset-password.ps1

# Verify database
.\verify_pgedge_setup.ps1

# Show certificate guide
.\show-key-upload-guide.ps1
```

---

## ⚙️ Script Parameters

### deploy-to-192.168.1.200.ps1
```powershell
.\deploy-to-192.168.1.200.ps1 `
    -ServerIP "192.168.1.200" `
    -Username "dev" `
    -Password "dev@2025"
```

### run-unittest.ps1
```powershell
.\run-unittest.ps1 -Send      # Send tests only
.\run-unittest.ps1 -Receive   # Receive tests only
.\run-unittest.ps1 -Coverage  # With coverage report
```

### run-integration-test.ps1
```powershell
.\run-integration-test.ps1 -ServerUrl "http://192.168.1.200:8001"
```

---

## 🔐 Security Notes

- Scripts contain server credentials (dev/dev@2025)
- Change default passwords in production
- Use SSH keys instead of passwords when possible
- Keep scripts in secure locations

---

## 🐛 Troubleshooting

### Script execution policy error
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Cannot find script
```powershell
# Make sure you're in the scripts directory
cd scripts
.\script-name.ps1
```

### SSH/SCP not found
- Install PuTTY (includes plink and pscp)
- Or use WSL/Git Bash for Linux commands

---

## 📚 Related Documentation

- [Main README](../README.md)
- [Deployment Guide](../docs/DEPLOYMENT.md)
- [Testing Guide](../docs/TESTING_SUMMARY.md)
- [Quick Start](../docs/QUICK_START.md)

---

**Note**: All paths in scripts are relative to the project root. Run scripts from the `scripts/` directory.
