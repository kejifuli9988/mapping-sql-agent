@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
set "VSCODE_EXE=C:\Users\Guozheyu\AppData\Local\Programs\Microsoft VS Code\Code.exe"

if not exist "%VSCODE_EXE%" (
    echo [ERROR] VS Code was not found at:
    echo %VSCODE_EXE%
    pause
    exit /b 1
)

start "" "%VSCODE_EXE%" "%SCRIPT_DIR%"
exit /b 0
