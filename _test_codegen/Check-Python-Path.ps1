# Check-Python-Path.ps1
# Tool to check if Python is in PATH and show PATH configuration

[CmdletBinding()]
param(
    [switch]$ShowAllPaths,
    [switch]$FixPath
)

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Python PATH Checker" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Check 1: Is python command available?
Write-Host "[Check 1] Testing 'python' command..." -ForegroundColor Yellow
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue

if ($pythonCmd) {
    Write-Host "  Status: FOUND" -ForegroundColor Green
    Write-Host "  Location: $($pythonCmd.Source)" -ForegroundColor Green
    
    $version = python --version 2>&1
    Write-Host "  Version: $version" -ForegroundColor Green
} else {
    Write-Host "  Status: NOT FOUND" -ForegroundColor Red
    Write-Host "  'python' is not recognized as a command in your PATH" -ForegroundColor Red
}

Write-Host ""

# Check 2: Is python3 command available?
Write-Host "[Check 2] Testing 'python3' command..." -ForegroundColor Yellow
$python3Cmd = Get-Command python3 -ErrorAction SilentlyContinue

if ($python3Cmd) {
    Write-Host "  Status: FOUND" -ForegroundColor Green
    Write-Host "  Location: $($python3Cmd.Source)" -ForegroundColor Green
    
    $version3 = python3 --version 2>&1
    Write-Host "  Version: $version3" -ForegroundColor Green
} else {
    Write-Host "  Status: NOT FOUND" -ForegroundColor Red
}

Write-Host ""

# Check 3: Is py launcher available?
Write-Host "[Check 3] Testing Python Launcher (py.exe)..." -ForegroundColor Yellow
$pyCmd = Get-Command py -ErrorAction SilentlyContinue

if ($pyCmd) {
    Write-Host "  Status: FOUND" -ForegroundColor Green
    Write-Host "  Location: $($pyCmd.Source)" -ForegroundColor Green
    Write-Host "  Installed versions:" -ForegroundColor Yellow
    py --list 2>&1 | ForEach-Object { Write-Host "    $_" }
} else {
    Write-Host "  Status: NOT FOUND" -ForegroundColor Red
    Write-Host "  Python Launcher (py.exe) not in PATH" -ForegroundColor Red
}

Write-Host ""

# Check 4: Analyze PATH for Python entries
Write-Host "[Check 4] Analyzing PATH for Python entries..." -ForegroundColor Yellow
Write-Host ""

$pathDirs = $env:Path -split ';' | Where-Object { $_ -and $_.Trim() }
$pythonPathDirs = @()

foreach ($dir in $pathDirs) {
    $trimmedDir = $dir.Trim()
    # Check if directory contains python.exe
    if (Test-Path (Join-Path $trimmedDir 'python.exe')) {
        $pythonPathDirs += $trimmedDir
    }
}

if ($pythonPathDirs.Count -gt 0) {
    Write-Host "  Found $($pythonPathDirs.Count) Python-related PATH entries:" -ForegroundColor Green
    Write-Host ""
    foreach ($pDir in $pythonPathDirs) {
        Write-Host "    [PYTHON] $pDir" -ForegroundColor Green
        
        # Count executables in this directory
        $exeCount = (Get-ChildItem -Path $pDir -Filter '*.exe' -ErrorAction SilentlyContinue).Count
        Write-Host "               Contains $exeCount executable(s)" -ForegroundColor Gray
    }
} else {
    Write-Host "  No Python directories found in PATH" -ForegroundColor Red
}

Write-Host ""

# Check 5: Show all PATH entries (verbose mode)
if ($ShowAllPaths) {
    Write-Host "[Verbose] Complete PATH directories:" -ForegroundColor Cyan
    Write-Host ""
    
    $i = 1
    foreach ($dir in $pathDirs) {
        $trimmedDir = $dir.Trim()
        $hasPython = Test-Path (Join-Path $trimmedDir 'python.exe')
        
        if ($hasPython) {
            Write-Host "  $i. [PYTHON] $trimmedDir" -ForegroundColor Green
        } else {
            Write-Host "  $i. $trimmedDir" -ForegroundColor Gray
        }
        $i++
    }
    
    Write-Host ""
    Write-Host "  Total PATH entries: $($pathDirs.Count)" -ForegroundColor Cyan
    Write-Host "  Python-related: $($pythonPathDirs.Count)" -ForegroundColor Green
    Write-Host ""
}

