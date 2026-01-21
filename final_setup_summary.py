#!/usr/bin/env python
"""
Final setup summary and status check for P1 and P2 AS2 servers
"""
import os
import sys
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists and report status"""
    if Path(filepath).exists():
        print(f"✓ {description}: {filepath}")
        return True
    else:
        print(f"✗ {description}: {filepath} (missing)")
        return False

def check_directory_exists(dirpath, description):
    """Check if a directory exists and report status"""
    if Path(dirpath).exists():
        print(f"✓ {description}: {dirpath}")
        return True
    else:
        print(f"✗ {description}: {dirpath} (missing)")
        return False

def main():
    """Main status check function"""
    print("P1 & P2 AS2 Server Setup Status")
    print("=" * 50)
    
    all_good = True
    
    # Check certificates
    print("\nCertificates:")
    cert_files = [
        ('P1_private.pem', 'P1 Private Key + Certificate'),
        ('P1_public.pem', 'P1 Public Certificate'),
        ('P2_private.pem', 'P2 Private Key + Certificate'),
        ('P2_public.pem', 'P2 Public Certificate')
    ]
    
    for cert_file, desc in cert_files:
        if not check_file_exists(cert_file, desc):
            all_good = False
    
    # Check project directories
    print("\nProject Directories:")
    dirs = [
        ('P1', 'P1 Django Project'),
        ('P2', 'P2 Django Project')
    ]
    
    # Check for different P1 structures
    if Path('P1/P1').exists():
        dirs.append(('P1/P1', 'P1 Settings Directory'))
    if Path('P2/P2').exists():
        dirs.append(('P2/P2', 'P2 Settings Directory'))
    
    for dir_path, desc in dirs:
        if not check_directory_exists(dir_path, desc):
            all_good = False
    
    # Check Django files
    print("\nDjango Configuration:")
    django_files = [
        ('P1/manage.py', 'P1 Django Management'),
        ('P2/manage.py', 'P2 Django Management'),
        ('P1/P1/settings.py', 'P1 Settings'),
        ('P2/P2/settings.py', 'P2 Settings'),
        ('P1/P1/urls.py', 'P1 URLs'),
        ('P2/P2/urls.py', 'P2 URLs')
    ]
    
    # Check if P1 has the alternative structure
    if Path('P1/P1/settings.py').exists():
        # Standard structure
        pass
    elif Path('P1/settings.py').exists():
        # Alternative structure - update the file list
        django_files = [
            ('P1/manage.py', 'P1 Django Management'),
            ('P2/manage.py', 'P2 Django Management'),
            ('P1/settings.py', 'P1 Settings'),
            ('P2/P2/settings.py', 'P2 Settings'),
            ('P1/urls.py', 'P1 URLs'),
            ('P2/P2/urls.py', 'P2 URLs')
        ]
    
    for django_file, desc in django_files:
        if not check_file_exists(django_file, desc):
            all_good = False
    
    # Check setup scripts
    print("\nSetup Scripts:")
    setup_scripts = [
        ('generate_certificates.py', 'Certificate Generator'),
        ('setup_pgedge_both.py', 'pgEdge Setup Script'),
        ('setup_p1_pgedge.py', 'P1 AS2 Configuration'),
        ('setup_p2_pgedge.py', 'P2 AS2 Configuration'),
        ('test_file_transfer_pgedge.py', 'File Transfer Test'),
        ('setup_docker_postgres.py', 'Docker PostgreSQL Setup')
    ]
    
    for script, desc in setup_scripts:
        if not check_file_exists(script, desc):
            all_good = False
    
    # Check data directories
    print("\nData Directories:")
    Path('P1/data').mkdir(exist_ok=True)
    Path('P2/data').mkdir(exist_ok=True)
    check_directory_exists('P1/data', 'P1 Data Directory')
    check_directory_exists('P2/data', 'P2 Data Directory')
    
    # Summary
    print("\n" + "=" * 50)
    if all_good:
        print("✓ All components are present!")
    else:
        print("⚠ Some components are missing")
    
    print("\nSetup Options:")
    print("\n1. With Docker PostgreSQL:")
    print("   - Start Docker Desktop")
    print("   - Run: python setup_docker_postgres.py")
    print("   - Run: python setup_pgedge_both.py")
    
    print("\n2. With pgEdge Cloud:")
    print("   - Create pgEdge Cloud account")
    print("   - Set DB_HOST, DB_USER, DB_PASSWORD environment variables")
    print("   - Run: python setup_pgedge_both.py")
    
    print("\n3. With existing PostgreSQL:")
    print("   - Set DB_HOST, DB_USER, DB_PASSWORD environment variables")
    print("   - Run: python setup_pgedge_both.py")
    
    print("\n4. Quick test with SQLite (fallback):")
    print("   - Run: python run_with_sqlite.py")
    
    print("\nAfter setup:")
    print("- Start P1: cd P1 && python start_p1_pgedge.py")
    print("- Start P2: cd P2 && python start_p2_pgedge.py")
    print("- Test: python test_file_transfer_pgedge.py")
    
    print("\nAccess Points:")
    print("- P1 Admin: http://127.0.0.1:8000/admin/ (admin/admin123)")
    print("- P2 Admin: http://127.0.0.1:8001/admin/ (admin/admin123)")
    print("- P1 AS2: http://127.0.0.1:8000/pyas2/as2receive")
    print("- P2 AS2: http://127.0.0.1:8001/pyas2/as2receive")
    
    return all_good

if __name__ == "__main__":
    main()