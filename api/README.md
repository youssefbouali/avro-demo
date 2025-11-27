# Avro vs JSON REST API Comparison - Complete Guide

A comprehensive real-time performance comparison tool between Avro and JSON serialization formats with streaming and batch data processing capabilities.

## 📋 Project Structure

```
avro-demo/
├── api/
│   ├── app.py                  # Flask REST API with JSON & Avro endpoints
│   ├── index.html              # Interactive web dashboard
│   ├── requirements.txt         # Python dependencies
│   └── Dockerfile              # Container configuration
├── docker-compose-api.yml       # Docker Compose for API
└── README.md                    # This file
```

## ✨ Features

### REST API Endpoints

#### JSON Endpoints
- **`GET /api/json/stream`** - Stream 100 users as JSON (line-delimited)
- **`GET /api/json/batch`** - Get 100 users as JSON in a single response

#### Avro Endpoints
- **`GET /api/avro/stream`** - Stream 100 users as Avro (base64 encoded)
- **`GET /api/avro/batch`** - Get 100 users as Avro in a single response

#### Utility Endpoints
- **`GET /api/health`** - Health check endpoint

### Real-Time Performance Metrics

The dashboard displays:
- **Processing Time** - Total time to send/receive all data
- **Data Size** - Total bytes transmitted
- **Throughput** - Records processed per second
- **Average Per Record** - Average processing time per record
- **Data Efficiency** - Compression ratio
- **Live Progress** - Real-time progress bars

### Comparison Analysis

Side-by-side comparison showing:
- Performance winner for each metric
- Percentage improvement between formats
- Detailed statistics table
- Sample data viewer

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

```powershell
# Navigate to project root
cd c:\Master IL\S3\Web Services et Web Analytics\avro\avro-demo

# Build and start the API
docker compose -f docker-compose-api.yml up -d

# Check if running
docker compose -f docker-compose-api.yml ps

# Access the dashboard
# Open browser: http://localhost:5000/
```

### Option 2: Local Python Development

```powershell
# Navigate to api directory
cd c:\Master IL\S3\Web Services et Web Analytics\avro\avro-demo\api

# Create virtual environment (optional but recommended)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run the server
python app.py

# Access the dashboard
# Open browser: http://localhost:5000/
```

## 📊 Usage

### Via Web Dashboard

1. **Open Dashboard**: http://localhost:5000/ in your browser
2. **Select Test Type**:
   - **Streaming**: Tests real-time data streaming (100 records with 50ms delay between each)
   - **Batch**: Tests bulk data transfer (all 100 records at once)
3. **Click "Start Test"**: Runs both JSON and Avro tests simultaneously
4. **View Results**: Real-time metrics and comparison

### Via Command Line/cURL

```powershell
# JSON Streaming (100 records, line-delimited)
curl http://localhost:5000/api/json/stream

# Avro Streaming (100 records, base64-encoded)
curl http://localhost:5000/api/avro/stream

# JSON Batch (all 100 records at once)
curl http://localhost:5000/api/json/batch | ConvertFrom-Json | ConvertTo-Json

# Avro Batch
curl http://localhost:5000/api/avro/batch | ConvertFrom-Json
```

## 📈 Performance Metrics Explained

### Processing Time (ms)
The total time taken to send all data from server to client.
- **Avro typically faster** due to smaller payload size
- **Winner**: Lower value is better

### Total Size (KB)
Total data transmitted (Avro encoded as base64).
- **Avro typically smaller** (~50-70% reduction)
- **Winner**: Lower value is better

### Throughput (rec/s)
Number of records processed per second.
- **Higher throughput = better**
- **Winner**: Higher value is better

### Average Per Record (ms)
Average processing time per individual record.
- **Useful for latency-sensitive applications**
- **Winner**: Lower value is better

### Data Efficiency (%)
Compression ratio relative to JSON baseline.
- **100% = same size as JSON**
- **Lower = better compression**

## 🔧 API Response Format

### JSON Stream Response (Line-Delimited)
```json
{
  "sequence": 1,
  "data": {
    "id": 1234,
    "name": "Alice",
    "email": "user@example.com",
    "age": 25,
    "country": "USA",
    "created_at": "2024-01-15T10:30:00.123456",
    "score": 87.5,
    "active": true
  },
  "format": "json",
  "size_bytes": 156,
  "processing_time_ms": 0.234,
  "timestamp": "2024-01-15T10:30:00.123456"
}
```

