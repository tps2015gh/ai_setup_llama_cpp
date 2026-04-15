@echo off
:: AI Coder Launcher
:: Quick start script for AI Coder - Modular Version
:: Version: 2.0.0

echo ============================================================
echo   AI Coder - Modular Agentic Code Editor v2.0
echo ============================================================
echo.

:: Find Python executable
set PYTHON_EXE=C:\Program Files\Blender Foundation\Blender 2.91\2.91\python\bin\python.exe

if not exist "%PYTHON_EXE%" (
    echo ERROR: Python not found at: %PYTHON_EXE%
    echo.
    echo Please install Python 3.7+ from https://www.python.org/downloads/
    echo Or update the PYTHON_EXE path in this script
    echo.
    pause
    exit /b 1
)

:: Check if colorama is installed
"%PYTHON_EXE%" -c "import colorama" 2>nul
if errorlevel 1 (
    echo Installing required packages...
    "%PYTHON_EXE%" -m pip install --user colorama requests
    echo.
)

:: Run AI Coder Modular
echo Starting AI Coder v2.0...
echo.
"%PYTHON_EXE%" "%~dp0ai_coder_modular\ai_coder.py"

pause
