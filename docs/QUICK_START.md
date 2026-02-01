# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Deploy to Server
```powershell
cd scripts
.\deploy-to-192.168.1.200.ps1
```

### 2. Access the Dashboard
Open your browser:
- **Dashboard**: http://192.168.1.200:8001/
- **Admin**: http://192.168.1.200:8001/admin/
  - Username: `admin`
  - Password: (set during deployment)

### 3. Send Test Messages
```powershell
cd scripts
.\deploy-and-test.ps1
```

This will:
- Deploy the latest code
- Send 5 test AS2 messages
- Verify they appear in the dashboard

### 4. Verify Results
Check the dashboard:
- Message count should increase
- Charts should show data
- Messages page should list sent messages

---

## 📁 Project Organization

```
paomi-as2/
├── docs/       # 📚 All documentation
├── scripts/    # 🔧 PowerShell and shell scripts
├── unittest/   # 🧪 All test files
├── frontend/   # 🎨 React dashboard
└── P1/         # 🚀 Django AS2 server
```

---

## 🔧 Common Commands

### Deployment
```powershell
# Deploy everything
cd scripts
.\deploy-to-192.168.1.200.ps1

# Deploy frontend only
.\deploy-frontend.ps1

# Deploy and test
.\deploy-and-test.ps1
```

### Testing
```powershell
# Run unit tests (fast, mock-based)
cd scripts
.\run-unittest.ps1

# Run integration tests (real messages)
.\deploy-and-test.ps1
```

### Utilities
```powershell
# Reset admin password
cd scripts
.\reset-password.ps1

# Verify database setup
.\verify_pgedge_setup.ps1

# Show certificate upload guide
.\show-key-upload-guide.ps1
```

---

## 📚 Documentation Index

### Getting Started
- [README](../README.md) - Project overview
- [Setup Guide](SETUP_GUIDE.md) - Detailed setup
- [Deployment Guide](DEPLOYMENT.md) - Deployment instructions

### Features
- [Dashboard Guide](DASHBOARD_QUICK_START.md) - Using the dashboard
- [Authentication](AUTHENTICATION_GUIDE.md) - User login/register
- [Heatmap Feature](HEATMAP_FEATURE.md) - Message visualization

### Testing
- [Testing Summary](TESTING_SUMMARY.md) - Testing overview
- [Unit Tests](UNITTEST_GUIDE.md) - Mock-based tests
- [Integration Tests](INTEGRATION_TEST_GUIDE.md) - Real message tests

### Configuration
- [pgEdge Setup](PGEDGE_INTEGRATION.md) - Database configuration
- [DBeaver Setup](DBEAVER_SETUP.md) - Database client
- [Private Keys](PRIVATE_KEY_TROUBLESHOOTING.md) - Certificate management

---

## ⚠️ Important Notes

### Unit Tests vs Integration Tests

**Unit Tests** (Mock-based):
- ❌ Do NOT send real messages
- ❌ Do NOT increase message counts
- ✅ Fast (< 1 second)
- ✅ Test logic in isolation

**Integration Tests** (Real system):
- ✅ DO send real messages
- ✅ DO increase message counts
- ✅ Verify end-to-end functionality
- ⏱️ Slower (5-10 seconds)

**To see message counts increase in Admin/UI, run integration tests!**

---

## 🎯 Quick Troubleshooting

### Messages not appearing?
1. Run integration tests: `.\deploy-and-test.ps1`
2. Check Docker: `docker ps`
3. Check logs: `docker logs paomi-as2-p1-1`

### Cannot access dashboard?
1. Verify server is running: http://192.168.1.200:8001/
2. Check Docker containers: `docker ps`
3. Restart: `docker-compose restart`

### Certificate upload fails?
1. Leave "Private Key Password" field EMPTY
2. Keys are NOT encrypted
3. See [Private Key Guide](PRIVATE_KEY_TROUBLESHOOTING.md)

---

## 📞 Need Help?

1. Check [documentation](.) for detailed guides
2. Review [troubleshooting guides](PRIVATE_KEY_TROUBLESHOOTING.md)
3. Check Docker logs for errors
4. Verify network connectivity

---

**Happy AS2 messaging! 🚀**
