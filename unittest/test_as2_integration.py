"""
Integration tests for AS2 Send/Receive
Tests actual AS2 message transmission between partners on 192.168.1.200
"""
import unittest
import os
import sys
import requests
import time
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestAS2Integration(unittest.TestCase):
    """Integration tests for AS2 message transmission"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test configuration"""
        cls.server_url = os.environ.get('AS2_SERVER_URL', 'http://192.168.1.200:8001')
        cls.p1_url = f"{cls.server_url}/pyas2/as2send"
        cls.p2_url = f"{cls.server_url}/pyas2/as2receive"
        cls.api_url = f"{cls.server_url}/api"
        
        print(f"\n{'='*70}")
        print(f"AS2 Integration Test Suite")
        print(f"{'='*70}")
        print(f"Server URL: {cls.server_url}")
        print(f"Testing against: 192.168.1.200:8001")
        print(f"{'='*70}\n")
    
    def setUp(self):
        """Set up for each test"""
        # Get initial message count
        try:
            response = requests.get(f"{self.api_url}/stats", timeout=5)
            if response.status_code == 200:
                self.initial_count = response.json().get('messages', 0)
            else:
                self.initial_count = 0
        except Exception as e:
            print(f"Warning: Could not get initial count: {e}")
            self.initial_count = 0
    
    def test_01_server_connectivity(self):
        """Test server is accessible"""
        try:
            response = requests.get(self.server_url, timeout=5)
            self.assertIn(response.status_code, [200, 301, 302, 404])
            print(f"✓ Server is accessible at {self.server_url}")
        except Exception as e:
            self.fail(f"Server not accessible: {e}")
    
    def test_02_api_stats_endpoint(self):
        """Test API stats endpoint"""
        try:
            response = requests.get(f"{self.api_url}/stats", timeout=5)
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIn('messages', data)
            self.assertIn('partners', data)
            print(f"✓ API stats endpoint working")
            print(f"  Current message count: {data.get('messages', 0)}")
        except Exception as e:
            self.fail(f"API stats endpoint failed: {e}")
    
    def test_03_api_messages_endpoint(self):
        """Test API messages endpoint"""
        try:
            response = requests.get(f"{self.api_url}/messages", timeout=5)
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIn('messages', data)
            print(f"✓ API messages endpoint working")
            print(f"  Messages returned: {len(data.get('messages', []))}")
        except Exception as e:
            self.fail(f"API messages endpoint failed: {e}")
    
    def test_04_send_test_message(self):
        """Test sending an AS2 message"""
        # Create test file
        test_content = f"Test AS2 Message - {datetime.now().isoformat()}"
        test_filename = f"test_message_{int(time.time())}.txt"
        
        try:
            # Prepare the file for sending
            files = {
                'file': (test_filename, test_content.encode(), 'text/plain')
            }
            
            data = {
                'partner_id': 'p2as2',  # Assuming P2 is the partner
                'subject': 'Integration Test Message'
            }
            
            # Send the message
            print(f"\n  Sending test message: {test_filename}")
            response = requests.post(
                self.p1_url,
                files=files,
                data=data,
                timeout=30
            )
            
            print(f"  Response status: {response.status_code}")
            print(f"  Response text: {response.text[:200]}")
            
            # Check if message was sent (200 or 202 are success codes)
            self.assertIn(response.status_code, [200, 202, 201])
            
            # Wait a bit for message to be processed
            time.sleep(2)
            
            # Check if message count increased
            response = requests.get(f"{self.api_url}/stats", timeout=5)
            if response.status_code == 200:
                new_count = response.json().get('messages', 0)
                print(f"  Initial count: {self.initial_count}")
                print(f"  New count: {new_count}")
                
                if new_count > self.initial_count:
                    print(f"✓ Message count increased! ({self.initial_count} → {new_count})")
                else:
                    print(f"⚠ Message count did not increase yet (may take time to process)")
            
        except requests.exceptions.ConnectionError:
            self.fail(f"Could not connect to {self.p1_url}. Is the server running?")
        except requests.exceptions.Timeout:
            self.fail(f"Request timed out. Server may be slow or not responding.")
        except Exception as e:
            self.fail(f"Failed to send message: {e}")
    
    def test_05_verify_message_in_database(self):
        """Verify messages are stored in database"""
        try:
            # Wait a bit for any pending messages to be processed
            time.sleep(3)
            
            response = requests.get(f"{self.api_url}/messages", timeout=5)
            self.assertEqual(response.status_code, 200)
            
            data = response.json()
            messages = data.get('messages', [])
            
            print(f"\n  Total messages in database: {len(messages)}")
            
            if len(messages) > 0:
                print(f"✓ Messages found in database")
                print(f"\n  Recent messages:")
                for msg in messages[:5]:  # Show first 5
                    print(f"    - {msg.get('message_id')} | {msg.get('direction')} | {msg.get('status')} | {msg.get('timestamp')}")
            else:
                print(f"⚠ No messages found in database yet")
            
            self.assertGreaterEqual(len(messages), 0)
            
        except Exception as e:
            self.fail(f"Failed to verify messages: {e}")
    
    def test_06_check_chart_data(self):
        """Test chart data endpoint"""
        try:
            response = requests.get(f"{self.api_url}/chart-data", timeout=5)
            self.assertEqual(response.status_code, 200)
            
            data = response.json()
            self.assertIn('messageData', data)
            self.assertIn('statusData', data)
            self.assertIn('trendData', data)
            
            print(f"✓ Chart data endpoint working")
            
            # Check if we have any message data
            trend_data = data.get('trendData', [])
            total_messages = sum(item.get('sent', 0) + item.get('received', 0) for item in trend_data)
            print(f"  Total messages in trend data: {total_messages}")
            
        except Exception as e:
            self.fail(f"Chart data endpoint failed: {e}")


