#!/usr/bin/env python
"""
Setup PostgreSQL database for P1 AS2 server
"""
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os

def get_db_config():
    """Get database configuration from environment or use defaults"""
    return {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': os.getenv('DB_PORT', '5432'),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', 'postgres'),
        'database': os.getenv('DB_NAME', 'p1_as2_db')
    }

def create_database():
    """Create the P1 AS2 database if it doesn't exist"""
    config = get_db_config()
    
    try:
        # Connect to PostgreSQL server (default database)
        conn = psycopg2.connect(
            host=config['host'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            database='postgres'  # Connect to default database first
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (config['database'],))
        exists = cursor.fetchone()
        
        if not exists:
            # Create database
            cursor.execute(f"CREATE DATABASE {config['database']}")
            print(f"Database '{config['database']}' created successfully!")
        else:
            print(f"Database '{config['database']}' already exists.")
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        print(f"\nConnection details:")
        print(f"  Host: {config['host']}")
        print(f"  Port: {config['port']}")
        print(f"  User: {config['user']}")
        print(f"  Database: {config['database']}")
        print("\nPlease ensure:")
        print("1. PostgreSQL/pgEdge is running")
        print("2. Connection details are correct")
        print("3. User has permission to create databases")
        print("\nYou can set environment variables:")
        print("  DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME")
        return False

def test_connection():
    """Test connection to the target database"""
    config = get_db_config()
    
    try:
        conn = psycopg2.connect(
            host=config['host'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            database=config['database']
        )
        conn.close()
        print(f"✓ Successfully connected to database '{config['database']}'")
        return True
    except psycopg2.Error as e:
        print(f"✗ Failed to connect to database '{config['database']}': {e}")
        return False

if __name__ == "__main__":
    print("Setting up PostgreSQL database for P1 AS2 server...")
    print("=" * 50)
    
    if create_database():
        if test_connection():
            print("\nDatabase setup completed successfully!")
            print("You can now run: python manage.py migrate")
        else:
            print("\nDatabase created but connection test failed.")
    else:
        print("\nDatabase setup failed. Please check your PostgreSQL configuration.")
        print("\nFor pgEdge setup instructions, see: setup_pgedge.md")