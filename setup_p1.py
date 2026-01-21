#!/usr/bin/env python
"""
Complete setup script for P1 AS2 server
"""
import os
import django
import sys

def setup_django():
    """Setup Django environment"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'P1.settings')
    django.setup()

def create_organization():
    """Create P1 organization"""
    from pyas2.models import Organization, PrivateKey
    
    # Create or get P1 private key
    try:
        with open('P1_private.pem', 'r') as f:
            private_key_content = f.read()
    except FileNotFoundError:
        print("Error: P1_private.pem not found. Please run generate_certificates.py first.")
        return False
    
    p1_private_key, created = PrivateKey.objects.get_or_create(
        name='P1_private_key',
        defaults={'key': private_key_content}
    )
    print(f"✓ P1 Private Key {'created' if created else 'exists'}")
    
    # Create or update P1 organization
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
    
    if created:
        print("✓ P1 Organization created successfully")
    else:
        print("✓ P1 Organization already exists")
    
    return True

def create_partner():
    """Create P2 partner configuration"""
    from pyas2.models import Partner, PublicKey
    
    # Create or get P2 public key
    try:
        with open('P2_public.pem', 'r') as f:
            p2_public_key_content = f.read()
    except FileNotFoundError:
        print("Error: P2_public.pem not found. Please run generate_certificates.py first.")
        return False
    
    p2_public_key, created = PublicKey.objects.get_or_create(
        name='P2_public_key',
        defaults={'key': p2_public_key_content}
    )
    print(f"✓ P2 Public Key {'created' if created else 'exists'}")
    
    # Create or update P2 partner
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
            'encryption_key': p2_public_key,
            'signature': 'sha256',
            'signature_key': p2_public_key,
            'mdn_mode': 'SYNC',
            'mdn_sign': 'sha256'
        }
    )
    
    if created:
        print("✓ P2 Partner created successfully")
    else:
        print("✓ P2 Partner already exists")
    
    return True

def create_data_directory():
    """Create data directory for file storage"""
    data_dir = 'data'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"✓ Data directory '{data_dir}' created")
    else:
        print(f"✓ Data directory '{data_dir}' already exists")

def main():
    """Main setup function"""
    print("Setting up P1 AS2 Server...")
    print("=" * 40)
    
    # Setup Django
    try:
        setup_django()
        print("✓ Django environment initialized")
    except Exception as e:
        print(f"✗ Failed to initialize Django: {e}")
        return False
    
    # Create data directory
    create_data_directory()
    
    # Create organization
    if not create_organization():
        return False
    
    # Create partner
    if not create_partner():
        return False
    
    print("\n" + "=" * 40)
    print("P1 AS2 Server setup completed successfully!")
    print("\nNext steps:")
    print("1. Start the server: python manage.py runserver")
    print("2. Access admin interface: http://127.0.0.1:8000/admin/")
    print("3. Login with: admin / admin123")
    print("4. AS2 endpoint: http://127.0.0.1:8000/pyas2/as2receive")
    print("\nConfiguration summary:")
    print("- Organization: P1 (AS2 ID: P1)")
    print("- Partner: P2 (AS2 ID: P2)")
    print("- Encryption: AES-128-CBC")
    print("- Signature: SHA-256")
    print("- MDN Mode: Synchronous")
    
    return True

if __name__ == "__main__":
    if not main():
        sys.exit(1)