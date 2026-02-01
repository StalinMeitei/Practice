# DBeaver Connection Guide for pgEdge AS2 Docker Setup

## Overview
This guide explains how to connect DBeaver to your pgEdge PostgreSQL database running in Docker.

## Connection Details

### PostgreSQL Server Information
- **Host**: `localhost` (or your Docker host IP)
- **Port**: `5432`
- **Database**: `postgres` (default), `p1_as2_db`, or `p2_as2_db`
- **Username**: `postgres`
- **Password**: `postgres`

## DBeaver Setup Steps

### 1. Install DBeaver
Download from: https://dbeaver.io/download/

### 2. Create New Connection

1. Open DBeaver
2. Click **Database** → **New Database Connection**
3. Select **PostgreSQL**
4. Click **Next**

### 3. Configure Connection

#### Main Tab:
- **Host**: `localhost`
- **Port**: `5432`
- **Database**: `postgres` (or specific database)
- **Username**: `postgres`
- **Password**: `postgres`
- **Show all databases**: ✓ (checked)

#### PostgreSQL Tab:
- **Show all databases**: ✓ (checked)

#### SSH Tab:
- Leave unchecked (not needed for local Docker)

### 4. Test Connection
- Click **Test Connection**
- If prompted, download PostgreSQL driver
- Should see "Connected" message

### 5. Access Your Databases

After connecting, you'll see three databases:
- `postgres` - Default PostgreSQL database
- `p1_as2_db` - P1 AS2 Server database
- `p2_as2_db` - P2 AS2 Server database

## Available Databases

### P1 AS2 Database (`p1_as2_db`)
Contains tables for:
- Organizations
- Partners
- Messages
- Certificates
- MDN records

### P2 AS2 Database (`p2_as2_db`)
Contains tables for:
- Organizations
- Partners
- Messages
- Certificates
- MDN records

## pgEdge Agentic AI Toolkit

The pgEdge Agentic AI Toolkit is now installed in your Docker containers. You can:

1. **Query with AI assistance**: Use natural language to query your data
2. **Automated insights**: Get AI-powered analytics on your AS2 messages
3. **Smart monitoring**: AI-driven monitoring of message flows

### Using pgEdge Agentic AI in Python

```python
from pgedge_agentic_ai import AgenticAI

# Connect to database
agentic = AgenticAI(
    host='localhost',
    port=5432,
    user='postgres',
    password='postgres',
    database='p1_as2_db'
)

# Example: Query messages with AI
result = agentic.query("Show me all failed messages from last week")
print(result)
```

## Troubleshooting

### Cannot Connect to Database

1. **Check Docker is running**:
   ```bash
   docker ps
   ```
   Should show `pgedge-as2` container running

2. **Check port is exposed**:
   ```bash
   docker port pgedge-as2
   ```
   Should show: `5432/tcp -> 0.0.0.0:5432`

3. **Check PostgreSQL is ready**:
   ```bash
   docker logs pgedge-as2
   ```
   Should see "database system is ready to accept connections"

### Port Already in Use

If port 5432 is already in use, modify `docker-compose.yml`:
```yaml
ports:
  - "5433:5432"  # Use different host port
```

Then connect DBeaver to port `5433` instead.

### Connection Timeout

1. Check firewall settings
2. Ensure Docker network is properly configured
3. Try using Docker host IP instead of `localhost`

## Advanced: Remote Access

To access from another machine:

1. **Find Docker host IP**:
   ```bash
   ipconfig  # Windows
   ```

2. **Update DBeaver connection**:
   - Host: `<your-docker-host-ip>`
   - Port: `5432`

3. **Ensure firewall allows port 5432**

## Security Notes

⚠️ **Production Warning**: The default credentials (`postgres`/`postgres`) are for development only.

For production:
1. Change passwords in `docker-compose.yml`
2. Use environment variables for credentials
3. Restrict network access
4. Enable SSL/TLS connections

## Useful SQL Queries

### Check AS2 Messages
```sql
-- P1 messages
SELECT * FROM pyas2_message 
ORDER BY timestamp DESC 
LIMIT 10;

-- P2 messages
SELECT * FROM pyas2_message 
ORDER BY timestamp DESC 
LIMIT 10;
```

### Check Partners
```sql
SELECT * FROM pyas2_partner;
```

### Check Organizations
```sql
SELECT * FROM pyas2_organization;
```

### Message Statistics
```sql
SELECT 
    status,
    COUNT(*) as count,
    DATE(timestamp) as date
FROM pyas2_message
GROUP BY status, DATE(timestamp)
ORDER BY date DESC;
```

## Next Steps

1. Connect DBeaver using the credentials above
2. Explore your AS2 databases
3. Use pgEdge Agentic AI for intelligent queries
4. Set up custom SQL queries and dashboards
5. Export data for reporting

## Support

For issues:
- Check Docker logs: `docker logs pgedge-as2`
- Check container status: `docker ps -a`
- Restart containers: `docker-compose restart`
