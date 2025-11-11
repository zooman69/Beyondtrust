@echo off
REM Start Enhanced BeyondTrust Report Watcher
REM Monitors Downloads folder and automatically processes new CSV reports

echo ============================================================
echo BeyondTrust Enhanced Report Watcher
echo ============================================================
echo.
echo Starting folder watcher with:
echo - Desktop notifications
echo - Activity logging
echo - Processing history tracking
echo - Error recovery
echo.
echo Press Ctrl+C to stop the watcher
echo ============================================================
echo.

python "%~dp0enhanced_watch_folder.py"

pause
