@echo off
REM Support Session Report Generator - Batch File
REM Drag and drop a CSV file onto this batch file to automatically clean and generate a report

echo ============================================================
echo Support Session Report Auto-Generator
echo ============================================================
echo.

if "%~1"=="" (
    echo Error: No file specified!
    echo.
    echo Usage: Drag and drop a CSV file onto this batch file
    echo.
    pause
    exit /b 1
)

echo Processing: %~nx1
echo.

python "c:\Beyondtrust\auto_generate_report.py" "%~1"

echo.
echo ============================================================
echo Press any key to close this window...
pause >nul
