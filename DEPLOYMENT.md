# Deployment Guide for paomi-as2

This guide covers deploying the containerized paomi-as2 application to a remote server.

## Architecture

The deployment includes:
- **PostgreSQL (pgedge)**: Database for both P1 and P2 servers
- **P1 AS2 Server**: Running on port 8000 with Gunicorn
- **P2 AS2 Server**: Running on port 8001 with Gunicorn
- **Nginx**: Reverse proxy on port 80

## Prerequisites

### On Your Local Machine
- Git
- SSH access to remote server
- SSH config already set up (dev_192168_rsa)

### On Remote Server (192.168.1.200)
- Docker and Docker Compose installed
- User: dev with password: dev@2025
- Ports 80, 8000, 8001, 5432 available

## Quick Deployment

### Option 1: Using SSH Config (Recommended)
```bash
cd paomi-as2
chmod +x deploy-simple.sh
./deploy-simple.sh
```

### Option 2: Manual Deployment
```bash
# 1. Create package
tar -czf paomi-as2.tar.gz --exclude='.git' --exclude='__pycache__' .

# 2. Copy to server
scp paomi-as2.tar.gz dev@192.168.1.200:/tmp/

# 3. SSH to server
ssh dev@192.168.1.200

# 4. Extract and deploy
cd /home/dev
mkdir -p paomi-as2
cd paomi-as2
tar -xzf /tmp/paomi-as2.tar.gz
docker-compose up -d --build

# 5. Check status
docker-compose ps
docker-compose logs -f
```

## Access Points

After deployment, access the application at:

- **P1 Admin Interface**: http://192.168.1.200/admin/
  - Username: admin
  - Password: admin123

- **P2 Admin Interface**: http://192.168.1.200/p2/admin/
  - Username: admin
  - Password: admin123

- **P1 AS2 Endpoint**: http://192.168.1.200/pyas2/as2receive
- **P2 AS2 Endpoint**: http://192.168.1.200/p2/pyas2/as2receive

## Initial Setup

After first deployment, you need to create admin users and configure AS2 partners:

```bash
# SSH to server
ssh dev@192.168.1.200
cd /home/dev/paomi-as2

# Create P1 admin user
docker-compose exec p1 python manage.py createsuperuser

# Create P2 admin user
docker-compose exec p2 python manage.py createsuperuser

# Or use the automated setup script
docker-compose exec p1 python /app/setup_p1_pgedge.py
docker-compose exec p2 python /app/setup_p2_pgedge.py
```

## Management Commands

### View Logs
```bash
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
```

### Stop/Start
```bash
# Stop all
docker-compose down

# Start all
docker-compose up -d

# Rebuild and start
docker-compose up -d --build
```

### Database Access
```bash
# Access PostgreSQL
docker-compose exec postgres psql -U postgres -d p1_as2_db
docker-compose exec postgres psql -U postgres -d p2_as2_db

# Backup database
docker-compose exec postgres pg_dump -U postgres p1_as2_db > p1_backup.sql
docker-compose exec postgres pg_dump -U postgres p2_as2_db > p2_backup.sql
```

### Django Management
```bash
# P1 migrations
docker-compose exec p1 python manage.py migrate
docker-compose exec p1 python manage.py makemigrations

# P2 migrations
docker-compose exec p2 python manage.py migrate
docker-compose exec p2 python manage.py makemigrations

# Collect static files
docker-compose exec p1 python manage.py collectstatic --noinput
docker-compose exec p2 python manage.py collectstatic --noinput
```

## Troubleshooting

### Container Issues
```bash
# Check container status
docker-compose ps

# Check container logs
docker-compose logs -f [service_name]

# Restart container
docker-compose restart [service_name]

# Rebuild container
docker-compose up -d --build [service_name]
```

### Database Connection Issues
```bash
# Check if PostgreSQL is running
docker-compose exec postgres pg_isready

# Check database exists
docker-compose exec postgres psql -U postgres -c "\l"

# Recreate databases
docker-compose exec postgres psql -U postgres -c "DROP DATABASE IF EXISTS p1_as2_db;"
docker-compose exec postgres psql -U postgres -c "DROP DATABASE IF EXISTS p2_as2_db;"
docker-compose exec postgres psql -U postgres -c "CREATE DATABASE p1_as2_db;"
docker-compose exec postgres psql -U postgres -c "CREATE DATABASE p2_as2_db;"
```

### Network Issues
```bash
# Check network
docker network ls
docker network inspect paomi-as2_as2-network

# Test connectivity between containers
docker-compose exec p1 ping postgres
docker-compose exec p1 ping p2
```

### Nginx Issues
```bash
# Test nginx configuration
docker-compose exec nginx nginx -t

# Reload nginx
docker-compose exec nginx nginx -s reload

# Check nginx logs
docker-compose logs nginx
```

## Security Considerations

### Production Deployment
Before deploying to production:

1. **Change default passwords**:
   - Update admin passwords
   - Change PostgreSQL password
   - Update Django SECRET_KEY

2. **Enable HTTPS**:
   - Add SSL certificates to nginx
   - Update nginx.conf for SSL
   - Update CSRF_TRUSTED_ORIGINS

3. **Disable DEBUG mode**:
   - Set DEBUG=False in environment
   - Configure proper logging

4. **Firewall Configuration**:
   - Only expose port 80/443
   - Restrict database access
   - Use internal Docker network

5. **Regular Updates**:
   - Keep Docker images updated
   - Update Python dependencies
   - Apply security patches

## Monitoring

### Health Checks
```bash
# Check all services
docker-compose ps

# Check specific endpoints
curl http://192.168.1.200/admin/
curl http://192.168.1.200/p2/admin/
```

### Resource Usage
```bash
# Container stats
docker stats

# Disk usage
docker system df
```

## Backup and Recovery

### Backup
```bash
# Backup databases
docker-compose exec postgres pg_dump -U postgres p1_as2_db > backup/p1_$(date +%Y%m%d).sql
docker-compose exec postgres pg_dump -U postgres p2_as2_db > backup/p2_$(date +%Y%m%d).sql

# Backup volumes
docker run --rm -v paomi-as2_p1_data:/data -v $(pwd)/backup:/backup alpine tar czf /backup/p1_data.tar.gz /data
docker run --rm -v paomi-as2_p2_data:/data -v $(pwd)/backup:/backup alpine tar czf /backup/p2_data.tar.gz /data
```

### Restore
```bash
# Restore database
cat backup/p1_20260130.sql | docker-compose exec -T postgres psql -U postgres p1_as2_db
cat backup/p2_20260130.sql | docker-compose exec -T postgres psql -U postgres p2_as2_db
```

## Support

For issues or questions:
- Check logs: `docker-compose logs -f`
- Review Django admin for AS2 configuration
- Verify network connectivity between containers
- Check PostgreSQL connection and database status
