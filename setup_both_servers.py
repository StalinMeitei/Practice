#!/usr/bin/env python
"""
Complete setup script for both P1 and P2 AS2 servers
"""
import os
import sys
import subprocess
import django
from pathlib import Path

def setup_django_for_project(project_name):
    """Setup Django environment for a specific project"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{project_name}.settings')
    django.setup()

def run_command(command, cwd=None):
    """Run a shell command and return success status"""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error running command: {command}")
            print(f"Error output: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"Exception running command {command}: {e}")
        return False

def setup_project(project_name, port, partner_name, partner_port):
    """Setup a single AS2 project"""
    print(f"\n{'='*50}")
    print(f"Setting up {project_name} AS2 Server")
    print(f"{'='*50}")
    
    project_dir = Path(project_name)
    
    # Change to project directory
    os.chdir(project_dir)
    
    # Run migrations
    print("Running migrations...")
    if not run_command("python manage.py migrate"):
        return False
    print("✓ Migrations completed")
    
    # Create superuser
    print("Creating admin user...")
    if not run_command(f"python manage.py shell -c \"from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@{project_name.lower()}.com', 'admin123')\""):
        return False
    print("✓ Admin user created (admin/admin123)")
    
    # Setup Django environment
    setup_django_for_project(project_name)
    
    # Setup AS2 configuration
    if not setup_as2_config(project_name, partner_name, partner_port):
        return False
    
    # Create data directory
    data_dir = Path('data')
    if not data_dir.exists():
        data_dir.mkdir()
        print("✓ Data directory created")
    else:
        print("✓ Data directory exists")
    
    # Go back to parent directory
    os.chdir('..')
    
    print(f"✓ {project_name} setup completed successfully!")
    return True

def setup_as2_config(project_name, partner_name, partner_port):
    """Setup AS2 organization and partner for a project"""
    from pyas2.models import Organization, Partner, PrivateKey, PublicCertificate
    
    # Read certificates
    try:
        with open(f'../{project_name}_private.pem', 'r') as f:
            private_key_content = f.read()
        with open(f'../{partner_name}_public.pem', 'r') as f:
            partner_cert_content = f.read()
    except FileNotFoundError as e:
        print(f"✗ Certificate file not found: {e}")
        print("Make sure certificates are generated in the parent directory")
        return False
    
    # Create private key
    private_key, created = PrivateKey.objects.get_or_create(
        name=f'{project_name}_private_key',
        defaults={'key': private_key_content}
    )
    print(f"✓ {project_name} Private Key {'created' if created else 'exists'}")
    
    # Create partner certificate
    partner_cert, created = PublicCertificate.objects.get_or_create(
        name=f'{partner_name}_public_cert',
        defaults={'certificate': partner_cert_content}
    )
    print(f"✓ {partner_name} Public Certificate {'created' if created else 'exists'}")
    
    # Create organization
    org, created = Organization.objects.get_or_create(
        as2_name=project_name,
        defaults={
            'name': f'{project_name} Organization',
            'email_address': f'admin@{project_name.lower()}.com',
            'encryption_key': private_key,
            'signature_key': private_key,
            'confirmation_message': f'Message received successfully by {project_name}'
        }
    )
    print(f"✓ {project_name} Organization {'created' if created else 'exists'}")
    
    # Create partner
    partner, created = Partner.objects.get_or_create(
        as2_name=partner_name,
        defaults={
            'name': f'{partner_name} Partner',
            'email_address': f'admin@{partner_name.lower()}.com',
            'target_url': f'http://127.0.0.1:{partner_port}/pyas2/as2receive',
            'subject': f'AS2 Message from {project_name} to {partner_name}',
            'content_type': 'application/edi-x12',
            'compress': False,
            'encryption': 'aes_128_cbc',
            'encryption_cert': partner_cert,
            'signature': 'sha256',
            'signature_cert': partner_cert,
            'mdn_mode': 'SYNC',
            'mdn_sign': 'sha256'
        }
    )
    print(f"✓ {partner_name} Partner {'created' if created else 'exists'}")
    
    return True

def create_startup_scripts():
    """Create startup scripts for both servers"""
    
    # P1 startup script
    p1_script = """#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'P1.settings')
