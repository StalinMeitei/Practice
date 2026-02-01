# AS2 Dashboard Frontend - Complete Guide

## Overview

A modern React dashboard for managing AS2 partners, keys, and messages. Built with Material-UI and inspired by the Devias Kit design.

## Quick Start

### Option 1: Docker Deployment (Recommended)

```powershell
# Deploy everything (backend + frontend)
.\deploy-pgedge.ps1

# Or deploy frontend only
.\deploy-frontend.ps1
```

Access at: **http://localhost:3000**

### Option 2: Development Mode

```bash
cd frontend
npm install
npm run dev
```

Access at: **http://localhost:3000**

## Features

### 1. Dashboard Overview
- **Statistics Cards**: Partners, Keys, Messages, Success Rate
- **Message Chart**: Monthly message volume (bar chart)
- **Status Chart**: Message status distribution (pie chart)
- **Real-time Updates**: Auto-refresh statistics

### 2. Partners Management
- **List View**: All AS2 partners with details
- **Search**: Filter partners by name or AS2 name
- **Details**: AS2 name, target URL, encryption, signature
- **Status**: Active/Inactive indicators
- **Actions**: Add, Edit, Delete partners

### 3. Keys & Certificates
- **Statistics**: Total keys, private keys, public certificates, expiring keys
- **List View**: All keys and certificates
- **Search**: Filter by name or organization
- **Details**: Type, algorithm, organization, expiration, fingerprint
- **Type Indicators**: Color-coded private/public keys
- **Actions**: Download, Edit, Delete keys

### 4. Messages
- **Tabs**: All, Inbound, Outbound messages
- **Search**: Filter by message ID or partner
- **Details**: Message ID, direction, partner, status, timestamp, size
- **Status Indicators**: Success, Pending, Failed
- **Actions**: View message details

## Design System

### Color Palette

| Color | Hex | Usage |
|-------|-----|-------|
| Primary | `#5048E5` | Buttons, links, primary actions |
| Success | `#10B981` | Success states, positive indicators |
| Warning | `#F59E0B` | Warning states, pending actions |
| Error | `#EF4444` | Error states, failed actions |
| Info | `#06B6D4` | Informational elements |
| Background | `#F9FAFC` | Page background |
| Paper | `#FFFFFF` | Card/paper background |
| Sidebar | `#1E293B` | Dark sidebar background |

### Typography

- **Font Family**: Inter, Roboto, Helvetica, Arial
- **Headings**: 600 weight
- **Body**: 400 weight
- **Monospace**: For IDs and fingerprints

### Components

- **Cards**: Rounded corners (8px), subtle shadows
- **Tables**: Hover effects, clean borders
- **Chips**: Color-coded status indicators
- **Buttons**: Rounded, no text transform
- **Icons**: Material-UI icons throughout

## Architecture

### Frontend Stack

```
React 18
├── Material-UI (MUI) - UI components
├── React Router - Navigation
├── Recharts - Data visualization
├── Axios - API communication
└── Vite - Build tool
```

### Backend API

```
Django REST API
├── /api/partners/ - Partner data
├── /api/keys/ - Keys and certificates
├── /api/messages/ - Message data
└── /api/stats/ - Dashboard statistics
```

### Docker Setup

```
Docker Compose
├── postgres - Database
├── p1 - AS2 Server 1
├── p2 - AS2 Server 2
├── nginx - Reverse proxy
└── frontend - React dashboard
```

## File Structure

```
frontend/
├── src/
│   ├── components/
│   │   └── Layout.jsx              # Main layout with sidebar
│   ├── pages/
│   │   ├── Dashboard.jsx           # Dashboard overview
│   │   ├── Partners.jsx            # Partners management
│   │   ├── Keys.jsx               # Keys & certificates
│   │   └── Messages.jsx           # Messages list
│   ├── App.jsx                    # Main app with routing
│   ├── main.jsx                   # Entry point
│   └── index.css                  # Global styles
├── public/                        # Static assets
├── Dockerfile                     # Docker build
├── nginx.conf                     # Production nginx config
├── vite.config.js                # Vite configuration
├── package.json                   # Dependencies
└── README.md                      # Frontend docs
```

## API Integration

### Fetching Data

```javascript
import axios from 'axios'

// Get partners
const response = await axios.get('/api/partners/')
const partners = response.data.partners

// Get keys
const response = await axios.get('/api/keys/')
const keys = response.data.keys

// Get messages
const response = await axios.get('/api/messages/')
const messages = response.data.messages

// Get stats
const response = await axios.get('/api/stats/')
const stats = response.data
```

### API Response Format

**Partners:**
```json
{
  "partners": [
    {
      "id": 1,
      "as2_name": "P1",
      "name": "P1 Organization",
      "target_url": "http://p1:8000/pyas2/as2receive",
      "encryption": "tripledes_192_cbc",
      "signature": "sha256",
      "status": "active"
    }
  ]
}
```

