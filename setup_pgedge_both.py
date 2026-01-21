#!/usr/bin/env python
"""
Setup both P1 and P2 AS2 servers with pgEdge/PostgreSQL
"""
import os
import sys
import subprocess
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from pathlib import Path

def get_db_config(project_name):
    """Get database configuration for a project"""
    return {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': os.getenv('DB_PORT', '5432'),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', 'postgres'),
        'database': f'{project_name.lower()}_as2_db'
    }

def create_database(project_name):
    """Create database for a project"""
    config = get_db_config(project_name)
    
    try:
        # Connect to PostgreSQL server (default database)
        conn = psycopg2.connect(
            host=config['host'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            database='postgres'  # Connect to default database first
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (config['database'],))
        exists = cursor.fetchone()
        
        if not exists:
            # Create database
            cursor.execute(f"CREATE DATABASE {config['database']}")
            print(f"✓ Database '{config['database']}' created successfully!")
        else:
            print(f"✓ Database '{config['database']}' already exists.")
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.Error as e:
        print(f"✗ Error connecting to PostgreSQL for {project_name}: {e}")
        print(f"\nConnection details:")
        print(f"  Host: {config['host']}")
        print(f"  Port: {config['port']}")
        print(f"  User: {config['user']}")
        print(f"  Database: {config['database']}")
        return False

def test_connection(project_name):
    """Test connection to the target database"""
    config = get_db_config(project_name)
    
    try:
        conn = psycopg2.connect(
            host=config['host'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            database=config['database']
        )
        conn.close()
        print(f"✓ Successfully connected to {project_name} database")
        return True
    except psycopg2.Error as e:
        print(f"✗ Failed to connect to {project_name} database: {e}")
        return False

def update_settings_for_pgedge(project_name):
    """Update Django settings to use the correct database"""
    config = get_db_config(project_name)
    
    settings_file = Path(project_name) / project_name / 'settings.py'
    
    # Read current settings
    with open(settings_file, 'r') as f:
        content = f.read()
    
    # Update database configuration
    db_config = f"""DATABASES = {{
    'default': {{
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '{config['database']}',
        'USER': '{config['user']}',
        'PASSWORD': '{config['password']}',
        'HOST': '{config['host']}',
        'PORT': '{config['port']}',
    }}
}}"""
    
    # Replace the database configuration
    import re
    pattern = r'DATABASES\s*=\s*\{[^}]*\{[^}]*\}[^}]*\}'
    if re.search(pattern, content):
        content = re.sub(pattern, db_config, content)
    else:
        # If pattern not found, append at the end
        content += f"\n\n# Database Configuration\n{db_config}\n"
    
    # Write back to file
    with open(settings_file, 'w') as f:
        f.write(content)
    
    print(f"✓ Updated {project_name} settings for pgEdge")

def run_command(command, cwd=None):
    """Run a shell command"""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error running command: {command}")
            print(f"Error output: {result.stderr}")
            return False
        if result.stdout.strip():
            print(result.stdout.strip())
        return True
    except Exception as e:
        print(f"Exception running command {command}: {e}")
        return False

def setup_project(project_name, port):
    """Setup a single AS2 project with pgEdge"""
    print(f"\n{'='*50}")
    print(f"Setting up {project_name} AS2 Server with pgEdge")
    print(f"{'='*50}")
    
    # Create database
    if not create_database(project_name):
        return False
    
    # Test connection
    if not test_connection(project_name):
        return False
    
    # Update settings
    update_settings_for_pgedge(project_name)
    
    # Run migrations
    print(f"Running {project_name} migrations...")
    if not run_command("python manage.py migrate", cwd=project_name):
        return False
    print(f"✓ {project_name} migrations completed")
    
    # Create superuser
    print(f"Creating {project_name} admin user...")
    create_user_cmd = f"python manage.py shell -c \"from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@{project_name.lower()}.com', 'admin123')\""
    if not run_command(create_user_cmd, cwd=project_name):
        return False
    print(f"✓ {project_name} admin user created (admin/admin123)")
    
    # Create data directory
    data_dir = Path(project_name) / 'data'
    data_dir.mkdir(exist_ok=True)
    print(f"✓ {project_name} data directory created")
    
    print(f"✓ {project_name} setup completed successfully!")
    return True

def setup_as2_configuration():
    """Setup AS2 organizations and partners for both servers"""
    print(f"\n{'='*50}")
    print("Setting up AS2 Organizations and Partners")
    print(f"{'='*50}")
    
    # Setup P1 AS2 configuration
    print("Configuring P1 AS2 settings...")
    if not run_command("python ../setup_p1_pgedge.py", cwd="P1"):
        print("✗ Failed to configure P1 AS2 settings")
        return False
    
    # Setup P2 AS2 configuration
    print("Configuring P2 AS2 settings...")
    if not run_command("python ../setup_p2_pgedge.py", cwd="P2"):
        print("✗ Failed to configure P2 AS2 settings")
        return False
    
    print("✓ AS2 configuration completed for both servers")
    return True

def create_startup_scripts():
    """Create startup scripts for both servers"""
    
    # P1 startup script
    p1_script = """#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'P1.settings')
django.setup()

print("Starting P1 AS2 Server on http://127.0.0.1:8000")
print("Admin: http://127.0.0.1:8000/admin/ (admin/admin123)")
print("AS2 Endpoint: http://127.0.0.1:8000/pyas2/as2receive")
print("Press Ctrl+C to stop")

from django.core.management import execute_from_command_line
execute_from_command_line(['manage.py', 'runserver'])
"""
    
    # P2 startup script
    p2_script = """#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'P2.settings')
django.setup()

print("Starting P2 AS2 Server on http://127.0.0.1:8001")
print("Admin: http://127.0.0.1:8001/admin/ (admin/admin123)")
print("AS2 Endpoint: http://127.0.0.1:8001/pyas2/as2receive")
print("Press Ctrl+C to stop")

from django.core.management import execute_from_command_line
execute_from_command_line(['manage.py', 'runserver', '127.0.0.1:8001'])
"""
    
    with open('P1/start_p1_pgedge.py', 'w') as f:
        f.write(p1_script)
    
    with open('P2/start_p2_pgedge.py', 'w') as f:
        f.write(p2_script)
    
    print("✓ pgEdge startup scripts created:")
    print("  - P1/start_p1_pgedge.py")
    print("  - P2/start_p2_pgedge.py")

def main():
    """Main setup function"""
    print("Setting up P1 and P2 AS2 Servers with pgEdge")
    print("=" * 60)
    
    # Check database connection first
    print("Checking pgEdge/PostgreSQL connection...")
    config = get_db_config('test')
    try:
        conn = psycopg2.connect(
            host=config['host'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            database='postgres'
        )
        conn.close()
        print("✓ PostgreSQL/pgEdge connection successful")
    except psycopg2.Error as e:
        print(f"✗ Cannot connect to PostgreSQL/pgEdge: {e}")
        print("\nPlease ensure:")
        print("1. PostgreSQL/pgEdge is running")
        print("2. Connection credentials are correct")
        print("3. Set environment variables if needed:")
        print("   export DB_HOST=your_host")
        print("   export DB_PORT=your_port")
        print("   export DB_USER=your_username")
        print("   export DB_PASSWORD=your_password")
        return False
    
    # Check if certificates exist
    cert_files = ['P1_private.pem', 'P1_public.pem', 'P2_private.pem', 'P2_public.pem']
    missing_certs = [f for f in cert_files if not Path(f).exists()]
    
    if missing_certs:
        print("Generating certificates...")
        if not run_command("python generate_certificates.py"):
            print("✗ Failed to generate certificates")
            return False
        print("✓ Certificates generated")
    else:
        print("✓ All certificates present")
    
    # Setup P1
    if not setup_project('P1', 8000):
        return False
    
    # Setup P2
    if not setup_project('P2', 8001):
        return False
    
    # Setup AS2 configuration for both servers
    if not setup_as2_configuration():
        print("⚠ AS2 configuration failed, but servers are set up")
        print("You can configure AS2 settings manually via admin interface")
    
    # Create startup scripts
    create_startup_scripts()
    
    print("\n" + "=" * 60)
    print("✓ Both P1 and P2 AS2 Servers setup completed with pgEdge!")
    print("\nDatabase Information:")
    p1_config = get_db_config('P1')
    p2_config = get_db_config('P2')
    print(f"P1 Database: {p1_config['database']} on {p1_config['host']}:{p1_config['port']}")
    print(f"P2 Database: {p2_config['database']} on {p2_config['host']}:{p2_config['port']}")
    
    print("\nTo start the servers:")
    print("1. Terminal 1: cd P1 && python start_p1_pgedge.py")
    print("2. Terminal 2: cd P2 && python start_p2_pgedge.py")
    
    print("\nAccess points:")
    print("P1 Admin: http://127.0.0.1:8000/admin/ (admin/admin123)")
    print("P1 AS2: http://127.0.0.1:8000/pyas2/as2receive")
    print("P2 Admin: http://127.0.0.1:8001/admin/ (admin/admin123)")
    print("P2 AS2: http://127.0.0.1:8001/pyas2/as2receive")
    
    print("\nNext steps:")
    print("1. Configure AS2 organizations and partners via admin interface")
    print("2. Test file transfer between P1 and P2")
    
    return True

if __name__ == "__main__":
    try:
        if not main():
            sys.exit(1)
    except KeyboardInterrupt:
        print("\nSetup interrupted.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)