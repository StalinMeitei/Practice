# Quick Reference Guide

## Access URLs

### Production (192.168.1.200)
- P1 Admin: http://192.168.1.200:8080/admin/
- P2 Admin: http://192.168.1.200:8080/p2/admin/
- Credentials: admin / admin123

### Direct Access
- P1: http://192.168.1.200:8000/admin/
- P2: http://192.168.1.200:8001/admin/

## Quick Commands

### Deploy
```powershell
cd paomi-as2
.\deploy-windows.ps1
```

### SSH to Server
```bash
ssh dev_192168_rsa
# or
ssh dev@192.168.1.200
# password: dev@2025
```

### Container Management
```bash
cd /home/dev/paomi-as2

# Status
docker-compose ps

# Logs
docker-compose logs -f
docker-compose logs -f p1
docker-compose logs -f p2

# Restart
docker-compose restart
docker-compose restart p1

# Stop/Start
docker-compose down
docker-compose up -d

# Rebuild
docker-compose up -d --build
```

### Database
```bash
# Access
docker-compose exec postgres psql -U postgres -d p1_as2_db

# Backup
docker-compose exec postgres pg_dump -U postgres p1_as2_db > backup.sql
```

## Ports

- 8080: Nginx (HTTP)
- 8443: Nginx (HTTPS)
- 8000: P1 AS2 Server
- 8001: P2 AS2 Server
- 5432: PostgreSQL

## Container Names

- `pgedge-as2` - PostgreSQL
- `p1-as2` - P1 Server
- `p2-as2` - P2 Server
- `nginx-as2` - Nginx

## Files

- `docker-compose.yml` - Container orchestration
- `Dockerfile` - Image definition
- `nginx.conf` - Nginx config
- `P1/settings.py` - P1 Django settings
- `P2/P2/settings.py` - P2 Django settings

## Troubleshooting

### Containers not starting
```bash
docker-compose logs [service_name]
docker-compose restart [service_name]
```

### Database issues
```bash
docker-compose exec postgres pg_isready
docker-compose logs postgres
```

### Network issues
```bash
docker-compose exec p1 ping p2
docker-compose exec p1 ping postgres
```

### Rebuild everything
```bash
docker-compose down -v  # Warning: removes volumes
docker-compose up -d --build
```

## Environment Variables

Set in docker-compose.yml:
- `DB_HOST` - Database host
- `DB_NAME` - Database name
- `DB_USER` - Database user
- `DB_PASSWORD` - Database password
- `ALLOWED_HOSTS` - Django allowed hosts
- `DEBUG` - Debug mode (True/False)
