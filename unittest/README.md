# AS2 Unit Tests and Integration Tests

All test files for the AS2 system.

## 📁 Test Files

### Unit Tests (Mock-based)
- **`test_as2_send.py`** - Send API tests (17 tests) - Uses mocks, NO real messages
- **`test_as2_receive.py`** - Receive API tests (20 tests) - Uses mocks, NO real messages
- **`run_tests.py`** - Test runner for unit tests

### Integration Tests (Real AS2 Messages)
- **`test_send_messages_to_server.py`** - Send real messages using Django commands ✅ UPDATED
- **`test_real_as2_send_receive.py`** - Comprehensive AS2 protocol test ✅ NEW
- **`test_real_as2_integration.py`** - API-based integration test
- **`test_file_transfer_pgedge.py`** - pgEdge file transfer tests
- **`test_as2_integration.py`** - Remote API tests
- **`test_file_transfer.py`** - File transfer tests

### Setup Tests
- **`test_setup.py`** - Setup verification tests

---

## 🚀 Quick Start

### Run Unit Tests (Fast, No Real Messages)
```powershell
# From Windows
cd scripts
.\run-unittest.ps1

# Or directly
cd unittest
python run_tests.py
```

### Run Integration Tests (Real Messages, Increases Counts)

#### Option 1: Complete Integration Test (Recommended)
```powershell
cd scripts
.\run-integration-test-docker.ps1
```

#### Option 2: Inside Docker Container
```bash
# On server
docker exec -it p1-as2 python3 /app/unittest/test_send_messages_to_server.py
```

#### Option 3: Comprehensive AS2 Test
```powershell
cd scripts
.\run-real-as2-test.ps1
```

#### Option 4: API-based Test (From Anywhere)
```powershell
cd unittest
python test_real_as2_integration.py
```

---

## ⚠️ Important: Unit Tests vs Integration Tests

### Unit Tests (Mock-based)
- ✓ Use mock objects (fake data)
- ✗ **Do NOT** send real messages
- ✗ **Do NOT** increase message counts
- ✓ Fast execution (< 1 second)
- ✓ Test logic in isolation
- ✓ No server required

**Files:**
- `test_as2_send.py`
- `test_as2_receive.py`

**Run with:**
```powershell
.\scripts\run-unittest.ps1
```

### Integration Tests (Real AS2 Messages)
- ✓ Use real database
- ✓ **DO** send real AS2 messages
- ✓ **DO** increase message counts
- ✓ Slower execution (15-30 seconds)
- ✓ Test entire AS2 protocol
- ✓ Requires running servers

**Files:**
- `test_send_messages_to_server.py` ✅ UPDATED
- `test_real_as2_send_receive.py` ✅ NEW
- `test_real_as2_integration.py`

**Run with:**
```powershell
.\scripts\run-integration-test-docker.ps1
```

---

## 📊 Test Details

### test_as2_send.py (Unit Test)
**Tests**: 17  
**Type**: Mock-based  
**Message Count**: Does NOT increase  
**Run Time**: ~0.5 seconds

**Coverage:**
- Message creation
- Encryption (3DES, AES128, AES192, AES256)
- Signing (SHA-1, SHA-256, SHA-384, SHA-512)
- Compression
- MDN requests
- Error handling

### test_as2_receive.py (Unit Test)
**Tests**: 20  
**Type**: Mock-based  
**Message Count**: Does NOT increase  
**Run Time**: ~0.5 seconds

**Coverage:**
- Message reception
- Decryption
- Signature verification
- Decompression
- MDN generation
- Error handling
- Invalid messages

### test_send_messages_to_server.py (Integration) ✅ UPDATED
**Tests**: End-to-end AS2 send  
**Type**: Real AS2 messages  
**Message Count**: DOES increase (+5 messages)  
**Run Time**: ~15 seconds

**Features:**
- Sends 5 real AS2 messages
- Uses Django management commands
- Works in Docker environment
- Verifies message count increase
- Shows results in Admin/UI

**Run:**
```bash
docker exec -it p1-as2 python3 /app/unittest/test_send_messages_to_server.py
```

### test_real_as2_send_receive.py (Integration) ✅ NEW
**Tests**: Comprehensive AS2 protocol  
**Type**: Real AS2 messages  
**Message Count**: DOES increase (+3 messages)  
**Run Time**: ~20 seconds

**Features:**
- Full AS2 message exchange
- Partner configuration check
- Encryption/signing verification
- MDN monitoring
- Detailed progress reporting

**Run:**
```bash
docker exec -it p1-as2 python3 /app/unittest/test_real_as2_send_receive.py
```

