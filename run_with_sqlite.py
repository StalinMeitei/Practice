#!/usr/bin/env python
"""
Run P1 AS2 server with SQLite fallback (for testing without PostgreSQL)
"""
import os
import django
import sys

def setup_sqlite_database():
    """Configure Django to use SQLite temporarily"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'P1.settings')
    
    # Override database setting to use SQLite
    import P1.settings as settings
    settings.DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'p1_as2_db.sqlite3',
        }
    }
    
    django.setup()
    print("✓ Using SQLite database for testing")

def run_migrations():
    """Run Django migrations"""
    from django.core.management import execute_from_command_line
    print("Running migrations...")
    execute_from_command_line(['manage.py', 'migrate'])
    print("✓ Migrations completed")

def create_superuser():
    """Create admin user"""
    from django.contrib.auth.models import User
    
    if not User.objects.filter(username='admin').exists():
        admin_user = User.objects.create_superuser('admin', 'admin@p1.com', 'admin123')
        print("✓ Admin user created (admin/admin123)")
    else:
        print("✓ Admin user already exists")

def setup_as2_config():
    """Setup AS2 organization and partner"""
    from pyas2.models import Organization, Partner, PrivateKey, PublicCertificate
    
    # Create or get P1 private key
    try:
        with open('P1_private.pem', 'r') as f:
            p1_key_content = f.read()
        
        p1_private_key, created = PrivateKey.objects.get_or_create(
            name='P1_private_key',
            defaults={'key': p1_key_content}
        )
        print(f"✓ P1 Private Key {'created' if created else 'exists'}")
    except FileNotFoundError:
        print("✗ P1_private.pem not found")
        print("Run: python generate_certificates.py")
        return False
    
    # Create or get P2 public certificate
    try:
        with open('P2_public.pem', 'r') as f:
            p2_cert_content = f.read()
        
        p2_public_cert, created = PublicCertificate.objects.get_or_create(
            name='P2_public_cert',
            defaults={'certificate': p2_cert_content}
        )
        print(f"✓ P2 Public Certificate {'created' if created else 'exists'}")
    except FileNotFoundError:
        print("✗ P2_public.pem not found")
        print("Run: python generate_certificates.py")
        return False
    
    # Create P1 organization
    org, created = Organization.objects.get_or_create(
        as2_name='P1',
        defaults={
            'name': 'P1 Organization',
            'email_address': 'admin@p1.com',
            'encryption_key': p1_private_key,
            'signature_key': p1_private_key,
            'confirmation_message': 'Message received successfully by P1'
        }
    )
    print(f"✓ P1 Organization {'created' if created else 'exists'}")
    
    # Create P2 partner
    partner, created = Partner.objects.get_or_create(
        as2_name='P2',
        defaults={
            'name': 'P2 Partner',
            'email_address': 'admin@p2.com',
            'target_url': 'http://127.0.0.1:8001/pyas2/as2receive',
            'subject': 'AS2 Message from P1 to P2',
            'content_type': 'application/edi-x12',
            'compress': False,
            'encryption': 'aes_128_cbc',
            'encryption_cert': p2_public_cert,
            'signature': 'sha256',
            'signature_cert': p2_public_cert,
            'mdn_mode': 'SYNC',
            'mdn_sign': 'sha256'
        }
    )
    print(f"✓ P2 Partner {'created' if created else 'exists'}")
    
    return True

def main():
    """Main setup and run function"""
    print("Setting up P1 AS2 Server with SQLite")
    print("=" * 40)
    
    # Setup Django with SQLite
    setup_sqlite_database()
    
    # Run migrations
    run_migrations()
    
    # Create admin user
    create_superuser()
    
    # Setup AS2 configuration
    if not setup_as2_config():
        return False
    
    print("\n" + "=" * 40)
    print("✓ P1 AS2 Server setup completed!")
    print("\nServer details:")
    print("- Database: SQLite (p1_as2_db.sqlite3)")
    print("- Admin: http://127.0.0.1:8000/admin/ (admin/admin123)")
    print("- AS2 Endpoint: http://127.0.0.1:8000/pyas2/as2receive")
    print("- Organization: P1")
    print("- Partner: P2 (target: http://127.0.0.1:8001/pyas2/as2receive)")
    
    print("\nStarting development server...")
    print("Press Ctrl+C to stop the server")
    
    # Start the development server
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'runserver'])

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nServer stopped.")
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)