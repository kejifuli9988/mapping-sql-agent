@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

set "HOST=127.0.0.1"
set "PORT=8000"
set "URL=http://%HOST%:%PORT%/"

where python >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Python not found in PATH.
    echo Please install Python 3 and make sure "python" is available in the terminal.
    pause
    exit /b 1
)

echo Checking whether port %PORT% is already in use...
netstat -ano | findstr /R /C:":%PORT% .*LISTENING" >nul
if not errorlevel 1 (
    echo Port %PORT% is already in use. Trying to open the page directly...
    start "" "%URL%"
    exit /b 0
)

echo Starting Mapping SQL Agent Web...
start "Mapping SQL Agent Web" cmd /k "cd /d ""%SCRIPT_DIR%"" && python webapp.py --host %HOST% --port %PORT%"

echo Waiting for the local server to start...
timeout /t 3 /nobreak >nul

echo Opening %URL%
start "" "%URL%"

exit /b 0
