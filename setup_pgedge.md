# Setting up pgEdge for P1 AS2 Server

## Option 1: Install pgEdge Cloud (Recommended)

1. Visit [pgEdge Cloud](https://www.pgedge.com/cloud) and create an account
2. Create a new database cluster
3. Note down the connection details provided
4. Update the database configuration in `P1/settings.py`

## Option 2: Install pgEdge Locally

1. Download pgEdge from [https://www.pgedge.com/download](https://www.pgedge.com/download)
2. Follow the installation instructions for your platform
3. Create a database for the P1 AS2 server

## Option 3: Use Regular PostgreSQL (Fallback)

If pgEdge is not available, you can use regular PostgreSQL:

### Windows:
1. Download PostgreSQL from [https://www.postgresql.org/download/windows/](https://www.postgresql.org/download/windows/)
2. Install with default settings
3. Remember the password you set for the 'postgres' user

### Using Docker:
```bash
docker run --name postgres-p1 -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:15
```

## Database Configuration

Update the database settings in `P1/settings.py` with your connection details:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_name',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'your_host',  # e.g., 'localhost' or pgEdge cloud host
        'PORT': 'your_port',  # e.g., '5432'
    }
}
```

## Next Steps

After setting up the database:

1. Run migrations: `python manage.py migrate`
2. Run the P1 setup: `python setup_p1.py`
3. Start the server: `python manage.py runserver`