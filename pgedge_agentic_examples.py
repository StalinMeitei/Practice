#!/usr/bin/env python3
"""
pgEdge Agentic AI Toolkit - Usage Examples for AS2 Servers
"""
import os
from datetime import datetime, timedelta

def example_basic_connection():
    """Example: Basic connection to pgEdge"""
    try:
        from pgedge_agentic_ai import AgenticAI
        
        # Connect to P1 database
        agentic = AgenticAI(
            host='localhost',
            port=5432,
            user='postgres',
            password='postgres',
            database='p1_as2_db'
        )
        
        print("✓ Connected to P1 AS2 database")
        return agentic
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return None

def example_query_messages(agentic):
    """Example: Query AS2 messages with AI"""
    if not agentic:
        return
    
    try:
        # Natural language query
        result = agentic.query(
            "Show me all messages from the last 7 days with their status"
        )
        print("\nRecent Messages:")
        print(result)
    except Exception as e:
        print(f"Query failed: {e}")

def example_analyze_failures(agentic):
    """Example: Analyze failed messages"""
    if not agentic:
        return
    
    try:
        result = agentic.query(
            "Analyze all failed messages and identify common patterns"
        )
        print("\nFailure Analysis:")
        print(result)
    except Exception as e:
        print(f"Analysis failed: {e}")

def example_partner_statistics(agentic):
    """Example: Get partner statistics"""
    if not agentic:
        return
    
    try:
        result = agentic.query(
            "Show message count by partner for the last month"
        )
        print("\nPartner Statistics:")
        print(result)
    except Exception as e:
        print(f"Statistics query failed: {e}")

def example_performance_insights(agentic):
    """Example: Get performance insights"""
    if not agentic:
        return
    
    try:
        result = agentic.query(
            "What are the average processing times for messages by hour of day?"
        )
        print("\nPerformance Insights:")
        print(result)
    except Exception as e:
        print(f"Performance query failed: {e}")

def example_data_quality_check(agentic):
    """Example: Check data quality"""
    if not agentic:
        return
    
    try:
        result = agentic.query(
            "Identify any messages with missing or invalid data"
        )
        print("\nData Quality Check:")
        print(result)
    except Exception as e:
        print(f"Quality check failed: {e}")

def main():
    """Run all examples"""
    print("=" * 60)
    print("pgEdge Agentic AI Toolkit - AS2 Examples")
    print("=" * 60)
    
    # Connect
    agentic = example_basic_connection()
    
    if agentic:
        print("\n" + "=" * 60)
        print("Running Example Queries...")
        print("=" * 60)
        
        # Run examples
        example_query_messages(agentic)
        example_analyze_failures(agentic)
        example_partner_statistics(agentic)
        example_performance_insights(agentic)
        example_data_quality_check(agentic)
    
    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)

if __name__ == "__main__":
    main()
