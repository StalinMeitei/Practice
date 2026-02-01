# AS2 Unit Tests

All test files for the AS2 system.

## 📁 Test Files

### Unit Tests (Mock-based)
- **`test_as2_send.py`** - Send API tests (17 tests)
- **`test_as2_receive.py`** - Receive API tests (20 tests)
- **`run_tests.py`** - Test runner

### Integration Tests (Real system)
- **`test_real_as2_integration.py`** - Real AS2 message tests (NEW!)
- **`test_send_messages_to_server.py`** - Send messages on server
- **`test_as2_integration.py`** - Remote API tests
- **`test_file_transfer.py`** - File transfer tests
- **`test_file_transfer_pgedge.py`** - pgEdge file transfer tests

### Setup Tests
- **`test_setup.py`** - Setup verification tests

---

## 🚀 Quick Start

### Run Unit Tests
```powershell
# From project root
cd scripts
.\run-unittest.ps1

# Or directly
cd unittest
python run_tests.py
```

### Run Integration Tests
```powershell
# From project root
cd scripts
.\deploy-and-test.ps1

# Or directly
cd unittest
python test_real_as2_integration.py
```

---

## ⚠️ Important: Unit Tests vs Integration Tests

### Unit Tests (Mock-based)
- Use mock objects (fake data)
- **Do NOT** send real messages
- **Do NOT** increase message counts
- Fast execution (< 1 second)
- Test logic in isolation

**Run with:**
```powershell
cd ../scripts
.\run-unittest.ps1
```

### Integration Tests (Real system)
- Use real database
- **DO** send real messages
- **DO** increase message counts
- Slower execution (5-10 seconds)
- Test entire system

**Run with:**
```powershell
cd ../scripts
.\deploy-and-test.ps1
```

---

## 📚 Related Documentation

- [Testing Summary](../docs/TESTING_SUMMARY.md)
- [Unit Test Guide](../docs/UNITTEST_GUIDE.md)
- [Integration Test Guide](../docs/INTEGRATION_TEST_GUIDE.md)
- [Quick Start](../docs/QUICK_START.md)
