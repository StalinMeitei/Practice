#!/usr/bin/env python3
"""
Check and display AS2 configuration
Run: docker exec p1-as2 python3 /app/check_as2_config.py
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
print("AS2 Configuration Check")
print("="*70 + "\n")

# Check Organization
print("ORGANIZATION:")
orgs = Organization.objects.all()
if orgs.exists():
    for org in orgs:
        print(f"  Name: {org.as2_name}")
        print(f"  Signature Key: {org.signature_key.name if org.signature_key else 'NOT SET ❌'}")
        print(f"  Encryption Key: {org.encryption_key.name if org.encryption_key else 'NOT SET ❌'}")
else:
    print("  ❌ No organization configured!")

print("\nPARTNERS:")
partners = Partner.objects.all()
if partners.exists():
    for partner in partners:
        print(f"  Name: {partner.as2_name}")
        print(f"  Target URL: {partner.target_url}")
        print(f"  Signature: {partner.signature}")
        print(f"  Encryption: {partner.encryption}")
        print(f"  Signature Cert: {partner.signature_cert.name if partner.signature_cert else 'NOT SET ❌'}")
        print(f"  Encryption Cert: {partner.encryption_cert.name if partner.encryption_cert else 'NOT SET ❌'}")
else:
    print("  ❌ No partners configured!")

print("\nPRIVATE KEYS:")
keys = PrivateKey.objects.all()
if keys.exists():
    for key in keys:
        print(f"  - {key.name}")
else:
    print("  ❌ No private keys!")

print("\nPUBLIC CERTIFICATES:")
certs = PublicCertificate.objects.all()
if certs.exists():
    for cert in certs:
        print(f"  - {cert.name}")
else:
    print("  ❌ No public certificates!")

print("\n" + "="*70 + "\n")
