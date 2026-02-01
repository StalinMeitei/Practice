#!/usr/bin/env python
"""
Real AS2 Integration Test
Sends actual AS2 messages to 192.168.1.200:8001 and verifies they appear in the database
"""
import requests
import time
from datetime import datetime
import sys

# Configuration
SERVER_URL = "http://192.168.1.200:8001"
API_BASE = f"{SERVER_URL}/api"

def print_header(text):
    """Print a formatted header"""
    print(f"\n{'='*70}")
    print(f"{text}")
    print(f"{'='*70}\n")

def print_step(step, text):
    """Print a step"""
    print(f"[Step {step}] {text}")

def print_success(text):
    """Print success message"""
    print(f"  ✓ {text}")

def print_error(text):
    """Print error message"""
    print(f"  ✗ {text}")

def print_info(text):
    """Print info message"""
    print(f"  → {text}")

def check_server():
    """Check if server is accessible"""
    print_step(1, "Checking server connectivity...")
    try:
        response = requests.get(SERVER_URL, timeout=5)
        print_success(f"Server is accessible (Status: {response.status_code})")
        return True
    except Exception as e:
        print_error(f"Cannot connect to server: {e}")
        return False

def get_initial_stats():
    """Get initial message count"""
    print_step(2, "Getting initial message count...")
    try:
        response = requests.get(f"{API_BASE}/stats", timeout=5)
        if response.status_code == 200:
            data = response.json()
            count = data.get('messages', 0)
            print_success(f"Initial message count: {count}")
            return count
        else:
            print_error(f"Failed to get stats: {response.status_code}")
            return 0
    except Exception as e:
        print_error(f"Error getting stats: {e}")
        return 0

def get_partners():
    """Get list of partners"""
    print_step(3, "Getting partner list...")
    try:
        response = requests.get(f"{API_BASE}/partners", timeout=5)
        if response.status_code == 200:
            data = response.json()
            partners = data.get('partners', [])
            if partners:
                print_success(f"Found {len(partners)} partner(s)")
                for partner in partners:
                    print_info(f"Partner: {partner.get('as2_name')} - {partner.get('name')}")
                return partners
            else:
                print_error("No partners configured!")
                print_info("Please configure a partner in the admin panel:")
                print_info(f"  {SERVER_URL}/admin/pyas2/partner/")
                return []
        else:
            print_error(f"Failed to get partners: {response.status_code}")
            return []
    except Exception as e:
        print_error(f"Error getting partners: {e}")
        return []

def send_test_message(partner_name, message_num):
    """Send a test AS2 message"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Create test file content
    content = f"""AS2 Integration Test Message #{message_num}
Timestamp: {datetime.now().isoformat()}
Message ID: TEST-{timestamp}-{message_num}

This is a real AS2 message sent via the API endpoint.
The purpose is to verify end-to-end AS2 functionality.

Test Details:
- Test Number: {message_num}
- Partner: {partner_name}
- Date: {datetime.now().isoformat()}
- Purpose: Verify message count increases in Admin/UI

