#!/usr/bin/env python
"""
Setup Docker PostgreSQL for testing P1 and P2 AS2 servers
"""
import subprocess
import time
import psycopg2
import sys

def run_command(command):
    """Run a shell command"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            return False
        if result.stdout.strip():
            print(result.stdout.strip())
        return True
    except Exception as e:
        print(f"Exception: {e}")
        return False

def check_docker():
    """Check if Docker is available"""
    return run_command("docker --version")

def setup_postgres_container():
    """Setup PostgreSQL container"""
    print("Setting up PostgreSQL container...")
    
    # Stop and remove existing container if it exists
    run_command("docker stop pgedge-as2 2>nul")
    run_command("docker rm pgedge-as2 2>nul")
    
    # Start new PostgreSQL container
    cmd = "docker run --name pgedge-as2 -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:15"
    if not run_command(cmd):
        return False
    
    print("✓ PostgreSQL container started")
    print("Waiting for PostgreSQL to be ready...")
    
    # Wait for PostgreSQL to be ready
    for i in range(30):
        try:
            conn = psycopg2.connect(
                host="localhost",
                port="5432",
                user="postgres",
                password="postgres",
                database="postgres"
            )
            conn.close()
            print("✓ PostgreSQL is ready!")
            return True
        except psycopg2.Error:
            time.sleep(1)
            print(f"  Waiting... ({i+1}/30)")
    
    print("✗ PostgreSQL failed to start within 30 seconds")
    return False

def main():
    """Main setup function"""
    print("Setting up Docker PostgreSQL for AS2 Servers")
    print("=" * 50)
    
    # Check Docker
    if not check_docker():
        print("✗ Docker is not available")
        print("\nPlease install Docker or set up PostgreSQL manually:")
        print("1. Install Docker Desktop")
        print("2. Or install PostgreSQL directly")
        print("3. Or use pgEdge Cloud")
        return False
    
    print("✓ Docker is available")
    
    # Setup PostgreSQL container
    if not setup_postgres_container():
        return False
    
    print("\n" + "=" * 50)
    print("✓ PostgreSQL setup completed!")
    print("\nConnection details:")
    print("  Host: localhost")
    print("  Port: 5432")
    print("  User: postgres")
    print("  Password: postgres")
    
    print("\nNext steps:")
    print("1. Run: python setup_pgedge_both.py")
    print("2. Start servers and test file transfer")
    
    print("\nTo stop PostgreSQL later:")
    print("  docker stop pgedge-as2")
    
    return True

if __name__ == "__main__":
    if not main():
        sys.exit(1)