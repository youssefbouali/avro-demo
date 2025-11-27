# Avro vs JSON REST API - Configuration & Examples

## Configuration Files Created

### 1. `api/app.py` - Main Flask Application
Provides REST endpoints for JSON and Avro streaming/batch operations.

**Key Components:**
- User data schema (8 fields)
- Random data generation
- Streaming endpoints (100 records with delays)
- Batch endpoints (bulk transfers)
- Performance metrics tracking
- CORS enabled

### 2. `api/index.html` - Interactive Dashboard
Real-time comparison interface with live metrics.

**Features:**
- Dual format comparison (JSON vs Avro)
- Streaming and batch test modes
- Real-time progress tracking
- Performance metrics display
- Detailed comparison table
- Sample data viewer
- Responsive design

### 3. `api/requirements.txt` - Python Dependencies
```
Flask==2.3.3          # Web framework
Flask-CORS==4.0.0     # Cross-origin requests
fastavro==1.8.3       # Avro serialization
```

### 4. `api/Dockerfile` - Container Configuration
Python 3.11-slim image with all dependencies installed.

### 5. `docker-compose-api.yml` - Container Orchestration
Single service: `avro-api` on port 5000

---

## API Endpoints Reference

### JSON Streaming
```
GET /api/json/stream
```
Returns 100 user records as line-delimited JSON.

**Response:**
```json
{
  "sequence": 1,
  "data": {
    "id": 1234,
    "name": "Alice",
    "email": "user@example.com",
    "age": 25,
    "country": "USA",
    "created_at": "2024-01-15T10:30:00",
    "score": 87.5,
    "active": true
  },
  "format": "json",
  "size_bytes": 156,
  "processing_time_ms": 0.234,
  "timestamp": "2024-01-15T10:30:00"
}
```

### Avro Streaming
```
GET /api/avro/stream
```
Returns 100 user records as base64-encoded Avro.

**Response:**
```json
{
  "sequence": 1,
  "data": "AoIKQWxpY2UaGnVzZXJAZXhhbXBsZS5jb20YCgpVU0EcNjA4MzMzMzMzM2FzAQ==",
  "format": "avro",
  "size_bytes": 58,
  "processing_time_ms": 0.156,
  "timestamp": "2024-01-15T10:30:00"
}
```

### JSON Batch
```
GET /api/json/batch
```
Returns all 100 records in single JSON response.

**Response:**
```json
{
  "format": "json",
  "count": 100,
  "data": [ {...}, {...}, ... ],
  "size_bytes": 15600,
  "processing_time_ms": 2.456,
  "timestamp": "2024-01-15T10:30:00"
}
```

### Avro Batch
```
GET /api/avro/batch
```
Returns all 100 records as Avro (base64).

**Response:**
```json
{
  "format": "avro",
  "count": 100,
  "data": "Obj4AoIKQWxpY2U...",
  "size_bytes": 5800,
  "processing_time_ms": 1.234,
  "timestamp": "2024-01-15T10:30:00"
}
```

### Health Check
```
GET /api/health
```

**Response:**
```json
{
  "status": "ok"
}
```

---

## User Schema Definition

```python
{
  "type": "record",
  "name": "User",
  "namespace": "com.example",
  "fields": [
    {"name": "id", "type": "long"},           # 64-bit integer
    {"name": "name", "type": "string"},       # Variable string
    {"name": "email", "type": "string"},      # Variable string
    {"name": "age", "type": "int"},           # 32-bit integer
    {"name": "country", "type": "string"},    # Variable string
    {"name": "created_at", "type": "string"}, # ISO 8601 timestamp
    {"name": "score", "type": "double"},      # 64-bit float
    {"name": "active", "type": "boolean"}     # True/False
  ]
}
```

**Total Fixed Fields:** 3 (id, age, active, score)
**Total Variable Fields:** 5 (name, email, country, created_at, but encoded in Avro)
**Approximate Size:**
- JSON: 150-200 bytes per record
- Avro: 50-80 bytes per record

---

## Sample Data Generation

### Field Values (Randomly Selected)

**Names:**
```
Alice, Bob, Charlie, Diana, Edward, Fiona, George, Hannah, Isaac, Julia
```

