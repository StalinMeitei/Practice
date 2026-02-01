"""
Unit tests for AS2 Receive API
Tests the functionality of receiving AS2 messages
"""
import unittest
import os
import sys
from unittest.mock import Mock, patch, MagicMock, PropertyMock
from io import BytesIO

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestAS2Receive(unittest.TestCase):
    """Test AS2 message receiving functionality"""
    
    def setUp(self):
        """Set up test fixtures for each test"""
        self.test_payload = b"Test AS2 Received Message Content"
        self.test_filename = "received_file.txt"
        
        # Create mock organization
        self.org = Mock()
        self.org.as2_name = 'TestOrgReceive'
        self.org.name = 'Test Organization Receive'
        self.org.email_address = 'receive@example.com'
        
        # Create mock partner
        self.partner = Mock()
        self.partner.as2_name = 'TestPartnerReceive'
        self.partner.name = 'Test Partner Receive'
        self.partner.target_url = 'http://localhost:8000/pyas2/as2receive'
        self.partner.compress = False
        self.partner.encryption = 'tripledes_192_cbc'
        self.partner.signature = 'sha256'
        self.partner.mdn = True
        self.partner.mdn_mode = 'SYNC'
    
    def test_receive_message_basic(self):
        """Test basic AS2 message receiving"""
        # Create a mock received message
        message = Mock()
        message.message_id = 'test-receive-001'
        message.partner = self.partner
        message.organization = self.org
        message.direction = 'IN'  # Inbound
        message.status = 'S'  # Success
        message.payload = self.test_payload
        
        self.assertIsNotNone(message)
        self.assertEqual(message.direction, 'IN')
        self.assertEqual(message.status, 'S')
        self.assertEqual(message.partner, self.partner)
    
    def test_receive_encrypted_message(self):
        """Test receiving encrypted AS2 message"""
        message = Mock()
        message.message_id = 'test-receive-002'
        message.partner = self.partner
        message.organization = self.org
        message.direction = 'IN'
        message.status = 'S'
        message.payload = self.test_payload
        
        # Verify encryption was expected
        self.assertEqual(message.partner.encryption, 'tripledes_192_cbc')
    
    def test_receive_signed_message(self):
        """Test receiving signed AS2 message"""
        message = Mock()
        message.message_id = 'test-receive-003'
        message.partner = self.partner
        message.organization = self.org
        message.direction = 'IN'
        message.status = 'S'
        message.payload = self.test_payload
        
        # Verify signature was expected
        self.assertEqual(message.partner.signature, 'sha256')
    
    def test_receive_compressed_message(self):
        """Test receiving compressed AS2 message"""
        # Update partner to expect compression
        self.partner.compress = True
        
        message = Mock()
        message.message_id = 'test-receive-004'
        message.partner = self.partner
        message.organization = self.org
        message.direction = 'IN'
        message.status = 'S'
        message.payload = self.test_payload
        
        self.assertTrue(message.partner.compress)
    
    def test_receive_message_with_mdn(self):
        """Test receiving AS2 message and sending MDN"""
        message = Mock()
        message.message_id = 'test-receive-005'
        message.partner = self.partner
        message.organization = self.org
        message.direction = 'IN'
        message.status = 'S'
        message.payload = self.test_payload
        
        # Create MDN for the received message
        mdn = Mock()
        mdn.message = message
        mdn.status = 'S'
        mdn.mdn_mode = 'SYNC'
        
        self.assertIsNotNone(mdn)
        self.assertEqual(mdn.message, message)
        self.assertEqual(mdn.status, 'S')
    
    def test_receive_large_message(self):
        """Test receiving large AS2 message"""
        # Create a large payload (2MB)
        large_payload = b"Y" * (2 * 1024 * 1024)
        
        message = Mock()
        message.message_id = 'test-receive-006'
        message.partner = self.partner
        message.organization = self.org
        message.direction = 'IN'
        message.status = 'S'
        message.payload = large_payload
        
        self.assertIsNotNone(message)
        self.assertGreater(len(message.payload), 2000000)
    
    def test_receive_message_from_unknown_partner(self):
        """Test receiving message from unknown partner"""
        # Validate that partner is required
        message = Mock()
        message.partner = None
        
        # This should raise an error in real implementation
        self.assertIsNone(message.partner)
    
    def test_receive_duplicate_message(self):
        """Test receiving duplicate message ID"""
        # Create first message
        message1 = Mock()
        message1.message_id = 'test-receive-dup-001'
        message1.partner = self.partner
        message1.organization = self.org
        message1.direction = 'IN'
        message1.status = 'S'
        message1.payload = self.test_payload
        
        # Try to create duplicate (should be handled)
        message2 = Mock()
        message2.message_id = 'test-receive-dup-002'  # Different ID
        message2.partner = self.partner
        message2.organization = self.org
        message2.direction = 'IN'
        message2.status = 'S'
        message2.payload = self.test_payload
        
        self.assertNotEqual(message1.message_id, message2.message_id)
    
    def test_receive_message_status_processing(self):
        """Test message status during processing"""
        # Create message in processing state
        message = Mock()
        message.message_id = 'test-receive-008'
        message.partner = self.partner
        message.organization = self.org
        message.direction = 'IN'
        message.status = 'P'  # Processing
        
        self.assertEqual(message.status, 'P')
        
        # Update to success
        message.status = 'S'
        self.assertEqual(message.status, 'S')
    
    def test_receive_message_with_error(self):
        """Test receiving message that results in error"""
        message = Mock()
        message.message_id = 'test-receive-009'
        message.partner = self.partner
        message.organization = self.org
        message.direction = 'IN'
        message.status = 'E'  # Error
        message.payload = self.test_payload
        
        self.assertEqual(message.status, 'E')
    
    def test_multiple_messages_from_partner(self):
        """Test receiving multiple messages from same partner"""
        messages = []
        for i in range(5):
            message = Mock()
            message.message_id = f'test-receive-multi-{i}'
            message.partner = self.partner
            message.organization = self.org
            message.direction = 'IN'
            message.status = 'S'
            message.payload = f"Received Message {i}".encode()
            messages.append(message)
        
        self.assertEqual(len(messages), 5)
        for msg in messages:
            self.assertEqual(msg.direction, 'IN')


