@echo off
REM Setup BeyondTrust Daily Report to run at 5:00 AM every day

echo ============================================================
echo BeyondTrust Daily Report - 5 AM Scheduler Setup
echo ============================================================
echo.
echo This will configure the daily report automation to run
echo automatically every day at 5:00 AM.
echo.
echo The automation will:
echo   1. Download yesterday's report from BeyondTrust
echo   2. Generate the HTML report
echo   3. Send you a notification when ready
echo.

pause

echo.
echo Creating scheduled task...
echo.

schtasks /Create /TN "BeyondTrustDailyReport5AM" /TR "python \"%~dp0daily_report_automation.py\"" /SC DAILY /ST 05:00 /RL HIGHEST /F

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================================
    echo [SUCCESS] Scheduled task created successfully!
    echo ============================================================
    echo.
    echo The daily report will run automatically at 5:00 AM every day.
    echo.
    echo Task Management:
    echo   - View task: Task Scheduler ^> BeyondTrustDailyReport5AM
    echo   - Run now:   schtasks /Run /TN BeyondTrustDailyReport5AM
    echo   - Disable:   schtasks /Change /TN BeyondTrustDailyReport5AM /DISABLE
    echo   - Enable:    schtasks /Change /TN BeyondTrustDailyReport5AM /ENABLE
    echo   - Delete:    schtasks /Delete /TN BeyondTrustDailyReport5AM /F
    echo.
) else (
    echo.
    echo [ERROR] Failed to create scheduled task
    echo.
    echo You may need to run this as Administrator.
    echo Right-click this file and select "Run as administrator"
    echo.
)

pause
