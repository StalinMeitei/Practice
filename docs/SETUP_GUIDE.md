# Complete Setup Guide for P1 & P2 AS2 Servers with pgEdge

This guide provides multiple options for setting up the P1 and P2 AS2 servers with different database backends.

## Option 1: Quick Setup with Docker PostgreSQL (Recommended for Testing)

### Prerequisites
- Docker Desktop installed
- Python 3.6+ with pip

### Steps
1. **Setup Docker PostgreSQL**
   ```bash
   python setup_docker_postgres.py
   ```

2. **Setup AS2 Servers**
   ```bash
   python setup_pgedge_both.py
   ```

3. **Start Servers**
   ```bash
   # Terminal 1
   cd P1
   python start_p1_pgedge.py
   
   # Terminal 2
   cd P2
   python start_p2_pgedge.py
   ```

4. **Test File Transfer**
   ```bash
   python test_file_transfer_pgedge.py
   ```

## Option 2: pgEdge Cloud (Recommended for Production)

### Prerequisites
- pgEdge Cloud account
- Python 3.6+ with pip

### Steps
1. **Create pgEdge Cloud Database**
   - Visit [pgEdge Cloud](https://www.pgedge.com/cloud)
   - Create account and database cluster
   - Note connection details

2. **Set Environment Variables**
   ```bash
   export DB_HOST=your-pgedge-host.com
   export DB_PORT=5432
   export DB_USER=your_username
   export DB_PASSWORD=your_password
   ```

3. **Setup AS2 Servers**
   ```bash
   python setup_pgedge_both.py
   ```

4. **Start and Test** (same as Option 1, steps 3-4)

## Option 3: Local pgEdge Installation

### Prerequisites
- pgEdge software installed locally
- Python 3.6+ with pip

### Steps
1. **Install pgEdge**
   - Download from [pgEdge Downloads](https://www.pgedge.com/download)
   - Follow installation instructions for your OS
   - Start pgEdge service

2. **Configure Connection**
   ```bash
   export DB_HOST=localhost
   export DB_PORT=5432
   export DB_USER=your_pgedge_user
   export DB_PASSWORD=your_pgedge_password
   ```

3. **Setup AS2 Servers**
   ```bash
   python setup_pgedge_both.py
   ```

4. **Start and Test** (same as Option 1, steps 3-4)

## Option 4: Existing PostgreSQL Server

### Prerequisites
- Existing PostgreSQL server
- Database admin access
- Python 3.6+ with pip

### Steps
1. **Configure Connection**
   ```bash
   export DB_HOST=your_postgres_host
   export DB_PORT=5432
   export DB_USER=your_username
   export DB_PASSWORD=your_password
   ```

2. **Setup AS2 Servers**
   ```bash
   python setup_pgedge_both.py
   ```

3. **Start and Test** (same as Option 1, steps 3-4)

## Verification Steps

After setup, verify everything is working:

### 1. Check Database Connections
```bash
# Test P1 database
python -c "
import psycopg2
conn = psycopg2.connect(host='localhost', port='5432', user='postgres', password='postgres', database='p1_as2_db')
print('P1 database: OK')
conn.close()
"

# Test P2 database
python -c "
import psycopg2
conn = psycopg2.connect(host='localhost', port='5432', user='postgres', password='postgres', database='p2_as2_db')
print('P2 database: OK')
conn.close()
"
```

### 2. Check Web Interfaces
- P1 Admin: http://127.0.0.1:8000/admin/ (admin/admin123)
- P2 Admin: http://127.0.0.1:8001/admin/ (admin/admin123)

### 3. Check AS2 Configuration
- P1 PyAS2: http://127.0.0.1:8000/admin/pyas2/
- P2 PyAS2: http://127.0.0.1:8001/admin/pyas2/

### 4. Test File Transfer
```bash
python test_file_transfer_pgedge.py
```

## Troubleshooting

### Database Connection Issues

**Error: Connection refused**
```bash
# Check if PostgreSQL is running
docker ps | grep pgedge-as2  # For Docker setup
# or
pg_isready -h localhost -p 5432  # For local PostgreSQL
```

**Error: Authentication failed**
- Verify username and password
- Check environment variables
- Ensure user has database creation privileges

**Error: Database does not exist**
- The setup script creates databases automatically
- Ensure user has CREATE DATABASE privileges

### AS2 Configuration Issues

**Error: Certificate not found**
```bash
# Regenerate certificates
python generate_certificates.py
```

**Error: Partner configuration failed**
- Check admin interface manually
- Verify certificates are loaded correctly
- Check AS2 identifiers match

### Server Startup Issues

**Error: Port already in use**
```bash
# Check what's using the port
netstat -an | findstr :8000
netstat -an | findstr :8001

# Kill processes if needed
taskkill /F /PID <process_id>
```

**Error: Django configuration**
- Check settings.py files
- Verify database configuration
- Check installed apps

### File Transfer Issues

**Error: Connection timeout**
- Ensure both servers are running
- Check firewall settings
- Verify target URLs in partner configuration

**Error: Certificate validation failed**
- Check certificate validity
- Verify certificate format (PEM)
- Ensure certificates match partner configuration

## Performance Tuning

### Database Optimization
```python
# Add to Django settings.py
DATABASES = {
    'default': {
        # ... existing config ...
        'CONN_MAX_AGE': 600,  # Connection pooling
        'OPTIONS': {
            'MAX_CONNS': 20,
            'MIN_CONNS': 5,
        }
    }
}
```

### AS2 Optimization
- Enable message compression for large files
- Configure appropriate timeouts
- Monitor message queue size
- Use asynchronous MDNs for high volume

## Security Considerations

### Database Security
- Use strong passwords
- Enable SSL connections for remote databases
- Restrict database access by IP
- Regular security updates

### AS2 Security
- Use strong encryption (AES-256)
- Enable message signing
- Validate certificates regularly
- Monitor for failed authentication attempts

### Network Security
- Use HTTPS for AS2 endpoints in production
- Configure firewalls appropriately
- Use VPN for remote connections
- Monitor network traffic

## Production Deployment

### Database
- Use pgEdge Cloud or managed PostgreSQL
- Set up automated backups
- Configure high availability
- Monitor performance metrics

### Application
- Use production WSGI server (gunicorn, uWSGI)
- Configure reverse proxy (nginx, Apache)
- Set up SSL certificates
- Configure logging and monitoring

### Infrastructure
- Use container orchestration (Docker, Kubernetes)
- Set up load balancing
- Configure auto-scaling
- Implement disaster recovery

## Support and Resources

### Documentation
- [django-pyas2 Documentation](https://django-pyas2.readthedocs.io/)
- [pgEdge Documentation](https://www.pgedge.com/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

### Community
- [django-pyas2 GitHub](https://github.com/abhishek-ram/django-pyas2)
- [pgEdge Community](https://www.pgedge.com/community)
- [PostgreSQL Community](https://www.postgresql.org/community/)

### Commercial Support
- [pgEdge Support](https://www.pgedge.com/support)
- [PostgreSQL Professional Services](https://www.postgresql.org/support/professional_support/)