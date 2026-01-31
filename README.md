# P1 & P2 AS2 Server Setup with pgEdge

This implements both P1 and P2 parts of the django-pyas2 quickstart guide using pgEdge/PostgreSQL databases. P1 and P2 are AS2 servers that can send and receive AS2 messages between each other.

## 🚨 Important: Private Key Upload

If you're getting "Invalid Private Key" errors when uploading keys in Django admin:

**→ See: [PRIVATE_KEY_FIX_SUMMARY.md](PRIVATE_KEY_FIX_SUMMARY.md)** ← Start here!

**Quick fix**: Leave the "Private Key Password" field **EMPTY** when uploading keys.

**Visual guide**: Run `.\show-key-upload-guide.ps1`

## 📚 Documentation Quick Links

| Guide | Purpose |
|-------|---------|
| [PRIVATE_KEY_FIX_SUMMARY.md](PRIVATE_KEY_FIX_SUMMARY.md) | Fix "Invalid Private Key" errors |
| [PRIVATE_KEY_TROUBLESHOOTING.md](PRIVATE_KEY_TROUBLESHOOTING.md) | Detailed troubleshooting |
| [PGEDGE_QUICK_START.md](PGEDGE_QUICK_START.md) | pgEdge Agentic AI quick start |
| [DBEAVER_SETUP.md](DBEAVER_SETUP.md) | Connect DBeaver to database |
| [README_DOCKER.md](README_DOCKER.md) | Docker deployment guide |

## Project Structure

```
.
├── P1/                         # P1 AS2 Server (Port 8000)
│   ├── P1/                     # Django project settings
│   │   ├── settings.py         # P1 configuration (pgEdge)
│   │   └── urls.py            # P1 URL routing
│   ├── data/                  # P1 AS2 data directory
│   ├── start_p1_pgedge.py     # P1 startup script (pgEdge)
│   └── manage.py             # P1 Django management
├── P2/                         # P2 AS2 Server (Port 8001)
│   ├── P2/                     # Django project settings
│   │   ├── settings.py         # P2 configuration (pgEdge)
│   │   └── urls.py            # P2 URL routing
│   ├── data/                  # P2 AS2 data directory
│   ├── start_p2_pgedge.py     # P2 startup script (pgEdge)
│   └── manage.py             # P2 Django management
├── P1_private.pem             # P1 private key + certificate
├── P1_public.pem              # P1 public certificate
├── P2_private.pem             # P2 private key + certificate
├── P2_public.pem              # P2 public certificate
├── generate_certificates.py   # Certificate generation script
├── setup_pgedge_both.py      # Complete pgEdge setup script
├── setup_p1_pgedge.py        # P1 AS2 configuration script
├── setup_p2_pgedge.py        # P2 AS2 configuration script
├── test_file_transfer_pgedge.py # File transfer test script
└── README.md                 # This file
```

## Prerequisites

- Python 3.6+
- pgEdge or PostgreSQL database server
- Network access to your database server

## Quick Start with pgEdge

### 1. Install Dependencies

```bash
pip install django django-pyas2 psycopg2-binary
```

### 2. Setup pgEdge Database

