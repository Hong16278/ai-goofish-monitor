@echo off
title Sync to GitHub
echo ==========================================
echo       Syncing Code to GitHub...
echo ==========================================
echo.

:: Ensure correct directory
cd /d "%~dp0"

:: 1. Check Status
echo [1/3] Checking file changes...
git status
echo.

:: 2. Add Changes
echo [2/3] Adding changes...
git add .

:: 3. Commit
echo.
set /p commit_msg="Enter commit message (Press Enter for default): "
if "%commit_msg%"=="" set commit_msg=Auto update: %date% %time%

echo.
echo Committing: "%commit_msg%"
git commit -m "%commit_msg%"

:: 4. Push
echo.
echo [3/3] Pushing to GitHub (origin master)...
echo Note: If it freezes or fails, please check your VPN/Proxy.
git push origin master

if %errorlevel% neq 0 (
    echo.
    echo ==========================================
    echo [ERROR] Push Failed!
    echo ==========================================
    echo Possible reasons:
    echo 1. Network timeout (Try turning on VPN)
    echo 2. Authentication failed
    echo.
) else (
    echo.
    echo ==========================================
    echo [SUCCESS] Code uploaded to GitHub!
    echo ==========================================
)

pause
