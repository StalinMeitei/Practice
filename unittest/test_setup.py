#!/usr/bin/env python
"""
Test P1 AS2 server setup without database dependency
"""
import os
import sys

def check_certificates():
    """Check if certificates exist"""
    certs = ['P1_private.pem', 'P1_public.pem', 'P2_private.pem', 'P2_public.pem']
    missing = []
    
    for cert in certs:
        if not os.path.exists(cert):
            missing.append(cert)
    
    if missing:
        print("✗ Missing certificates:")
        for cert in missing:
            print(f"  - {cert}")
        print("\nRun: python generate_certificates.py")
        return False
    else:
        print("✓ All certificates present")
        return True

def check_django_config():
    """Check Django configuration"""
    try:
        # Check if settings file exists and is valid
        from P1 import settings
        print("✓ Django settings loaded successfully")
        
        # Check if pyas2 is in INSTALLED_APPS
        if 'pyas2' in settings.INSTALLED_APPS:
            print("✓ pyas2 app is installed")
        else:
            print("✗ pyas2 app not found in INSTALLED_APPS")
            return False
        
        # Check database configuration
        db_config = settings.DATABASES['default']
        if db_config['ENGINE'] == 'django.db.backends.postgresql':
            print("✓ PostgreSQL database configured")
        else:
            print("✗ Database not configured for PostgreSQL")
            return False
        
        return True
        
    except ImportError as e:
        print(f"✗ Failed to import Django settings: {e}")
        return False
    except Exception as e:
        print(f"✗ Django configuration error: {e}")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'django',
        'pyas2',
        'psycopg2',
        'cryptography',
        'requests'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print("✗ Missing packages:")
        for package in missing:
            print(f"  - {package}")
        print("\nInstall with: pip install django django-pyas2 psycopg2-binary")
        return False
    else:
        print("✓ All required packages installed")
        return True

def check_data_directory():
    """Check if data directory exists"""
    if os.path.exists('data'):
        print("✓ Data directory exists")
        return True
    else:
        print("✗ Data directory missing")
        print("Creating data directory...")
        os.makedirs('data')
        print("✓ Data directory created")
        return True

def main():
    """Main test function"""
    print("Testing P1 AS2 Server Setup")
    print("=" * 40)
    
    all_good = True
    
    # Check dependencies
    if not check_dependencies():
        all_good = False
    
    # Check Django configuration
    if not check_django_config():
        all_good = False
    
    # Check certificates
    if not check_certificates():
        all_good = False
    
    # Check data directory
    if not check_data_directory():
        all_good = False
    
    print("\n" + "=" * 40)
    
    if all_good:
        print("✓ All checks passed!")
        print("\nNext steps:")
        print("1. Setup database: python setup_database.py")
        print("2. Run migrations: python manage.py migrate")
        print("3. Configure P1: python setup_p1.py")
        print("4. Start server: python manage.py runserver")
    else:
        print("✗ Some checks failed. Please fix the issues above.")
        return False
    
    return True

if __name__ == "__main__":
    if not main():
        sys.exit(1)