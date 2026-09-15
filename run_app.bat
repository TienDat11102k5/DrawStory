@echo off
title DrawStory AI Launcher
cd /d "%~dp0"

echo ========================================================
echo           STARTING DRAWSTORY AI SYSTEM
echo ========================================================
echo.

echo [1/3] Starting Backend API Server (port 8000)...
start "DrawStory Backend" cmd /k ".\venv\Scripts\uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload"

echo [2/3] Starting Frontend Studio (port 3000)...
start "DrawStory Frontend" cmd /k "cd /d "%~dp0frontend" && npm run dev"

timeout /t 2 /nobreak > nul

echo [3/3] Opening browser...
start http://localhost:3000

echo.
echo ========================================================
echo   Website:     http://localhost:3000
echo   Swagger API: http://127.0.0.1:8000/docs
echo ========================================================
echo.
