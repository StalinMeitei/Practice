#!/usr/bin/env python3
"""
Integration Test: Send AS2 Messages to Server
This script should be run ON the server (192.168.1.200) to send real AS2 messages
Can be run either:
1. Inside Docker container: docker exec -it p1-as2 python3 /app/unittest/test_send_messages_to_server.py
2. On host with proper Django setup
"""
import os
import sys
import django
from pathlib import Path
from datetime import datetime
import time
import tempfile

# Add parent directory to path for Docker environment
sys.path.insert(0, '/app')

def setup_django():
    """Setup Django for P1"""
    # Check if we're in Docker
    if os.path.exists('/app/P1/settings.py'):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
        os.chdir('/app/P1')
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'P1.settings')
    
    django.setup()

def create_test_file(index):
    """Create a test file to send"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    test_content = f"""Integration Test Message #{index}
Timestamp: {timestamp}
Message ID: TEST-{timestamp}-{index}

This is a test message for AS2 integration testing.
The purpose is to verify that messages are being sent, received,
and stored in the database correctly.

Test Details:
- Test Number: {index}
- Date: {datetime.now().isoformat()}
- Purpose: Verify message count increases in Admin/UI
"""
    
    # Create temporary file (works in Docker and host)
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tmp_file:
        tmp_file.write(test_content)
        tmp_file_path = tmp_file.name
    
    return Path(tmp_file_path)

def get_message_count():
    """Get current message count from database"""
    try:
        from pyas2.models import Message
        return Message.objects.count()
    except Exception as e:
        print(f"Warning: Could not get message count: {e}")
        return 0

def send_test_messages(count=5):
    """Send multiple test messages"""
    from django.core.management import call_command
    from pyas2.models import Partner
    
    print(f"\n{'='*70}")
    print(f"AS2 Integration Test - Sending {count} Messages")
    print(f"{'='*70}\n")
    
    # Get initial count
    initial_count = get_message_count()
    print(f"Initial message count: {initial_count}")
    
    # Check if partner exists
    try:
        partners = Partner.objects.all()
        if not partners.exists():
            print("\n✗ No partners configured!")
            print("Please configure at least one partner in the admin interface:")
            print("  http://192.168.1.200:8001/admin/pyas2/partner/")
            return False
        
        # Use first available partner
        partner = partners.first()
        print(f"Using partner: {partner.as2_name}")
        
    except Exception as e:
        print(f"✗ Error checking partners: {e}")
        return False
    
    print(f"\nSending {count} test messages...")
    print("-" * 70)
    
    success_count = 0
    failed_count = 0
    
    for i in range(1, count + 1):
        try:
            # Create test file
            test_file = create_test_file(i)
            print(f"\n[{i}/{count}] Sending: {test_file.name}")
            
            # Send using django-pyas2 management command
            call_command('sendas2message', 
                        '--partner', partner.as2_name,
                        '--file', str(test_file),
                        '--delete')
            
            print(f"  ✓ Message {i} sent successfully")
            success_count += 1
            
            # Small delay between messages
            time.sleep(1)
            
        except Exception as e:
            print(f"  ✗ Message {i} failed: {e}")
            failed_count += 1
        finally:
            # Clean up temp file if it still exists
            if test_file.exists():
                try:
                    test_file.unlink()
                except:
                    pass
    
    print("\n" + "-" * 70)
    print(f"Results: {success_count} succeeded, {failed_count} failed")
    
    # Wait for processing
    print("\nWaiting 3 seconds for messages to be processed...")
    time.sleep(3)
    
    # Get final count
    final_count = get_message_count()
    print(f"\nFinal message count: {final_count}")
    print(f"Increase: +{final_count - initial_count}")
    
    if final_count > initial_count:
        print(f"\n✅ SUCCESS! Message count increased in database!")
        print(f"\nVerify in:")
        print(f"  - Admin: http://192.168.1.200:8001/admin/pyas2/message/")
        print(f"  - Dashboard: http://192.168.1.200:8001/")
        print(f"  - Messages page: http://192.168.1.200:8001/messages")
    else:
        print(f"\n⚠ Message count did not increase.")
        print(f"Check server logs for errors.")
    
    print("\n" + "=" * 70)
    
    return success_count > 0

def main():
    """Main function"""
    print("AS2 Integration Test - Send Messages to Server")
    print("=" * 70)
    print("This script sends real AS2 messages to increase message counts")
    print("=" * 70)
    
    # Setup Django
    try:
        setup_django()
        print("✓ Django environment initialized")
    except Exception as e:
        print(f"✗ Failed to initialize Django: {e}")
        print("\nMake sure you're running this script:")
        print("  - Inside Docker: docker exec -it p1-as2 python3 /app/unittest/test_send_messages_to_server.py")
        print("  - Or from project root: cd /path/to/paomi-as2 && python unittest/test_send_messages_to_server.py")
        return False
    
    # Send test messages
    try:
        return send_test_messages(count=5)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

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
