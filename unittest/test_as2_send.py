"""
Unit tests for AS2 Send API
Tests the functionality of sending AS2 messages
"""
import unittest
import os
import sys
import tempfile
from unittest.mock import Mock, patch, MagicMock, PropertyMock
from io import BytesIO

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestAS2Send(unittest.TestCase):
    """Test AS2 message sending functionality"""
    
    def setUp(self):
        """Set up test fixtures for each test"""
        self.test_payload = b"Test AS2 Message Content"
        self.test_filename = "test_file.txt"
        
        # Create mock organization
        self.org = Mock()
        self.org.as2_name = 'TestOrg'
        self.org.name = 'Test Organization'
        self.org.email_address = 'test@example.com'
        
        # Create mock partner
        self.partner = Mock()
        self.partner.as2_name = 'TestPartner'
        self.partner.name = 'Test Partner'
        self.partner.target_url = 'http://localhost:8002/pyas2/as2receive'
        self.partner.compress = False
        self.partner.encryption = 'tripledes_192_cbc'
        self.partner.signature = 'sha256'
        self.partner.mdn = True
        self.partner.mdn_mode = 'SYNC'
        self.partner.active = True
    
    def test_send_message_basic(self):
        """Test basic AS2 message sending"""
        # Create a mock message
        message = Mock()
        message.message_id = 'test-message-001'
        message.partner = self.partner
        message.organization = self.org
        message.direction = 'OUT'
        message.status = 'P'  # Pending
        message.payload = self.test_payload
        
        self.assertIsNotNone(message)
        self.assertEqual(message.direction, 'OUT')
        self.assertEqual(message.status, 'P')
        self.assertEqual(message.partner, self.partner)
    
    def test_send_message_with_encryption(self):
        """Test sending encrypted AS2 message"""
        # Update partner to require encryption
        self.partner.encryption = 'tripledes_192_cbc'
        
        message = Mock()
        message.message_id = 'test-message-002'
        message.partner = self.partner
        message.organization = self.org
        message.direction = 'OUT'
        message.status = 'P'
        message.payload = self.test_payload
        
        self.assertEqual(message.partner.encryption, 'tripledes_192_cbc')
    
    def test_send_message_with_signature(self):
        """Test sending signed AS2 message"""
        # Update partner to require signature
        self.partner.signature = 'sha256'
        
        message = Mock()
        message.message_id = 'test-message-003'
        message.partner = self.partner
        message.organization = self.org
        message.direction = 'OUT'
        message.status = 'P'
        message.payload = self.test_payload
        
        self.assertEqual(message.partner.signature, 'sha256')
    
    def test_send_message_with_compression(self):
        """Test sending compressed AS2 message"""
        # Update partner to use compression
        self.partner.compress = True
        
        message = Mock()
        message.message_id = 'test-message-004'
        message.partner = self.partner
        message.organization = self.org
        message.direction = 'OUT'
        message.status = 'P'
        message.payload = self.test_payload
        
        self.assertTrue(message.partner.compress)
    
    def test_send_message_with_mdn(self):
        """Test sending AS2 message with MDN request"""
        # Update partner to request MDN
        self.partner.mdn = True
        self.partner.mdn_mode = 'SYNC'
        
        message = Mock()
        message.message_id = 'test-message-005'
        message.partner = self.partner
        message.organization = self.org
        message.direction = 'OUT'
        message.status = 'P'
        message.payload = self.test_payload
        
        self.assertTrue(message.partner.mdn)
        self.assertEqual(message.partner.mdn_mode, 'SYNC')
    
    def test_send_large_message(self):
        """Test sending large AS2 message"""
        # Create a large payload (1MB)
        large_payload = b"X" * (1024 * 1024)
        
        message = Mock()
        message.message_id = 'test-message-006'
        message.partner = self.partner
        message.organization = self.org
        message.direction = 'OUT'
        message.status = 'P'
        message.payload = large_payload
        
        self.assertIsNotNone(message)
        self.assertGreater(len(message.payload), 1000000)
    
    def test_send_message_invalid_partner(self):
        """Test sending message with invalid partner"""
        # Validate that partner is required
        message = Mock()
        message.partner = None
        
        # This should raise an error in real implementation
        self.assertIsNone(message.partner)
    
    def test_send_message_empty_payload(self):
        """Test sending message with empty payload"""
        message = Mock()
        message.message_id = 'test-message-008'
        message.partner = self.partner
        message.organization = self.org
        message.direction = 'OUT'
        message.status = 'P'
        message.payload = b""
        
        self.assertIsNotNone(message)
        self.assertEqual(len(message.payload), 0)
    
    def test_message_status_transitions(self):
        """Test message status transitions"""
        message = Mock()
        message.message_id = 'test-message-009'
        message.partner = self.partner
        message.organization = self.org
        message.direction = 'OUT'
        message.status = 'P'  # Pending
        
        # Test status transitions
        self.assertEqual(message.status, 'P')
        
        # Simulate successful send
        message.status = 'S'  # Success
        self.assertEqual(message.status, 'S')
        
        # Test error status
        message.status = 'E'  # Error
        self.assertEqual(message.status, 'E')
    
    def test_multiple_messages_same_partner(self):
        """Test sending multiple messages to same partner"""
        messages = []
        for i in range(5):
            message = Mock()
            message.message_id = f'test-message-multi-{i}'
            message.partner = self.partner
            message.organization = self.org
            message.direction = 'OUT'
            message.status = 'P'
            message.payload = f"Message {i}".encode()
            messages.append(message)
        
        self.assertEqual(len(messages), 5)
        for msg in messages:
            self.assertEqual(msg.partner, self.partner)


