#!/usr/bin/env python3
"""
Fix Private Key Format for django-pyas2
Converts keys to the correct format and provides troubleshooting
"""
import os
import sys
from pathlib import Path

def check_key_format(key_file):
    """Check if key file has the correct format"""
    if not os.path.exists(key_file):
        return False, f"File {key_file} does not exist"
    
    with open(key_file, 'r') as f:
        content = f.read()
    
    has_private_key = '-----BEGIN PRIVATE KEY-----' in content
    has_certificate = '-----BEGIN CERTIFICATE-----' in content
    has_rsa_key = '-----BEGIN RSA PRIVATE KEY-----' in content
    has_encrypted = 'ENCRYPTED' in content
    
    issues = []
    
    if has_encrypted:
        issues.append("Key is encrypted (password protected)")
    
    if has_rsa_key and not has_private_key:
        issues.append("Key is in PKCS#1 format (needs PKCS#8)")
    
    if not has_private_key and not has_rsa_key:
        issues.append("No private key found in file")
    
    if not has_certificate:
        issues.append("Certificate not found in file (should be appended)")
    
    if issues:
        return False, "; ".join(issues)
    
    return True, "Key format is correct"

def convert_rsa_to_pkcs8(input_file, output_file):
    """Convert RSA private key (PKCS#1) to PKCS#8 format"""
    try:
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.backends import default_backend
        
        # Read the key
        with open(input_file, 'rb') as f:
            key_data = f.read()
        
        # Try to load as RSA key
        try:
            from cryptography.hazmat.primitives.serialization import load_pem_private_key
            private_key = load_pem_private_key(key_data, password=None, backend=default_backend())
        except Exception as e:
            return False, f"Cannot load key: {e}"
        
        # Convert to PKCS#8
        pkcs8_key = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        # Write converted key
        with open(output_file, 'wb') as f:
            f.write(pkcs8_key)
        
        return True, f"Converted to {output_file}"
    
    except ImportError:
        return False, "cryptography library not installed"
    except Exception as e:
        return False, f"Conversion failed: {e}"

def remove_password_protection(input_file, output_file, password):
    """Remove password protection from private key"""
    try:
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.backends import default_backend
        from cryptography.hazmat.primitives.serialization import load_pem_private_key
        
        # Read the encrypted key
        with open(input_file, 'rb') as f:
            key_data = f.read()
        
        # Load with password
        private_key = load_pem_private_key(
            key_data, 
            password=password.encode() if password else None,
            backend=default_backend()
        )
        
        # Save without encryption
        unencrypted_key = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        with open(output_file, 'wb') as f:
            f.write(unencrypted_key)
        
        return True, f"Removed password protection, saved to {output_file}"
    
    except Exception as e:
        return False, f"Failed to remove password: {e}"

def combine_key_and_cert(key_file, cert_file, output_file):
    """Combine private key and certificate into one file"""
    try:
        with open(key_file, 'r') as f:
            key_content = f.read()
        
        with open(cert_file, 'r') as f:
            cert_content = f.read()
        
        # Ensure proper formatting
        if not key_content.endswith('\n'):
            key_content += '\n'
        
        combined = key_content + cert_content
        
        with open(output_file, 'w') as f:
            f.write(combined)
        
        return True, f"Combined key and certificate saved to {output_file}"
    
    except Exception as e:
        return False, f"Failed to combine: {e}"

def main():
    print("=" * 60)
    print("Private Key Format Checker and Fixer")
    print("=" * 60)
    print()
    
    # Check existing keys
    keys_to_check = ['P1_private.pem', 'P2_private.pem']
    
    for key_file in keys_to_check:
        if os.path.exists(key_file):
            print(f"Checking {key_file}...")
            is_valid, message = check_key_format(key_file)
            
            if is_valid:
                print(f"  ✓ {message}")
            else:
                print(f"  ✗ {message}")
        else:
            print(f"  ⚠ {key_file} not found")
    
    print()
    print("=" * 60)
    print("Key Format Requirements for django-pyas2:")
    print("=" * 60)
    print()
    print("1. Format: PKCS#8 (not PKCS#1 or RSA)")
    print("2. Encryption: None (no password protection)")
    print("3. Structure: Private key + Certificate in same file")
    print("4. Headers:")
    print("   - -----BEGIN PRIVATE KEY----- (not RSA PRIVATE KEY)")
    print("   - -----BEGIN CERTIFICATE-----")
    print()
    print("=" * 60)
    print("How to Use in django-pyas2 Admin:")
    print("=" * 60)
    print()
    print("1. Go to: http://localhost:8001/admin/")
    print("2. Navigate to: Organizations")
    print("3. Click on your organization (P1 or P2)")
    print("4. In 'Private Key' section:")
    print("   - Key file: Choose P1_private.pem (or P2_private.pem)")
    print("   - Private Key Password: LEAVE EMPTY")
    print("5. Click 'Save'")
    print()
    print("⚠️  IMPORTANT: Leave the password field EMPTY!")
    print()
    print("=" * 60)
    print("Troubleshooting:")
    print("=" * 60)
    print()
    print("If you still get 'Invalid Private Key' error:")
    print()
    print("1. Regenerate certificates:")
    print("   python generate_certificates.py")
    print()
    print("2. Verify format:")
    print("   python fix_private_key_format.py")
    print()
    print("3. Check file contents:")
    print("   - Should start with: -----BEGIN PRIVATE KEY-----")
    print("   - Should contain: -----BEGIN CERTIFICATE-----")
    print("   - Should NOT contain: ENCRYPTED")
    print()
    print("4. In Django admin:")
    print("   - Upload the _private.pem file")
    print("   - Leave password field EMPTY")
    print("   - Do NOT enter any password")
    print()

if __name__ == "__main__":
    main()
