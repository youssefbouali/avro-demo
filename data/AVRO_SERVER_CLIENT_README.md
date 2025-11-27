# Simple Avro Server & Client

A simple Python implementation of Avro server and client for testing and comparing Avro vs JSON serialization.

## Files

- **`avro_server.py`** - Simple HTTP server serving Avro and JSON data
- **`avro_client.py`** - Client to fetch and compare data formats

## Quick Start

### 1. Start the Server

```powershell
cd data
python avro_server.py
```

Output:
```
🚀 Avro Server started on http://localhost:8000/
   Endpoints:
   - http://localhost:8000/avro/single
   - http://localhost:8000/avro/batch
   - http://localhost:8000/json/single
   - http://localhost:8000/json/batch

Press Ctrl+C to stop
```

### 2. Run the Client (in another terminal)

```powershell
cd data
python avro_client.py
```

## Server Endpoints

| Endpoint | Description | Format |
|----------|-------------|--------|
| `/` | HTML home page with links | HTML |
| `/health` | Health check | JSON |
| `/avro/single` | Single user record | Avro (binary) |
| `/avro/batch` | 10 user records | Avro (binary) |
| `/json/single` | Single user record | JSON |
| `/json/batch` | 10 user records | JSON |

## Sample User Schema

```json
{
  "id": 123,
  "name": "Alice",
  "email": "alice@example.com",
  "age": 30,
  "country": "USA",
  "active": true
}
```

## Example Output

```
============================================================
  Simple Avro vs JSON Client
============================================================

📍 Checking server health...
✓ Server is running!

============================================================
SINGLE RECORD TEST
============================================================

📥 Fetching single Avro user...
✓ Received 52 bytes in 1.23ms
  Data:
  ID: 456
  Name: Charlie
  Email: user789@example.com
  Age: 35
  Country: Germany
  Active: True

📥 Fetching single JSON user...
✓ Received 124 bytes in 1.45ms
  Data:
  ID: 456
  Name: Charlie
  Email: user789@example.com
  Age: 35
  Country: Germany
  Active: True

📊 SINGLE RECORD COMPARISON
  Avro is 58.1% smaller (52 vs 124 bytes)
  Avro is 15.2% faster (1.23ms vs 1.45ms)

============================================================
BATCH RECORDS TEST (10 users)
============================================================

📥 Fetching batch Avro users...
✓ Received 10 users in 520 bytes (2.34ms)
  First user: Diana

📥 Fetching batch JSON users...
✓ Received 10 users in 1240 bytes (2.67ms)
  First user: Diana

📊 BATCH RECORDS COMPARISON (10 users)
  Avro is 58.1% smaller (520 vs 1240 bytes)
  Avro is 12.3% faster (2.34ms vs 2.67ms)

============================================================
SUMMARY
============================================================

Format  | Single Record | Batch (10 users)
--------|---------------|------------------
Avro    |     52 bytes  |    520 bytes
JSON    |    124 bytes  |   1240 bytes

🎯 Avro advantage: 58% smaller for single records
🎯 Avro advantage: 58% smaller for batch records
```

## Testing with curl

### Get single Avro record (binary output)
```bash
curl -v http://localhost:8000/avro/single
```

### Get batch Avro records
```bash
curl -v http://localhost:8000/avro/batch
```

### Get single JSON record
```bash
curl http://localhost:8000/json/single
```

### Get batch JSON records
```bash
curl http://localhost:8000/json/batch
```

### Check health
```bash
curl http://localhost:8000/health
```

## Windows PowerShell Examples

```powershell
# Get single Avro user
$response = Invoke-WebRequest -Uri "http://localhost:8000/avro/single"
$response.Content.Length  # Shows size in bytes

# Get single JSON user
$response = Invoke-WebRequest -Uri "http://localhost:8000/json/single"
$json = $response.Content | ConvertFrom-Json
$json.name  # Shows the name

# Compare sizes
$avro = (Invoke-WebRequest -Uri "http://localhost:8000/avro/batch").Content.Length
$json = (Invoke-WebRequest -Uri "http://localhost:8000/json/batch").Content.Length
$reduction = (1 - $avro/$json) * 100
Write-Host "Avro is $reduction% smaller"
```

## Customizing the Data

Edit `avro_server.py` to modify:

### Change number of records in batch
```python
# Change this line in the batch endpoints:
users = [generate_user() for _ in range(10)]  # Change 10 to desired count
```

### Add more fields to schema
```python
SCHEMA = {
    "type": "record",
    "name": "User",
    "namespace": "com.example",
    "fields": [
        # ...existing fields...
        {"name": "phone", "type": ["null", "string"], "default": None},
        {"name": "premium", "type": "boolean", "default": False}
    ]
}
```

### Modify sample data
```python
NAMES = ["Alice", "Bob", "Charlie", ...]  # Add more names
COUNTRIES = ["USA", "UK", ...]  # Add more countries
```

## Performance Tips

1. **Run server and client on same machine** for accurate timing
2. **Run multiple times** to get average performance
3. **Use batch endpoints** to see more significant Avro advantages
4. **Monitor network** to see actual bandwidth savings

## Troubleshooting

### Port already in use
```powershell
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Import errors
```powershell
pip install fastavro
```

### Server not responding
- Make sure server is running: `python avro_server.py`
- Check port: `netstat -ano | findstr :8000`
- Try http://localhost:8000/ in browser

## Key Findings

✅ **Avro is typically 50-70% smaller** than JSON
✅ **Avro is 10-20% faster** to process
✅ **Bigger advantage with batch operations**
✅ **No schema transmission overhead** (schema shared)
✅ **Binary format** requires proper deserialization

---

**Created**: November 27, 2025  
**Status**: ✅ Ready to use
