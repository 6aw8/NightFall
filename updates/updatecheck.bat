@echo off
setlocal enabledelayedexpansion

:: Set expected version
set "expected_version=0.1.0"

:: Temp file to store fetched version
set "temp_file=%temp%\version_check.txt"

:: Fetch version from URL using PowerShell
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/6aw8/Tool-Updates/refs/heads/master/version' -UseBasicParsing -OutFile '%temp_file%'"

:: Read the version from file
set /p fetched_version=<"%temp_file%"

:: Trim whitespace (optional)
for /f "tokens=* delims=" %%i in ("!fetched_version!") do set "fetched_version=%%i"

:: Compare versions
if "!fetched_version!"=="%expected_version%" (
    echo Checking Current Version...
    timeout /t 3 >nul
    echo [Updated] NightFall, Version: !fetched_version!
) else (
    echo Checking Current Version...
    timeout /t 3 >nul
    echo [Not Updated] NightFall, version: !expected_version!
    echo [CURRENT VERSION] NightFall, Version: !fetched_version!
)

:: Wait for 20 seconds before closing
timeout /t 20 >nul
endlocal