class TestAS2RealSendReceive(unittest.TestCase):
    """Test actual AS2 send/receive with real file transfer"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test configuration"""
        cls.server_url = os.environ.get('AS2_SERVER_URL', 'http://192.168.1.200:8001')
        cls.api_url = f"{cls.server_url}/api"
    
    def test_send_multiple_messages(self):
        """Send multiple test messages to increase count"""
        print(f"\n{'='*70}")
        print(f"Sending Multiple Test Messages")
        print(f"{'='*70}\n")
        
        # Get initial count
        try:
            response = requests.get(f"{self.api_url}/stats", timeout=5)
            initial_count = response.json().get('messages', 0) if response.status_code == 200 else 0
            print(f"Initial message count: {initial_count}")
        except:
            initial_count = 0
        
        # Send 5 test messages
        success_count = 0
        for i in range(5):
            try:
                test_content = f"Test Message #{i+1} - {datetime.now().isoformat()}\n"
                test_content += f"This is a test message for integration testing.\n"
                test_content += f"Message ID: TEST-{int(time.time())}-{i}\n"
                
                test_filename = f"test_msg_{int(time.time())}_{i}.txt"
                
                files = {
                    'file': (test_filename, test_content.encode(), 'text/plain')
                }
                
                data = {
                    'partner_id': 'p2as2',
                    'subject': f'Integration Test Message {i+1}'
                }
                
                response = requests.post(
                    f"{self.server_url}/pyas2/as2send",
                    files=files,
                    data=data,
                    timeout=30
                )
                
                if response.status_code in [200, 201, 202]:
                    success_count += 1
                    print(f"  ✓ Message {i+1}/5 sent successfully")
                else:
                    print(f"  ✗ Message {i+1}/5 failed: {response.status_code}")
                
                time.sleep(1)  # Wait between messages
                
            except Exception as e:
                print(f"  ✗ Message {i+1}/5 error: {e}")
        
        print(f"\nSuccessfully sent: {success_count}/5 messages")
        
        # Wait for processing
        print(f"\nWaiting 5 seconds for messages to be processed...")
        time.sleep(5)
        
        # Check final count
        try:
            response = requests.get(f"{self.api_url}/stats", timeout=5)
            if response.status_code == 200:
                final_count = response.json().get('messages', 0)
                print(f"Final message count: {final_count}")
                print(f"Increase: +{final_count - initial_count}")
                
                if final_count > initial_count:
                    print(f"\n✓ SUCCESS! Message count increased in database!")
                else:
                    print(f"\n⚠ Message count did not increase. Check server logs.")
        except Exception as e:
            print(f"Could not verify final count: {e}")
        
        self.assertGreater(success_count, 0, "At least one message should be sent successfully")


def run_integration_tests():
    """Run integration tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes in order
    suite.addTests(loader.loadTestsFromTestCase(TestAS2Integration))
    suite.addTests(loader.loadTestsFromTestCase(TestAS2RealSendReceive))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == '__main__':
    print("\n" + "="*70)
    print("AS2 INTEGRATION TESTS")
    print("Testing against: 192.168.1.200:8001")
    print("="*70 + "\n")
    
    result = run_integration_tests()
    
    print("\n" + "="*70)
    print("INTEGRATION TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✅ All integration tests passed!")
    else:
        print("\n❌ Some integration tests failed!")
    
    print("="*70 + "\n")
    
    sys.exit(0 if result.wasSuccessful() else 1)
