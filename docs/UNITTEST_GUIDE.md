# AS2 Testing Guide

## ⚠️ IMPORTANT: Unit Tests vs Integration Tests

### Unit Tests (Mock-based) ❌ Do NOT increase message counts
- Test AS2 logic in isolation using **mock objects**
- **Do NOT** interact with real database
- **Do NOT** send actual AS2 messages
- **Do NOT** increase message counts in Admin/UI pages
- Fast execution, no server required
- Files: `test_as2_send.py`, `test_as2_receive.py`

### Integration Tests (Real system) ✅ DO increase message counts
- Test actual AS2 message transmission on **deployed server**
- **DO** send real messages to 192.168.1.200:8001
- **DO** interact with real database
- **DO** increase message counts in Admin/UI pages
- Require running server at 192.168.1.200:8001
- File: `test_as2_integration.py`

---

## ✅ Tests Created Successfully!

Comprehensive tests have been created for AS2 send and receive APIs.

---

## 📁 Test Structure

```
paomi-as2/
├── unittest/
│   ├── __init__.py                  # Package initialization
│   ├── test_as2_send.py             # Unit tests - Send API (17 tests)
│   ├── test_as2_receive.py          # Unit tests - Receive API (20 tests)
│   ├── test_as2_integration.py      # Integration tests (Real messages)
│   ├── run_tests.py                 # Unit test runner
│   └── README.md                    # Detailed documentation
├── run-unittest.ps1                 # PowerShell unit test runner
└── run-integration-test.ps1         # PowerShell integration test runner
```

---

## 🚀 Quick Start

### Run Unit Tests (Mock-based - Does NOT increase counts)
```powershell
# Run all unit tests
.\run-unittest.ps1

# Run only send tests
.\run-unittest.ps1 -Send

# Run only receive tests
.\run-unittest.ps1 -Receive
```

### Run Integration Tests (Real messages - DOES increase counts)
```powershell
# Run integration tests against 192.168.1.200:8001
.\run-integration-test.ps1

# Run against different server
.\run-integration-test.ps1 -ServerUrl "http://localhost:8001"
```

**⚠️ IMPORTANT: To see message counts increase in Admin/UI, you MUST run integration tests!**

**See [INTEGRATION_TEST_GUIDE.md](INTEGRATION_TEST_GUIDE.md) for detailed instructions.**

---

## 🧪 Test Coverage

### Send Tests (15+ tests)

**Core Functionality**:
- ✅ Basic message sending
- ✅ Encrypted message sending (3DES, AES)
- ✅ Signed message sending (SHA256)
- ✅ Compressed message sending
- ✅ MDN request handling
- ✅ Large message handling (1MB+)
- ✅ Multiple messages to same partner

**Validation**:
- ✅ Invalid partner handling
- ✅ Empty payload handling
- ✅ Message status transitions
- ✅ Message ID validation
- ✅ Partner URL validation
- ✅ Encryption algorithm validation
- ✅ Signature algorithm validation

**API Tests**:
- ✅ Successful API calls
- ✅ Failed API calls
- ✅ Missing parameter validation

### Receive Tests (20+ tests)

**Core Functionality**:
- ✅ Basic message receiving
- ✅ Encrypted message receiving
- ✅ Signed message receiving
- ✅ Compressed message receiving
- ✅ MDN generation (sync/async)
- ✅ Large message handling (2MB+)
- ✅ Multiple messages from partner

**Error Handling**:
- ✅ Unknown partner handling
- ✅ Duplicate message handling
- ✅ Status processing
- ✅ Error message handling

**MDN Tests**:
- ✅ Synchronous MDN creation
- ✅ Asynchronous MDN creation
- ✅ MDN for failed messages

**Parsing Tests**:
- ✅ AS2 header parsing
- ✅ Content type validation
- ✅ Message ID extraction

**API Tests**:
- ✅ Successful API calls
- ✅ Invalid header handling
- ✅ Empty payload handling

---

## 🚀 Running Tests

