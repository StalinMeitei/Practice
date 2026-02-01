# Paomi AS2 - Complete Documentation Index

## 🚨 Having Issues?

### 🔐 NEW: Authentication System

**Dashboard now requires login!**

**Quick Start**:
1. Open: http://192.168.1.200:8001
2. Click: "Sign Up" to create account
3. Login: With your credentials
4. Explore: Dashboard, Partners, Keys, Messages

**Documentation**:
- [WHATS_NEW.md](WHATS_NEW.md) - See what's new!
- [AUTHENTICATION_GUIDE.md](AUTHENTICATION_GUIDE.md) - Complete guide
- [AUTH_QUICK_REFERENCE.md](AUTH_QUICK_REFERENCE.md) - Quick reference

### Private Key Upload Error
**Error**: "Invalid Private Key or password is not correct"

**Quick Fix**: Leave the password field **EMPTY**

**Start Here**:
1. Run: `.\show-key-upload-guide.ps1` (interactive guide)
2. Read: [PRIVATE_KEY_FIX_SUMMARY.md](PRIVATE_KEY_FIX_SUMMARY.md)
3. Detailed help: [PRIVATE_KEY_TROUBLESHOOTING.md](PRIVATE_KEY_TROUBLESHOOTING.md)

## 📖 Documentation by Topic

### Getting Started

| Document | Description | When to Use |
|----------|-------------|-------------|
| [README.md](README.md) | Main project documentation | First time setup |
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | Quick command reference | Daily operations |
| [SETUP_GUIDE.md](SETUP_GUIDE.md) | Detailed setup instructions | Initial installation |

### Frontend Dashboard

| Document | Description | When to Use |
|----------|-------------|-------------|
| [WHATS_NEW.md](WHATS_NEW.md) | Latest updates & features | See what's new! |
| [AUTHENTICATION_GUIDE.md](AUTHENTICATION_GUIDE.md) | Complete auth guide | User registration & login |
| [AUTH_QUICK_REFERENCE.md](AUTH_QUICK_REFERENCE.md) | Auth quick reference | Quick auth commands |
| [FRONTEND_GUIDE.md](FRONTEND_GUIDE.md) | Complete frontend guide | Dashboard setup & customization |
| [frontend/README.md](frontend/README.md) | Frontend technical docs | Development reference |
| [DASHBOARD_QUICK_START.md](DASHBOARD_QUICK_START.md) | Dashboard quick start | Fast dashboard setup |

### Docker Deployment

| Document | Description | When to Use |
|----------|-------------|-------------|
| [README_DOCKER.md](README_DOCKER.md) | Docker deployment guide | Docker setup |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Production deployment | Server deployment |
| [DEPLOYMENT_TO_192.168.1.200.md](DEPLOYMENT_TO_192.168.1.200.md) | Server deployment guide | Deploy to 192.168.1.200 |
| [DEPLOYMENT_SUCCESS.md](DEPLOYMENT_SUCCESS.md) | Deployment summary | Post-deployment |
| [ACCESS_GUIDE.md](ACCESS_GUIDE.md) | Access all services | Service URLs & access |
| [TASK_COMPLETION_SUMMARY.md](TASK_COMPLETION_SUMMARY.md) | Implementation summary | See what was built |

### pgEdge & Database

| Document | Description | When to Use |
|----------|-------------|-------------|
| [PGEDGE_INTEGRATION.md](PGEDGE_INTEGRATION.md) | Complete pgEdge integration | pgEdge setup |
| [PGEDGE_QUICK_START.md](PGEDGE_QUICK_START.md) | Quick start guide | Fast pgEdge setup |
| [DBEAVER_SETUP.md](DBEAVER_SETUP.md) | DBeaver connection guide | Database access |
| [setup_pgedge.md](setup_pgedge.md) | pgEdge setup details | pgEdge configuration |

### Private Key & Certificates

| Document | Description | When to Use |
|----------|-------------|-------------|
| [PRIVATE_KEY_FIX_SUMMARY.md](PRIVATE_KEY_FIX_SUMMARY.md) | Private key issue fix | Key upload errors |
| [PRIVATE_KEY_TROUBLESHOOTING.md](PRIVATE_KEY_TROUBLESHOOTING.md) | Detailed troubleshooting | Complex key issues |
| [upload_private_key_guide.txt](upload_private_key_guide.txt) | Visual upload guide | Step-by-step help |

