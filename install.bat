@echo off
REM SnapBase Installation Helper for Windows
REM This script checks for Python and guides users through setup

setlocal enabledelayedexpansion

echo.
echo ========================================
echo   SnapBase Installation Helper
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo.
    echo To fix this, visit: https://www.python.org/downloads/
    echo.
    echo IMPORTANT: During installation, check "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

REM Get Python version
for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo [OK] %PYTHON_VERSION% detected
echo.

REM Check if pip is available for this Python
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] pip is not available for this Python interpreter
    echo.
    echo Try reinstalling Python and ensure "pip" is selected during installation
    echo Visit: https://www.python.org/downloads/
    echo Or run: python -m ensurepip --upgrade
    echo.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python -m pip --version') do set PIP_VERSION=%%i
echo [OK] !PIP_VERSION!
echo.

REM Check if git is installed (optional but recommended)
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Git is not installed (optional)
    echo To use git: https://git-scm.com/download/win
    echo.
) else (
    for /f "tokens=*" %%i in ('git --version') do set GIT_VERSION=%%i
    echo [OK] !GIT_VERSION!
    echo.
)

REM Install SnapBase
echo Installing SnapBase...
echo.

python -m pip install -e .

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Installation failed
    echo.
    echo Troubleshooting:
    echo 1. Make sure you're in the correct directory (sql-bot-3)
    echo 2. Try running: python -m pip install --upgrade pip
    echo 3. Check your internet connection
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Installation Complete!
echo ========================================
echo.
echo You can now use: snapbase
echo.
pause
