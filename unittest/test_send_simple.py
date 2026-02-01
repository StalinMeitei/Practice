#!/usr/bin/env python3
"""
Simple AS2 Message Sender - Works in Docker
Run: docker exec p1-as2 python3 /app/unittest/test_send_simple.py
"""
import os
import sys
import tempfile
from datetime import datetime

# Set up Django environment
os.chdir('/app/P1')
sys.path.insert(0, '/app/P1')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django
django.setup()

from django.core.management import call_command
from pyas2.models import Partner, Message

def main():
    print("\n" + "="*70)
    print("AS2 Simple Message Sender")
    print("="*70 + "\n")
    
    # Get initial count
    initial_count = Message.objects.count()
    print(f"Initial message count: {initial_count}")
    
    # Check partners
    partners = Partner.objects.all()
    if not partners.exists():
        print("\n✗ No partners configured!")
        print("Configure at: http://192.168.1.200:8001/admin/pyas2/partner/")
        return False
    
    partner = partners.first()
    print(f"Using partner: {partner.as2_name}\n")
    
    # Send 5 messages
    print("Sending 5 test messages...")
    print("-" * 70)
    
    success_count = 0
    for i in range(1, 6):
        try:
            # Create test content
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            content = f"""Test Message #{i}
Timestamp: {timestamp}
This is a real AS2 message for testing.
"""
            
            # Create temp file in /app/P1/data
            temp_path = f'/app/P1/data/test_msg_{timestamp}_{i}.txt'
            with open(temp_path, 'w') as f:
                f.write(content)
            
            try:
                print(f"[{i}/5] Sending message {i}...", end=" ")
                
                # Send using management command
                call_command('sendas2message',
                           'P1',  # org_as2name
                           partner.as2_name,  # partner_as2name
                           temp_path,  # path_to_payload
                           delete=True)
                
                print("✓ Success")
                success_count += 1
                
            finally:
                # Clean up
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
                    
        except Exception as e:
            print(f"✗ Failed: {e}")
    
    print("-" * 70)
    print(f"\nResults: {success_count}/5 messages sent\n")
    
    # Get final count
    import time
    time.sleep(2)
    final_count = Message.objects.count()
    print(f"Final message count: {final_count}")
    print(f"Increase: +{final_count - initial_count}\n")
    
    if final_count > initial_count:
        print("✅ SUCCESS! Messages sent and counted!\n")
        print("Verify at:")
        print("  - Dashboard: http://192.168.1.200:8001/")
        print("  - Admin: http://192.168.1.200:8001/admin/pyas2/message/")
    else:
        print("⚠ Message count did not increase")
    
    print("\n" + "="*70 + "\n")
    return success_count > 0

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
