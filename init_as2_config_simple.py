#!/usr/bin/env python
"""
Initialize AS2 configuration for P1 and P2 servers (Simplified)
Run this after first deployment to set up organizations and partners
"""
import os
import sys
import django

def setup_p1():
    """Setup P1 AS2 configuration"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    sys.path.insert(0, '/app/P1')
    django.setup()
    
    from django.contrib.auth import get_user_model
    from pyas2.models import Organization, Partner
    
    User = get_user_model()
    
    # Create admin user if not exists
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@p1.com', 'admin123')
        print("✓ P1 admin user created")
    else:
        print("✓ P1 admin user already exists")
    
    # Create P1 Organization
    org, created = Organization.objects.get_or_create(
        as2_name='P1',
        defaults={
            'name': 'P1 Organization',
            'email_address': 'admin@p1.com',
        }
    )
    if created:
        print("✓ P1 Organization created")
    else:
        print("✓ P1 Organization already exists")
    
    # Create P2 Partner
    partner, created = Partner.objects.get_or_create(
        as2_name='P2',
        defaults={
            'name': 'P2 Partner',
            'target_url': 'http://p2:8002/pyas2/as2receive',
            'compress': False,
            'encryption': 'tripledes_192_cbc',
            'signature': 'sha256',
            'mdn_mode': 'SYNC',
        }
    )
    if created:
        print("✓ P2 Partner created")
    else:
        print("✓ P2 Partner already exists")
    
    print("\n✓ P1 configuration completed!")

def setup_p2():
    """Setup P2 AS2 configuration"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'P2.settings')
    sys.path.insert(0, '/app/P2')
    django.setup()
    
    from django.contrib.auth import get_user_model
    from pyas2.models import Organization, Partner
    
    User = get_user_model()
    
    # Create admin user if not exists
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@p2.com', 'admin123')
        print("✓ P2 admin user created")
    else:
        print("✓ P2 admin user already exists")
    
    # Create P2 Organization
    org, created = Organization.objects.get_or_create(
        as2_name='P2',
        defaults={
            'name': 'P2 Organization',
            'email_address': 'admin@p2.com',
        }
    )
    if created:
        print("✓ P2 Organization created")
    else:
        print("✓ P2 Organization already exists")
    
    # Create P1 Partner
    partner, created = Partner.objects.get_or_create(
        as2_name='P1',
        defaults={
            'name': 'P1 Partner',
            'target_url': 'http://p1:8000/pyas2/as2receive',
            'compress': False,
            'encryption': 'tripledes_192_cbc',
            'signature': 'sha256',
            'mdn_mode': 'SYNC',
        }
    )
    if created:
        print("✓ P1 Partner created")
    else:
        print("✓ P1 Partner already exists")
    
    print("\n✓ P2 configuration completed!")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python init_as2_config_simple.py [p1|p2|both]")
        sys.exit(1)
    
    target = sys.argv[1].lower()
    
    if target in ['p1', 'both']:
        print("\n" + "="*50)
        print("Setting up P1 AS2 Configuration")
        print("="*50)
        setup_p1()
    
    if target in ['p2', 'both']:
        print("\n" + "="*50)
        print("Setting up P2 AS2 Configuration")
        print("="*50)
        setup_p2()
    
    if target == 'both':
        print("\n" + "="*50)
        print("✓ All configurations completed!")
        print("="*50)
        print("\nAccess Points:")
        print("  P1 Admin: http://localhost/admin/ (admin/admin123)")
        print("  P2 Admin: http://localhost/p2/admin/ (admin/admin123)")
    
    # Print private key usage instructions
    print("\n" + "="*50)
    print("IMPORTANT: Private Key Upload Instructions")
    print("="*50)
    print("\nIf you need to manually upload private keys:")
    print("1. Go to Django Admin → Organizations")
    print("2. Click on your organization (P1 or P2)")
    print("3. Upload the private key file:")
    print("   - For P1: Use P1_private.pem")
    print("   - For P2: Use P2_private.pem")
    print("4. ⚠️  CRITICAL: Leave 'Private Key Password' field EMPTY")
    print("5. Click Save")
    print("\nThe keys are NOT password protected!")
    print("See: upload_private_key_guide.txt for visual guide")
    print("See: PRIVATE_KEY_TROUBLESHOOTING.md for detailed help")
    print("="*50)
