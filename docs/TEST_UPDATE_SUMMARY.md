# Test Update Summary - February 1, 2026

## Overview
Fixed and updated the unittest system to support real AS2 send and receive operations that actually increase message counts in the database and UI.

## Problem
The existing unit tests used mock objects and did NOT send real AS2 messages, so they did NOT increase message counts visible in the Admin panel or Dashboard.

## Solution
Created and updated integration test scripts that send REAL AS2 messages using the actual AS2 protocol, increasing message counts in the database.

## Changes Made

### 1. New Test Script: test_real_as2_send_receive.py ✅ NEW
**Location**: `unittest/test_real_as2_send_receive.py`

**Features**:
- Comprehensive AS2 protocol test
- Sends 3 real AS2 messages
- Checks partner configuration
- Verifies encryption/signing
- Monitors MDN responses
- Detailed step-by-step progress
- Works inside Docker containers

**Run**:
```bash
docker exec -it p1-as2 python3 /app/unittest/test_real_as2_send_receive.py
```

### 2. Updated Test Script: test_send_messages_to_server.py ✅ UPDATED
**Location**: `unittest/test_send_messages_to_server.py`

**Changes**:
- Added Docker environment support
- Uses temporary files instead of fixed paths
- Better error handling
- Works both in Docker and on host
- Proper cleanup of temp files

**Run**:
```bash
docker exec -it p1-as2 python3 /app/unittest/test_send_messages_to_server.py
```

### 3. New PowerShell Script: run-integration-test-docker.ps1 ✅ NEW
**Location**: `scripts/run-integration-test-docker.ps1`

**Features**:
- Uploads test scripts to server
- Checks Docker containers
- Gets initial message count
- Runs test inside P1 container
- Verifies message count increase
- Shows final results

**Run**:
```powershell
.\scripts\run-integration-test-docker.ps1
```

### 4. New PowerShell Script: run-real-as2-test.ps1 ✅ NEW
**Location**: `scripts/run-real-as2-test.ps1`

**Features**:
- Uploads comprehensive test script
- Runs inside Docker container
- Shows detailed test output

**Run**:
```powershell
.\scripts\run-real-as2-test.ps1
```

### 5. Updated Documentation: REAL_AS2_TESTING.md ✅ NEW
**Location**: `docs/REAL_AS2_TESTING.md`

**Content**:
- Complete testing guide
- All test scripts explained
- Prerequisites and setup
- Expected results
- Troubleshooting guide
- API endpoints reference

### 6. Updated Documentation: unittest/README.md ✅ UPDATED
**Location**: `unittest/README.md`

**Changes**:
- Clear distinction between unit and integration tests
- Updated test file descriptions
- Added new test scripts
- Comprehensive quick reference
- Test summary table

## Test Types

### Unit Tests (Mock-based)
- **Files**: `test_as2_send.py`, `test_as2_receive.py`
- **Messages**: Mock objects (fake)
- **Count Increase**: NO
- **Run Time**: ~1 second
- **Purpose**: Fast, isolated code testing

### Integration Tests (Real AS2)
- **Files**: `test_send_messages_to_server.py`, `test_real_as2_send_receive.py`, `test_real_as2_integration.py`
- **Messages**: Real AS2 protocol
- **Count Increase**: YES
- **Run Time**: 15-30 seconds
- **Purpose**: End-to-end AS2 testing

## How to Use

### Quick Test (Recommended)
```powershell
# From Windows, run complete integration test
cd paomi-as2/scripts
.\run-integration-test-docker.ps1
```

This will:
1. Upload test scripts to server
2. Check Docker containers
3. Get initial message count
4. Run test inside P1 container
5. Verify message count increased
6. Show results

### Manual Test
```bash
# SSH to server
ssh dev@192.168.1.200

# Run test inside Docker
docker exec -it p1-as2 python3 /app/unittest/test_send_messages_to_server.py
```

### API-based Test
```powershell
# From Windows, test via API
cd paomi-as2/unittest
python test_real_as2_integration.py
```

## Verification

After running integration tests, verify in:

1. **Dashboard**: http://192.168.1.200:8001/
   - Message counts should increase
   - Charts should show new data
   - Heatmap should populate

2. **Admin Panel**: http://192.168.1.200:8001/admin/pyas2/message/
   - New messages visible
   - Status indicators correct
   - Timestamps recent

3. **API Endpoints**:
   ```bash
   # Check stats
   curl http://192.168.1.200:8001/api/stats/
   
   # Check messages
   curl http://192.168.1.200:8001/api/messages/
   ```