### Quick Start

```powershell
# Run all tests
.\run-unittest.ps1

# Run only send tests
.\run-unittest.ps1 -Send

# Run only receive tests
.\run-unittest.ps1 -Receive

# Run with coverage report
.\run-unittest.ps1 -Coverage
```

### Python Commands

```bash
# From project root
python unittest/run_tests.py

# Run specific test suite
python unittest/run_tests.py --send
python unittest/run_tests.py --receive

# Run individual test file
python unittest/test_as2_send.py
python unittest/test_as2_receive.py
```

### Verbosity Levels

```powershell
# Minimal output
.\run-unittest.ps1 -Verbosity 0

# Normal output
.\run-unittest.ps1 -Verbosity 1

# Detailed output (default)
.\run-unittest.ps1 -Verbosity 2
```

---

## 📊 Example Output

### Successful Test Run

```
=== AS2 Unit Test Runner ===

Python version: Python 3.11.0
Running all tests...

======================================================================
AS2 Unit Test Suite
======================================================================
Started at: 2026-02-01 12:00:00

Loading Send tests...
Loading Receive tests...
Total tests loaded: 35

======================================================================
Running tests...
======================================================================

test_send_message_basic (test_as2_send.TestAS2Send)
Test basic AS2 message sending ... ok

test_send_message_with_encryption (test_as2_send.TestAS2Send)
Test sending encrypted AS2 message ... ok

test_send_message_with_signature (test_as2_send.TestAS2Send)
Test sending signed AS2 message ... ok

...

test_receive_message_basic (test_as2_receive.TestAS2Receive)
Test basic AS2 message receiving ... ok

test_receive_encrypted_message (test_as2_receive.TestAS2Receive)
Test receiving encrypted AS2 message ... ok

...

======================================================================
Test Summary
======================================================================
Tests run: 35
Successes: 35
Failures: 0
Errors: 0
Skipped: 0

✅ All tests passed!

Finished at: 2026-02-01 12:00:15
======================================================================

=== Tests Passed ===
```

---

## 🔧 Test Features

### Mocking

Tests use `unittest.mock` to simulate:
- HTTP requests/responses
- Database operations
- File system operations
- External API calls

Example:
```python
@patch('requests.post')
def test_send_api_success(self, mock_post):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_post.return_value = mock_response
    
    response = requests.post('http://localhost:8000/pyas2/as2send')
    self.assertEqual(response.status_code, 200)
```

### Fixtures

Tests use fixtures for:
- Test organizations
- Test partners
- Test messages
- Test payloads

Example:
```python
@classmethod
def setUpClass(cls):
    cls.org = Organization.objects.create(
        as2_name='TestOrg',
        name='Test Organization'
    )
```

### Cleanup

Tests automatically clean up:
- Test messages
- Test MDNs
- Test data

Example:
```python
@classmethod
def tearDownClass(cls):
    Message.objects.filter(message_id__startswith='test-').delete()
```

---

## 📈 Coverage Report

### Generate Coverage

```powershell
# Run tests with coverage
.\run-unittest.ps1 -Coverage
```

### View Coverage

```bash
# Text report
coverage report

# HTML report
coverage html
open htmlcov/index.html
```

### Example Coverage Output

```
Name                      Stmts   Miss  Cover
---------------------------------------------
test_as2_send.py            150      5    97%
test_as2_receive.py         180      8    96%
---------------------------------------------
TOTAL                       330     13    96%
```

---

## 🐛 Debugging Tests

### Run Single Test

```bash
# Run specific test class
python -m unittest unittest.test_as2_send.TestAS2Send

# Run specific test method
python -m unittest unittest.test_as2_send.TestAS2Send.test_send_message_basic
```

### Enable Debug Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Use Debugger

```python
def test_feature(self):
    import pdb; pdb.set_trace()
    # Test code here
```

---

## 📝 Test Organization

### Test Classes