#### Option A: pgEdge Cloud (Recommended)
1. Visit [pgEdge Cloud](https://www.pgedge.com/cloud)
2. Create an account and database cluster
3. Note your connection details

#### Option B: Local pgEdge Installation
1. Download from [pgEdge Downloads](https://www.pgedge.com/download)
2. Follow installation instructions
3. Start the pgEdge service

#### Option C: Docker PostgreSQL (Alternative)
```bash
docker run --name pgedge-as2 -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:15
```

### 3. Configure Database Connection

Set environment variables for your pgEdge connection:

```bash
# For pgEdge Cloud
export DB_HOST=your-pgedge-host.com
export DB_PORT=5432
export DB_USER=your_username
export DB_PASSWORD=your_password

# For local setup
export DB_HOST=localhost
export DB_PORT=5432
export DB_USER=postgres
export DB_PASSWORD=postgres
```

### 4. Complete Setup (Automated)

```bash
python setup_pgedge_both.py
```

This script will:
- Test pgEdge connection
- Generate SSL certificates for both servers
- Create separate databases (p1_as2_db and p2_as2_db)
- Set up P1 and P2 Django projects
- Run database migrations
- Create admin users
- Configure AS2 organizations and partners
- Create startup scripts

### 5. Start Both Servers

**Terminal 1 (P1):**
```bash
cd P1
python start_p1_pgedge.py
```

**Terminal 2 (P2):**
```bash
cd P2
python start_p2_pgedge.py
```

### 6. Test File Transfer

```bash
python test_file_transfer_pgedge.py
```

## Access Points

### P1 Server (Port 8000)
- **Admin Interface**: http://127.0.0.1:8000/admin/
- **AS2 Endpoint**: http://127.0.0.1:8000/pyas2/as2receive
- **PyAS2 Management**: http://127.0.0.1:8000/admin/pyas2/
- **Login**: admin / admin123
- **Database**: p1_as2_db

### P2 Server (Port 8001)
- **Admin Interface**: http://127.0.0.1:8001/admin/
- **AS2 Endpoint**: http://127.0.0.1:8001/pyas2/as2receive
- **PyAS2 Management**: http://127.0.0.1:8001/admin/pyas2/
- **Login**: admin / admin123
- **Database**: p2_as2_db

## Configuration Details

### P1 Configuration (pgEdge)
- **AS2 ID**: P1
- **Organization**: P1 Organization
- **Email**: admin@p1.com
- **Database**: p1_as2_db
- **Partner**: P2 (target: http://127.0.0.1:8001/pyas2/as2receive)
- **Encryption**: AES-128-CBC
- **Signature**: SHA-256
- **MDN Mode**: Synchronous

### P2 Configuration (pgEdge)
- **AS2 ID**: P2
- **Organization**: P2 Organization
- **Email**: admin@p2.com
- **Database**: p2_as2_db
- **Partner**: P1 (target: http://127.0.0.1:8000/pyas2/as2receive)
- **Encryption**: AES-128-CBC
- **Signature**: SHA-256
- **MDN Mode**: Synchronous

## Manual Setup (Alternative)

If you prefer manual setup:

### 1. Generate Certificates
```bash
python generate_certificates.py
```

### 2. Setup Databases
```bash
# Set your database connection variables
export DB_HOST=your_host
export DB_USER=your_user
export DB_PASSWORD=your_password

# Create databases
python -c "
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
conn = psycopg2.connect(host='$DB_HOST', user='$DB_USER', password='$DB_PASSWORD', database='postgres')
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = conn.cursor()
cursor.execute('CREATE DATABASE p1_as2_db')
cursor.execute('CREATE DATABASE p2_as2_db')
conn.close()
"
```

### 3. Setup P1
```bash
cd P1
python manage.py migrate
python manage.py createsuperuser
python ../setup_p1_pgedge.py
```

### 4. Setup P2
```bash
cd P2
python manage.py migrate
python manage.py createsuperuser
python ../setup_p2_pgedge.py
```

## pgEdge Specific Features

### Database Separation
- P1 uses database: `p1_as2_db`
- P2 uses database: `p2_as2_db`
- Complete isolation between servers
- Independent scaling and backup

### Connection Pooling
pgEdge provides built-in connection pooling for better performance:
- Automatic connection management
- Reduced connection overhead
- Better resource utilization

### High Availability
With pgEdge Cloud:
- Automatic failover
- Multi-region deployment
- Backup and recovery

## Testing File Transfer

### Using Management Command
```bash
cd P1
python manage.py sendas2message --partner P2 --file path/to/your/file.edi
```

### Using Test Script
```bash
python test_file_transfer_pgedge.py
```

### Using Admin Interface
1. Go to P1 admin: http://127.0.0.1:8000/admin/pyas2/
2. Create a new message
3. Select P2 as partner
4. Upload your file
5. Send the message

### Monitoring with pgEdge
- Use pgEdge monitoring tools
- Check database performance metrics
- Monitor connection usage
- Review query performance

## Troubleshooting

### Database Connection Issues

1. **Connection refused**
   ```bash
   # Check if pgEdge is running
   pg_isready -h $DB_HOST -p $DB_PORT
   
   # Test connection
   psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d postgres
   ```

2. **Authentication failed**
   - Verify username and password
   - Check pgEdge user permissions
   - Ensure database exists

3. **Network issues**
   - Check firewall settings
   - Verify network connectivity
   - Check pgEdge configuration

### AS2 Message Issues

1. **Partner not found**
   - Check AS2 partner configuration
   - Verify AS2 identifiers match

2. **Certificate errors**
   - Regenerate certificates: `python generate_certificates.py`
   - Check certificate validity
   - Verify certificate format

3. **Connection timeout**
   - Check if target server is running
   - Verify network connectivity
   - Check firewall rules

### Performance Optimization

1. **Database tuning**
   - Configure pgEdge connection pooling
   - Optimize database parameters
   - Monitor query performance

2. **AS2 optimization**
   - Enable message compression
   - Configure appropriate timeouts
   - Monitor message queue

## Advanced Configuration

### Custom pgEdge Settings
Update Django settings for pgEdge-specific features:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'your_pgedge_host',
        'PORT': '5432',
        'OPTIONS': {
            'sslmode': 'require',  # For pgEdge Cloud
            'connect_timeout': 10,
            'options': '-c default_transaction_isolation=serializable'
        },
        'CONN_MAX_AGE': 600,  # Connection pooling
    }
}
```

### Backup and Recovery
With pgEdge:
- Automated backups
- Point-in-time recovery
- Cross-region replication

### Monitoring and Alerting
- pgEdge monitoring dashboard
- Custom alerts for AS2 failures
- Performance metrics tracking

## Support

For pgEdge-specific issues:
- [pgEdge Documentation](https://www.pgedge.com/docs)
- [pgEdge Support](https://www.pgedge.com/support)

For django-pyas2 issues:
- [Documentation](https://django-pyas2.readthedocs.io/)
- [GitHub Repository](https://github.com/abhishek-ram/django-pyas2)
- [PyPI Package](https://pypi.org/project/django-pyas2/)