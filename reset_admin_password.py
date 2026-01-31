#!/usr/bin/env python
"""
Reset admin password for P1 and P2 servers
Run this inside the Docker containers
"""
import os
import sys
import django

def reset_p1_password():
    """Reset P1 admin password"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    sys.path.insert(0, '/app/P1')
    django.setup()
    
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    try:
        admin_user = User.objects.get(username='admin')
        admin_user.set_password('admin123')
        admin_user.save()
        print("✓ P1 admin password reset to 'admin123'")
    except User.DoesNotExist:
        admin_user = User.objects.create_superuser('admin', 'admin@p1.com', 'admin123')
        print("✓ P1 admin user created with password 'admin123'")

def reset_p2_password():
    """Reset P2 admin password"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'P2.settings')
    sys.path.insert(0, '/app/P2')
    django.setup()
    
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    try:
        admin_user = User.objects.get(username='admin')
        admin_user.set_password('admin123')
        admin_user.save()
        print("✓ P2 admin password reset to 'admin123'")
    except User.DoesNotExist:
        admin_user = User.objects.create_superuser('admin', 'admin@p2.com', 'admin123')
        print("✓ P2 admin user created with password 'admin123'")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python reset_admin_password.py [p1|p2|both]")
        sys.exit(1)
    
    target = sys.argv[1].lower()
    
    if target in ['p1', 'both']:
        print("\nResetting P1 admin password...")
        reset_p1_password()
    
    if target in ['p2', 'both']:
        print("\nResetting P2 admin password...")
        reset_p2_password()
    
    if target == 'both':
        print("\n✓ All passwords reset!")
        print("\nLogin credentials:")
        print("  Username: admin")
        print("  Password: admin123")
