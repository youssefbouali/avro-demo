#!/usr/bin/env pwsh

# ===============================================
# Avro vs JSON REST API - PowerShell Quick Start
# ===============================================

function Show-Menu {
    Clear-Host
    Write-Host "======================================" -ForegroundColor Cyan
    Write-Host "  Avro vs JSON REST API - Quick Start  " -ForegroundColor Cyan
    Write-Host "======================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "1. Start with Docker Compose (Recommended)" -ForegroundColor Green
    Write-Host "2. Start with Local Python" -ForegroundColor Green
    Write-Host "3. Stop containers" -ForegroundColor Yellow
    Write-Host "4. View logs" -ForegroundColor Yellow
    Write-Host "5. Check status" -ForegroundColor Yellow
    Write-Host "6. Clean up everything" -ForegroundColor Red
    Write-Host "7. Exit" -ForegroundColor Gray
    Write-Host ""
}

function Start-DockerCompose {
    Clear-Host
    Write-Host "Starting with Docker Compose..." -ForegroundColor Green
    Write-Host ""
    
    # Check Docker
    $docker = docker --version 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Docker is not installed!" -ForegroundColor Red
        Read-Host "Press Enter to continue"
        return
    }
    
    Write-Host "Docker version: $docker" -ForegroundColor Green
    Write-Host ""
    
    # Change to project directory
    $projectPath = "c:\Master IL\S3\Web Services et Web Analytics\avro\avro-demo"
    Set-Location $projectPath
    
    Write-Host "Building containers..." -ForegroundColor Yellow
    docker compose -f docker-compose-api.yml up -d
    
    Write-Host "Waiting for services to start..." -ForegroundColor Yellow
    Start-Sleep -Seconds 5
    
    Write-Host ""
    Write-Host "Checking status..." -ForegroundColor Yellow
    docker compose -f docker-compose-api.yml ps
    
    Write-Host ""
    Write-Host "Opening dashboard in browser..." -ForegroundColor Green
    Start-Sleep -Seconds 2
    
    try {
        Start-Process "http://localhost:5000/"
        Write-Host "Dashboard opened in your browser!" -ForegroundColor Green
    }
    catch {
        Write-Host "Please open http://localhost:5000/ manually in your browser" -ForegroundColor Yellow
    }
    
    Write-Host ""
    Write-Host "To stop: docker compose -f docker-compose-api.yml down" -ForegroundColor Gray
    Write-Host "To view logs: docker compose -f docker-compose-api.yml logs -f avro-api" -ForegroundColor Gray
    Write-Host ""
    
    Read-Host "Press Enter to continue"
}

function Start-PythonLocal {
    Clear-Host
    Write-Host "Starting with Local Python..." -ForegroundColor Green
    Write-Host ""
    
    # Check Python
    $python = python --version 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Python is not installed!" -ForegroundColor Red
        Read-Host "Press Enter to continue"
        return
    }
    
    Write-Host "Python version: $python" -ForegroundColor Green
    Write-Host ""
    
    # Change to api directory
    $apiPath = "c:\Master IL\S3\Web Services et Web Analytics\avro\avro-demo\api"
    Set-Location $apiPath
    
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & "$apiPath\venv\Scripts\Activate.ps1"
    
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    pip install -q -r requirements.txt
    
    Write-Host ""
    Write-Host "Starting Flask server..." -ForegroundColor Green
    Write-Host "Opening http://localhost:5000/ in 2 seconds..." -ForegroundColor Yellow
    
    Start-Sleep -Seconds 2
    try {
        Start-Process "http://localhost:5000/"
    }
    catch {
        Write-Host "Please open http://localhost:5000/ manually" -ForegroundColor Yellow
    }
    
    Write-Host ""
    Write-Host "Running Flask app..." -ForegroundColor Green
    python app.py
}

function Stop-Containers {
    Clear-Host
    Write-Host "Stopping containers..." -ForegroundColor Yellow
    
    $projectPath = "c:\Master IL\S3\Web Services et Web Analytics\avro\avro-demo"
    Set-Location $projectPath
    
    docker compose -f docker-compose-api.yml stop
    
    Write-Host "Containers stopped." -ForegroundColor Green
    Read-Host "Press Enter to continue"
}

function View-Logs {
    Clear-Host
    Write-Host "Viewing logs (Press Ctrl+C to exit)..." -ForegroundColor Yellow
    Write-Host ""
    
    $projectPath = "c:\Master IL\S3\Web Services et Web Analytics\avro\avro-demo"
    Set-Location $projectPath
    
    docker compose -f docker-compose-api.yml logs -f avro-api
}

function Check-Status {
    Clear-Host
    Write-Host "Checking container status..." -ForegroundColor Yellow
    Write-Host ""
    
    $projectPath = "c:\Master IL\S3\Web Services et Web Analytics\avro\avro-demo"
    Set-Location $projectPath
    
    docker compose -f docker-compose-api.yml ps
    
    Write-Host ""
    Write-Host "Health check..." -ForegroundColor Yellow
    
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:5000/api/health" -TimeoutSec 5
        Write-Host "API Status: $($response.StatusCode)" -ForegroundColor Green
        Write-Host "Response: $($response.Content)" -ForegroundColor Green
    }
    catch {
        Write-Host "ERROR: API not responding" -ForegroundColor Red
    }
    
    Write-Host ""
    Read-Host "Press Enter to continue"
}

function Clean-Up {
    Clear-Host
    Write-Host "WARNING: This will remove all containers and volumes!" -ForegroundColor Red
    Write-Host ""
    
    $confirm = Read-Host "Are you sure? (yes/no)"
    
    if ($confirm -eq "yes") {
        Write-Host ""
        Write-Host "Cleaning up..." -ForegroundColor Yellow
        
        $projectPath = "c:\Master IL\S3\Web Services et Web Analytics\avro\avro-demo"
        Set-Location $projectPath
        
        docker compose -f docker-compose-api.yml down -v
        
        Write-Host "Docker system prune..." -ForegroundColor Yellow
        docker system prune -f
        
        Write-Host ""
        Write-Host "Cleanup complete!" -ForegroundColor Green
    }
    else {
        Write-Host "Cleanup cancelled." -ForegroundColor Yellow
    }
    
    Write-Host ""
    Read-Host "Press Enter to continue"
}

# Main loop
do {
    Show-Menu
    
    $choice = Read-Host "Enter your choice (1-7)"
    
    switch ($choice) {
        "1" { Start-DockerCompose }
        "2" { Start-PythonLocal }
        "3" { Stop-Containers }
        "4" { View-Logs }
        "5" { Check-Status }
        "6" { Clean-Up }
        "7" { 
            Clear-Host
            Write-Host "Thank you for using Avro vs JSON API!" -ForegroundColor Cyan
            Write-Host ""
            exit
        }
        default {
            Write-Host "Invalid choice. Please try again." -ForegroundColor Red
            Read-Host "Press Enter to continue"
        }
    }
} while ($true)
