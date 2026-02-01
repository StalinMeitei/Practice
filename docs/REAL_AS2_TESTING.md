# Real AS2 Send and Receive Testing

## Overview
This document describes how to run real AS2 integration tests that actually send and receive messages between P1 and P2 servers, increasing message counts in the database and UI.

## Test Scripts

### 1. test_send_messages_to_server.py
**Purpose**: Send real AS2 messages from P1 to P2 using Django management commands

**Location**: `unittest/test_send_messages_to_server.py`

**Features**:
- Sends 5 test messages by default
- Uses Django's `sendas2message` management command
- Works inside Docker containers
- Creates temporary test files
- Verifies message count increases
- Shows results in Admin/UI

**Run inside Docker**:
```bash
docker exec -it p1-as2 python3 /app/unittest/test_send_messages_to_server.py
```

**Run from Windows**:
```powershell
.\scripts\run-integration-test-docker.ps1
```

### 2. test_real_as2_send_receive.py
**Purpose**: Comprehensive AS2 send/receive test with detailed verification

**Location**: `unittest/test_real_as2_send_receive.py`

**Features**:
- Sends 3 test messages with full AS2 protocol
- Checks partner configuration
- Verifies encryption/signing
- Monitors MDN responses
- Shows detailed step-by-step progress
- Validates message counts

**Run inside Docker**:
```bash
docker exec -it p1-as2 python3 /app/unittest/test_real_as2_send_receive.py
```

**Run from Windows**:
```powershell
.\scripts\run-real-as2-test.ps1
```

### 3. test_real_as2_integration.py
**Purpose**: API-based integration test (runs from outside Docker)

**Location**: `unittest/test_real_as2_integration.py`

**Features**:
- Uses REST API to send messages
- Can run from any machine
- Tests `/api/send-message/` endpoint
- Verifies stats, messages, and chart data
- Comprehensive test report

**Run from Windows**:
```powershell
cd paomi-as2
python unittest/test_real_as2_integration.py
```

## PowerShell Scripts

### run-integration-test-docker.ps1
Complete integration test workflow:
1. Uploads test scripts to server
2. Checks Docker containers
3. Gets initial message count
4. Runs test inside P1 container
5. Verifies message count increase
6. Shows final results

```powershell
.\scripts\run-integration-test-docker.ps1
```

### run-real-as2-test.ps1
Runs the comprehensive AS2 test:
```powershell
.\scripts\run-real-as2-test.ps1
```

### send-test-messages.ps1
Quick script to send test messages:
```powershell
.\scripts\send-test-messages.ps1
```

## Prerequisites

### 1. Partner Configuration
Before running tests, ensure partners are configured:

```bash
# Access admin panel
http://192.168.1.200:8001/admin/pyas2/partner/
```

Required partner settings:
- AS2 Name: P2 (or your partner name)
- Target URL: http://p2:8002/pyas2/as2receive (for Docker)
- Encryption: 3DES or AES
- Signature: SHA-256
- MDN: Enabled

### 2. Certificates
Ensure certificates are properly configured:
- P1 private key: For signing outbound messages
- P1 public cert: For partner to encrypt messages to P1
- P2 public cert: For P1 to encrypt messages to P2
- P2 private key: For P2 to decrypt messages

### 3. Docker Containers Running
```bash
docker ps | grep 'p1-as2\|p2-as2'
```

Both P1 and P2 containers should be running.

## Test Workflow

### Step 1: Check Initial State
```bash
# Get initial message count
curl http://192.168.1.200:8001/api/stats/
```

### Step 2: Run Test
```powershell
# From Windows
.\scripts\run-integration-test-docker.ps1
```

### Step 3: Verify Results

**In Browser**:
- Dashboard: http://192.168.1.200:8001/
- Admin: http://192.168.1.200:8001/admin/pyas2/message/
- Messages: http://192.168.1.200:8001/messages

**Via API**:
```bash
# Check stats
curl http://192.168.1.200:8001/api/stats/

# Check messages
curl http://192.168.1.200:8001/api/messages/

# Check chart data
curl http://192.168.1.200:8001/api/chart-data/
```

## Expected Results

### Successful Test
- ✓ Messages sent successfully
- ✓ Message count increases in database
- ✓ Messages visible in Admin panel
- ✓ Dashboard statistics update
- ✓ Charts show new data
- ✓ MDN responses received (if enabled)

### Test Output Example
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
...

Results: 5 succeeded, 0 failed

Final message count: 10
Increase: +5

✅ SUCCESS! Message count increased in database!
```

## Troubleshooting

### No Partners Configured
```
✗ No partners configured!
```
**Solution**: Configure partner in admin panel:
http://192.168.1.200:8001/admin/pyas2/partner/

### Message Count Not Increasing
**Possible causes**:
1. Partner target URL incorrect
2. P2 server not running
3. Certificate issues
4. Network connectivity problems

**Check logs**:
```bash
docker logs p1-as2
docker logs p2-as2
```

### Certificate Errors
```
✗ Error: Certificate verification failed
```
**Solution**: 
1. Verify certificates are uploaded
2. Check certificate format (PEM)
3. Ensure private keys are accessible
4. Check certificate expiration

### Connection Refused
```
✗ Error: Connection refused to http://p2:8002
```
**Solution**:
1. Check P2 container is running: `docker ps`
2. Verify network connectivity: `docker network inspect as2-network`
3. Check P2 logs: `docker logs p2-as2`

## Differences from Unit Tests

### Unit Tests (test_as2_send.py, test_as2_receive.py)
- Use mock objects
- Do NOT send real messages
- Do NOT increase message counts
- Fast execution
- Test code logic only

### Integration Tests (test_send_messages_to_server.py, etc.)
- Send REAL AS2 messages
- DO increase message counts
- Slower execution
- Test end-to-end functionality
- Require running servers

## API Endpoints Used

### Send Message
```
POST /api/send-message/
Content-Type: multipart/form-data

partner: P2
file: <file content>
```

### Get Stats
```
GET /api/stats/
Response: {"partners": 1, "keys": 4, "messages": 10, "successRate": 95.0}
```

### Get Messages
```
GET /api/messages/
Response: {"messages": [...]}
```

### Get Chart Data
```
GET /api/chart-data/
Response: {"messageData": [...], "statusData": [...], "trendData": [...]}
```

## Continuous Testing

### Automated Testing
Add to CI/CD pipeline:
```bash
# In deployment script
docker exec p1-as2 python3 /app/unittest/test_send_messages_to_server.py
```

### Scheduled Testing
Use cron to run tests periodically:
```bash
# Run every hour
0 * * * * docker exec p1-as2 python3 /app/unittest/test_send_messages_to_server.py
```

## Summary

The real AS2 integration tests provide:
- ✓ End-to-end AS2 protocol testing
- ✓ Real message exchange between P1 and P2
- ✓ Database verification
- ✓ UI/Dashboard validation
- ✓ API endpoint testing
- ✓ Comprehensive error reporting

Use these tests to verify your AS2 setup is working correctly and to populate the dashboard with real data for demonstration purposes.
