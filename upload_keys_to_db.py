#!/usr/bin/env python3
"""
Upload keys and certificates to AS2 database
Run: docker exec p1-as2 python3 /app/upload_keys_to_db.py
"""
import os
import sys

os.chdir('/app/P1')
sys.path.insert(0, '/app/P1')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django
django.setup()

from pyas2.models import Organization, Partner, PrivateKey, PublicCertificate

print("\n" + "="*70)
print("Uploading Keys and Certificates to Database")
print("="*70 + "\n")

# Read P1 private key
print("1. Reading P1 private key...")
with open('/app/P1_private.pem', 'rb') as f:
    p1_private_content = f.read()
print("   ✓ P1 private key read")

# Read P1 public cert
print("2. Reading P1 public certificate...")
with open('/app/P1_public.pem', 'rb') as f:
    p1_public_content = f.read()
print("   ✓ P1 public certificate read")

# Read P2 public cert
print("3. Reading P2 public certificate...")
with open('/app/P2_public.pem', 'rb') as f:
    p2_public_content = f.read()
print("   ✓ P2 public certificate read")

# Create or update P1 private key
print("\n4. Creating P1 private key in database...")
p1_private_key, created = PrivateKey.objects.get_or_create(
    name='P1_private',
    defaults={'key': p1_private_content, 'key_pass': ''}
)
if not created:
    p1_private_key.key = p1_private_content
    p1_private_key.key_pass = ''
    p1_private_key.save()
print(f"   ✓ P1 private key {'created' if created else 'updated'}")

# Create or update P1 public cert
print("5. Creating P1 public certificate in database...")
p1_public_cert, created = PublicCertificate.objects.get_or_create(
    name='P1_public',
    defaults={'certificate': p1_public_content, 'verify_cert': False}
)
if not created:
    p1_public_cert.certificate = p1_public_content
    p1_public_cert.save()
print(f"   ✓ P1 public certificate {'created' if created else 'updated'}")

# Create or update P2 public cert
print("6. Creating P2 public certificate in database...")
p2_public_cert, created = PublicCertificate.objects.get_or_create(
    name='P2_public',
    defaults={'certificate': p2_public_content, 'verify_cert': False}
)
if not created:
    p2_public_cert.certificate = p2_public_content
    p2_public_cert.save()
print(f"   ✓ P2 public certificate {'created' if created else 'updated'}")

# Update P1 organization with keys
print("\n7. Updating P1 organization with keys...")
org = Organization.objects.get(as2_name='P1')
org.signature_key = p1_private_key
org.encryption_key = p1_private_key  # Use private key for decryption
org.save()
print("   ✓ P1 organization updated")

# Update P2 partner with certs
print("8. Updating P2 partner with certificates...")
partner = Partner.objects.get(as2_name='P2')
partner.signature_cert = p2_public_cert
partner.encryption_cert = p2_public_cert
partner.save()
print("   ✓ P2 partner updated")

print("\n" + "="*70)
print("✅ ALL KEYS AND CERTIFICATES UPLOADED SUCCESSFULLY!")
print("="*70 + "\n")

print("Configuration:")
print(f"  P1 Organization:")
print(f"    - Signature Key: {org.signature_key.name}")
print(f"    - Encryption Key: {org.encryption_key.name}")
print(f"  P2 Partner:")
print(f"    - Signature Cert: {partner.signature_cert.name}")
print(f"    - Encryption Cert: {partner.encryption_cert.name}")

print("\n✅ Ready to send AS2 messages!\n")