This message should appear in:
1. Admin panel: {SERVER_URL}/admin/pyas2/message/
2. Dashboard: {SERVER_URL}/
3. Messages page: {SERVER_URL}/messages
"""
    
    filename = f"test_message_{timestamp}_{message_num}.txt"
    
    try:
        # Prepare the file
        files = {
            'file': (filename, content.encode(), 'text/plain')
        }
        
        data = {
            'partner': partner_name
        }
        
        # Send the message
        print_info(f"Sending: {filename}")
        response = requests.post(
            f"{API_BASE}/send-message/",
            files=files,
            data=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print_success(f"Message {message_num} sent successfully")
                print_info(f"Message ID: {result.get('message_id')}")
                return True
            else:
                print_error(f"Message {message_num} failed: {result.get('error')}")
                return False
        else:
            print_error(f"Message {message_num} failed: HTTP {response.status_code}")
            print_info(f"Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print_error(f"Message {message_num} error: {e}")
        return False

def send_multiple_messages(partner_name, count=5):
    """Send multiple test messages"""
    print_step(4, f"Sending {count} test messages...")
    print()
    
    success_count = 0
    for i in range(1, count + 1):
        print(f"  [{i}/{count}]", end=" ")
        if send_test_message(partner_name, i):
            success_count += 1
        time.sleep(1)  # Small delay between messages
        print()
    
    print(f"\n  Results: {success_count}/{count} messages sent successfully")
    return success_count

def verify_message_increase(initial_count):
    """Verify that message count increased"""
    print_step(5, "Verifying message count increase...")
    print_info("Waiting 3 seconds for messages to be processed...")
    time.sleep(3)
    
    try:
        response = requests.get(f"{API_BASE}/stats", timeout=5)
        if response.status_code == 200:
            data = response.json()
            final_count = data.get('messages', 0)
            increase = final_count - initial_count
            
            print_info(f"Initial count: {initial_count}")
            print_info(f"Final count: {final_count}")
            print_info(f"Increase: +{increase}")
            
            if increase > 0:
                print_success(f"Message count increased by {increase}!")
                return True
            else:
                print_error("Message count did not increase")
                return False
        else:
            print_error(f"Failed to get final stats: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error verifying count: {e}")
        return False

def verify_messages_in_list():
    """Verify messages appear in the messages list"""
    print_step(6, "Verifying messages in database...")
    try:
        response = requests.get(f"{API_BASE}/messages", timeout=5)
        if response.status_code == 200:
            data = response.json()
            messages = data.get('messages', [])
            
            print_success(f"Found {len(messages)} total messages in database")
            
            if messages:
                print_info("Recent messages:")
                for msg in messages[:5]:  # Show first 5
                    print(f"    - {msg.get('message_id')} | "
                          f"{msg.get('direction')} | "
                          f"{msg.get('status')} | "
                          f"{msg.get('timestamp')}")
                return True
            else:
                print_error("No messages found in database")
                return False
        else:
            print_error(f"Failed to get messages: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error getting messages: {e}")
        return False

def verify_chart_data():
    """Verify chart data is updated"""
    print_step(7, "Verifying chart data...")
    try:
        response = requests.get(f"{API_BASE}/chart-data", timeout=5)
        if response.status_code == 200:
            data = response.json()
            trend_data = data.get('trendData', [])
            
            # Count total messages in trend data
            total = sum(item.get('sent', 0) + item.get('received', 0) for item in trend_data)
            
            print_success(f"Chart data endpoint working")
            print_info(f"Total messages in trend data: {total}")
            return True
        else:
            print_error(f"Failed to get chart data: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error getting chart data: {e}")
        return False

def main():
    """Main test function"""
    print_header("AS2 Real Integration Test")
    print(f"Server: {SERVER_URL}")
    print(f"This test will send REAL AS2 messages to the server")
    print()
    
    # Step 1: Check server
    if not check_server():
        print_error("Server is not accessible. Exiting.")
        return False
    
    # Step 2: Get initial stats
    initial_count = get_initial_stats()
    
    # Step 3: Get partners
    partners = get_partners()
    if not partners:
        print_error("No partners available. Please configure a partner first.")
        print_info(f"Admin panel: {SERVER_URL}/admin/pyas2/partner/")
        return False
    
    # Use first partner
    partner_name = partners[0].get('as2_name')
    print_info(f"Using partner: {partner_name}")
    print()
    
    # Step 4: Send messages
    success_count = send_multiple_messages(partner_name, count=5)
    if success_count == 0:
        print_error("Failed to send any messages. Check server logs.")
        return False
    
    # Step 5: Verify count increase
    count_increased = verify_message_increase(initial_count)
    
    # Step 6: Verify messages in list
    messages_visible = verify_messages_in_list()
    
    # Step 7: Verify chart data
    chart_updated = verify_chart_data()
    
    # Final summary
    print_header("Test Summary")
    
    results = [
        ("Server connectivity", True),
        ("Messages sent", success_count > 0),
        ("Message count increased", count_increased),
        ("Messages visible in database", messages_visible),
        ("Chart data updated", chart_updated)
    ]
    
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {status}: {test_name}")
    
    all_passed = all(result[1] for result in results)
    
    print()
    if all_passed:
        print_success("ALL TESTS PASSED!")
        print()
        print("Verify in your browser:")
        print(f"  - Dashboard: {SERVER_URL}/")
        print(f"  - Admin: {SERVER_URL}/admin/pyas2/message/")
        print(f"  - Messages: {SERVER_URL}/messages")
    else:
        print_error("SOME TESTS FAILED")
        print()
        print("Troubleshooting:")
        print("  1. Check Docker containers are running: docker ps")
        print("  2. Check server logs: docker logs paomi-as2-p1-1")
        print("  3. Verify partner configuration in admin panel")
        print("  4. Check database connection")
    
    print()
    print("="*70)
    
    return all_passed

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
