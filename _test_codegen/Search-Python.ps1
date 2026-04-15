# Search-Python.ps1
# Tool to search for Python installations on Windows

Write-Host "Searching for Python installations..." -ForegroundColor Cyan
Write-Host ""

$pythonPaths = @()

# Search in PATH
Write-Host "[1/6] Checking PATH..." -ForegroundColor Yellow
$pathDirs = $env:Path -split ';' | Where-Object { $_ -and $_.Trim() }
foreach ($dir in $pathDirs) {
    $trimmedDir = $dir.Trim().TrimEnd('\')
    $pythonExe = Join-Path $trimmedDir 'python.exe'
    if (Test-Path $pythonExe) {
        $version = & $pythonExe --version 2>&1
        $pythonPaths += [PSCustomObject]@{
            Path = $pythonExe
            Version = $version -replace 'Python ', ''
            Source = 'PATH'
        }
        Write-Host "  Found: $pythonExe ($version)" -ForegroundColor Green
    }
}

# Search common installation locations
Write-Host "[2/6] Checking common installation locations..." -ForegroundColor Yellow

$searchLocations = @(
    'C:\Python*',
    'C:\Program Files\Python*',
    'C:\Program Files (x86)\Python*',
    "$env:LOCALAPPDATA\Programs\Python\*\*",
    "$env:APPDATA\Local\Programs\Python\*\*",
    'C:\ProgramData\Python*'
)

foreach ($location in $searchLocations) {
    $found = Get-ChildItem -Path $location -Filter 'python.exe' -Recurse -ErrorAction SilentlyContinue
    foreach ($exe in $found) {
        $fullPath = $exe.FullName
        if ($pythonPaths.Path -notcontains $fullPath) {
            $version = & $fullPath --version 2>&1
            $pythonPaths += [PSCustomObject]@{
                Path = $fullPath
                Version = $version -replace 'Python ', ''
                Source = 'File System'
            }
            Write-Host "  Found: $fullPath ($version)" -ForegroundColor Green
        }
    }
}

# Check Windows Store installations
Write-Host "[3/6] Checking Windows Store Python installations..." -ForegroundColor Yellow
$storePath = "$env:LOCALAPPDATA\Microsoft\WindowsApps\python.exe"
if (Test-Path $storePath) {
    $pythonPaths += [PSCustomObject]@{
        Path = $storePath
        Version = 'Windows Store (stub)'
        Source = 'Windows Store'
    }
    Write-Host "  Found: $storePath (Windows Store stub)" -ForegroundColor Yellow
}

# Check PowerShell commands
Write-Host "[4/6] Checking PowerShell command availability..." -ForegroundColor Yellow
$psPython = Get-Command python -ErrorAction SilentlyContinue
if ($psPython) {
    Write-Host "  PowerShell 'python' command: $($psPython.Source)" -ForegroundColor Green
} else {
    Write-Host "  PowerShell 'python' command: Not found" -ForegroundColor Red
}

$psPython3 = Get-Command python3 -ErrorAction SilentlyContinue
if ($psPython3) {
    Write-Host "  PowerShell 'python3' command: $($psPython3.Source)" -ForegroundColor Green
} else {
    Write-Host "  PowerShell 'python3' command: Not found" -ForegroundColor Red
}

# Check py launcher
Write-Host "[5/6] Checking Python Launcher (py.exe)..." -ForegroundColor Yellow
$pyLauncher = Get-Command py -ErrorAction SilentlyContinue
if ($pyLauncher) {
    Write-Host "  Python Launcher found: $($pyLauncher.Source)" -ForegroundColor Green
    Write-Host "  Installed Python versions:" -ForegroundColor Yellow
    & py --list 2>&1 | ForEach-Object { Write-Host "    $_" }
} else {
    Write-Host "  Python Launcher (py.exe): Not found" -ForegroundColor Red
}

# Check registry
Write-Host "[6/6] Checking Windows Registry..." -ForegroundColor Yellow
$regPaths = @(
    'HKLM:\SOFTWARE\Python\PythonCore\*\InstallPath',
    'HKCU:\SOFTWARE\Python\PythonCore\*\InstallPath',
    'HKLM:\SOFTWARE\WOW6432Node\Python\PythonCore\*\InstallPath'
)

foreach ($regPath in $regPaths) {
    $resolved = Get-Item -Path $regPath -ErrorAction SilentlyContinue
    if ($resolved) {
        $installPath = Join-Path $resolved.PSPath 'python.exe' | Split-Path | Join-Path -ChildPath 'python.exe'
        $versionKey = $resolved.PSPath.Split('\')[-2]
        if ($pythonPaths.Path -notcontains $installPath) {
            $pythonPaths += [PSCustomObject]@{
                Path = $installPath
                Version = $versionKey
                Source = 'Registry'
            }
            Write-Host "  Registry: $installPath (Python $versionKey)" -ForegroundColor Green
        }
    }
}

# Summary
Write-Host ""
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host "SUMMARY" -ForegroundColor Cyan
Write-Host "=" * 80 -ForegroundColor Cyan

if ($pythonPaths.Count -gt 0) {
    Write-Host "Found $($pythonPaths.Count) Python installation(s):" -ForegroundColor Green
    Write-Host ""
    $pythonPaths | Format-Table -AutoSize -Property @(
        @{Label='Version'; Expression={$_.Version}},
        @{Label='Path'; Expression={$_.Path}},
        @{Label='Source'; Expression={$_.Source}}
    )
} else {
    Write-Host "No Python installations found." -ForegroundColor Red
}