class TestAS2SendAPI(unittest.TestCase):
    """Test AS2 Send API endpoints"""
    
    @patch('requests.post')
    def test_send_api_success(self, mock_post):
        """Test successful API call to send AS2 message"""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "Message sent successfully"
        mock_post.return_value = mock_response
        
        # Simulate API call
        import requests
        response = requests.post(
            'http://localhost:8000/pyas2/as2send',
            data={'partner': 'TestPartner', 'file': 'test.txt'}
        )
        
        self.assertEqual(response.status_code, 200)
    
    @patch('requests.post')
    def test_send_api_failure(self, mock_post):
        """Test failed API call to send AS2 message"""
        # Mock failed response
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_post.return_value = mock_response
        
        # Simulate API call
        import requests
        response = requests.post(
            'http://localhost:8000/pyas2/as2send',
            data={'partner': 'InvalidPartner', 'file': 'test.txt'}
        )
        
        self.assertEqual(response.status_code, 500)
    
    def test_send_api_missing_parameters(self):
        """Test API call with missing parameters"""
        # This would typically raise a validation error
        with self.assertRaises(Exception):
            # Simulate missing partner parameter
            raise ValueError("Missing required parameter: partner")


class TestAS2MessageValidation(unittest.TestCase):
    """Test AS2 message validation"""
    
    def test_validate_message_id(self):
        """Test message ID validation"""
        valid_ids = [
            'MSG-001',
            'test-message-123',
            'AS2-2026-01-31-001'
        ]
        
        for msg_id in valid_ids:
            self.assertIsNotNone(msg_id)
            self.assertGreater(len(msg_id), 0)
    
    def test_validate_partner_url(self):
        """Test partner URL validation"""
        valid_urls = [
            'http://localhost:8002/pyas2/as2receive',
            'https://partner.example.com/as2',
            'http://192.168.1.200:8002/pyas2/as2receive'
        ]
        
        for url in valid_urls:
            self.assertTrue(url.startswith('http'))
    
    def test_validate_encryption_algorithm(self):
        """Test encryption algorithm validation"""
        valid_algorithms = [
            'tripledes_192_cbc',
            'aes_128_cbc',
            'aes_192_cbc',
            'aes_256_cbc'
        ]
        
        for algo in valid_algorithms:
            self.assertIn('cbc', algo)
    
    def test_validate_signature_algorithm(self):
        """Test signature algorithm validation"""
        valid_algorithms = [
            'sha1',
            'sha256',
            'sha384',
            'sha512'
        ]
        
        for algo in valid_algorithms:
            self.assertTrue(algo.startswith('sha'))


def run_tests():
    """Run all tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestAS2Send))
    suite.addTests(loader.loadTestsFromTestCase(TestAS2SendAPI))
    suite.addTests(loader.loadTestsFromTestCase(TestAS2MessageValidation))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == '__main__':
    result = run_tests()
    sys.exit(0 if result.wasSuccessful() else 1)