django.setup()

# Override database to use SQLite for quick testing
from P1 import settings
settings.DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'p1_as2_db.sqlite3',
    }
}

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
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'P2.settings')
django.setup()

# Override database to use SQLite for quick testing
from P2 import settings
settings.DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'p2_as2_db.sqlite3',
    }
}

print("Starting P2 AS2 Server on http://127.0.0.1:8001")
print("Admin: http://127.0.0.1:8001/admin/ (admin/admin123)")
print("AS2 Endpoint: http://127.0.0.1:8001/pyas2/as2receive")
print("Press Ctrl+C to stop")

from django.core.management import execute_from_command_line
execute_from_command_line(['manage.py', 'runserver', '127.0.0.1:8001'])
"""
    
    with open('P1/start_p1.py', 'w') as f:
        f.write(p1_script)
    
    with open('P2/start_p2.py', 'w') as f:
        f.write(p2_script)
    
    print("✓ Startup scripts created:")
    print("  - P1/start_p1.py")
    print("  - P2/start_p2.py")

def main():
    """Main setup function"""
    print("Setting up P1 and P2 AS2 Servers")
    print("=" * 50)
    
    # Check if certificates exist
    cert_files = ['P1_private.pem', 'P1_public.pem', 'P2_private.pem', 'P2_public.pem']
    missing_certs = [f for f in cert_files if not Path(f).exists()]
    
    if missing_certs:
        print("✗ Missing certificate files:")
        for cert in missing_certs:
            print(f"  - {cert}")
        print("\nGenerating certificates...")
        if not run_command("python generate_certificates.py"):
            print("✗ Failed to generate certificates")
            return False
        print("✓ Certificates generated")
    else:
        print("✓ All certificates present")
    
    # Setup P1 (SQLite for simplicity)
    print("\nSetting up P1 with SQLite...")
    os.chdir('P1')
    
    # Override P1 to use SQLite
    setup_django_for_project('P1')
    from P1 import settings
    settings.DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'p1_as2_db.sqlite3',
        }
    }
    
    # Run P1 migrations
    if not run_command("python manage.py migrate"):
        return False
    print("✓ P1 migrations completed")
    
    # Create P1 admin user
    if not run_command("python manage.py shell -c \"from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@p1.com', 'admin123')\""):
        return False
    print("✓ P1 admin user created")
    
    # Setup P1 AS2 config
    if not setup_as2_config('P1', 'P2', '8001'):
        return False
    
    os.chdir('..')
    
    # Setup P2 (SQLite for simplicity)
    print("\nSetting up P2 with SQLite...")
    os.chdir('P2')
    
    # Override P2 to use SQLite
    setup_django_for_project('P2')
    from P2 import settings
    settings.DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'p2_as2_db.sqlite3',
        }
    }
    
    # Run P2 migrations
    if not run_command("python manage.py migrate"):
        return False
    print("✓ P2 migrations completed")
    
    # Create P2 admin user
    if not run_command("python manage.py shell -c \"from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@p2.com', 'admin123')\""):
        return False
    print("✓ P2 admin user created")
    
    # Setup P2 AS2 config
    if not setup_as2_config('P2', 'P1', '8000'):
        return False
    
    os.chdir('..')
    
    # Create data directories
    for project in ['P1', 'P2']:
        data_dir = Path(project) / 'data'
        if not data_dir.exists():
            data_dir.mkdir()
            print(f"✓ {project} data directory created")
        else:
            print(f"✓ {project} data directory exists")
    
    # Create startup scripts
    create_startup_scripts()
    
    print("\n" + "=" * 50)
    print("✓ Both P1 and P2 AS2 Servers setup completed!")
    print("\nTo start the servers:")
    print("1. Terminal 1: cd P1 && python start_p1.py")
    print("2. Terminal 2: cd P2 && python start_p2.py")
    print("\nAccess points:")
    print("P1 Admin: http://127.0.0.1:8000/admin/ (admin/admin123)")
    print("P1 AS2: http://127.0.0.1:8000/pyas2/as2receive")
    print("P2 Admin: http://127.0.0.1:8001/admin/ (admin/admin123)")
    print("P2 AS2: http://127.0.0.1:8001/pyas2/as2receive")
    
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