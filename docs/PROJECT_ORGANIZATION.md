# Project Organization

The PaomiAS2 project has been reorganized for better maintainability and clarity.

## 📁 New Structure

```
paomi-as2/
├── 📚 docs/                    # All documentation files
│   ├── README.md              # Main documentation (moved from root)
│   ├── QUICK_START.md         # Quick start guide
│   ├── DEPLOYMENT.md          # Deployment instructions
│   ├── TESTING_SUMMARY.md     # Testing overview
│   ├── UNITTEST_GUIDE.md      # Unit test guide
│   ├── INTEGRATION_TEST_GUIDE.md  # Integration test guide
│   ├── AUTHENTICATION_GUIDE.md    # Auth documentation
│   ├── DASHBOARD_QUICK_START.md   # Dashboard guide
│   ├── HEATMAP_FEATURE.md         # Heatmap documentation
│   ├── PGEDGE_INTEGRATION.md      # Database setup
│   ├── DBEAVER_SETUP.md           # Database client
│   ├── PRIVATE_KEY_TROUBLESHOOTING.md  # Certificate guide
│   └── ... (30+ documentation files)
│
├── 🔧 scripts/                # All PowerShell and shell scripts
│   ├── README.md              # Scripts documentation
│   ├── deploy-to-192.168.1.200.ps1  # Main deployment
│   ├── deploy-and-test.ps1          # Deploy and test
│   ├── run-unittest.ps1             # Run unit tests
│   ├── run-integration-test.ps1     # Run integration tests
│   ├── reset-password.ps1           # Reset admin password
│   ├── verify_pgedge_setup.ps1      # Verify database
│   ├── deploy.sh                    # Linux deployment
│   └── ... (20+ scripts)
│
├── 🧪 unittest/               # All test files
│   ├── README.md              # Test documentation
│   ├── test_as2_send.py       # Send API tests (17 tests)
│   ├── test_as2_receive.py    # Receive API tests (20 tests)
│   ├── test_real_as2_integration.py  # Real integration tests
│   ├── test_send_messages_to_server.py  # Server tests
│   ├── run_tests.py           # Test runner
│   └── ... (10+ test files)
│
├── 🎨 frontend/               # React dashboard
│   ├── src/                   # React source code
│   ├── dist/                  # Built frontend
│   ├── package.json           # Dependencies
│   └── vite.config.js         # Build configuration
│
├── 🚀 P1/                     # Django AS2 server P1
│   ├── settings.py            # Django settings
│   ├── urls.py                # URL routing
│   └── ...
│
├── 🚀 P2/                     # Django AS2 server P2
│   └── ...
│
├── 🔐 Certs/                  # SSL/TLS certificates
│   └── Cert1/
│
├── 📄 Root Files
│   ├── README.md              # Main project README (NEW!)
│   ├── docker-compose.yml     # Docker configuration
│   ├── Dockerfile             # Docker image
│   ├── api_views.py           # REST API endpoints
│   ├── manage.py              # Django management
│   └── nginx.conf             # Nginx configuration
```

---

## 🎯 Benefits of New Organization

### 1. Clear Separation of Concerns
- **Documentation** → `docs/`
- **Scripts** → `scripts/`
- **Tests** → `unittest/`
- **Code** → Root and subdirectories

### 2. Easier Navigation
- All docs in one place
- All scripts in one place
- All tests in one place

### 3. Better Discoverability
- README files in each directory
- Clear naming conventions
- Logical grouping

### 4. Improved Maintainability
- Easy to find files
- Clear purpose for each directory
- Reduced clutter in root

---

## 📝 File Locations

### Documentation Files (docs/)
All `.md` and `.txt` files moved to `docs/`:
- Guides and tutorials
- API documentation
- Troubleshooting guides
- Feature documentation
- Deployment instructions

### Script Files (scripts/)
All `.ps1` and `.sh` files moved to `scripts/`:
- Deployment scripts
- Testing scripts
- Utility scripts
- Setup scripts

### Test Files (unittest/)
All `test_*.py` files moved to `unittest/`:
- Unit tests
- Integration tests
- Setup tests
- File transfer tests

---

## 🚀 Updated Commands

### Before (Old Structure)
```powershell
# From root
.\run-unittest.ps1
.\deploy-to-192.168.1.200.ps1
python test_real_as2_integration.py
```

### After (New Structure)
```powershell
# From root
cd scripts
.\run-unittest.ps1
.\deploy-to-192.168.1.200.ps1

cd ../unittest
python test_real_as2_integration.py
```

Or use the convenience script:
```powershell
# From root
cd scripts
.\deploy-and-test.ps1  # Handles paths automatically
```

---

## 📚 Quick Reference

### Deploy to Server
```powershell
cd scripts
.\deploy-to-192.168.1.200.ps1
```

### Run Tests
```powershell
# Unit tests
cd scripts
.\run-unittest.ps1

# Integration tests
.\deploy-and-test.ps1
```

### Access Documentation
```powershell
# Open docs folder
cd docs

# View main README
cat README.md

# View quick start
cat QUICK_START.md
```

---

## 🔄 Migration Notes

### What Changed
1. ✅ All `.md` files → `docs/`
2. ✅ All `.txt` files → `docs/`
3. ✅ All `.ps1` files → `scripts/`
4. ✅ All `.sh` files → `scripts/`
5. ✅ All `test_*.py` files → `unittest/`
6. ✅ New README.md in root
7. ✅ README.md in each directory

### What Stayed the Same
- Python source files (`.py`) in root
- Docker files in root
- Configuration files in root
- Frontend directory structure
- P1/P2 directory structure
- Certs directory structure

---

## 📖 Documentation Index

### Getting Started
- [Main README](../README.md)
- [Quick Start](QUICK_START.md)
- [Setup Guide](SETUP_GUIDE.md)

### Deployment
- [Deployment Guide](DEPLOYMENT.md)
- [Docker Guide](README_DOCKER.md)
- [Deployment Success](DEPLOYMENT_SUCCESS.md)

### Features
- [Dashboard Guide](DASHBOARD_QUICK_START.md)
- [Authentication](AUTHENTICATION_GUIDE.md)
- [Heatmap Feature](HEATMAP_FEATURE.md)

### Testing
- [Testing Summary](TESTING_SUMMARY.md)
- [Unit Tests](UNITTEST_GUIDE.md)
- [Integration Tests](INTEGRATION_TEST_GUIDE.md)

### Configuration
- [pgEdge Setup](PGEDGE_INTEGRATION.md)
- [DBeaver Setup](DBEAVER_SETUP.md)
- [Private Keys](PRIVATE_KEY_TROUBLESHOOTING.md)

---

## ✅ Checklist for New Users

- [ ] Read [Main README](../README.md)
- [ ] Follow [Quick Start](QUICK_START.md)
- [ ] Deploy using [scripts/deploy-to-192.168.1.200.ps1](../scripts/deploy-to-192.168.1.200.ps1)
- [ ] Run tests using [scripts/deploy-and-test.ps1](../scripts/deploy-and-test.ps1)
- [ ] Access dashboard at http://192.168.1.200:8001/
- [ ] Review [Testing Summary](TESTING_SUMMARY.md)

---

**The project is now better organized and easier to navigate! 🎉**
