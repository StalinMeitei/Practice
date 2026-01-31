# Paomi AS2 - Docker Deployment

This is a containerized version of the paomi-as2 application with PostgreSQL (pgedge), pgEdge Agentic AI Toolkit, and Nginx.

## Quick Start

### Deploy with pgEdge Agentic AI
```powershell
# Windows - Full deployment with pgEdge
.\deploy-pgedge.ps1
```

### Local Development
```bash
./start-local.sh
```
Access at: http://localhost:8080/admin/

### Deploy to Server
```powershell
# Windows
.\deploy-windows.ps1

# Linux/Mac
./deploy-simple.sh
```

## New Features

### pgEdge Agentic AI Toolkit
The deployment now includes the pgEdge Agentic AI Toolkit, enabling:
- Natural language queries on your AS2 data
- AI-powered analytics and insights
- Intelligent monitoring and alerting
- Automated data quality checks

See `DBEAVER_SETUP.md` for DBeaver connection details and `pgedge_agentic_examples.py` for usage examples.

## Architecture

```
┌─────────────────────────────────────────────┐
│           Nginx (Port 8080)                 │
│         Reverse Proxy & Load Balancer       │
└──────────────┬──────────────────────────────┘
               │
       ┌───────┴────────┐
       │                │
┌──────▼──────┐  ┌──────▼──────┐
│  P1 Server  │  │  P2 Server  │
│  Port 8000  │  │  Port 8001  │
│  Gunicorn   │  │  Gunicorn   │
└──────┬──────┘  └──────┬──────┘
       │                │
       └───────┬────────┘
               │
        ┌──────▼──────┐
        │  PostgreSQL │
        │  Port 5432  │
        │   (pgedge)  │
        └─────────────┘
```

## Components

### 1. PostgreSQL (pgedge-as2)
- Image: postgres:15-alpine
- Port: 5432 (exposed for DBeaver access)
- Databases: p1_as2_db, p2_as2_db
- User: postgres / postgres
- Features: pgEdge Agentic AI Toolkit enabled

### 2. P1 AS2 Server (p1-as2)
- Port: 8000
- Workers: 3 Gunicorn workers
- Database: p1_as2_db
- Admin: http://192.168.1.200:8080/admin/

### 3. P2 AS2 Server (p2-as2)
- Port: 8001
- Workers: 3 Gunicorn workers
- Database: p2_as2_db
- Admin: http://192.168.1.200:8080/p2/admin/

### 4. Nginx (nginx-as2)
- Port: 8080 (HTTP)
- Port: 8443 (HTTPS)
- Routes /p1/ → P1 Server
- Routes /p2/ → P2 Server
- Default → P1 Server

## Configuration

### Environment Variables

Set in `docker-compose.yml`:

```yaml
environment:
  - DB_HOST=postgres
  - DB_PORT=5432
  - DB_NAME=p1_as2_db
  - DB_USER=postgres
  - DB_PASSWORD=postgres
  - ALLOWED_HOSTS=*
  - DEBUG=True
```

### Volumes

- `postgres_data` - Database persistence
- `p1_data` - P1 AS2 data files
- `p2_data` - P2 AS2 data files
- `p1_static` - P1 static files
- `p2_static` - P2 static files

### Networks

- `as2-network` - Bridge network for inter-container communication

## Usage

### Start Services
```bash
docker-compose up -d
```

### Stop Services
```bash
docker-compose down
```

### View Logs
```bash
docker-compose logs -f
docker-compose logs -f p1
docker-compose logs -f p2
```

### Restart Service
```bash
docker-compose restart p1
```

### Rebuild
```bash
docker-compose up -d --build
```

### Execute Commands
```bash
# Django shell
docker-compose exec p1 python manage.py shell

# Create superuser
docker-compose exec p1 python manage.py createsuperuser

# Run migrations
docker-compose exec p1 python manage.py migrate
```

## Deployment

### Production Server (192.168.1.200)

**Status**: ✅ Deployed and Running

**Access Points**:
- P1 Admin: http://192.168.1.200:8080/admin/
- P2 Admin: http://192.168.1.200:8080/p2/admin/
- Credentials: admin / admin123

**SSH Access**:
```bash
ssh dev@192.168.1.200
# Password: dev@2025
```

**Container Status**:
```bash
cd /home/dev/paomi-as2
docker-compose ps
```

## Maintenance

### Backup Database
```bash
docker-compose exec postgres pg_dump -U postgres p1_as2_db > p1_backup.sql
docker-compose exec postgres pg_dump -U postgres p2_as2_db > p2_backup.sql
```

### Restore Database
```bash
cat p1_backup.sql | docker-compose exec -T postgres psql -U postgres p1_as2_db
```

### Update Application
```bash
# Pull latest code
git pull

# Rebuild and restart
docker-compose down
docker-compose up -d --build
```

### Clean Up
```bash
# Remove containers and networks
docker-compose down

# Remove containers, networks, and volumes
docker-compose down -v

# Remove unused images
docker system prune -a
```

## Monitoring

### Container Health
```bash
docker-compose ps
docker stats
```

### Application Logs
```bash
docker-compose logs --tail=100 -f
```

### Database Status
```bash
docker-compose exec postgres pg_isready
```

### Network Connectivity
```bash
docker-compose exec p1 ping p2
docker-compose exec p1 ping postgres
```

## Troubleshooting

### Container Won't Start
```bash
# Check logs
docker-compose logs [service_name]

# Restart container
docker-compose restart [service_name]

# Rebuild container
docker-compose up -d --build [service_name]
```

### Database Connection Error
```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# Check database logs
docker-compose logs postgres

# Test connection
docker-compose exec postgres psql -U postgres -c "SELECT 1"
```

### Port Already in Use
```bash
# Check what's using the port
netstat -tln | grep :8080

# Change port in docker-compose.yml
ports:
  - "8081:80"  # Use different port
```

### Permission Issues
```bash
# Fix volume permissions
docker-compose exec p1 chown -R 1000:1000 /app/P1/data
docker-compose exec p2 chown -R 1000:1000 /app/P2/data
```

## Security

### Production Checklist

- [ ] Change default admin password
- [ ] Update Django SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS
- [ ] Use strong PostgreSQL password
- [ ] Enable SSL/TLS for Nginx
- [ ] Configure firewall rules
- [ ] Set up automated backups
- [ ] Enable container resource limits
- [ ] Configure log rotation

### Firewall Configuration
```bash
# Allow only necessary ports
sudo ufw allow 8080/tcp
sudo ufw allow 22/tcp
sudo ufw deny 5432/tcp
sudo ufw deny 8000/tcp
sudo ufw deny 8001/tcp
```

## Documentation

- `DBEAVER_SETUP.md` - DBeaver connection guide for database access
- `pgedge_agentic_examples.py` - pgEdge Agentic AI usage examples
- `DEPLOYMENT.md` - Detailed deployment guide
- `DEPLOYMENT_SUCCESS.md` - Deployment summary
- `QUICK_REFERENCE.md` - Quick command reference
- `README.md` - Original project documentation

## Support

For issues or questions:
1. Check container logs
2. Verify container status
3. Test network connectivity
4. Review Django admin configuration
5. Check database connectivity

## License

Same as original paomi-as2 project.
