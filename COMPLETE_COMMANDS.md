# 🚀 COMPLETE COMMANDS - Avro vs JSON REST API

## ⚡ FASTEST WAY TO START

### Use the Interactive Script (Easiest!)

**PowerShell:**
```powershell
cd "c:\Master IL\S3\Web Services et Web Analytics\avro\avro-demo"
.\START.ps1
```

**Or Batch (CMD):**
```batch
cd "c:\Master IL\S3\Web Services et Web Analytics\avro\avro-demo"
START.bat
```

Then select option **1** for Docker Compose or **2** for Local Python.

---

## 🐳 DOCKER COMPOSE COMMANDS

### Start Services
```powershell
cd "c:\Master IL\S3\Web Services et Web Analytics\avro\avro-demo"
docker compose -f docker-compose-api.yml up -d
```

### Wait for Startup & Open Dashboard
```powershell
Start-Sleep -Seconds 5
Start-Process "http://localhost:5000/"
```

### Check Status
```powershell
docker compose -f docker-compose-api.yml ps
```

### View Logs (Real-time)
```powershell
docker compose -f docker-compose-api.yml logs -f avro-api
```

### Stop Services
```powershell
docker compose -f docker-compose-api.yml stop
```

### Stop & Remove Everything
```powershell
docker compose -f docker-compose-api.yml down -v
```

### Rebuild Containers
```powershell
docker compose -f docker-compose-api.yml up -d --build
```

### Full Reset (Clean Start)
```powershell
docker compose -f docker-compose-api.yml down -v
docker system prune -f
docker compose -f docker-compose-api.yml up -d --build
```

---

## 🐍 LOCAL PYTHON COMMANDS

### Setup Virtual Environment
```powershell
cd "c:\Master IL\S3\Web Services et Web Analytics\avro\avro-demo\api"
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Install Dependencies
```powershell
pip install -r requirements.txt
```

### Run the Server
```powershell
python app.py
```

### Open Dashboard
```powershell
Start-Process "http://localhost:5000/"
```

### Deactivate Virtual Environment (when done)
```powershell
deactivate
```

---

## 🧪 TESTING COMMANDS

### Test Health Check
```powershell
Invoke-WebRequest -Uri "http://localhost:5000/api/health"
```

### Test JSON Streaming
```powershell
$response = Invoke-WebRequest -Uri "http://localhost:5000/api/json/stream"
$response.StatusCode  # Should be 200
```

### Test Avro Streaming
```powershell
$response = Invoke-WebRequest -Uri "http://localhost:5000/api/avro/stream"
$response.StatusCode  # Should be 200
```

### Test JSON Batch
```powershell
$response = Invoke-WebRequest -Uri "http://localhost:5000/api/json/batch"
$data = $response.Content | ConvertFrom-Json
$data.count  # Should be 100
$data.size_bytes  # Total size
```

### Test Avro Batch
```powershell
$response = Invoke-WebRequest -Uri "http://localhost:5000/api/avro/batch"
$data = $response.Content | ConvertFrom-Json
$data.count  # Should be 100
$data.size_bytes  # Total size (should be smaller than JSON)
```

### Compare Sizes
```powershell
$json = (Invoke-WebRequest -Uri "http://localhost:5000/api/json/batch").Content | ConvertFrom-Json
$avro = (Invoke-WebRequest -Uri "http://localhost:5000/api/avro/batch").Content | ConvertFrom-Json
$reduction = (1 - $avro.size_bytes / $json.size_bytes) * 100
Write-Host "Avro is $(($reduction).ToString('F1'))% smaller"
```

---

## 🔍 TROUBLESHOOTING COMMANDS

### Check if Port 5000 is in Use
```powershell
netstat -ano | findstr :5000
```

### Kill Process on Port 5000
```powershell
# First get the PID from netstat command above
taskkill /PID <PID> /F
```

### Check Docker Installation
```powershell
docker --version
docker compose version
```

### Check Python Installation
```powershell
python --version
pip --version
```

### View All Docker Containers
```powershell
docker ps -a
```

### View All Docker Images
```powershell
docker images
```

### Check Docker Disk Usage
```powershell
docker system df
```

### Clean Docker Cache
```powershell
docker system prune -f
docker builder prune -f
```

---

## 📊 API ENDPOINTS REFERENCE

### JSON Streaming (100 records, line-delimited)
```
GET http://localhost:5000/api/json/stream
```

### Avro Streaming (100 records, base64-encoded, line-delimited)
```
GET http://localhost:5000/api/avro/stream
```

### JSON Batch (100 records in single response)
```
GET http://localhost:5000/api/json/batch
```

### Avro Batch (100 records in single response)
```
GET http://localhost:5000/api/avro/batch
```

### Health Check
```
GET http://localhost:5000/api/health
```

---

## 📁 PROJECT STRUCTURE

```
avro-demo/
├── START.ps1                      ← Run this (PowerShell)
├── START.bat                      ← Or this (CMD)
├── docker-compose-api.yml         ← Docker configuration
├── IMPLEMENTATION_SUMMARY.md      ← What was created
├── COMPLETE_COMMANDS.md           ← This file
│
└── api/
    ├── app.py                     ← Flask server
    ├── index.html                 ← Web dashboard
    ├── requirements.txt           ← Python dependencies
    ├── Dockerfile                 ← Container config
    ├── README.md                  ← Full documentation
    ├── QUICKSTART.md              ← Quick setup
    └── CONFIG_EXAMPLES.md         ← Customization guide
