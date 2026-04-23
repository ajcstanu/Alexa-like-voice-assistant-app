@echo off
:: setup.bat — Windows setup for AI Voice Assistant

echo ==================================================
echo   AI Voice Assistant — Windows Setup
echo ==================================================

:: Check Python
where python >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Download from https://python.org
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do echo %%i found.

:: Create venv
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate
call venv\Scripts\activate.bat

:: Upgrade pip
pip install --upgrade pip -q

:: Install packages
echo Installing packages...
pip install -r requirements.txt

echo.
echo ==================================================
echo   Setup complete!
echo ==================================================
echo.
echo   Set your API key:
echo     set ANTHROPIC_API_KEY=sk-ant-...
echo.
echo   Run the assistant:
echo     python assistant.py
echo.
pause
