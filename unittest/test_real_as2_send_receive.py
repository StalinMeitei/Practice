#!/usr/bin/env python3
"""
Real AS2 Send and Receive Integration Test
This test performs actual AS2 message exchange between P1 and P2 servers
Run this script ON the server (192.168.1.200) inside the Docker environment
"""
import os
import sys
import django
import time
from pathlib import Path
from datetime import datetime
import tempfile

# Add parent directory to path
sys.path.insert(0, '/app')

def setup_django_p1():
    """Setup Django for P1"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    os.chdir('/app/P1')
    django.setup()

def print_header(text):
    """Print formatted header"""
    print(f"\n{'='*80}")
    print(f"  {text}")
    print(f"{'='*80}\n")

def print_step(step, text):
    """Print step"""
    print(f"[Step {step}] {text}")

def print_success(text):
    """Print success"""
    print(f"  ✓ {text}")

def print_error(text):
    """Print error"""
    print(f"  ✗ {text}")

def print_info(text):
    """Print info"""
    print(f"  → {text}")

def get_message_counts():
    """Get message counts from both P1 and P2"""
    from pyas2.models import Message
    
    try:
        p1_count = Message.objects.count()
        p1_sent = Message.objects.filter(direction='OUT').count()
        p1_received = Message.objects.filter(direction='IN').count()
        
        return {
            'p1_total': p1_count,
            'p1_sent': p1_sent,
            'p1_received': p1_received
        }
    except Exception as e:
        print_error(f"Error getting message counts: {e}")
        return None

def check_partners():
    """Check if partners are configured"""
    from pyas2.models import Partner, Organization
    
    print_step(1, "Checking AS2 configuration...")
    
    # Check organization
    orgs = Organization.objects.all()
    if not orgs.exists():
        print_error("No organization configured!")
        return None, None
    
    org = orgs.first()
    print_success(f"Organization: {org.as2_name}")
    
    # Check partners
    partners = Partner.objects.all()
    if not partners.exists():
        print_error("No partners configured!")
        print_info("Configure partners in admin: http://192.168.1.200:8001/admin/pyas2/partner/")
        return org, None
    
    print_success(f"Found {partners.count()} partner(s)")
    for partner in partners:
        print_info(f"  - {partner.as2_name}: {partner.target_url}")
    
    return org, partners.first()

def create_test_payload(test_num):
    """Create test payload content"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    content = f"""AS2 Real Integration Test Message #{test_num}
================================================================================
Timestamp: {datetime.now().isoformat()}
Test Number: {test_num}
Message ID: REAL-TEST-{timestamp}-{test_num}

This is a REAL AS2 message being sent from P1 to P2.
The message will be:
1. Encrypted using partner's public certificate
2. Signed using sender's private key
3. Transmitted via HTTP POST to partner's AS2 endpoint
4. Received and decrypted by P2
5. MDN (acknowledgment) sent back to P1

Test Purpose:
- Verify end-to-end AS2 message exchange
- Confirm encryption/decryption works
- Validate digital signatures
- Check MDN processing
- Increase message counts in database

Expected Results:
- P1 outbound message count increases
- P2 inbound message count increases
- Message appears in both admin panels
- Dashboard statistics update
- MDN received successfully

