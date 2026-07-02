@echo off
title Chatty Talkie - Translator
echo.
echo  =============================================
echo       Chatty Talkie - Starting...
echo  =============================================
echo.

cd /d "%~dp0backend"

:: Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo [1/3] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment. Is Python installed?
        pause
        exit /b 1
    )
    echo       Done!
    echo.

    echo [2/3] Installing dependencies (first time only, please wait...
    call venv\Scripts\activate.bat
    pip install -r requirements.txt --quiet
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies.
        pause
        exit /b 1
    )
    echo       Done!
    echo.
) else (
    call venv\Scripts\activate.bat
    echo [OK] Virtual environment activated.
    echo.
)

echo [3/3] Starting Chatty Talkie server...
echo.
echo  =============================================
echo   Open your browser at:
echo   http://127.0.0.1:8000
echo  =============================================
echo.
echo   Press Ctrl+C to stop the server.
echo.

:: Open browser automatically after 5 seconds
start "" cmd /c "timeout /t 5 /nobreak >nul & start http://127.0.0.1:8000"

:: Start the server
uvicorn main:app --host 127.0.0.1 --port 8000

pause
