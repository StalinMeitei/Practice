# Deployment Successful! 🎉

The paomi-as2 application has been successfully deployed to **192.168.1.200**.

## Deployment Summary

### Architecture
- **PostgreSQL Database (pgedge)**: Running on port 5432
- **P1 AS2 Server**: Running on port 8000 with Gunicorn (3 workers)
- **P2 AS2 Server**: Running on port 8001 with Gunicorn (3 workers)
- **Nginx Reverse Proxy**: Running on port 8080 (port 80 was in use)

### Access Points

#### Via Nginx (Recommended)
- **P1 Admin**: http://192.168.1.200:8080/admin/
- **P2 Admin**: http://192.168.1.200:8080/p2/admin/
- **P1 AS2 Endpoint**: http://192.168.1.200:8080/pyas2/as2receive
- **P2 AS2 Endpoint**: http://192.168.1.200:8080/p2/pyas2/as2receive

#### Direct Access
- **P1 Direct**: http://192.168.1.200:8000/admin/
- **P2 Direct**: http://192.168.1.200:8001/admin/

### Default Credentials
- **Username**: admin
- **Password**: admin123

## Container Status

All containers are running:
- `pgedge-as2` - PostgreSQL database (healthy)
- `p1-as2` - P1 AS2 server
- `p2-as2` - P2 AS2 server
- `nginx-as2` - Nginx reverse proxy

## Management Commands

### View Logs
```bash
ssh dev@192.168.1.200
cd /home/dev/paomi-as2

# All services
docker-compose logs -f

# Specific service
docker-compose logs -f p1
docker-compose logs -f p2
docker-compose logs -f nginx
docker-compose logs -f postgres
```

### Restart Services
```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart p1
docker-compose restart p2
docker-compose restart nginx
```

### Stop/Start
```bash
# Stop all
docker-compose down

# Start all
docker-compose up -d
```

### Check Status
```bash
docker-compose ps
```

## Initial Configuration

### Create Admin Users (if needed)
```bash
# P1 admin
docker-compose exec p1 python manage.py createsuperuser

# P2 admin
docker-compose exec p2 python manage.py createsuperuser
```

### Configure AS2 Organizations and Partners

1. **Access P1 Admin**: http://192.168.1.200:8080/admin/
   - Login with admin/admin123
   - Go to PyAS2 section
   - Create Organization for P1
   - Upload P1 certificates
   - Create Partner for P2 with target URL: http://p2:8001/pyas2/as2receive

2. **Access P2 Admin**: http://192.168.1.200:8080/p2/admin/
   - Login with admin/admin123
   - Go to PyAS2 section
   - Create Organization for P2
   - Upload P2 certificates
   - Create Partner for P1 with target URL: http://p1:8000/pyas2/as2receive

## Database Access

```bash
# Access PostgreSQL
docker-compose exec postgres psql -U postgres -d p1_as2_db
docker-compose exec postgres psql -U postgres -d p2_as2_db

# List databases
docker-compose exec postgres psql -U postgres -c "\l"
```

## Backup

### Database Backup
```bash
docker-compose exec postgres pg_dump -U postgres p1_as2_db > p1_backup.sql
docker-compose exec postgres pg_dump -U postgres p2_as2_db > p2_backup.sql
```

### Full Backup
```bash
cd /home/dev
tar -czf paomi-as2-backup-$(date +%Y%m%d).tar.gz paomi-as2/
```

## Troubleshooting

### Check Container Logs
```bash
docker-compose logs --tail=100 [service_name]
```

### Restart a Service
```bash
docker-compose restart [service_name]
```

### Rebuild and Restart
```bash
docker-compose down
docker-compose up -d --build
```

### Check Network Connectivity
```bash
# Test P1 to P2
docker-compose exec p1 ping p2

# Test P1 to database
docker-compose exec p1 ping postgres
```

## Redeployment

To redeploy with updates:

```bash
# From your local machine
cd paomi-as2
.\deploy-windows.ps1
```

Or manually:
```bash
# On the server
cd /home/dev/paomi-as2
git pull  # if using git
docker-compose down
docker-compose build
docker-compose up -d
```

## Security Notes

### For Production Use:
1. **Change default passwords** immediately
2. **Update Django SECRET_KEY** in settings
3. **Set DEBUG=False** in production
4. **Configure SSL/TLS** for nginx
5. **Use strong PostgreSQL password**
6. **Restrict firewall rules** to only necessary ports
7. **Enable HTTPS** and update CSRF_TRUSTED_ORIGINS

### Firewall Configuration
```bash
# Allow only necessary ports
sudo ufw allow 8080/tcp  # Nginx
sudo ufw allow 22/tcp    # SSH
sudo ufw deny 5432/tcp   # PostgreSQL (internal only)
sudo ufw deny 8000/tcp   # P1 (internal only)
sudo ufw deny 8001/tcp   # P2 (internal only)
```

## Next Steps

1. ✅ Deployment completed
2. ⏳ Configure AS2 organizations and partners via admin interface
3. ⏳ Upload SSL certificates for P1 and P2
4. ⏳ Test AS2 message exchange between P1 and P2
5. ⏳ Configure production security settings
6. ⏳ Set up monitoring and alerting
7. ⏳ Configure automated backups

## Support

For issues:
1. Check container logs: `docker-compose logs -f`
2. Verify container status: `docker-compose ps`
3. Check network connectivity between containers
4. Review Django admin for AS2 configuration
5. Verify database connectivity

## Files Created

- `Dockerfile` - Container image definition
- `docker-compose.yml` - Multi-container orchestration
- `nginx.conf` - Nginx reverse proxy configuration
- `init-db.sh` - Database initialization script
- `init_as2_config.py` - AS2 configuration script
- `deploy-windows.ps1` - Windows deployment script
- `deploy-simple.sh` - Simple bash deployment script
- `start-local.sh` - Local testing script
- `DEPLOYMENT.md` - Detailed deployment guide
- `.dockerignore` - Docker build exclusions

## Deployment Complete! ✅

Your AS2 servers are now running and ready for configuration.
