# AS2 Dashboard - Access Guide

## ✅ All Services Running Successfully!

### 🌐 Main Access Point

**Dashboard**: http://192.168.1.200:8001

This is your main entry point - it shows the React dashboard with:
- Overview statistics
- Partners management
- Keys & certificates
- Messages tracking

### 🔐 Authentication Required

**First Time Users**:
1. Go to http://192.168.1.200:8001
2. You'll be redirected to the login page
3. Click **"Sign Up"** to create an account
4. Fill in username, email, and password
5. Login with your credentials

**See full authentication guide**: `AUTHENTICATION_GUIDE.md`

### 📊 Dashboard Pages

| Page | URL | Description |
|------|-----|-------------|
| **Overview** | http://192.168.1.200:8001 | Statistics, charts, success rate |
| **Partners** | http://192.168.1.200:8001 (click Partners) | Manage AS2 partners |
| **Keys** | http://192.168.1.200:8001 (click Keys) | View certificates |
| **Messages** | http://192.168.1.200:8001 (click Messages) | Track AS2 messages |

### 🔧 Admin Interfaces

| Service | URL | Credentials |
|---------|-----|-------------|
| **P1 Admin** | http://192.168.1.200:8001/admin/ | admin / admin123 |
| **P2 Admin** | http://192.168.1.200:8001/p2/admin/ | admin / admin123 |

### 🔌 API Endpoints

Base URL: `http://192.168.1.200:8001/api/`

| Endpoint | URL | Description |
|----------|-----|-------------|
| Stats | http://192.168.1.200:8001/api/stats/ | Dashboard statistics |
| Partners | http://192.168.1.200:8001/api/partners/ | All partners |
| Keys | http://192.168.1.200:8001/api/keys/ | All keys |
| Messages | http://192.168.1.200:8001/api/messages/ | All messages |

### 🗄️ Database Access

**PostgreSQL**:
- Host: `192.168.1.200`
- Port: `5432`
- Username: `postgres`
- Password: `postgres`
- Databases: `p1_as2_db`, `p2_as2_db`

**DBeaver Connection**: See `DBEAVER_SETUP.md`

### 🐳 Alternative Access (Direct Ports)

If you need direct access to services:

| Service | Direct URL |
|---------|-----------|
| Dashboard | http://192.168.1.200:3000 |
| P1 Server | http://192.168.1.200:8000 |
| P2 Server | http://192.168.1.200:8002 |

## 🎯 Quick Start

### 1. Open Dashboard
```
http://192.168.1.200:8001
```

### 2. Navigate
- Click **Overview** - See statistics
- Click **Partners** - Manage partners
- Click **Keys** - View certificates
- Click **Messages** - Track messages

### 3. Admin Access
```
http://192.168.1.200:8001/admin/
Username: admin
Password: admin123
```

## 🎨 Dashboard Features

### Overview Page
- **Statistics Cards**: Partners, Keys, Messages, Success Rate
- **Message Chart**: Monthly volume (bar chart)
- **Status Chart**: Distribution (pie chart)
- **Trend Indicators**: Up/down arrows with percentages

### Partners Page
- **Search**: Filter partners by name
- **Table View**: AS2 name, URL, encryption, signature
- **Status**: Active/Inactive indicators
- **Actions**: Add, Edit, Delete buttons

### Keys Page
- **Statistics**: Total, Private, Public, Expiring
- **Search**: Filter by name or organization
- **Table View**: Type, algorithm, expiration
- **Color Coding**: Red for private, Green for public

### Messages Page
- **Tabs**: All, Inbound, Outbound
- **Search**: Filter by message ID or partner
- **Table View**: Direction, status, timestamp, size
- **Status**: Success (green), Pending (orange), Failed (red)

## 📱 Mobile Access

The dashboard is responsive and works on mobile devices:
- Open http://192.168.1.200:8001 on your phone
- Sidebar collapses to hamburger menu
- Tables scroll horizontally
- Charts adapt to screen size

## 🔐 Security Notes

⚠️ **Current Setup**: Development configuration

**Default Credentials**:
- Admin: `admin` / `admin123`
- Database: `postgres` / `postgres`

**For Production**:
1. Change all passwords
2. Enable HTTPS
3. Configure firewall
4. Restrict database access
5. Add authentication to dashboard

## 🛠️ Management

### Check Status
```bash
ssh dev@192.168.1.200
cd /home/dev/paomi-as2
docker-compose ps
```

### View Logs
```bash
# Dashboard logs
docker-compose logs frontend -f

# Backend logs
docker-compose logs p1 -f
docker-compose logs p2 -f

# All logs
docker-compose logs -f
```

### Restart Services
```bash
# Restart all
docker-compose restart

# Restart dashboard only
docker-compose restart frontend nginx
```

## 🐛 Troubleshooting

### Dashboard Not Loading
1. Check if containers are running:
   ```bash
   docker-compose ps
   ```

2. Check frontend logs:
   ```bash
   docker logs as2-frontend
   docker logs nginx-as2
   ```

3. Restart services:
   ```bash
   docker-compose restart frontend nginx
   ```

### API Not Responding
1. Check backend logs:
   ```bash
   docker logs p1-as2
   ```

2. Test API directly:
   ```bash
   curl http://192.168.1.200:8001/api/stats/
   ```

3. Restart backend:
   ```bash
   docker-compose restart p1 p2
   ```

### Cannot Access from Browser
1. Check firewall:
   ```bash
   sudo ufw status
   ```

2. Verify port is open:
   ```bash
   netstat -tln | grep 8001
   ```

3. Try different browser or clear cache

## 📞 Support

### Quick Checks
- ✅ All containers running: `docker-compose ps`
- ✅ Dashboard accessible: http://192.168.1.200:8001
- ✅ API responding: http://192.168.1.200:8001/api/stats/
- ✅ Admin accessible: http://192.168.1.200:8001/admin/

### Common Issues
- **Blank page**: Clear browser cache, check console for errors
- **API errors**: Check P1 logs, verify database connection
- **Slow loading**: Check server resources, restart containers

### Documentation
- **Frontend Guide**: `FRONTEND_GUIDE.md`
- **Dashboard Quick Start**: `DASHBOARD_QUICK_START.md`
- **Deployment Guide**: `DEPLOYMENT_TO_192.168.1.200.md`
- **Docker Guide**: `README_DOCKER.md`

## 🎉 Success!

Your AS2 Dashboard is now live at:

### **http://192.168.1.200:8001**

Features:
- ✅ Modern React UI with Material-UI
- ✅ Real-time statistics and charts
- ✅ Partner management
- ✅ Certificate tracking
- ✅ Message monitoring
- ✅ REST API access
- ✅ Django admin interfaces
- ✅ PostgreSQL database

Enjoy your new dashboard!

---

**Last Updated**: January 31, 2026  
**Server**: 192.168.1.200  
**Status**: ✅ All services running