## 🛠️ Scripts & Tools

### Setup Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `setup_pgedge_both.py` | Setup both P1 and P2 | `python setup_pgedge_both.py` |
| `setup_p1_pgedge.py` | Setup P1 only | `python setup_p1_pgedge.py` |
| `setup_p2_pgedge.py` | Setup P2 only | `python setup_p2_pgedge.py` |
| `setup_both_servers.py` | Setup both servers | `python setup_both_servers.py` |
| `setup_both_simple.py` | Simple setup | `python setup_both_simple.py` |

### Certificate Management

| Script | Purpose | Usage |
|--------|---------|-------|
| `generate_certificates.py` | Generate SSL certificates | `python generate_certificates.py` |
| `fix_private_key_format.py` | Check/fix key format | `python fix_private_key_format.py` |

### Database Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `setup_database.py` | Setup database | `python setup_database.py` |
| `setup_docker_postgres.py` | Docker PostgreSQL setup | `python setup_docker_postgres.py` |
| `init_as2_config.py` | Initialize AS2 config | `python init_as2_config.py [p1\|p2\|both]` |

### pgEdge Agentic AI

| Script | Purpose | Usage |
|--------|---------|-------|
| `init_pgedge_agentic.py` | Initialize pgEdge AI | `python init_pgedge_agentic.py` |
| `pgedge_agentic_examples.py` | Usage examples | `python pgedge_agentic_examples.py` |

### Testing

| Script | Purpose | Usage |
|--------|---------|-------|
| `test_file_transfer.py` | Test file transfer | `python test_file_transfer.py` |
| `test_file_transfer_pgedge.py` | Test with pgEdge | `python test_file_transfer_pgedge.py` |
| `test_setup.py` | Test setup | `python test_setup.py` |

### Deployment Scripts (PowerShell)

| Script | Purpose | Usage |
|--------|---------|-------|
| `deploy-pgedge.ps1` | Deploy with pgEdge | `.\deploy-pgedge.ps1` |
| `deploy-frontend.ps1` | Deploy frontend only | `.\deploy-frontend.ps1` |
| `deploy-windows.ps1` | Windows deployment | `.\deploy-windows.ps1` |
| `deploy.ps1` | Standard deployment | `.\deploy.ps1` |
| `verify_pgedge_setup.ps1` | Verify pgEdge setup | `.\verify_pgedge_setup.ps1` |
| `show-key-upload-guide.ps1` | Show key upload guide | `.\show-key-upload-guide.ps1` |

### Deployment Scripts (Bash)

| Script | Purpose | Usage |
|--------|---------|-------|
| `deploy-simple.sh` | Simple deployment | `./deploy-simple.sh` |
| `deploy.sh` | Standard deployment | `./deploy.sh` |
| `start-local.sh` | Start locally | `./start-local.sh` |

### Admin Tools

| Script | Purpose | Usage |
|--------|---------|-------|
| `reset_admin_password.py` | Reset admin password | `python reset_admin_password.py` |
| `reset-password.ps1` | Reset password (PS) | `.\reset-password.ps1` |
| `set_admin_password.py` | Set admin password | `python set_admin_password.py` |

## 🎯 Common Tasks

### First Time Setup

1. Read: [README.md](README.md)
2. Run: `python generate_certificates.py`
3. Run: `python setup_pgedge_both.py`
4. Test: `python test_file_transfer_pgedge.py`

### Docker Deployment

1. Read: [README_DOCKER.md](README_DOCKER.md)
2. Run: `.\deploy-pgedge.ps1`
3. Verify: `.\verify_pgedge_setup.ps1`
4. Access: http://localhost:8001/admin/

### Fix Private Key Error

1. Run: `.\show-key-upload-guide.ps1`
2. Read: [PRIVATE_KEY_FIX_SUMMARY.md](PRIVATE_KEY_FIX_SUMMARY.md)
3. Check: `python fix_private_key_format.py`
4. Upload key with **EMPTY** password field

### Connect DBeaver