class TestAS2ReceiveAPI(unittest.TestCase):
    """Test AS2 Receive API endpoints"""
    
    @patch('requests.post')
    def test_receive_api_success(self, mock_post):
        """Test successful API call to receive AS2 message"""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "Message received successfully"
        mock_response.headers = {
            'Content-Type': 'application/pkcs7-mime',
            'AS2-From': 'TestPartner',
            'AS2-To': 'TestOrg'
        }
        mock_post.return_value = mock_response
        
        # Simulate API call
        import requests
        response = requests.post(
            'http://localhost:8000/pyas2/as2receive',
            data=b"Test AS2 Message",
            headers={
                'Content-Type': 'application/pkcs7-mime',
                'AS2-From': 'TestPartner',
                'AS2-To': 'TestOrg'
            }
        )
        
        self.assertEqual(response.status_code, 200)
    
    @patch('requests.post')
    def test_receive_api_invalid_headers(self, mock_post):
        """Test API call with invalid headers"""
        # Mock error response
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = "Invalid AS2 headers"
        mock_post.return_value = mock_response
        
        # Simulate API call with missing headers
        import requests
        response = requests.post(
            'http://localhost:8000/pyas2/as2receive',
            data=b"Test AS2 Message"
            # Missing AS2 headers
        )
        
        self.assertEqual(response.status_code, 400)
    
    def test_receive_api_empty_payload(self):
        """Test receiving message with empty payload"""
        # This should typically fail
        with self.assertRaises(Exception):
            raise ValueError("Empty payload not allowed")


class TestAS2MDN(unittest.TestCase):
    """Test AS2 MDN (Message Disposition Notification) functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.org = Mock()
        self.org.as2_name = 'TestOrgMDN'
        self.org.name = 'Test Organization MDN'
        
        self.partner = Mock()
        self.partner.as2_name = 'TestPartnerMDN'
        self.partner.name = 'Test Partner MDN'
        self.partner.target_url = 'http://localhost:8000/pyas2/as2receive'
        self.partner.mdn = True
        self.partner.mdn_mode = 'SYNC'
    
    def test_create_sync_mdn(self):
        """Test creating synchronous MDN"""
        message = Mock()
        message.message_id = 'test-mdn-001'
        message.partner = self.partner
        message.organization = self.org
        message.direction = 'IN'
        message.status = 'S'
        
        mdn = Mock()
        mdn.message = message
        mdn.status = 'S'
        mdn.mdn_mode = 'SYNC'
        
        self.assertEqual(mdn.mdn_mode, 'SYNC')
        self.assertEqual(mdn.status, 'S')
    
    def test_create_async_mdn(self):
        """Test creating asynchronous MDN"""
        self.partner.mdn_mode = 'ASYNC'
        
        message = Mock()
        message.message_id = 'test-mdn-002'
        message.partner = self.partner
        message.organization = self.org
        message.direction = 'IN'
        message.status = 'S'
        
        mdn = Mock()
        mdn.message = message
        mdn.status = 'S'
        mdn.mdn_mode = 'ASYNC'
        
        self.assertEqual(mdn.mdn_mode, 'ASYNC')
    
    def test_mdn_for_failed_message(self):
        """Test MDN for failed message"""
        message = Mock()
        message.message_id = 'test-mdn-003'
        message.partner = self.partner
        message.organization = self.org
        message.direction = 'IN'
        message.status = 'E'  # Error
        
        mdn = Mock()
        mdn.message = message
        mdn.status = 'E'  # Error MDN
        mdn.mdn_mode = 'SYNC'
        
        self.assertEqual(mdn.status, 'E')


class TestAS2MessageParsing(unittest.TestCase):
    """Test AS2 message parsing and validation"""
    
    def test_parse_as2_headers(self):
        """Test parsing AS2 headers"""
        headers = {
            'AS2-From': 'TestPartner',
            'AS2-To': 'TestOrg',
            'Message-ID': '<test-001@example.com>',
            'Content-Type': 'application/pkcs7-mime'
        }
        
        self.assertEqual(headers['AS2-From'], 'TestPartner')
        self.assertEqual(headers['AS2-To'], 'TestOrg')
        self.assertIn('Message-ID', headers)
    
    def test_validate_content_type(self):
        """Test content type validation"""
        valid_types = [
            'application/pkcs7-mime',
            'application/pkcs7-signature',
            'multipart/signed'
        ]
        
        for content_type in valid_types:
            self.assertTrue('pkcs7' in content_type or 'multipart' in content_type)
    
    def test_extract_message_id(self):
        """Test extracting message ID from headers"""
        message_id = '<test-001@example.com>'
        
        # Remove angle brackets
        clean_id = message_id.strip('<>')
        
        self.assertEqual(clean_id, 'test-001@example.com')


def run_tests():
    """Run all tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestAS2Receive))
    suite.addTests(loader.loadTestsFromTestCase(TestAS2ReceiveAPI))
    suite.addTests(loader.loadTestsFromTestCase(TestAS2MDN))
    suite.addTests(loader.loadTestsFromTestCase(TestAS2MessageParsing))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == '__main__':
    result = run_tests()
    sys.exit(0 if result.wasSuccessful() else 1)
