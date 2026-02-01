# Message Viewer and Retry Feature - February 1, 2026

## Overview
Added functionality to view message payload content and retry failed messages in the Messages page.

## Features Implemented

### 1. View Message Payload ✅
- Click the eye icon (👁️) on any message to view full details
- Shows message metadata (ID, direction, partner, status, timestamp, size, filename)
- Displays actual payload content in a scrollable, monospace text box
- Properly reads file content from Django FileField

### 2. Retry Failed Messages ✅
- Retry button (🔄) appears for failed outbound messages
- Available both in the message list and in the detail dialog
- Creates a new message with the same payload
- Attempts to resend using the AS2 protocol
- Updates message status based on retry result

### 3. Message Status Display ✅
- Success: Green chip with checkmark icon
- Pending: Orange chip with clock icon
- Failed: Red chip with error icon
- All messages stored in database with proper status

## API Endpoints

### GET /api/messages/
Returns list of all messages with basic information.

**Response**:
```json
{
  "messages": [
    {
      "id": 1,
      "message_id": "176995863211.140.3729798047534038994@6b2025efaffe",
      "direction": "OUT",
      "partner": "P2",
      "status": "success",
      "timestamp": "2026-02-01 15:10:32",
      "size": "0.08 KB"
    }
  ]
}
```

### GET /api/messages/{id}/
Returns detailed message information including payload content.

**Response**:
```json
{
  "id": 1,
  "message_id": "176995863211.140.3729798047534038994@6b2025efaffe",
  "direction": "Outbound",
  "partner": "P2",
  "status": "Success",
  "timestamp": "2026-02-01 15:10:32",
  "size": "0.08 KB",
  "payload": "Test Message #1\nTimestamp: 20260201_151032\nThis is a real AS2 message for testing.\n",
  "filename": "N/A",
  "content_type": "text/plain"
}
```

### POST /api/messages/{id}/retry/
Retries a failed or pending outbound message.

**Response (Success)**:
```json
{
  "success": true,
  "message": "Message retried successfully",
  "new_message_id": "176995863211.140.3729798047534038995@6b2025efaffe",
  "original_message_id": "176995863211.140.3729798047534038994@6b2025efaffe"
}
```

**Response (Error)**:
```json
{
  "error": "Only failed or pending messages can be retried"
}
```

## Implementation Details

### Backend (api_views.py)

#### get_message_detail()
- Reads message from database
- Opens payload file using Django FileField
- Decodes binary content to UTF-8 text
- Handles errors gracefully with fallback messages
- Returns JSON with all message details

#### retry_message()
- Validates message can be retried (failed/pending, outbound only)
- Reads original payload content
- Creates new message with same payload
- Uses Django management command to send
- Updates status based on send result
- Returns success/error response

### Frontend (Messages.jsx)

#### Message List
- Displays all messages in a table
- Color-coded status chips
- Direction indicators (Inbound/Outbound)
- View icon for all messages
- Retry icon for failed outbound messages

#### Message Detail Dialog
- Shows full message metadata
- Displays payload in monospace font
- Scrollable content area (max 400px height)
- Retry button for failed messages
- Loading states for async operations

## Usage

### View Message Content
1. Navigate to Messages page
2. Click the eye icon (👁️) next to any message
3. Dialog opens showing:
   - Message ID
   - Direction (Inbound/Outbound)
   - Partner name
   - Status (Success/Pending/Failed)
   - Timestamp
   - File size
   - Filename
   - Content type
   - **Payload content** (actual message text)

### Retry Failed Message
1. Find a failed message in the list
2. Click the retry icon (🔄) in the Actions column
   - OR open the message detail dialog and click "Retry Message" button
3. Confirm the retry action
4. System creates new message and attempts to send
5. Success/error message displayed
6. Message list refreshes automatically

## Message Status Flow

```
┌─────────────┐
│   Created   │
│  (Pending)  │
└──────┬──────┘
       │
       ├──────────┐
       │          │
       ▼          ▼
┌──────────┐  ┌──────────┐
│ Success  │  │  Failed  │
│   (S)    │  │   (E)    │
└──────────┘  └────┬─────┘
                   │
                   │ Retry
                   ▼
            ┌──────────────┐
            │  New Message │
            │  (Pending)   │
            └──────────────┘
```

## Files Modified

### Backend
- `api_views.py` - Added `get_message_detail()` and `retry_message()` functions
- `P1/urls.py` - Added routes for message detail and retry endpoints

### Frontend
- `frontend/src/pages/Messages.jsx` - Added dialog, retry functionality, and payload display

## Testing

### Test Message Viewing
```bash
# Get message list
curl http://192.168.1.200:8001/api/messages/

# Get message detail
curl http://192.168.1.200:8001/api/messages/1/
```

### Test Message Retry
```bash
# Retry a failed message
curl -X POST http://192.168.1.200:8001/api/messages/1/retry/
```

### Test in Browser
1. Open http://192.168.1.200:8001/messages
2. Click eye icon on any message
3. Verify payload content is visible
4. For failed messages, click retry button
5. Verify new message is created

## Error Handling

### Payload Reading Errors
- If file doesn't exist: `[Unable to read file content]`
- If file can't be decoded: `[Error reading payload: {error}]`
- If no payload: `[No payload available]`

### Retry Errors
- Non-failed message: "Only failed or pending messages can be retried"
- Inbound message: "Only outbound messages can be retried"
- Payload not found: "Message payload not found"
- Send failure: "Failed to retry message: {error}"

## Benefits

1. **Transparency**: Users can see actual message content
2. **Debugging**: Easy to identify what was sent/received
3. **Recovery**: Failed messages can be retried without manual intervention
4. **Audit**: Complete message history with status tracking
5. **User-Friendly**: Simple UI with clear actions

## Future Enhancements

Potential improvements:
- Download payload as file
- Edit and resend message
- Bulk retry for multiple failed messages
- Message filtering by date range
- Search within payload content
- Message comparison (diff view)
- Automatic retry with exponential backoff

## Summary

✅ **Message viewing working** - Can see actual payload content  
✅ **Retry functionality working** - Can retry failed messages  
✅ **Status tracking working** - Success/Pending/Failed properly displayed  
✅ **API endpoints working** - All endpoints tested and functional  
✅ **UI updated** - Clean, intuitive interface with proper icons  

The Messages page now provides complete visibility into AS2 message exchange with the ability to view content and retry failed transmissions!
