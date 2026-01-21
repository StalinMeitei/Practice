#!/usr/bin/env python
"""
Generate SSL certificates for P1 and P2 AS2 servers
"""
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import datetime

def generate_certificate(org_name, common_name, filename_prefix):
    """Generate a self-signed certificate and private key"""
    
    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    
    # Create certificate
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "California"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "San Francisco"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, org_name),
        x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, "AS2"),
        x509.NameAttribute(NameOID.COMMON_NAME, common_name),
    ])
    
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        datetime.datetime.utcnow() + datetime.timedelta(days=365)
    ).add_extension(
        x509.SubjectAlternativeName([
            x509.DNSName("localhost"),
            x509.DNSName("127.0.0.1"),
        ]),
        critical=False,
    ).sign(private_key, hashes.SHA256())
    
    # Write private key
    with open(f"{filename_prefix}_private.pem", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))
    
    # Write public certificate
    with open(f"{filename_prefix}_public.pem", "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    
    # Combine private key and certificate (as required by pyas2)
    with open(f"{filename_prefix}_private.pem", "ab") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    
    print(f"Generated certificates for {org_name}:")
    print(f"  - {filename_prefix}_private.pem (private key + certificate)")
    print(f"  - {filename_prefix}_public.pem (public certificate)")

if __name__ == "__main__":
    # Generate P1 certificates
    generate_certificate("P1", "p1as2", "P1")
    
    # Generate P2 certificates (for later use)
    generate_certificate("P2", "p2as2", "P2")
    
    print("\nCertificates generated successfully!")