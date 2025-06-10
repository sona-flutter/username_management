@echo off
echo Setting up User Management API...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH!
    echo Please install Python 3.12+ and try again.
    pause
    exit /b 1
)

echo Python is installed.
echo Installing required packages...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo Failed to install packages!
    pause
    exit /b 1
)

echo.
echo Starting User Management API...
echo.
echo API will be available at:
echo - Local: http://localhost:5000
echo - Network: http://0.0.0.0:5000
echo - Swagger UI: http://localhost:5000/swagger/
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py

pause 