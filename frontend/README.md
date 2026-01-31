# AS2 Dashboard - React Frontend

Modern React dashboard for managing AS2 partners, keys, and messages.

## Features

- 📊 **Dashboard Overview** - Real-time statistics and charts
- 👥 **Partners Management** - View and manage AS2 partners
- 🔐 **Keys & Certificates** - Manage encryption keys and certificates
- 📨 **Messages** - Track inbound and outbound AS2 messages
- 🎨 **Material-UI Design** - Clean, modern interface inspired by Devias Kit

## Tech Stack

- **React 18** - UI framework
- **Material-UI (MUI)** - Component library
- **Recharts** - Data visualization
- **React Router** - Navigation
- **Axios** - API calls
- **Vite** - Build tool

## Development

### Prerequisites

- Node.js 18+
- npm or yarn

### Install Dependencies

```bash
cd frontend
npm install
```

### Run Development Server

```bash
npm run dev
```

Access at: http://localhost:3000

### Build for Production

```bash
npm run build
```

## Docker Deployment

The frontend is automatically built and deployed with Docker Compose:

```bash
docker-compose up -d frontend
```

Access at: http://localhost:3000

## API Integration

The frontend connects to the Django backend API:

- `/api/partners/` - Get all partners
- `/api/keys/` - Get all keys and certificates
- `/api/messages/` - Get all messages
- `/api/stats/` - Get dashboard statistics

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   └── Layout.jsx          # Main layout with sidebar
│   ├── pages/
│   │   ├── Dashboard.jsx       # Dashboard overview
│   │   ├── Partners.jsx        # Partners list
│   │   ├── Keys.jsx           # Keys & certificates
│   │   └── Messages.jsx       # Messages list
│   ├── App.jsx                # Main app component
│   ├── main.jsx               # Entry point
│   └── index.css              # Global styles
├── public/                    # Static assets
├── Dockerfile                 # Docker build config
├── nginx.conf                 # Nginx config for production
├── vite.config.js            # Vite configuration
└── package.json              # Dependencies
```

## Features by Page

### Dashboard
- Total partners, keys, messages statistics
- Success rate tracking
- Monthly message chart
- Message status pie chart

### Partners
- List all AS2 partners
- Search functionality
- Partner details (AS2 name, URL, encryption, signature)
- Status indicators
- Add/Edit/Delete actions

### Keys & Certificates
- View all private keys and public certificates
- Key statistics (total, private, public, expiring)
- Search functionality
- Key details (type, algorithm, organization, expiration)
- Download/Edit/Delete actions

### Messages
- View all AS2 messages
- Filter by direction (inbound/outbound)
- Search functionality
- Message details (ID, partner, status, timestamp, size)
- Status indicators (success, pending, failed)

## Customization

### Theme

Edit `src/App.jsx` to customize the Material-UI theme:

```javascript
const theme = createTheme({
  palette: {
    primary: {
      main: '#5048E5', // Change primary color
    },
    // ... more theme options
  },
})
```

### Colors

Main colors used:
- Primary: `#5048E5` (Purple)
- Success: `#10B981` (Green)
- Warning: `#F59E0B` (Orange)
- Error: `#EF4444` (Red)
- Info: `#06B6D4` (Cyan)

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

Same as parent project.
