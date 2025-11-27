@echo off
REM ===============================================
REM Avro vs JSON REST API - Quick Start Script
REM ===============================================

REM Colors
set /A COLOR_GREEN=02
set /A COLOR_YELLOW=0E
set /A COLOR_RED=0C

echo.
echo ===============================================
echo   Avro vs JSON REST API - Quick Start
echo ===============================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Docker is installed
) else (
    echo [ERROR] Docker is not installed. Please install Docker first.
    pause
    exit /b 1
)

echo.
echo Choose an option:
echo 1. Start with Docker Compose (Recommended)
echo 2. Start with Local Python
echo 3. Stop containers
echo 4. View logs
echo 5. Check status
echo 6. Clean up everything
echo 7. Exit
echo.

set /p choice="Enter your choice (1-7): "

if "%choice%"=="1" goto docker_start
if "%choice%"=="2" goto python_start
if "%choice%"=="3" goto docker_stop
if "%choice%"=="4" goto view_logs
if "%choice%"=="5" goto check_status
if "%choice%"=="6" goto cleanup
if "%choice%"=="7" goto end
goto invalid

:docker_start
cls
echo.
echo Starting with Docker Compose...
echo.
cd /d "c:\Master IL\S3\Web Services et Web Analytics\avro\avro-demo"
echo Building containers...
docker compose -f docker-compose-api.yml up -d
echo.
echo Waiting for services to start...
timeout /t 5 /nobreak
echo.
echo Checking status...
docker compose -f docker-compose-api.yml ps
echo.
echo Opening dashboard in browser...
start http://localhost:5000/
echo.
echo Dashboard should open in your browser!
echo.
echo To stop: docker compose -f docker-compose-api.yml down
echo To view logs: docker compose -f docker-compose-api.yml logs -f avro-api
pause
goto end

:python_start
cls
echo.
echo Starting with Local Python...
echo.
cd /d "c:\Master IL\S3\Web Services et Web Analytics\avro\avro-demo\api"
echo.
echo Creating virtual environment...
python -m venv venv
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Starting Flask server...
echo.
python app.py
goto end

:docker_stop
cls
echo.
echo Stopping containers...
cd /d "c:\Master IL\S3\Web Services et Web Analytics\avro\avro-demo"
docker compose -f docker-compose-api.yml stop
echo.
echo Containers stopped.
pause
goto end

:view_logs
cls
echo.
echo Viewing logs (Press Ctrl+C to exit)...
cd /d "c:\Master IL\S3\Web Services et Web Analytics\avro\avro-demo"
docker compose -f docker-compose-api.yml logs -f avro-api
goto end

:check_status
cls
echo.
echo Checking container status...
cd /d "c:\Master IL\S3\Web Services et Web Analytics\avro\avro-demo"
docker compose -f docker-compose-api.yml ps
echo.
echo Health check...
timeout /t 1 /nobreak
curl -s http://localhost:5000/api/health || echo [ERROR] API not responding
echo.
pause
goto end

:cleanup
cls
echo.
echo WARNING: This will remove all containers and volumes!
set /p confirm="Are you sure? (yes/no): "
if /i "%confirm%"=="yes" (
    echo.
    echo Cleaning up...
    cd /d "c:\Master IL\S3\Web Services et Web Analytics\avro\avro-demo"
    docker compose -f docker-compose-api.yml down -v
    echo Docker system prune...
    docker system prune -f
    echo.
    echo Cleanup complete!
) else (
    echo Cleanup cancelled.
)
echo.
pause
goto end

:invalid
cls
echo.
echo Invalid choice. Please try again.
pause
goto start

:end
echo.
echo ===============================================
echo   Thank you for using Avro vs JSON API!
echo ===============================================
echo.
pause
