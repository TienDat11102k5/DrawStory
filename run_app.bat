@echo off
chcp 65001 > nul
title DrawStory AI Launcher
echo ========================================================
echo       🎨 ĐANG KHỞI ĐỘNG HỆ THỐNG DRAWSTORY AI ✍️
echo ========================================================
echo.

cd /d "%~dp0"

echo [1/3] Đang khởi động Backend API Server (cổng 8000)...
start "DrawStory Backend API" cmd /k ".\venv\Scripts\uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload"

timeout /t 3 /nobreak > nul

echo [2/3] Đang khởi động Frontend Web Studio (cổng 3000)...
cd frontend
start "DrawStory Frontend Studio" cmd /k "npm run dev"

timeout /t 3 /nobreak > nul

echo [3/3] Đang mở ứng dụng trên trình duyệt web...
start http://localhost:3000

echo.
echo ========================================================
echo   ✅ Hệ thống đã sẵn sàng tại: http://localhost:3000
echo   📚 Tài liệu Swagger API tại: http://127.0.0.1:8000/docs
echo ========================================================
echo.
pause
