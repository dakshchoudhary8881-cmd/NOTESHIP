@echo off
title NOTESHIP Launcher

:: === CONFIG ===
set BACKEND_DIR=%~dp0backend
set FRONTEND_DIR=%~dp0frontend

echo.
echo -----------------------------------------
echo        NOTESHIP – Launcher Started
echo -----------------------------------------
echo.

:: === Start Backend ===
echo Starting Backend (Flask)...
start cmd /k "cd /d %BACKEND_DIR% && python app.py"

:: === Start Frontend ===
echo Starting Frontend (Static Server)...
start cmd /k "cd /d %FRONTEND_DIR% && python -m http.server 8000 --bind 127.0.0.1 --directory ."

echo.
echo Frontend: http://localhost:8000
echo Backend : http://127.0.0.1:5000
echo -----------------------------------------
echo  Both servers launched in separate windows
echo -----------------------------------------
echo.
pause
