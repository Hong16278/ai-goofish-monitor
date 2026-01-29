@echo off
title Stop PriceMonitor
echo ==========================================
echo       Stopping PriceMonitor System...
echo ==========================================
echo.

:: Kill Backend
echo [1/2] Stopping Backend Service...
taskkill /FI "WINDOWTITLE eq PriceMonitor Backend" /T /F >nul 2>&1

:: Kill Frontend
echo [2/2] Stopping Web Interface...
taskkill /FI "WINDOWTITLE eq PriceMonitor WebUI" /T /F >nul 2>&1

echo.
echo ==========================================
echo       System Stopped Successfully!
echo ==========================================
echo.
echo (Window will close in 3 seconds)
timeout /t 3 >nul
