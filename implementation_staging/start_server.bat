@echo off
cd /d "%~dp0"
title PiaomiaoLocalServer
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0restart_server.ps1"
set "ERR=%ERRORLEVEL%"
if "%ERR%"=="2" (
    echo.
    echo Another start is in progress. This extra window will close.
    timeout /t 2 /nobreak >nul
    exit /b 0
)
if not "%ERR%"=="0" (
    echo.
    echo Server exited with code %ERR%.
    pause
)