```

---

## 🎯 COMPLETE ONE-LINE COMMANDS

### Option 1: Docker Compose (Recommended)
```powershell
cd "c:\Master IL\S3\Web Services et Web Analytics\avro\avro-demo"; docker compose -f docker-compose-api.yml up -d; Start-Sleep -Seconds 5; Start-Process "http://localhost:5000/"
```

### Option 2: Local Python
```powershell
cd "c:\Master IL\S3\Web Services et Web Analytics\avro\avro-demo\api"; python -m venv venv; .\venv\Scripts\Activate.ps1; pip install -q -r requirements.txt; python app.py
```

---

## 🔄 COMMON WORKFLOWS

### Workflow 1: Start Fresh Development Environment
```powershell
# Clean up old containers
docker compose -f docker-compose-api.yml down -v

# Start fresh
docker compose -f docker-compose-api.yml up -d --build

# Wait and verify
Start-Sleep -Seconds 5
docker compose -f docker-compose-api.yml ps

# Open dashboard
Start-Process "http://localhost:5000/"
```

### Workflow 2: Development with Live Editing
```powershell
# Go to api directory
cd "c:\Master IL\S3\Web Services et Web Analytics\avro\avro-demo\api"

# Setup Python
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Run in development mode (watch for changes)
$env:FLASK_APP = "app.py"
$env:FLASK_ENV = "development"
python app.py
```

### Workflow 3: Run Tests Without UI
```powershell
# Start just the API
docker compose -f docker-compose-api.yml up -d

# Run tests
Invoke-WebRequest "http://localhost:5000/api/json/stream" | Select-Object StatusCode
Invoke-WebRequest "http://localhost:5000/api/avro/stream" | Select-Object StatusCode
Invoke-WebRequest "http://localhost:5000/api/health" | ConvertFrom-Json

# Stop when done
docker compose -f docker-compose-api.yml down
```

### Workflow 4: Performance Benchmarking
```powershell
# Run test 10 times and average results
for ($i = 1; $i -le 10; $i++) {
    Write-Host "Test run $i..."
    $json = (Invoke-WebRequest "http://localhost:5000/api/json/batch").Content | ConvertFrom-Json
    $avro = (Invoke-WebRequest "http://localhost:5000/api/avro/batch").Content | ConvertFrom-Json
    Write-Host "JSON: $($json.size_bytes) bytes, $($json.processing_time_ms)ms"
    Write-Host "Avro: $($avro.size_bytes) bytes, $($avro.processing_time_ms)ms"
    Write-Host ""
}
```

---

## 💡 USEFUL POWERSHELL FUNCTIONS

Add these to your PowerShell profile for convenience:

```powershell
# Start Avro API
function Start-AvroAPI {
    cd "c:\Master IL\S3\Web Services et Web Analytics\avro\avro-demo"
    docker compose -f docker-compose-api.yml up -d
    Start-Sleep -Seconds 5
    Start-Process "http://localhost:5000/"
    Write-Host "API started at http://localhost:5000/" -ForegroundColor Green
}