1. Read: [DBEAVER_SETUP.md](DBEAVER_SETUP.md)
2. Host: `localhost`, Port: `5432`
3. User: `postgres`, Password: `postgres`
4. Database: `p1_as2_db` or `p2_as2_db`

### Use pgEdge Agentic AI

1. Read: [PGEDGE_QUICK_START.md](PGEDGE_QUICK_START.md)
2. Run: `python pgedge_agentic_examples.py`
3. See: [PGEDGE_INTEGRATION.md](PGEDGE_INTEGRATION.md)

## 🔍 Troubleshooting

### Issue: Private Key Upload Error

**Documents**:
- [PRIVATE_KEY_FIX_SUMMARY.md](PRIVATE_KEY_FIX_SUMMARY.md)
- [PRIVATE_KEY_TROUBLESHOOTING.md](PRIVATE_KEY_TROUBLESHOOTING.md)

**Scripts**:
- `.\show-key-upload-guide.ps1`
- `python fix_private_key_format.py`

### Issue: Docker Container Won't Start

**Documents**:
- [README_DOCKER.md](README_DOCKER.md) (Troubleshooting section)

**Commands**:
```bash
docker-compose logs -f
docker-compose restart
```

### Issue: Database Connection Error

**Documents**:
- [DBEAVER_SETUP.md](DBEAVER_SETUP.md) (Troubleshooting section)

**Commands**:
```bash
docker-compose logs postgres
docker exec -it pgedge-as2 psql -U postgres
```

### Issue: Message Send/Receive Failure

**Documents**:
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md)

**Scripts**:
- `python test_file_transfer.py`

## 📊 Architecture

### Components

```
┌─────────────────────────────────────────────┐
│           Nginx (Port 8001)                 │
│         Reverse Proxy                       │
└──────────────┬──────────────────────────────┘
               │
       ┌───────┴────────┐
       │                │
┌──────▼──────┐  ┌──────▼──────┐
│  P1 Server  │  │  P2 Server  │
│  Port 8000  │  │  Port 8002  │
└──────┬──────┘  └──────┬──────┘
       │                │
       └───────┬────────┘
               │
        ┌──────▼──────┐
        │  PostgreSQL │
        │  Port 5432  │
        │  + pgEdge   │
        └─────────────┘
```

### Access Points

| Service | URL | Credentials |
|---------|-----|-------------|
| **Dashboard** | http://localhost:3000 | N/A |
| P1 Admin | http://localhost:8001/admin/ | admin/admin123 |
| P2 Admin | http://localhost:8001/p2/admin/ | admin/admin123 |
| PostgreSQL | localhost:5432 | postgres/postgres |

### API Endpoints

| Endpoint | Description |
|----------|-------------|
| http://localhost:8001/api/partners/ | Get all partners |
| http://localhost:8001/api/keys/ | Get all keys |
| http://localhost:8001/api/messages/ | Get all messages |
| http://localhost:8001/api/stats/ | Get statistics |

## 🔐 Security Notes

⚠️ **Development Setup**: Default credentials are for development only.

For production:
1. Change all passwords
2. Use environment variables
3. Enable SSL/TLS
4. Restrict network access
5. Configure firewall

See: [DEPLOYMENT.md](DEPLOYMENT.md) for production security checklist.

## 📞 Support

### Quick Help

1. Check relevant documentation above
2. Run verification scripts
3. Check Docker logs: `docker-compose logs -f`
4. Review error messages

### Common Solutions

- **Private Key Error**: Run `.\show-key-upload-guide.ps1`
- **Docker Issues**: Run `.\verify_pgedge_setup.ps1`
- **Database Issues**: See [DBEAVER_SETUP.md](DBEAVER_SETUP.md)
- **Setup Issues**: See [SETUP_GUIDE.md](SETUP_GUIDE.md)

## 📝 License

Same as original paomi-as2 project.

---

**Quick Start**: New to the project? Start with [README.md](README.md)

**Having Issues**: Check the troubleshooting section above or run `.\show-key-upload-guide.ps1`

**Need Database Access**: See [DBEAVER_SETUP.md](DBEAVER_SETUP.md)

**Want AI Features**: See [PGEDGE_QUICK_START.md](PGEDGE_QUICK_START.md)
