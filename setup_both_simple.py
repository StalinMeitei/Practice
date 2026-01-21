#!/usr/bin/env python
"""
Simple setup script for both P1 and P2 AS2 servers
"""
import os
import subprocess
import sys
from pathlib import Path

def run_command(command, cwd=None):
    """Run a command and return success status"""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            return False
        print(result.stdout)
        return True
    except Exception as e:
        print(f"Exception: {e}")
        return False

def main():
    """Main setup function"""
    print("Setting up P1 and P2 AS2 Servers")
    print("=" * 50)
    
    # Check certificates
    if not Path('P1_private.pem').exists():
        print("Generating certificates...")
        if not run_command("python generate_certificates.py"):
            return False
    
    # Setup P1
    print("\nSetting up P1...")
    if not run_command("python manage.py migrate", cwd="P1"):
        return False
    
    if not run_command("python manage.py shell -c \"from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@p1.com', 'admin123')\"", cwd="P1"):
        return False
    
    # Setup P2
    print("\nSetting up P2...")
    if not run_command("python manage.py migrate", cwd="P2"):
        return False
    
    if not run_command("python manage.py shell -c \"from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@p2.com', 'admin123')\"", cwd="P2"):
        return False
    
    # Create data directories
    Path('P1/data').mkdir(exist_ok=True)
    Path('P2/data').mkdir(exist_ok=True)
    
    print("\n" + "=" * 50)
    print("✓ Basic setup completed!")
    print("\nTo configure AS2 settings, run:")
    print("1. cd P1 && python ../run_with_sqlite.py")
    print("2. cd P2 && python ../run_p2_sqlite.py")
    
    return True

if __name__ == "__main__":
    if not main():
        sys.exit(1)