**Email Domains:**
```
gmail.com, yahoo.com, outlook.com, hotmail.com, example.com
```

**Countries:**
```
USA, UK, France, Germany, Japan, Canada, Australia, Brazil, India, Mexico
```

**Random Ranges:**
- ID: 1 - 10,000
- Age: 18 - 80
- Score: 0.0 - 100.0
- Active: true/false (50% each)
- Timestamp: Current UTC time

---

## Performance Analysis

### What Gets Measured?

1. **Processing Time (ms)** - Time from sending first byte to receiving last byte
2. **Total Size (KB)** - Total bytes transmitted
3. **Records Processed** - Count of records sent/received
4. **Throughput (rec/s)** - Records per second = count / (time in seconds)
5. **Average Per Record (ms)** - Total time / record count
6. **Data Efficiency (%)** - (1 - Avro size / JSON size) × 100

### Typical Improvements with Avro

| Metric | Improvement |
|--------|---|
| Data Size | 60-70% reduction |
| Processing Time | 15-25% faster |
| Throughput | 20-30% increase |
| Bandwidth | 60-70% savings |

### When JSON Wins

- Single record transfers
- Cached responses (already processed)
- Schema very simple (2-3 fields)
- Network bandwidth not constrained

---

## Docker Compose Configuration

```yaml
services:
  avro-api:
    build:
      context: .
      dockerfile: api/Dockerfile
    ports:
      - "5000:5000"
    environment:
      FLASK_APP: app.py
      FLASK_ENV: production
    volumes:
      - ./api:/app
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 5s
```

---

## Customization Guide

### Add a New Field to User Schema

1. **Update USER_SCHEMA in app.py:**
```python
USER_SCHEMA = {
    "type": "record",
    "name": "User",
    "fields": [
        # ...existing fields...
        {"name": "phone", "type": ["null", "string"], "default": None},
    ]
}
```

2. **Update generate_user() function:**
```python
def generate_user():
    return {
        # ...existing fields...
        "phone": f"+1{random.randint(2000000000, 9999999999)}"
    }
```

### Change Number of Records

Edit both streaming endpoints:
```python
for i in range(1000):  # Change from 100 to 1000
```

### Adjust Streaming Delay

Edit streaming endpoint:
```python
time.sleep(0.1)  # 100ms delay between records
```

### Modify Server Port

In `docker-compose-api.yml`:
```yaml
ports:
  - "8000:5000"  # Access on http://localhost:8000
```

---

## Browser Developer Tools Usage

### View Network Traffic

1. Open DevTools (F12)
2. Go to "Network" tab
3. Click "Start Test"
4. Observe requests to `/api/json/stream` and `/api/avro/stream`
5. Click each request to see headers and response

### Monitor Console

1. Open DevTools (F12)
2. Go to "Console" tab
3. View real-time logs of metrics and errors

### Analyze Performance

1. Open DevTools (F12)
2. Go to "Performance" tab
3. Record while test runs
4. Analyze CPU usage and timing

---

## Production Deployment

### Recommended Changes

1. **Add authentication:**
```python
from flask import request
@app.before_request
def check_auth():
    token = request.headers.get('Authorization')
    # Validate token
```

2. **Add rate limiting:**
```python
from flask_limiter import Limiter
limiter = Limiter(app)

@app.route('/api/json/stream')
@limiter.limit("10 per minute")
def json_stream():
```

3. **Use HTTPS:**
```python
app.run(host='0.0.0.0', port=5000, ssl_context='adhoc')
```

4. **Add logging:**
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

5. **Configure for production:**
```python
# Use Gunicorn instead of Flask dev server
# gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## Troubleshooting Guide

### Dashboard shows "0" for all metrics
- Refresh page
- Check browser console for JavaScript errors
- Verify API is running: `curl http://localhost:5000/api/health`

### Port 5000 already in use
```powershell
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### CORS errors in browser
- Ensure Flask-CORS is installed
- Check that API is running on correct URL

### Docker build failures
```powershell
docker compose -f docker-compose-api.yml down -v
docker system prune -f
docker compose -f docker-compose-api.yml up -d --build
```

---

**Created:** November 27, 2025
**Last Updated:** November 27, 2025
**Version:** 1.0.0
