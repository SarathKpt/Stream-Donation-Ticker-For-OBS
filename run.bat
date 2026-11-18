@echo off
setlocal
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
    echo Python was not found. Install Python 3.8 or newer and add it to PATH.
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    python -m venv ".venv"
    if errorlevel 1 goto :error
)

".venv\Scripts\python.exe" -m pip install --disable-pip-version-check -r "%~dp0project\requirements.txt"
if errorlevel 1 goto :error

set "STREAM_DONATION_CONFIG_FILE=%~dp0config\config.json"
set "STREAM_DONATION_DATA_DIR=%~dp0data"
".venv\Scripts\python.exe" "%~dp0project\app\server.py"
if errorlevel 1 goto :error
exit /b 0

:error
echo.
echo The donation ticker did not start. Review the error above.
pause
exit /b 1
