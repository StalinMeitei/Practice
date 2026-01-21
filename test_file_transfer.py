#!/usr/bin/env python
"""
Test file transfer from P1 to P2
"""
import os
import sys
import django
from pathlib import Path

def setup_django():
    """Setup Django for P1"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'P1.settings')
    
    # Override to use SQLite
    import P1.settings as settings
    settings.DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'P1/p1_as2_db.sqlite3',
        }
    }
    
    django.setup()

def create_test_file():
    """Create a test file to send"""
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
    test_file_path = Path('P1/data/test_message.edi')
    test_file_path.parent.mkdir(exist_ok=True)
    
    with open(test_file_path, 'w') as f:
        f.write(test_content)
    
    print(f"✓ Test file created: {test_file_path}")
    return test_file_path

def send_file():
    """Send file from P1 to P2"""
    from django.core.management import call_command
    
    # Create test file
    test_file = create_test_file()
    
    print("Sending file from P1 to P2...")
    
    try:
        # Use django-pyas2 management command to send file
        call_command('sendas2message', 
                    '--partner', 'P2',
                    '--file', str(test_file),
                    '--delete')
        
        print("✓ File sent successfully!")
        print("\nCheck the following:")
        print("1. P1 Admin: http://127.0.0.1:8000/admin/pyas2/message/")
        print("2. P2 Admin: http://127.0.0.1:8001/admin/pyas2/message/")
        print("3. P2 data directory for received file")
        
    except Exception as e:
        print(f"✗ Error sending file: {e}")
        print("\nMake sure both P1 and P2 servers are running:")
        print("1. cd P1 && python start_p1.py")
        print("2. cd P2 && python start_p2.py")
        return False
    
    return True

def main():
    """Main function"""
    print("Testing AS2 File Transfer from P1 to P2")
    print("=" * 40)
    
    # Setup Django
    setup_django()
    
    # Send test file
    if not send_file():
        return False
    
    print("\n" + "=" * 40)
    print("✓ File transfer test completed!")
    
    return True

if __name__ == "__main__":
    try:
        if not main():
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)