### Avro Stream Response (Line-Delimited)
```json
{
  "sequence": 1,
  "data": "AoIKQWxpY2UaGnVzZXJAZXhhbXBsZS5jb20YCgpVU0EcNjA4MzMzMzMzM2FzAQ==",
  "format": "avro",
  "size_bytes": 58,
  "processing_time_ms": 0.156,
  "timestamp": "2024-01-15T10:30:00.123456"
}
```

## 📦 Sample Data Schema

User records contain:
```
- id (long): Unique identifier
- name (string): User full name
- email (string): Email address
- age (int): User age
- country (string): Country of residence
- created_at (string): ISO 8601 timestamp
- score (double): Numeric score
- active (boolean): Account active status
```

## 🐳 Docker Management

```powershell
# Start containers
docker compose -f docker-compose-api.yml up -d

# Stop containers
docker compose -f docker-compose-api.yml stop

# Restart containers
docker compose -f docker-compose-api.yml restart

# View logs
docker compose -f docker-compose-api.yml logs -f avro-api

# Remove containers
docker compose -f docker-compose-api.yml down

# Remove containers and volumes
docker compose -f docker-compose-api.yml down -v

# Check status
docker compose -f docker-compose-api.yml ps
```

## 📝 Key Findings

### When to Use JSON
- **Human readability** - Easy to debug and understand
- **Mixed data types** - Flexible schema
- **Browser-friendly** - Native JSON support
- **Small datasets** - Performance difference negligible

### When to Use Avro
- **High volume** - Significant bandwidth savings (50-70% reduction)
- **Real-time streaming** - Lower latency with smaller payloads
- **Schema evolution** - Built-in versioning support
- **Data lakes** - Efficient storage and processing
- **Bandwidth-constrained** - Mobile networks, IoT devices

### Typical Performance Results
| Metric | JSON | Avro | Avro Advantage |
|--------|------|------|---|
| Payload Size | 100% | 30-40% | 60-70% smaller |
| Processing Time | Baseline | -15 to -25% | 15-25% faster |
| Throughput | Baseline | +20 to +30% | 20-30% faster |

## 🛠️ Customization

### Add More Fields to User Schema

Edit `app.py`, in the `USER_SCHEMA` variable:
```python
USER_SCHEMA = {
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

Then update `generate_user()` function to include new fields.

### Change Data Volume

Edit `app.py`:
```python
@app.route('/api/json/stream', methods=['GET'])
def json_stream():
    def generate():
        for i in range(100):  # Change this number
```

### Adjust Stream Delay

Edit `app.py`:
```python
time.sleep(0.05)  # Change delay (in seconds)
```

## 🐛 Troubleshooting

### Port Already in Use
```powershell
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process
taskkill /PID <PID> /F
```

### CORS Errors
- Ensure `Flask-CORS` is installed
- The API is configured to accept requests from any origin

### Docker Build Issues
```powershell
# Clean build
docker compose -f docker-compose-api.yml build --no-cache

# Rebuild from scratch
docker compose -f docker-compose-api.yml down -v
docker compose -f docker-compose-api.yml up -d --build
```

### Performance Metrics Not Updating
- Check browser console for errors (F12)
- Verify API is running: http://localhost:5000/api/health
- Clear browser cache: Ctrl+Shift+Delete

## 📚 API Response Fields

All responses include:
- `sequence` - Record number (in streaming mode)
- `data` - The actual user record (or base64 for Avro)
- `format` - "json" or "avro"
- `size_bytes` - Size of serialized data
- `processing_time_ms` - Time to serialize (server-side)
- `timestamp` - ISO 8601 timestamp

## 🔐 Security Notes

⚠️ **This is a demo application. For production use:**
- Add authentication (JWT, OAuth2)
- Implement rate limiting
- Add input validation
- Use HTTPS
- Add request/response logging
- Implement caching strategies

## 📄 License

MIT License - Feel free to use for educational and commercial purposes.

## 🤝 Contributing

Contributions welcome! Please fork and submit pull requests.

---

**Built with ❤️ using Flask, Avro, and modern JavaScript**
