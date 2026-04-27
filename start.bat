@echo off
cd /d "%~dp0"
echo 正在启动生词本...
start /b python -m http.server 8080 > nul 2>&1
if errorlevel 1 (
    start /b python3 -m http.server 8080 > nul 2>&1
)
timeout /t 2 /nobreak > nul
start http://localhost:8080
echo 已打开浏览器，不要关闭这个窗口
pause
