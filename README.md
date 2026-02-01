# PaomiAS2 - AS2 Message Exchange System

A comprehensive AS2 (Applicability Statement 2) message exchange system with a modern React dashboard, built with Django and PostgreSQL.

## 📁 Project Structure

```
paomi-as2/
├── docs/                    # All documentation files
│   ├── README.md           # Main documentation
│   ├── QUICK_REFERENCE.md  # Quick start guide
│   ├── DEPLOYMENT.md       # Deployment instructions
│   ├── TESTING_SUMMARY.md  # Testing guide
│   └── ...                 # Other guides
├── scripts/                # PowerShell and shell scripts
│   ├── deploy-to-192.168.1.200.ps1  # Main deployment script
│   ├── run-unittest.ps1             # Run unit tests
│   ├── deploy-and-test.ps1          # Deploy and test
│   └── ...                          # Other scripts
├── unittest/               # All test files
│   ├── test_as2_send.py              # Send API tests
│   ├── test_as2_receive.py           # Receive API tests
│   ├── test_real_as2_integration.py  # Real integration tests
│   └── ...                           # Other tests
├── frontend/               # React dashboard
│   ├── src/               # React source code
│   └── dist/              # Built frontend
├── P1/                    # Django AS2 server P1
├── P2/                    # Django AS2 server P2
├── Certs/                 # SSL/TLS certificates
├── api_views.py           # REST API endpoints
├── docker-compose.yml     # Docker configuration
└── Dockerfile             # Docker image definition
```

## 🚀 Quick Start

### 1. Deploy to Server
```powershell
cd scripts
.\deploy-to-192.168.1.200.ps1
```

### 2. Access the System
- **Dashboard**: http://192.168.1.200:8001/
- **Admin Panel**: http://192.168.1.200:8001/admin/
- **API Docs**: See `docs/API_REFERENCE.md`

### 3. Run Tests
```powershell
# Unit tests (mock-based)
cd scripts
.\run-unittest.ps1

# Integration tests (real messages)
.\deploy-and-test.ps1
```

## 📚 Documentation

All documentation is in the `docs/` folder:

### Getting Started
- [Quick Reference](docs/QUICK_REFERENCE.md) - Quick start guide
- [Setup Guide](docs/SETUP_GUIDE.md) - Detailed setup instructions
- [Deployment Guide](docs/DEPLOYMENT.md) - Deployment instructions

### Features
- [Dashboard Guide](docs/DASHBOARD_QUICK_START.md) - Using the dashboard
- [Authentication Guide](docs/AUTHENTICATION_GUIDE.md) - User authentication
- [Heatmap Feature](docs/HEATMAP_FEATURE.md) - Message heatmap visualization

### Testing
- [Testing Summary](docs/TESTING_SUMMARY.md) - Overview of testing
- [Unit Test Guide](docs/UNITTEST_GUIDE.md) - Running unit tests
- [Integration Test Guide](docs/INTEGRATION_TEST_GUIDE.md) - Running integration tests

### Configuration
- [pgEdge Integration](docs/PGEDGE_INTEGRATION.md) - PostgreSQL setup
- [DBeaver Setup](docs/DBEAVER_SETUP.md) - Database client setup
- [Private Key Guide](docs/PRIVATE_KEY_TROUBLESHOOTING.md) - Certificate management

## 🧪 Testing

### Unit Tests (Mock-based)
Fast tests that validate logic without touching the database:
```powershell
cd scripts
.\run-unittest.ps1
```
- 37 tests covering send/receive APIs
- Execution time: < 1 second
- Does NOT increase message counts

### Integration Tests (Real System)
Tests that send actual AS2 messages:
```powershell
cd scripts
.\deploy-and-test.ps1
```
- Sends real messages to the server
- Verifies database updates
- DOES increase message counts in Admin/UI

See [Testing Summary](docs/TESTING_SUMMARY.md) for details.

## 🔧 Scripts

All scripts are in the `scripts/` folder:

### Deployment Scripts
- `deploy-to-192.168.1.200.ps1` - Deploy to production server
- `deploy-and-test.ps1` - Deploy and run integration tests
- `deploy-frontend.ps1` - Deploy frontend only

### Testing Scripts
- `run-unittest.ps1` - Run unit tests
- `run-integration-test.ps1` - Run integration tests
- `deploy-and-test.ps1` - Deploy and test

### Utility Scripts
- `reset-password.ps1` - Reset admin password
- `verify_pgedge_setup.ps1` - Verify database setup
- `show-key-upload-guide.ps1` - Show certificate upload guide

## 🎯 Key Features

- ✅ **AS2 Message Exchange** - Full AS2 protocol support
- ✅ **Modern Dashboard** - React-based UI with Material-UI
- ✅ **Real-time Charts** - Line graphs and heatmaps
- ✅ **User Authentication** - Login/register system
- ✅ **REST API** - Complete API for integration
- ✅ **Docker Deployment** - Easy containerized deployment
- ✅ **PostgreSQL Database** - Robust data storage
- ✅ **Comprehensive Testing** - Unit and integration tests

## 📊 Dashboard Features

- **Statistics Cards** - Partners, Keys, Messages, Success Rate
- **Line Chart** - Sent/Received/Failed messages over time
- **Heatmap** - Message activity patterns (hourly/daily/weekly/monthly/yearly)
- **Messages List** - View all AS2 messages
- **Partners Management** - Manage trading partners
- **Keys Management** - Certificate and key management

## 🔐 Security

- SSL/TLS encryption for AS2 messages
- Digital signatures for message integrity
- User authentication for dashboard access
- Certificate-based partner authentication

## 🐳 Docker Services

- **p1** - AS2 Server P1 (Port 8001)
- **postgres** - PostgreSQL Database (Port 5432)
- **frontend** - React Dashboard (Port 80)
- **nginx** - Reverse Proxy (Port 8001)

## 📝 License

[Your License Here]

## 🤝 Contributing

[Your Contributing Guidelines Here]

## 📞 Support

For issues and questions:
- Check the [documentation](docs/)
- Review [troubleshooting guides](docs/PRIVATE_KEY_TROUBLESHOOTING.md)
- Contact support

---

**Version**: 1.0.0  
**Last Updated**: February 2026
