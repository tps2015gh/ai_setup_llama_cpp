@echo off
:: Add-Python-To-Path.bat
// Searches for Python and adds it to PATH, then tests python --version

setlocal EnableDelayedExpansion

echo ============================================================
echo Python PATH Manager
echo ============================================================
echo.

:: Step 1: Search for Python
echo [Step 1] Searching for Python...
set PYTHON_PATH=

:: Check common locations
for %%p in (
    "C:\Python39\python.exe"
    "C:\Python310\python.exe"
    "C:\Python311\python.exe"
    "C:\Python312\python.exe"
    "C:\Python313\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python39\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
    "C:\Program Files\Python39\python.exe"
    "C:\Program Files\Python310\python.exe"
    "C:\Program Files\Python311\python.exe"
    "C:\Program Files\Python312\python.exe"
    "C:\Program Files\Python313\python.exe"
) do (
    if not defined PYTHON_PATH (
        if exist %%p (
            set PYTHON_PATH=%%~dp
            echo Found: %%p
        )
    )
)

:: Check if already in PATH
where python >nul 2>&1
if %errorlevel% equ 0 (
    echo.
    echo Python is already in PATH:
    where python
    echo.
    set PYTHON_PATH=
    goto test_python
)

if not defined PYTHON_PATH (
    echo.
    echo ERROR: Python not found!
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

:: Step 2: Add to PATH
echo.
echo [Step 2] Adding Python to PATH...
echo Current PATH does not include: %PYTHON_PATH%

:: Add to current session PATH
set "PATH=%PYTHON_PATH%;%PATH%"
echo.
echo Added to session PATH: %PYTHON_PATH%
echo.
echo NOTE: This only affects the current command session.
echo To make it permanent, you need to:
echo   1. Open System Properties ^> Environment Variables
echo   2. Add %PYTHON_PATH% to your PATH variable
echo.
echo Or run this PowerShell command as Administrator:
echo   [Environment]::SetEnvironmentVariable("Path", "$env:Path;%PYTHON_PATH%", "Machine")
echo.

:: Step 3: Test Python
:test_python
echo ============================================================
echo [Step 3] Testing Python...
echo ============================================================
echo.

python --version

if %errorlevel% equ 0 (
    echo.
    echo SUCCESS: Python is working!
    echo Full path: 
    where python
) else (
    echo.
    echo FAILED: Python --version returned an error.
    exit /b 1
)

echo.
echo ============================================================
python -c "import sys; print('Python executable:', sys.executable); print('Python version:', sys.version)"
echo ============================================================

pause