## Expected Output

### Successful Test
```
AS2 Integration Test - Send Messages to Server
======================================================================
✓ Django environment initialized
Initial message count: 5

[Step 1] Checking AS2 configuration...
  ✓ Organization: P1
  ✓ Found 1 partner(s)
  → Partner: P2 - http://p2:8002/pyas2/as2receive

[Step 2] Sending 5 test messages...
----------------------------------------------------------------------
[1/5] Sending: test_message_20260201_123456_1.txt
  ✓ Message 1 sent successfully
[2/5] Sending: test_message_20260201_123457_2.txt
  ✓ Message 2 sent successfully
[3/5] Sending: test_message_20260201_123458_3.txt
  ✓ Message 3 sent successfully
[4/5] Sending: test_message_20260201_123459_4.txt
  ✓ Message 4 sent successfully
[5/5] Sending: test_message_20260201_123500_5.txt
  ✓ Message 5 sent successfully

Results: 5 succeeded, 0 failed

Final message count: 10
Increase: +5

✅ SUCCESS! Message count increased in database!

Verify in:
  - Admin: http://192.168.1.200:8001/admin/pyas2/message/
  - Dashboard: http://192.168.1.200:8001/
  - Messages page: http://192.168.1.200:8001/messages
```

## Prerequisites

### 1. Docker Containers Running
```bash
docker ps | grep 'p1-as2\|p2-as2'
```

Both P1 and P2 containers must be running.

### 2. Partner Configured
Configure partner in admin panel:
http://192.168.1.200:8001/admin/pyas2/partner/

Required settings:
- AS2 Name: P2
- Target URL: http://p2:8002/pyas2/as2receive
- Encryption: 3DES or AES
- Signature: SHA-256
- MDN: Enabled

### 3. Certificates Set Up
- P1 private key for signing
- P1 public cert for partner
- P2 public cert for encryption
- P2 private key for decryption

## Troubleshooting

### No Partners Configured
```
✗ No partners configured!
```
**Solution**: Configure partner at http://192.168.1.200:8001/admin/pyas2/partner/

### Connection Refused
```
✗ Error: Connection refused to http://p2:8002
```
**Solution**:
```bash
docker ps  # Check containers
docker-compose restart  # Restart if needed
docker logs p1-as2  # Check logs
docker logs p2-as2  # Check logs
```

### Message Count Not Increasing
**Cause**: Running unit tests instead of integration tests

**Solution**: Use integration test scripts:
```powershell
.\scripts\run-integration-test-docker.ps1
```

### Certificate Errors
```
✗ Certificate verification failed
```
**Solution**:
1. Verify certificates uploaded in admin
2. Check certificate format (PEM)
3. Ensure private keys accessible
4. Check certificate expiration

## Files Created/Updated

### New Files
- `unittest/test_real_as2_send_receive.py` - Comprehensive AS2 test
- `scripts/run-integration-test-docker.ps1` - Complete integration test runner
- `scripts/run-real-as2-test.ps1` - AS2 protocol test runner
- `docs/REAL_AS2_TESTING.md` - Comprehensive testing documentation
- `docs/TEST_UPDATE_SUMMARY.md` - This file

### Updated Files
- `unittest/test_send_messages_to_server.py` - Docker support, temp files
- `unittest/README.md` - Updated with new tests and clear distinctions

## Summary

✅ **Fixed**: Unit tests now clearly separated from integration tests  
✅ **Added**: Real AS2 send/receive integration tests  
✅ **Updated**: Test scripts work in Docker environment  
✅ **Created**: PowerShell scripts for easy execution  
✅ **Documented**: Comprehensive testing guide  

**Result**: You can now run real AS2 integration tests that actually send messages and increase counts in the database and UI!

## Quick Reference

```powershell
# Run unit tests (fast, no real messages)
.\scripts\run-unittest.ps1

# Run integration tests (real messages, increases counts)
.\scripts\run-integration-test-docker.ps1

# Run comprehensive AS2 test
.\scripts\run-real-as2-test.ps1

# Send test messages quickly
.\scripts\send-test-messages.ps1
```

## Next Steps

1. Run integration test to verify setup:
   ```powershell
   .\scripts\run-integration-test-docker.ps1
   ```

2. Check results in browser:
   - Dashboard: http://192.168.1.200:8001/
   - Admin: http://192.168.1.200:8001/admin/pyas2/message/

3. Verify message counts increased

4. Use for demonstrations and testing