# Stop Avro API
function Stop-AvroAPI {
    cd "c:\Master IL\S3\Web Services et Web Analytics\avro\avro-demo"
    docker compose -f docker-compose-api.yml down
    Write-Host "API stopped" -ForegroundColor Yellow
}

# View Avro API logs
function Get-AvroAPILogs {
    cd "c:\Master IL\S3\Web Services et Web Analytics\avro\avro-demo"
    docker compose -f docker-compose-api.yml logs -f avro-api
}

# Check Avro API status
function Test-AvroAPI {
    try {
        $health = Invoke-WebRequest "http://localhost:5000/api/health" -TimeoutSec 5
        Write-Host "API Status: OK ($($health.StatusCode))" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "API Status: DOWN" -ForegroundColor Red
        return $false
    }
}

# Quick performance test
function Invoke-AvroPerformanceTest {
    param([int]$Iterations = 5)
    
    for ($i = 1; $i -le $Iterations; $i++) {
        $json = (Invoke-WebRequest "http://localhost:5000/api/json/batch").Content | ConvertFrom-Json
        $avro = (Invoke-WebRequest "http://localhost:5000/api/avro/batch").Content | ConvertFrom-Json
        
        $reduction = (1 - $avro.size_bytes / $json.size_bytes) * 100
        $speedup = ($json.processing_time_ms / $avro.processing_time_ms)
        
        Write-Host "Run $i: JSON ${json.size_bytes}B → Avro ${$avro.size_bytes}B (${reduction}% smaller), ${speedup}x faster"
    }
}
```

---

## 📞 NEED HELP?

### Check Documentation
- **Full Guide**: `api/README.md`
- **Quick Start**: `api/QUICKSTART.md`
- **Configuration**: `api/CONFIG_EXAMPLES.md`
- **Summary**: `IMPLEMENTATION_SUMMARY.md`

### Common Issues

**API won't start:**
```powershell
# Check if port is in use
netstat -ano | findstr :5000
# Kill if necessary
taskkill /PID <PID> /F
```

**Docker error:**
```powershell
# Clean everything
docker system prune -f -a
# Rebuild
docker compose -f docker-compose-api.yml up -d --build
```

**Python error:**
```powershell
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

---

## ✅ QUICK VERIFICATION CHECKLIST

Run these to verify everything is working:

```powershell
# 1. Docker running?
docker ps

# 2. API container running?
docker compose -f docker-compose-api.yml ps

# 3. API responding?
Invoke-WebRequest "http://localhost:5000/api/health"

# 4. JSON endpoint works?
Invoke-WebRequest "http://localhost:5000/api/json/batch" | Select-Object StatusCode

# 5. Avro endpoint works?
Invoke-WebRequest "http://localhost:5000/api/avro/batch" | Select-Object StatusCode

# 6. Dashboard loads?
Start-Process "http://localhost:5000/"
```

If all 6 tests pass ✅, you're ready to go!

---

## 🎓 LEARNING PATH

1. **Start**: Run `.\START.ps1`
2. **Test**: Click "Start Test" in dashboard
3. **Observe**: Watch JSON vs Avro metrics
4. **Analyze**: Check comparison table
5. **Experiment**: Try different test modes
6. **Customize**: Edit `api/app.py` to modify data
7. **Deploy**: Use Docker for production

---

**Version**: 1.0.0  
**Updated**: November 27, 2025  
**Status**: ✅ Ready to Use

Happy Testing! 🚀
