@echo off
title PriceMonitor Start Script
echo ==========================================
echo       Starting PriceMonitor System...
echo ==========================================
echo.

:: 1. Start Backend (Python)
echo [1/2] Starting Backend Service...
start "PriceMonitor Backend" cmd /k "cd /d "%~dp0" && python -m src.app"

:: Wait for backend init
timeout /t 2 /nobreak >nul

:: 2. Start Frontend (Web UI)
echo [2/2] Starting Web Interface...
cd /d "%~dp0web-ui"
start "PriceMonitor WebUI" cmd /k "npm run dev"

echo.
echo ==========================================
echo       Launch Commands Sent!
echo ==========================================
echo.
echo Please check the two new black windows for any errors.
echo If everything is fine, open browser at: http://localhost:5173
echo.
pause