### test_real_as2_integration.py (Integration)
**Tests**: API-based integration  
**Type**: Real AS2 messages via API  
**Message Count**: DOES increase (+5 messages)  
**Run Time**: ~30 seconds

**Features:**
- Uses REST API endpoints
- Can run from any machine
- Tests `/api/send-message/`
- Verifies stats and chart data
- Comprehensive test report

**Run:**
```bash
python unittest/test_real_as2_integration.py
```

---

## 🔧 Prerequisites

### For Unit Tests
- Python 3.x
- pytest
- No server required

### For Integration Tests
- Docker containers running (P1 and P2)
- Partner configured in admin panel
- Certificates properly set up
- Network connectivity between containers

**Check containers:**
```bash
docker ps | grep 'p1-as2\|p2-as2'
```

**Configure partner:**
http://192.168.1.200:8001/admin/pyas2/partner/

---

## ✅ Expected Results

### Unit Tests
```
============================= test session starts ==============================
collected 37 items

test_as2_send.py::test_create_message PASSED                             [  2%]
test_as2_send.py::test_encrypt_3des PASSED                               [  5%]
...
============================== 37 passed in 1.23s ===============================
```

### Integration Tests
```
AS2 Integration Test - Send Messages to Server
======================================================================
✓ Django environment initialized
Initial message count: 5

Sending 5 test messages...
[1/5] ✓ Message 1 sent successfully
[2/5] ✓ Message 2 sent successfully
[3/5] ✓ Message 3 sent successfully
[4/5] ✓ Message 4 sent successfully
[5/5] ✓ Message 5 sent successfully

Results: 5 succeeded, 0 failed
Final message count: 10
Increase: +5

✅ SUCCESS! Message count increased in database!
```

---

## 🔍 Verification

After running integration tests, verify in:

1. **Dashboard**: http://192.168.1.200:8001/
   - Message counts updated
   - Charts show new data
   - Heatmap populated

2. **Admin Panel**: http://192.168.1.200:8001/admin/pyas2/message/
   - All messages visible
   - Status indicators correct
   - MDN responses present

3. **Messages Page**: http://192.168.1.200:8001/messages
   - List of all messages
   - Filter by status
   - View details

4. **API Endpoints**:
   ```bash
   curl http://192.168.1.200:8001/api/stats/
   curl http://192.168.1.200:8001/api/messages/
   curl http://192.168.1.200:8001/api/chart-data/
   ```

---

## 🐛 Troubleshooting

### Unit Tests Failing
- Check Python version (3.x required)
- Install dependencies: `pip install pytest`
- Verify test files not corrupted

### Integration Tests Failing

#### No Partners Configured
```
✗ No partners configured!
```
**Solution**: Configure at http://192.168.1.200:8001/admin/pyas2/partner/

#### Connection Refused
```
✗ Error: Connection refused
```
**Solution**: 
```bash
docker ps  # Check containers running
docker-compose restart  # Restart if needed
```

#### Message Count Not Increasing
**Cause**: Using unit tests instead of integration tests  
**Solution**: Use integration test scripts:
```powershell
.\scripts\run-integration-test-docker.ps1
```

---

## 📚 Related Documentation

- [REAL_AS2_TESTING.md](../docs/REAL_AS2_TESTING.md) - Comprehensive testing guide ✅ NEW
- [Testing Summary](../docs/TESTING_SUMMARY.md)
- [Unit Test Guide](../docs/UNITTEST_GUIDE.md)
- [Integration Test Guide](../docs/INTEGRATION_TEST_GUIDE.md)
- [Quick Start](../docs/QUICK_START.md)

---

## 📝 Test Summary Table

| Test File | Type | Messages | Count Increase | Run Time |
|-----------|------|----------|----------------|----------|
| test_as2_send.py | Unit | Mock | No | ~0.5s |
| test_as2_receive.py | Unit | Mock | No | ~0.5s |
| test_send_messages_to_server.py | Integration | Real | Yes (+5) | ~15s |
| test_real_as2_send_receive.py | Integration | Real | Yes (+3) | ~20s |
| test_real_as2_integration.py | Integration | Real | Yes (+5) | ~30s |

---

## 🎯 Quick Reference

```powershell
# Unit tests (fast, no real messages)
.\scripts\run-unittest.ps1

# Integration tests (real messages, increases counts)
.\scripts\run-integration-test-docker.ps1

# Send test messages quickly
.\scripts\send-test-messages.ps1

# Run specific test in Docker
docker exec -it p1-as2 python3 /app/unittest/test_send_messages_to_server.py
```