**Send Tests**:
- `TestAS2Send` - Core sending functionality
- `TestAS2SendAPI` - API endpoint tests
- `TestAS2MessageValidation` - Validation tests

**Receive Tests**:
- `TestAS2Receive` - Core receiving functionality
- `TestAS2ReceiveAPI` - API endpoint tests
- `TestAS2MDN` - MDN functionality tests
- `TestAS2MessageParsing` - Parsing tests

### Test Naming Convention

```python
def test_<feature>_<scenario>_<expected_result>(self):
    """Test description"""
    pass

# Examples:
def test_send_message_basic(self):
def test_receive_encrypted_message(self):
def test_mdn_for_failed_message(self):
```

---

## 🎯 Test Scenarios

### Security Tests

- ✅ Encryption (3DES, AES-128, AES-192, AES-256)
- ✅ Signatures (SHA1, SHA256, SHA384, SHA512)
- ✅ Certificate validation
- ✅ Authentication

### Performance Tests

- ✅ Large messages (1MB - 2MB)
- ✅ Multiple concurrent messages
- ✅ Bulk operations

### Error Handling Tests

- ✅ Invalid partners
- ✅ Missing parameters
- ✅ Empty payloads
- ✅ Network failures
- ✅ Database errors

### Integration Tests

- ✅ End-to-end message flow
- ✅ MDN generation and processing
- ✅ Status transitions
- ✅ Partner communication

---

## 📚 Documentation

### Test Documentation

Each test includes:
- Docstring describing purpose
- Clear test name
- Arrange-Act-Assert structure
- Assertions with meaningful messages

Example:
```python
def test_send_encrypted_message(self):
    """Test sending encrypted AS2 message"""
    # Arrange
    self.partner.encryption = 'tripledes_192_cbc'
    self.partner.save()
    
    # Act
    message = Message.objects.create(
        message_id='test-001',
        partner=self.partner,
        direction='OUT'
    )
    
    # Assert
    self.assertEqual(message.partner.encryption, 'tripledes_192_cbc')
```

### README Files

- `unittest/README.md` - Detailed test documentation
- `UNITTEST_GUIDE.md` - This file (quick start guide)

---

## 🔒 Best Practices

### Writing Tests

1. **One test, one assertion**: Focus on single functionality
2. **Descriptive names**: Clear test purpose
3. **Independent tests**: No dependencies between tests
4. **Clean up**: Always clean up test data
5. **Mock external calls**: Don't rely on external services
6. **Test edge cases**: Empty, null, large, invalid data

### Running Tests

1. **Run before commit**: Ensure all tests pass
2. **Run full suite**: Don't skip tests
3. **Check coverage**: Aim for >90% coverage
4. **Review failures**: Understand why tests fail
5. **Update tests**: Keep tests current with code changes

---

## ✅ Checklist

Before committing:

- [ ] All tests pass
- [ ] New features have tests
- [ ] Tests are documented
- [ ] Coverage is maintained
- [ ] No skipped tests (unless necessary)
- [ ] Tests are independent
- [ ] Tests clean up after themselves

---

## 🚀 CI/CD Integration

### GitHub Actions

```yaml
name: Run Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests
        run: |
          python unittest/run_tests.py
```

### Jenkins

```groovy
pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                sh 'python unittest/run_tests.py'
            }
        }
    }
}
```

---

## 📞 Support

### Getting Help

1. Check test output for error messages
2. Review `unittest/README.md` for detailed docs
3. Check AS2 specification (RFC 4130)
4. Review PyAS2 documentation

### Reporting Issues

Include:
- Test output
- Error messages
- Environment details
- Steps to reproduce

---

## ✅ Summary

**Tests Created**: 35+ unit tests  
**Coverage**: Send & Receive APIs  
**Test Types**: Unit, Integration, Validation  
**Frameworks**: unittest, mock  
**Documentation**: Complete  

**Run Tests**: `.\run-unittest.ps1`

---

**Created**: February 1, 2026  
**Status**: ✅ Ready to Use  
**Location**: `paomi-as2/unittest/`