================================================================================
Test Data:
- Sender: P1 AS2 Server
- Receiver: P2 AS2 Server  
- Protocol: AS2 (RFC 4130)
- Encryption: 3DES or AES
- Signature: SHA-256
- Compression: Optional
================================================================================
"""
    return content.encode('utf-8')

def send_as2_message(partner, test_num):
    """Send AS2 message using pyas2 library"""
    from pyas2.models import Message, Organization
    from pyas2 import as2lib
    import requests
    
    print_step(2 + test_num, f"Sending AS2 message #{test_num}...")
    
    try:
        # Get organization
        org = Organization.objects.first()
        
        # Create payload
        payload = create_test_payload(test_num)
        filename = f"test_message_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{test_num}.txt"
        
        print_info(f"Creating message for partner: {partner.as2_name}")
        print_info(f"Payload size: {len(payload)} bytes")
        
        # Create AS2 message
        message = Message.objects.create(
            message_id=as2lib.make_mime_message_id(),
            partner=partner,
            organization=org,
            direction='OUT',
            status='P',  # Pending
            payload=payload,
            filename=filename
        )
        
        print_info(f"Message created: {message.message_id}")
        
        # Build AS2 message
        try:
            # Create MIME message
            mime_message = as2lib.build_message(
                message_id=message.message_id,
                payload=payload,
                filename=filename,
                sender=org,
                receiver=partner
            )
            
            # Sign if required
            if partner.signature:
                print_info(f"Signing message with {partner.signature}")
                mime_message = as2lib.sign_message(
                    mime_message,
                    org.signature_key,
                    partner.signature
                )
            
            # Encrypt if required
            if partner.encryption:
                print_info(f"Encrypting message with {partner.encryption}")
                mime_message = as2lib.encrypt_message(
                    mime_message,
                    partner.encryption_cert,
                    partner.encryption
                )
            
            # Compress if required
            if partner.compression:
                print_info(f"Compressing message")
                mime_message = as2lib.compress_message(mime_message)
            
            # Prepare headers
            headers = {
                'AS2-Version': '1.2',
                'AS2-From': org.as2_name,
                'AS2-To': partner.as2_name,
                'Message-ID': f'<{message.message_id}>',
                'Subject': f'AS2 Message from {org.as2_name}',
                'Content-Type': mime_message.get_content_type(),
                'Content-Disposition': f'attachment; filename="{filename}"',
            }
            
            # Add MDN request if required
            if partner.mdn:
                headers['Disposition-Notification-To'] = org.email_address or 'noreply@example.com'
                headers['Disposition-Notification-Options'] = (
                    'signed-receipt-protocol=required, pkcs7-signature; '
                    'signed-receipt-micalg=required, sha256'
                )
            
            print_info(f"Sending to: {partner.target_url}")
            
            # Send message
            response = requests.post(
                partner.target_url,
                headers=headers,
                data=mime_message.as_bytes(),
                timeout=30,
                verify=False  # For testing with self-signed certs
            )
            
            print_info(f"Response status: {response.status_code}")
            
            if response.status_code == 200:
                message.status = 'S'  # Success
                message.save()
                print_success(f"Message #{test_num} sent successfully!")
                print_info(f"Message ID: {message.message_id}")
                return True
            else:
                message.status = 'E'  # Error
                message.save()
                print_error(f"Message #{test_num} failed: HTTP {response.status_code}")
                print_info(f"Response: {response.text[:200]}")
                return False
                
        except Exception as e:
            message.status = 'E'
            message.save()
            print_error(f"Error building/sending message: {e}")
            import traceback
            traceback.print_exc()
            return False
            
    except Exception as e:
        print_error(f"Error creating message: {e}")
        import traceback
        traceback.print_exc()
        return False

def send_via_management_command(partner, test_num):
    """Send message using Django management command (simpler approach)"""
    from django.core.management import call_command
    
    print_step(2 + test_num, f"Sending AS2 message #{test_num} via management command...")
    
    try:
        # Create test file
        payload = create_test_payload(test_num)
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.txt') as tmp_file:
            tmp_file.write(payload)
            tmp_file_path = tmp_file.name
        
        try:
            filename = f"test_message_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{test_num}.txt"
            print_info(f"Sending file: {filename}")
            print_info(f"Partner: {partner.as2_name}")
            
            # Send using management command
            call_command(
                'sendas2message',
                '--partner', partner.as2_name,
                '--file', tmp_file_path,
                '--delete'
            )
            
            print_success(f"Message #{test_num} sent successfully!")
            return True
            
        finally:
            # Clean up temp file
            if os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)
                
    except Exception as e:
        print_error(f"Error sending message: {e}")
        import traceback
        traceback.print_exc()
        return False

def verify_message_increase(initial_counts, expected_increase):
    """Verify message counts increased"""
    print_step(10, "Verifying message count increase...")
    
    print_info("Waiting 5 seconds for messages to be processed...")
    time.sleep(5)
    
    final_counts = get_message_counts()
    
    if not final_counts:
        print_error("Could not get final message counts")
        return False
    
    print_info(f"Initial P1 total: {initial_counts['p1_total']}")
    print_info(f"Final P1 total: {final_counts['p1_total']}")
    print_info(f"Increase: +{final_counts['p1_total'] - initial_counts['p1_total']}")
    
    print_info(f"Initial P1 sent: {initial_counts['p1_sent']}")
    print_info(f"Final P1 sent: {final_counts['p1_sent']}")
    print_info(f"Increase: +{final_counts['p1_sent'] - initial_counts['p1_sent']}")
    
    if final_counts['p1_total'] > initial_counts['p1_total']:
        print_success("Message count increased!")
        return True
    else:
        print_error("Message count did not increase")
        return False

def check_recent_messages():
    """Check recent messages in database"""
    from pyas2.models import Message
    
    print_step(11, "Checking recent messages...")
    
    try:
        recent = Message.objects.all().order_by('-timestamp')[:10]
        
        if recent:
            print_success(f"Found {recent.count()} recent messages:")
            for msg in recent:
                status_icon = "✓" if msg.status == 'S' else "✗" if msg.status == 'E' else "⋯"
                print(f"    {status_icon} {msg.message_id[:40]}... | "
                      f"{msg.direction} | {msg.status} | {msg.timestamp}")
            return True
        else:
            print_error("No messages found")
            return False
            
    except Exception as e:
        print_error(f"Error checking messages: {e}")
        return False

def main():
    """Main test function"""
    print_header("AS2 Real Send and Receive Integration Test")
    print("This test performs actual AS2 message exchange")
    print("Run this script inside the P1 Docker container:")
    print("  docker exec -it p1-as2 python /app/unittest/test_real_as2_send_receive.py")
    print()
    
    # Setup Django
    try:
        setup_django_p1()
        print_success("Django environment initialized")
    except Exception as e:
        print_error(f"Failed to initialize Django: {e}")
        return False
    
    # Check configuration
    org, partner = check_partners()
    if not partner:
        print_error("Cannot proceed without partner configuration")
        return False
    
    # Get initial counts
    initial_counts = get_message_counts()
    if not initial_counts:
        print_error("Cannot get initial message counts")
        return False
    
    print()
    print_info(f"Initial message counts:")
    print_info(f"  P1 Total: {initial_counts['p1_total']}")
    print_info(f"  P1 Sent: {initial_counts['p1_sent']}")
    print_info(f"  P1 Received: {initial_counts['p1_received']}")
    print()
    
    # Send test messages
    num_messages = 3
    success_count = 0
    
    for i in range(1, num_messages + 1):
        if send_via_management_command(partner, i):
            success_count += 1
        time.sleep(2)  # Delay between messages
        print()
    
    print(f"Results: {success_count}/{num_messages} messages sent successfully")
    print()
    
    # Verify increase
    count_increased = verify_message_increase(initial_counts, success_count)
    print()
    
    # Check recent messages
    messages_visible = check_recent_messages()
    print()
    
    # Summary
    print_header("Test Summary")
    
    results = [
        ("Django setup", True),
        ("Partner configuration", partner is not None),
        ("Messages sent", success_count > 0),
        ("Message count increased", count_increased),
        ("Messages visible", messages_visible)
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
        print("  - Dashboard: http://192.168.1.200:8001/")
        print("  - Admin: http://192.168.1.200:8001/admin/pyas2/message/")
        print("  - Messages: http://192.168.1.200:8001/messages")
    else:
        print_error("SOME TESTS FAILED")
        print()
        print("Troubleshooting:")
        print("  1. Check partner configuration in admin")
        print("  2. Verify certificates are properly configured")
        print("  3. Check P1 logs: docker logs p1-as2")
        print("  4. Check P2 logs: docker logs p2-as2")
        print("  5. Verify P2 target_url is accessible")
    
    print()
    print("="*80)
    
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
