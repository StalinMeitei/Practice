# AS2 Dashboard - Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Deploy Everything

```powershell
.\deploy-pgedge.ps1
```

This deploys:
- PostgreSQL with pgEdge
- P1 AS2 Server
- P2 AS2 Server
- Nginx reverse proxy
- React Dashboard

### Step 2: Access Dashboard

Open your browser: **http://localhost:3000**

### Step 3: Explore

- **Dashboard**: View statistics and charts
- **Partners**: Manage AS2 partners
- **Keys**: View certificates and keys
- **Messages**: Track AS2 messages

## 📊 Dashboard Features

### Overview Page
- Total partners, keys, messages
- Success rate tracking
- Monthly message chart
- Status distribution

### Partners Page
- List all AS2 partners
- Search and filter
- View encryption settings
- Add/Edit/Delete partners

### Keys Page
- View all keys and certificates
- Private/Public key indicators
- Expiration tracking
- Download certificates

### Messages Page
- View all AS2 messages
- Filter by direction (inbound/outbound)
- Track message status
- View message details

## 🎨 Design

Inspired by **Devias Kit** with:
- Clean, modern interface
- Material-UI components
- Dark sidebar navigation
- Color-coded status indicators
- Responsive design

## 🔗 Access Points

| Service | URL |
|---------|-----|
| **Dashboard** | http://localhost:3000 |
| P1 Admin | http://localhost:8001/admin/ |
| P2 Admin | http://localhost:8001/p2/admin/ |
| API | http://localhost:8001/api/ |

## 🛠️ Quick Commands

### View Logs
```bash
docker logs as2-frontend -f
```

### Restart Frontend
```bash
docker-compose restart frontend
```

### Rebuild Frontend
```bash
docker-compose build --no-cache frontend
docker-compose up -d frontend
```

### Stop Everything
```bash
docker-compose down
```

## 📱 Screenshots

### Dashboard Overview
- Statistics cards with trend indicators
- Bar chart showing monthly messages
- Pie chart showing message status distribution

### Partners Management
- Table view with all partner details
- Search functionality
- Status indicators (active/inactive)
- Action buttons (edit/delete)

### Keys & Certificates
- Statistics cards (total, private, public, expiring)
- Table view with key details
- Type indicators (private/public)
- Download/Edit/Delete actions

### Messages
- Tabs for all/inbound/outbound
- Search functionality
- Status indicators (success/pending/failed)
- Direction indicators

## 🎯 Common Tasks

### View Partner Details
1. Click **Partners** in sidebar
2. Search for partner name
3. View details in table

### Check Message Status
1. Click **Messages** in sidebar
2. Use tabs to filter by direction
3. Check status column

### View Key Expiration
1. Click **Keys** in sidebar
2. Check "Expiring Soon" card
3. View expiration dates in table

### Monitor Success Rate
1. Go to **Dashboard**
2. Check "Success Rate" card
3. View trend indicator

## 🔧 Troubleshooting

### Dashboard Not Loading

```bash
# Check if container is running
docker ps | findstr as2-frontend

# Check logs
docker logs as2-frontend

# Restart
docker-compose restart frontend
```

### API Errors

```bash
# Check backend is running
docker ps | findstr p1-as2

# Test API
curl http://localhost:8001/api/stats/

# Check logs
docker logs p1-as2
```

### Port Already in Use

Edit `docker-compose.yml`:
```yaml
frontend:
  ports:
    - "3001:80"  # Change to different port
```

## 📚 Documentation

- **Complete Guide**: [FRONTEND_GUIDE.md](FRONTEND_GUIDE.md)
- **Technical Docs**: [frontend/README.md](frontend/README.md)
- **API Docs**: See Django admin
- **Deployment**: [README_DOCKER.md](README_DOCKER.md)

## 🎨 Customization

### Change Colors

Edit `frontend/src/App.jsx`:
```javascript
const theme = createTheme({
  palette: {
    primary: { main: '#YOUR_COLOR' },
  },
})
```

### Add Menu Item

Edit `frontend/src/components/Layout.jsx`:
```javascript
const menuItems = [
  // Add your item
  { text: 'New Page', icon: <Icon />, path: '/new' },
]
```

## 🚀 Next Steps

1. **Explore Dashboard**: Navigate through all pages
2. **Check API**: Test API endpoints
3. **Customize**: Change colors and branding
4. **Add Features**: Extend functionality
5. **Deploy Production**: Set up HTTPS and auth

## 💡 Tips

- Use search to quickly find partners/keys/messages
- Check dashboard regularly for success rate
- Monitor expiring keys in Keys page
- Filter messages by direction for easier tracking
- Use color indicators for quick status checks

## 🔐 Security Notes

⚠️ **Development Setup**: Current setup is for development.

For production:
1. Add authentication
2. Enable HTTPS
3. Configure CORS properly
4. Use environment variables
5. Set up proper firewall rules

## 📞 Support

Having issues?
1. Check [FRONTEND_GUIDE.md](FRONTEND_GUIDE.md)
2. View Docker logs
3. Test API endpoints
4. Check browser console

---

**Ready to start?** Run `.\deploy-pgedge.ps1` and open http://localhost:3000!
