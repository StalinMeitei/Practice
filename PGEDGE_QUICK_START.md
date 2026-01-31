# pgEdge Agentic AI - Quick Start Guide

## 🚀 Deploy in 3 Steps

### Step 1: Deploy
```powershell
.\deploy-pgedge.ps1
```

### Step 2: Verify
```powershell
.\verify_pgedge_setup.ps1
```

### Step 3: Connect DBeaver
- Host: `localhost`
- Port: `5432`
- User: `postgres`
- Password: `postgres`

## 📊 DBeaver Connection

### Quick Setup
1. Open DBeaver
2. New Connection → PostgreSQL
3. Enter credentials above
4. Test Connection → Finish

### Available Databases
- `postgres` - Default
- `p1_as2_db` - P1 AS2 data
- `p2_as2_db` - P2 AS2 data

## 🤖 Using pgEdge Agentic AI

### Python Example
```python
from pgedge_agentic_ai import AgenticAI

# Connect
agentic = AgenticAI(
    host='localhost',
    port=5432,
    user='postgres',
    password='postgres',
    database='p1_as2_db'
)

# Query with natural language
result = agentic.query("Show me all messages from last week")
print(result)
```

### Run Examples
```bash
python pgedge_agentic_examples.py
```

## 🔍 Common Queries

### View Recent Messages
```sql
SELECT * FROM pyas2_message 
ORDER BY timestamp DESC 
LIMIT 10;
```

### Check Message Status
```sql
SELECT status, COUNT(*) 
FROM pyas2_message 
GROUP BY status;
```

### Partner List
```sql
SELECT * FROM pyas2_partner;
```

## 🌐 Access Points

| Service | URL |
|---------|-----|
| P1 Admin | http://localhost:8001/admin/ |
| P2 Admin | http://localhost:8001/p2/admin/ |
| PostgreSQL | localhost:5432 |

## 🛠️ Useful Commands

### Docker
```powershell
# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Stop all
docker-compose down

# Rebuild
docker-compose up -d --build
```

### Database
```powershell
# Connect to PostgreSQL
docker exec -it pgedge-as2 psql -U postgres

# Backup database
docker exec pgedge-as2 pg_dump -U postgres p1_as2_db > backup.sql

# Check status
docker exec pgedge-as2 pg_isready -U postgres
```

## 📚 Documentation

| File | Purpose |
|------|---------|
| `PGEDGE_INTEGRATION.md` | Complete integration guide |
| `DBEAVER_SETUP.md` | Detailed DBeaver setup |
| `pgedge_agentic_examples.py` | Code examples |
| `README_DOCKER.md` | Docker documentation |

## ⚠️ Troubleshooting

### Cannot Connect to Database
```powershell
# Check containers
docker ps

# Check PostgreSQL
docker logs pgedge-as2

# Restart
docker-compose restart postgres
```

### Port Already in Use
Edit `docker-compose.yml`:
```yaml
ports:
  - "5433:5432"  # Change to 5433
```

### pgEdge Not Working
```powershell
# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## 💡 Tips

1. **Use Natural Language**: Ask questions in plain English
2. **Explore with DBeaver**: Visual interface for data exploration
3. **Check Logs**: `docker-compose logs -f` for debugging
4. **Backup Regularly**: Use pg_dump for backups
5. **Monitor Performance**: Use DBeaver's monitoring tools

## 🎯 Next Steps

1. ✅ Deploy with `.\deploy-pgedge.ps1`
2. ✅ Verify with `.\verify_pgedge_setup.ps1`
3. ✅ Connect DBeaver
4. ✅ Run example queries
5. ✅ Explore your data!

---

**Need Help?** Check the detailed guides:
- Full setup: `PGEDGE_INTEGRATION.md`
- DBeaver: `DBEAVER_SETUP.md`
- Docker: `README_DOCKER.md`