# Check 6: Common Python installation paths
Write-Host "[Check 5] Checking common Python installation paths..." -ForegroundColor Yellow
Write-Host ""

$commonPaths = @(
    @{Path='C:\Python*'; Label='C:\Python*'},
    @{Path="$env:LOCALAPPDATA\Programs\Python\*"; Label='LocalAppData\Programs\Python'},
    @{Path='C:\Program Files\Python*'; Label='Program Files\Python*'},
    @{Path='C:\Program Files (x86)\Python*'; Label='Program Files (x86)\Python*'}
)

$foundCommon = $false
foreach ($cp in $commonPaths) {
    $items = Get-Item -Path $cp.Path -ErrorAction SilentlyContinue
    if ($items) {
        $foundCommon = $true
        foreach ($item in $items) {
            $pythonExe = Join-Path $item.FullName 'python.exe'
            if (Test-Path $pythonExe) {
                $inPath = $pythonPathDirs -contains $item.FullName
                if ($inPath) {
                    Write-Host "  [$($cp.Label)] $($item.FullName) [IN PATH]" -ForegroundColor Green
                } else {
                    Write-Host "  [$($cp.Label)] $($item.FullName) [NOT IN PATH]" -ForegroundColor Yellow
                }
            }
        }
    }
}

if (-not $foundCommon) {
    Write-Host "  No common Python installations found" -ForegroundColor Red
}

Write-Host ""

# Summary
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "SUMMARY" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

$score = 0
$maxScore = 3

if ($pythonCmd) { $score++ }
if ($pythonPathDirs.Count -gt 0) { $score++ }
if ($pyCmd) { $score++ }

if ($score -eq $maxScore) {
    Write-Host "Python PATH Status: FULLY CONFIGURED" -ForegroundColor Green
    Write-Host "Python is properly configured in your PATH." -ForegroundColor Green
} elseif ($score -gt 0) {
    Write-Host "Python PATH Status: PARTIALLY CONFIGURED" -ForegroundColor Yellow
    Write-Host "Python is partially configured. Some commands may not work." -ForegroundColor Yellow
} else {
    Write-Host "Python PATH Status: NOT CONFIGURED" -ForegroundColor Red
    Write-Host "Python is not in your PATH. You need to add it." -ForegroundColor Red
}

Write-Host ""

# Provide fix suggestion
if (-not $pythonCmd -or $pythonPathDirs.Count -eq 0) {
    Write-Host "Recommended actions:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "1. Reinstall Python from https://www.python.org/downloads/" -ForegroundColor White
    Write-Host "   Make sure to check 'Add Python to PATH' during installation" -ForegroundColor Gray
    Write-Host ""
    Write-Host "2. Manually add Python to PATH (run as Administrator):" -ForegroundColor White
    Write-Host "   [Environment]::SetEnvironmentVariable('Path', `$env:Path + ';C:\Path\To\Python', 'Machine')" -ForegroundColor Gray
    Write-Host ""
    Write-Host "3. Use our tool to automatically add Python to PATH:" -ForegroundColor White
    Write-Host "   .\Add-Python-To-Path.ps1 -Permanent" -ForegroundColor Gray
    Write-Host ""
    
    if ($FixPath) {
        Write-Host "[AUTO-FIX] Attempting to add Python to PATH..." -ForegroundColor Cyan
        Write-Host ""
        
        # Run the add script
        $scriptPath = Join-Path $PSScriptRoot "Add-Python-To-Path.ps1"
        if (Test-Path $scriptPath) {
            & $scriptPath -Permanent
        } else {
            Write-Host "Error: Add-Python-To-Path.ps1 not found in same directory" -ForegroundColor Red
        }
    }
}

Write-Host "============================================================" -ForegroundColor Cyan
