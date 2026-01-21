#!/usr/bin/env python
"""
Setup P2 AS2 configuration with pgEdge
"""
import os
import django
import sys

def setup_django():
    """Setup Django environment for P2"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'P2.settings')
    django.setup()

def setup_as2_config():
    """Setup AS2 organization and partner for P2"""
    from pyas2.models import Organization, Partner, PrivateKey, PublicCertificate
    
    # Create or get P2 private key
    try:
        with open('../P2_private.pem', 'r') as f:
            p2_key_content = f.read()
        
        p2_private_key, created = PrivateKey.objects.get_or_create(
            name='P2_private_key',
            defaults={'key': p2_key_content}
        )
        print(f"✓ P2 Private Key {'created' if created else 'exists'}")
    except FileNotFoundError:
        print("✗ P2_private.pem not found in parent directory")
        return False
    
    # Create or get P1 public certificate
    try:
        with open('../P1_public.pem', 'r') as f:
            p1_cert_content = f.read()
        
        p1_public_cert, created = PublicCertificate.objects.get_or_create(
            name='P1_public_cert',
            defaults={'certificate': p1_cert_content}
        )
        print(f"✓ P1 Public Certificate {'created' if created else 'exists'}")
    except FileNotFoundError:
        print("✗ P1_public.pem not found in parent directory")
        return False
    
    # Create P2 organization
    org, created = Organization.objects.get_or_create(
        as2_name='P2',
        defaults={
            'name': 'P2 Organization',
            'email_address': 'admin@p2.com',
            'encryption_key': p2_private_key,
            'signature_key': p2_private_key,
            'confirmation_message': 'Message received successfully by P2'
        }
    )
    print(f"✓ P2 Organization {'created' if created else 'exists'}")
    
    # Create P1 partner
    partner, created = Partner.objects.get_or_create(
        as2_name='P1',
        defaults={
            'name': 'P1 Partner',
            'email_address': 'admin@p1.com',
            'target_url': 'http://127.0.0.1:8000/pyas2/as2receive',
            'subject': 'AS2 Message from P2 to P1',
            'content_type': 'application/edi-x12',
            'compress': False,
            'encryption': 'aes_128_cbc',
            'encryption_cert': p1_public_cert,
            'signature': 'sha256',
            'signature_cert': p1_public_cert,
            'mdn_mode': 'SYNC',
            'mdn_sign': 'sha256'
        }
    )
    print(f"✓ P1 Partner {'created' if created else 'exists'}")
    
    return True

def main():
    """Main setup function"""
    print("Setting up P2 AS2 Configuration")
    print("=" * 40)
    
    # Setup Django
    try:
        setup_django()
        print("✓ Django environment initialized")
    except Exception as e:
        print(f"✗ Failed to initialize Django: {e}")
        return False
    
    # Setup AS2 configuration
    if not setup_as2_config():
        return False
    
    print("\n" + "=" * 40)
    print("✓ P2 AS2 configuration completed!")
    print("\nConfiguration summary:")
    print("- Organization: P2 (AS2 ID: P2)")
    print("- Partner: P1 (AS2 ID: P1)")
    print("- Target URL: http://127.0.0.1:8000/pyas2/as2receive")
    print("- Encryption: AES-128-CBC")
    print("- Signature: SHA-256")
    print("- MDN Mode: Synchronous")
    
    return True

if __name__ == "__main__":
    if not main():
        sys.exit(1)