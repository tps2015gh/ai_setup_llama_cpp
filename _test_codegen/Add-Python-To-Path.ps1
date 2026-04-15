# Add-Python-To-Path.ps1
# PowerShell tool to add Python to PATH and test it

[CmdletBinding()]
param(
    [switch]$Permanent,
    [switch]$UserScope,
    [switch]$ListOnly
)

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Python PATH Manager (PowerShell)" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Function to search Python
function Find-Python {
    $pythonExes = @()
    
    # Search in common locations
    $searchPaths = @(
        'C:\Python*',
        'C:\Program Files\Python*',
        'C:\Program Files (x86)\Python*',
        "$env:LOCALAPPDATA\Programs\Python\Python*",
        "$env:APPDATA\Local\Programs\Python\Python*"
    )
    
    foreach ($pattern in $searchPaths) {
        $found = Get-ChildItem -Path $pattern -Filter 'python.exe' -Recurse -ErrorAction SilentlyContinue
        foreach ($exe in $found) {
            if ($pythonExes -notcontains $exe.FullName) {
                $pythonExes += $exe.FullName
            }
        }
    }
    
    # Check PATH
    $pathPython = Get-Command python -ErrorAction SilentlyContinue
    if ($pathPython) {
        if ($pythonExes -notcontains $pathPython.Source) {
            $pythonExes += $pathPython.Source
        }
    }
    
    return $pythonExes
}

# Find Python installations
Write-Host "[1/3] Searching for Python..." -ForegroundColor Yellow
$pythonPaths = Find-Python

if ($pythonPaths.Count -eq 0) {
    Write-Host "ERROR: No Python installations found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Python from https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "Make sure to check 'Add Python to PATH' during installation." -ForegroundColor Yellow
    exit 1
}

Write-Host "Found $($pythonPaths.Count) Python installation(s):" -ForegroundColor Green
foreach ($path in $pythonPaths) {
    $version = & $path --version 2>&1
    Write-Host "  - $path ($version)" -ForegroundColor Green
}

Write-Host ""

# Check if Python is already in PATH
$currentPython = Get-Command python -ErrorAction SilentlyContinue
if ($currentPython) {
    Write-Host "[INFO] Python is already in PATH:" -ForegroundColor Cyan
    Write-Host "  $($currentPython.Source)" -ForegroundColor Green
    Write-Host ""
    
    if ($ListOnly) {
        Write-Host "[INFO] List-only mode. Exiting." -ForegroundColor Yellow
        exit 0
    }
} else {
    if ($ListOnly) {
        Write-Host "[INFO] Python is NOT in current PATH." -ForegroundColor Yellow
        exit 0
    }
    
    # Add first found Python to PATH
    $pythonDir = Split-Path $pythonPaths[0] -Parent
    Write-Host "[2/3] Adding to PATH: $pythonDir" -ForegroundColor Yellow
    
    # Add to current session
    $env:Path = "$pythonDir;$env:Path"
    Write-Host "  Added to current session PATH" -ForegroundColor Green
    
    # Add permanently if requested
    if ($Permanent) {
        $scope = if ($UserScope) { "User" } else { "Machine" }
        Write-Host "  Adding to system PATH (permanent)..." -ForegroundColor Yellow
        
        try {
            [Environment]::SetEnvironmentVariable(
                "Path",
                "$env:Path",
                [EnvironmentVariableTarget]::$scope
            )
            Write-Host "  Successfully added to permanent PATH ($scope scope)" -ForegroundColor Green
        } catch {
            Write-Host "  ERROR: Failed to add to permanent PATH: $_" -ForegroundColor Red
            Write-Host "  TIP: Run PowerShell as Administrator to modify Machine-level PATH" -ForegroundColor Yellow
        }
    } else {
        Write-Host ""
        Write-Host "NOTE: This only affects the current PowerShell session." -ForegroundColor Yellow
        Write-Host "To make it permanent, run with -Permanent flag:" -ForegroundColor Yellow
        Write-Host "  .\Add-Python-To-Path.ps1 -Permanent" -ForegroundColor Gray
        Write-Host "Or run as Administrator for system-wide:" -ForegroundColor Yellow
        Write-Host "  .\Add-Python-To-Path.ps1 -Permanent" -ForegroundColor Gray
    }
    
    Write-Host ""
}

# Test Python
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "[3/3] Testing Python..." -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

python --version

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "SUCCESS: Python is working!" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "Details:" -ForegroundColor Cyan
    python -c "import sys; print(f'  Executable: {sys.executable}'); print(f'  Version: {sys.version}'); print(f'  Platform: {sys.platform}')"
    
    Write-Host ""
    Write-Host "All Python paths found:" -ForegroundColor Cyan
    foreach ($path in $pythonPaths) {
        $version = & $path --version 2>&1
        Write-Host "  [$version] $path" -ForegroundColor Gray
    }
} else {
    Write-Host ""
    Write-Host "FAILED: Python test failed!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