**Keys:**
```json
{
  "keys": [
    {
      "id": "priv_1",
      "name": "Private Key 1",
      "type": "Private",
      "algorithm": "RSA 2048",
      "organization": "P1 Organization",
      "expires": "2027-01-20",
      "status": "active",
      "fingerprint": "A1:B2:C3:D4:E5:F6"
    }
  ]
}
```

**Messages:**
```json
{
  "messages": [
    {
      "id": 1,
      "message_id": "MSG-2026-001",
      "direction": "outbound",
      "partner": "P2",
      "status": "success",
      "timestamp": "2026-01-31 10:30:00",
      "size": "2.5 MB"
    }
  ]
}
```

**Stats:**
```json
{
  "partners": 12,
  "keys": 24,
  "messages": 1847,
  "successRate": 95.5
}
```

## Customization

### Change Theme Colors

Edit `src/App.jsx`:

```javascript
const theme = createTheme({
  palette: {
    primary: {
      main: '#YOUR_COLOR', // Change primary color
    },
    secondary: {
      main: '#YOUR_COLOR', // Change secondary color
    },
  },
})
```

### Add New Page

1. Create page component in `src/pages/`:
```javascript
// src/pages/NewPage.jsx
export default function NewPage() {
  return <div>New Page</div>
}
```

2. Add route in `src/App.jsx`:
```javascript
import NewPage from './pages/NewPage'

<Route path="/new-page" element={<NewPage />} />
```

3. Add menu item in `src/components/Layout.jsx`:
```javascript
const menuItems = [
  // ... existing items
  { text: 'New Page', icon: <Icon />, path: '/new-page' },
]
```

### Modify Sidebar

Edit `src/components/Layout.jsx`:

```javascript
// Change sidebar width
const drawerWidth = 280 // Change this value

// Change sidebar color
<Box sx={{ bgcolor: '#YOUR_COLOR' }}>

// Add/remove menu items
const menuItems = [
  { text: 'Overview', icon: <DashboardIcon />, path: '/' },
  // Add your items here
]
```

## Development

### Install Dependencies

```bash
cd frontend
npm install
```

### Run Development Server

```bash
npm run dev
```

### Build for Production

```bash
npm run build
```

Output in `dist/` folder.

### Preview Production Build

```bash
npm run preview
```

## Docker Deployment

### Build and Run

```bash
# Build frontend image
docker-compose build frontend

# Start frontend container
docker-compose up -d frontend

# View logs
docker logs as2-frontend -f
```

### Rebuild After Changes

```bash
# Rebuild without cache
docker-compose build --no-cache frontend

# Restart container
docker-compose restart frontend
```

## Troubleshooting

### Frontend Won't Start

```bash
# Check logs
docker logs as2-frontend

# Check if port 3000 is available
netstat -ano | findstr :3000

# Restart container
docker-compose restart frontend
```

### API Calls Failing

1. Check backend is running:
```bash
docker ps | findstr p1-as2
```

2. Test API directly:
```bash
curl http://localhost:8001/api/stats/
```

3. Check CORS settings in Django

### Build Errors

```bash
# Clear node_modules
cd frontend
rm -rf node_modules
npm install

# Clear Docker cache
docker-compose build --no-cache frontend
```

### Styling Issues

1. Clear browser cache
2. Check Material-UI version compatibility
3. Verify CSS imports in components

## Performance

### Optimization Tips

1. **Code Splitting**: Already configured with React Router
2. **Lazy Loading**: Use `React.lazy()` for large components
3. **Memoization**: Use `React.memo()` for expensive renders
4. **API Caching**: Implement caching for API responses

### Production Build

The production build includes:
- Minification
- Tree shaking
- Gzip compression (via nginx)
- Asset optimization

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Security

### Best Practices

1. **API Authentication**: Implement JWT or session auth
2. **HTTPS**: Use SSL/TLS in production
3. **CORS**: Configure proper CORS headers
4. **Input Validation**: Validate all user inputs
5. **XSS Protection**: Material-UI handles most XSS risks

## Deployment Checklist

- [ ] Build frontend: `npm run build`
- [ ] Test production build: `npm run preview`
- [ ] Update API endpoints for production
- [ ] Configure CORS in Django
- [ ] Set up HTTPS/SSL
- [ ] Configure nginx properly
- [ ] Test all features
- [ ] Monitor performance
- [ ] Set up error logging

## Next Steps

1. **Authentication**: Add login/logout functionality
2. **Real-time Updates**: Implement WebSocket for live data
3. **Notifications**: Add toast notifications for actions
4. **Export**: Add CSV/PDF export for data
5. **Filters**: Add advanced filtering options
6. **Dark Mode**: Implement theme toggle
7. **Mobile**: Optimize for mobile devices

## Support

For issues:
- Check Docker logs: `docker logs as2-frontend`
- Check browser console for errors
- Verify API endpoints are accessible
- Review nginx configuration

## Resources

- [Material-UI Docs](https://mui.com/)
- [React Router Docs](https://reactrouter.com/)
- [Recharts Docs](https://recharts.org/)
- [Vite Docs](https://vitejs.dev/)

---

**Quick Access**: http://localhost:3000

**API Base**: http://localhost:8001/api/
