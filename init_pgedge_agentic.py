#!/usr/bin/env python3
"""
Initialize pgEdge Agentic AI Toolkit for AS2 servers
"""
import os
import sys

def init_pgedge_agentic():
    """Initialize pgEdge Agentic AI Toolkit"""
    try:
        from pgedge_agentic_ai import AgenticAI
        
        # Database connection parameters
        db_config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', 5432)),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', 'postgres'),
            'database': os.getenv('DB_NAME', 'postgres')
        }
        
        print(f"Initializing pgEdge Agentic AI for database: {db_config['database']}")
        
        # Initialize Agentic AI
        agentic = AgenticAI(
            host=db_config['host'],
            port=db_config['port'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database']
        )
        
        print("✓ pgEdge Agentic AI Toolkit initialized successfully")
        return agentic
        
    except ImportError:
        print("⚠ pgEdge Agentic AI Toolkit not installed. Install with: pip install pgedge-agentic-ai")
        return None
    except Exception as e:
        print(f"⚠ Error initializing pgEdge Agentic AI: {e}")
        return None

if __name__ == "__main__":
    init_pgedge_agentic()
