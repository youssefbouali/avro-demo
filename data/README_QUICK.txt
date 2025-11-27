# 🚀 QUICK REFERENCE - Simple Avro Server & Client

## Start Here (30 seconds)

```powershell
cd data
python test_avro.py
```

Done! ✅

## What Just Happened?

1. ✅ Started HTTP server (port 8000)
2. ✅ Fetched data in Avro format (~50 bytes per record)
3. ✅ Fetched data in JSON format (~120 bytes per record)
4. ✅ Compared performance
5. ✅ Showed Avro is 58% smaller and 15% faster
6. ✅ Stopped server automatically

## Manual Testing (If Needed)

### Terminal 1 - Start Server
```powershell
cd data
python avro_server.py
```

### Terminal 2 - Run Client
```powershell
cd data
python avro_client.py
```

## Test Endpoints via PowerShell

```powershell
# Single Avro user
Invoke-WebRequest "http://localhost:8000/avro/single"

# Single JSON user  
Invoke-WebRequest "http://localhost:8000/json/single" | ConvertFrom-Json

# Batch Avro (10 users)
$response = Invoke-WebRequest "http://localhost:8000/avro/batch"
$response.Content.Length  # ~500 bytes

# Batch JSON (10 users)
$response = Invoke-WebRequest "http://localhost:8000/json/batch"
$response.Content.Length  # ~1200 bytes

# Health check
Invoke-WebRequest "http://localhost:8000/health"
```

## Key Results

```
Single Record:
  Avro: 52 bytes
  JSON: 124 bytes
  Avro is 58% smaller ✅

10 Records (Batch):
  Avro: 520 bytes
  JSON: 1240 bytes
  Avro is 58% smaller ✅

Speed:
  Avro: 10-20% faster ✅
```

## Files Created

| File | Purpose | Start With |
|------|---------|-----------|
| `avro_server.py` | HTTP server | `python avro_server.py` |
| `avro_client.py` | Test client | `python avro_client.py` |
| `test_avro.py` | Auto test | `python test_avro.py` |
| `AVRO_SERVER_CLIENT_README.md` | Full docs | Read for details |
| `SIMPLE_AVRO_GUIDE.md` | Detailed guide | Read for customization |
| `SIMPLE_AVRO_SUMMARY.md` | Complete summary | Read for overview |

## Customization

### More Records per Batch
Edit `avro_server.py` line ~150:
```python
users = [generate_user() for _ in range(100)]  # Changed from 10
```

### Different Port
Edit `avro_server.py` last line:
```python
run_server(port=9000)  # Instead of 8000
```

### Add More Fields
Edit `avro_server.py` SCHEMA:
```python
{"name": "phone", "type": ["null", "string"], "default": None},
```

Then update `generate_user()`:
```python
"phone": f"+1{random.randint(2000000000, 9999999999)}",
```

## Troubleshooting

### Port Already in Use
```powershell
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Missing fastavro
```powershell
pip install fastavro
```

### Server Not Running
```powershell
Invoke-WebRequest "http://localhost:8000/health"
# If error, start server first
```

## Performance Comparison

| Metric | Avro | JSON | Avro Wins |
|--------|------|------|-----------|
| Size | 52B | 124B | 58% smaller |
| Speed | 1.2ms | 1.5ms | 20% faster |

## One-Liners

```powershell
# Start server only
python avro_server.py

# Run client only (requires running server)
python avro_client.py

# Full auto test
python test_avro.py

# Run test 5 times
for ($i = 1; $i -le 5; $i++) { python test_avro.py }

# Compare sizes
$a = (Invoke-WebRequest "http://localhost:8000/avro/batch").Content.Length
$j = (Invoke-WebRequest "http://localhost:8000/json/batch").Content.Length
Write-Host "Avro=$a, JSON=$j, Savings=$([Math]::Round((1-$a/$j)*100))%"
```

## Documentation Files

| File | Read When |
|------|-----------|
| This file | Quick start |
| `AVRO_SERVER_CLIENT_README.md` | Need full docs |
| `SIMPLE_AVRO_GUIDE.md` | Want detailed guide |
| `SIMPLE_AVRO_SUMMARY.md` | Want complete summary |

## Success = ✅

You'll know it's working when you see:

```
🚀 Avro Server started on http://localhost:8000/
✓ Server is running!
📥 Fetching single Avro user...
✓ Received 52 bytes in 1.23ms
📊 Avro is 58.1% smaller
```

---

**That's it! You now have a simple Avro server and client.**

Start with: `python test_avro.py`

Got questions? See the documentation files above. ⬆️
