# 🚀 Quick Start Commands

## Option 1: Using Docker Compose (Easiest)

```powershell
# Step 1: Navigate to project root
cd c:\Master IL\S3\Web Services et Web Analytics\avro\avro-demo

# Step 2: Start the API container
docker compose -f docker-compose-api.yml up -d

# Step 3: Wait 5 seconds for services to start
Start-Sleep -Seconds 5

# Step 4: Check if running
docker compose -f docker-compose-api.yml ps

# Step 5: Open in browser
Start-Process "http://localhost:5000/"

# Step 6: Run tests (streaming or batch)
# Click "Start Test" button in the browser dashboard

# To stop:
docker compose -f docker-compose-api.yml down
```

## Option 2: Using Local Python

```powershell
# Step 1: Navigate to api folder
cd c:\Master IL\S3\Web Services et Web Analytics\avro\avro-demo\api

# Step 2: Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Step 3: Install dependencies
pip install -r requirements.txt

# Step 4: Run the server
python app.py

# Step 5: Open browser
Start-Process "http://localhost:5000/"

# Step 6: Run tests in browser

# To stop: Press Ctrl+C in terminal
```

## 📊 Using the Dashboard

1. **Select Test Type**:
   - "Streaming" - Real-time 100 records with delays
   - "Batch" - All 100 records at once

2. **Click "Start Test"** - Automatically tests both JSON & Avro

3. **View Results**:
   - Left card: JSON performance
   - Right card: Avro performance
   - Bottom table: Direct comparison with winners

## 🧪 Testing via PowerShell

```powershell
# Test JSON Streaming
$response = Invoke-WebRequest -Uri "http://localhost:5000/api/json/stream"
$response.StatusCode  # Should be 200

# Test Avro Streaming
$response = Invoke-WebRequest -Uri "http://localhost:5000/api/avro/stream"
$response.StatusCode  # Should be 200

# Test JSON Batch
$response = Invoke-WebRequest -Uri "http://localhost:5000/api/json/batch"
$data = $response.Content | ConvertFrom-Json
$data.count  # Should be 100

# Test Avro Batch
$response = Invoke-WebRequest -Uri "http://localhost:5000/api/avro/batch"
$data = $response.Content | ConvertFrom-Json
$data.count  # Should be 100

# Health check
Invoke-WebRequest -Uri "http://localhost:5000/api/health"
```

## 📋 Expected Results

### Performance Comparison (100 records)

**Streaming Mode:**
- JSON: ~1500-2000 KB, 150-250ms
- Avro: ~450-600 KB, 100-150ms
- **Avro typically 60-70% smaller**

**Batch Mode:**
- JSON: ~1500-2000 KB, 50-100ms
- Avro: ~450-600 KB, 30-70ms
- **Avro typically 40-50% faster**

## 🔄 Restarting Services

```powershell
# Restart Docker container
docker compose -f docker-compose-api.yml restart avro-api

# Rebuild (if you modified files)
docker compose -f docker-compose-api.yml up -d --build

# Full reset
docker compose -f docker-compose-api.yml down -v
docker compose -f docker-compose-api.yml up -d
```

## 🆘 Troubleshooting

**Port 5000 already in use?**
```powershell
# Find and kill the process
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Docker issues?**
```powershell
# Check logs
docker compose -f docker-compose-api.yml logs avro-api

# Clean everything
docker compose -f docker-compose-api.yml down -v
docker system prune -f
docker compose -f docker-compose-api.yml up -d --build
```

**Python module errors?**
```powershell
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

## 📞 Dashboard Features

✅ Real-time performance metrics
✅ Streaming & batch test modes
✅ Side-by-side comparison
✅ Live progress bars
✅ Sample data viewer
✅ Processing time breakdown
✅ Throughput calculation
✅ Data efficiency analysis
✅ Responsive design
✅ No external dependencies

---

**That's it! Your Avro vs JSON comparison tool is ready to go!** 🎉
