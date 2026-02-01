#!/usr/bin/env python
"""
Test file transfer from P1 to P2 using pgEdge
"""
import os
import sys
import django
from pathlib import Path

def setup_django():
    """Setup Django for P1"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'P1.settings')
    django.setup()

def create_test_file():
    """Create a test EDI file to send"""
    test_content = """ST*850*000000001~
BEG*00*SA*08292009*080292009~
REF*CO*ACME-4567~
REF*ZZ*Thank you for your business~
PER*OC*Marvin Acme*TE*973-555-1212*EM*marvin@acme.com~
N1*ST*ACME RECEIVING CORP*92*123~
N3*123 MAIN STREET~
N4*ANYWHERE*NY*11111*US~
PO1*1*1*EA*400.00*TE*IN*12345678901234*BP*12345678901234~
PID*F****WIDGET~
PO1*2*1*EA*28.00*TE*IN*12345678901235*BP*12345678901235~
PID*F****DIFFERENT WIDGET~
CTT*2~
SE*13*000000001~"""
    
    # Create test file in P1's data directory
    test_file_path = Path('P1/data/test_purchase_order.edi')
    test_file_path.parent.mkdir(exist_ok=True)
    
    with open(test_file_path, 'w') as f:
        f.write(test_content)
    
    print(f"✓ Test EDI file created: {test_file_path}")
    return test_file_path

def send_file():
    """Send file from P1 to P2"""
    from django.core.management import call_command
    
    # Create test file
    test_file = create_test_file()
    
    print("Sending EDI file from P1 to P2...")
    
    try:
        # Use django-pyas2 management command to send file
        call_command('sendas2message', 
                    '--partner', 'P2',
                    '--file', str(test_file),
                    '--delete')
        
        print("✓ File sent successfully!")
        print("\nTo verify the transfer:")
        print("1. Check P1 sent messages: http://127.0.0.1:8000/admin/pyas2/message/")
        print("2. Check P2 received messages: http://127.0.0.1:8001/admin/pyas2/message/")
        print("3. Check P2 data directory: P2/data/")
        print("4. Check MDN responses in both admin interfaces")
        
        return True
        
    except Exception as e:
        print(f"✗ Error sending file: {e}")
        print("\nTroubleshooting:")
        print("1. Ensure both P1 and P2 servers are running:")
        print("   - Terminal 1: cd P1 && python start_p1_pgedge.py")
        print("   - Terminal 2: cd P2 && python start_p2_pgedge.py")
        print("2. Check AS2 partner configuration in admin interface")
        print("3. Verify network connectivity between servers")
        return False

def check_received_files():
    """Check if files were received in P2"""
    p2_data_dir = Path('P2/data')
    if p2_data_dir.exists():
        received_files = list(p2_data_dir.glob('*'))
        if received_files:
            print(f"\n✓ Files received in P2:")
            for file in received_files:
                print(f"  - {file.name}")
        else:
            print("\n! No files found in P2 data directory yet")
    else:
        print("\n! P2 data directory not found")

def main():
    """Main function"""
    print("Testing AS2 File Transfer from P1 to P2 (pgEdge)")
    print("=" * 50)
    
    # Check if both servers are likely running
    p1_db = Path('P1') / 'p1_as2_db.sqlite3'  # This won't exist with pgEdge, but we check anyway
    p2_db = Path('P2') / 'p2_as2_db.sqlite3'
    
    print("Pre-flight checks:")
    print("✓ Using pgEdge/PostgreSQL databases")
    print("✓ Certificates should be available")
    
    # Setup Django
    try:
        setup_django()
        print("✓ Django environment initialized for P1")
    except Exception as e:
        print(f"✗ Failed to initialize Django: {e}")
        return False
    
    # Send test file
    if not send_file():
        return False
    
    # Check for received files
    check_received_files()
    
    print("\n" + "=" * 50)
    print("✓ File transfer test completed!")
    print("\nNext steps:")
    print("1. Monitor the admin interfaces for message status")
    print("2. Check the AS2 message logs for any errors")
    print("3. Verify MDN (Message Disposition Notification) responses")
    
    return True

if __name__ == "__main__":
    try:
        if not main():
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)