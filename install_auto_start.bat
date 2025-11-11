@echo off
REM Install BeyondTrust Report Watcher to start automatically at Windows boot

echo ============================================================
echo BeyondTrust Report Watcher - Auto-Start Installation
echo ============================================================
echo.
echo This will configure the report watcher to start automatically
echo when Windows boots.
echo.
echo The watcher will run in the background and process new
echo BeyondTrust CSV reports as they appear in your Downloads folder.
echo.

pause

echo.
echo Installing scheduled task...
echo.

python "%~dp0setup_scheduler.py" startup

echo.
pause
