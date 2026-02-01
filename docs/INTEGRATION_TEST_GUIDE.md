# AS2 Integration Test Guide

## ⚠️ IMPORTANT: Why Unit Tests Don't Increase Message Counts

**Unit tests use MOCK objects** - they test logic in isolation without touching the real database or sending actual AS2 messages. This is why you don't see message counts increase in the Admin/UI.

**To see real message counts increase, you need to run INTEGRATION tests** that send actual AS2 messages through the system.

---

## 🚀 Quick Start: Send Real Messages

### Option 1: Run on Server (Recommended)

1. **SSH to the server:**
   ```bash
   ssh dev@192.168.1.200
   # Password: dev@2025
   ```

2. **Navigate to project directory:**
   ```bash
   cd /home/dev/paomi-as2
   ```

3. **Run the integration test:**
   ```bash
   python test_send_messages_to_server.py
   ```

4. **Verify in UI:**
   - Dashboard: http://192.168.1.200:8001/
   - Admin: http://192.168.1.200:8001/admin/pyas2/message/
   - Messages: http://192.168.1.200:8001/messages

### Option 2: Deploy and Run from Windows

```powershell
# Copy test script to server and run it
.\run-server-integration-test.ps1
```

---

## 📊 What the Integration Test Does

The integration test (`test_send_messages_to_server.py`):

1. ✅ Connects to the **real database** (PostgreSQL)
2. ✅ Gets the current message count
3. ✅ Creates 5 test files with unique content
4. ✅ Sends them as **real AS2 messages** using `sendas2message` command
5. ✅ Waits for processing
6. ✅ Verifies the message count increased
7. ✅ Shows where to verify in Admin/UI

**Result:** Message counts WILL increase in:
- Admin panel message list
- Dashboard statistics
- Messages page
- Chart data

---

## 🔍 Troubleshooting

### "No partners configured"
- Go to: http://192.168.1.200:8001/admin/pyas2/partner/
- Add at least one partner (e.g., P2)
- Run the test again

### "Django not initialized"
- Make sure you're in the `paomi-as2` directory
- Check that `P1/settings.py` exists
- Verify Docker containers are running: `docker ps`

### "Message count did not increase"
- Check Docker logs: `docker logs paomi-as2-p1-1`
- Verify partner configuration in admin
- Check that AS2 services are running

### Messages sent but not visible in UI
- Refresh the browser (Ctrl+F5)
- Check API endpoint directly: http://192.168.1.200:8001/api/messages
- Verify database connection in Docker

---

## 📝 Manual Testing (Alternative)

If you prefer to test manually:

1. **Login to Admin:**
   - URL: http://192.168.1.200:8001/admin/
   - Username: admin
   - Password: (your admin password)

2. **Send a message via Admin:**
   - Go to Messages → Add Message
   - Select a partner
   - Upload a file
   - Click "Send"

3. **Verify:**
   - Check Messages list
   - Check Dashboard statistics
   - Check Charts update

---

## 🎯 Expected Results

After running the integration test successfully:

```
Initial message count: 0
Sending 5 test messages...
----------------------------------------------------------------------
[1/5] Sending: test_message_20260201_130000_1.txt
  ✓ Message 1 sent successfully
[2/5] Sending: test_message_20260201_130001_2.txt
  ✓ Message 2 sent successfully
...
----------------------------------------------------------------------
Results: 5 succeeded, 0 failed

Final message count: 5
Increase: +5

✅ SUCCESS! Message count increased in database!
```

Then in the UI:
- Dashboard shows 5 messages
- Messages page lists 5 messages
- Charts show data points
- Heatmap shows activity

---

## 🔄 Difference: Unit Tests vs Integration Tests

| Feature | Unit Tests | Integration Tests |
|---------|-----------|-------------------|
| Uses real database | ❌ No (mocks) | ✅ Yes |
| Sends real AS2 messages | ❌ No (mocks) | ✅ Yes |
| Increases message counts | ❌ No | ✅ Yes |
| Visible in Admin/UI | ❌ No | ✅ Yes |
| Execution speed | ⚡ Fast (< 1s) | 🐢 Slower (5-10s) |
| Requires server | ❌ No | ✅ Yes |
| Purpose | Test logic | Test system |

---

## 📚 Related Files

- `test_send_messages_to_server.py` - Integration test script
- `run-server-integration-test.ps1` - Deploy and run from Windows
- `unittest/test_as2_send.py` - Unit tests (mock-based)
- `unittest/test_as2_receive.py` - Unit tests (mock-based)
- `unittest/test_as2_integration.py` - Remote integration tests (limited)

---

## ✅ Success Checklist

After running integration tests, verify:

- [ ] Message count increased in Dashboard
- [ ] Messages visible in Messages page
- [ ] Messages listed in Admin panel
- [ ] Charts show data (line graph, heatmap)
- [ ] Status statistics updated
- [ ] Recent messages show correct timestamps

If all checked, your AS2 system is working correctly! 🎉
