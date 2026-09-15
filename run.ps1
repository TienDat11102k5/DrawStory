# Khởi động Backend + Frontend + Mở trình duyệt bằng 1 lệnh: .\run.ps1
$root = $PSScriptRoot
Write-Host "Dang khoi dong DrawStory AI..." -ForegroundColor Cyan

# 1. Chay Backend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$root'; .\venv\Scripts\uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload"

# 2. Chay Frontend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$root\frontend'; npm run dev"

# 3. Mo Browser
Start-Sleep -Seconds 2
Start-Process "http://localhost:3000"

Write-Host "He thong da khoi dong thanh cong tai: http://localhost:3000" -ForegroundColor Green
