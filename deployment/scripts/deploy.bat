@echo off
echo.
echo Docker Churn Prediction System - Setup
echo ==========================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker is not installed!
    echo Please install Docker Desktop from: https://docs.docker.com/desktop/install/windows-install/
    pause
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker Compose is not installed!
    echo Please install Docker Compose
    pause
    exit /b 1
)

echo Docker installed
echo Docker Compose installed
echo.

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker daemon is not running!
    echo Please start Docker Desktop and try again.
    pause
    exit /b 1
)

echo Docker daemon is running
echo.

echo Building Docker image...
echo This may take 5-10 minutes on first run...
echo.

docker-compose build

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Build failed! Check the error messages above.
    pause
    exit /b 1
)

echo.
echo Build successful!
echo.

echo Starting application...
docker-compose up -d

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to start! Check the error messages above.
    pause
    exit /b 1
)

echo.
echo Waiting for application to be ready...
timeout /t 10 /nobreak >nul

echo.
echo ==========================================
echo DEPLOYMENT COMPLETE!
echo ==========================================
echo.
echo Access your dashboard at:
echo    http://localhost:8000
echo.
echo API Documentation:
echo    http://localhost:8000/docs
echo.
echo Useful commands:
echo    View logs:    docker-compose logs -f
echo    Stop app:     docker-compose down
echo    Restart:      docker-compose restart
echo.
echo For more info, see DOCKER_GUIDE.md
echo.
pause
