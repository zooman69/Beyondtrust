@echo off
REM Folder Watcher Launcher
REM This will monitor your Downloads folder for new CSV files and automatically process them

echo ============================================================
echo Support Session Report - Folder Watcher
echo ============================================================
echo.
echo This will monitor your Downloads folder for new CSV files.
echo When a new support session CSV is detected, it will:
echo   1. Clean the CSV (remove unnecessary columns)
echo   2. Generate an HTML report
echo   3. Open the report in your browser
echo.
echo Press Ctrl+C to stop watching
echo ============================================================
echo.

REM Run the folder watcher
python "%~dp0watch_folder.py"

pause
