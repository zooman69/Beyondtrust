@echo off
REM ===========================================================
REM BeyondTrust Daily Report - Fully Automated 5 AM Setup
REM ===========================================================
REM
REM This creates a Windows scheduled task that runs completely
REM automatically at 5:00 AM every day with NO interaction needed!
REM
REM What it does:
REM   - Downloads yesterday's report from BeyondTrust (no 2FA)
REM   - Generates beautiful HTML report
REM   - Sends desktop notification when ready
REM   - Zero interaction required from you!
REM ===========================================================

echo.
echo ============================================================
echo   BeyondTrust Fully Automated Daily Report Setup
echo ============================================================
echo.
echo This will set up COMPLETELY HANDS-FREE daily reports!
echo.
echo Schedule: Monday-Friday at 5:00 AM
echo.
echo What happens automatically:
echo   [1] Login to BeyondTrust (using zooman account - no 2FA)
echo   [2] Download yesterday's support session report
echo   [3] Clean the CSV data
echo   [4] Generate beautiful HTML report
echo   [5] Send you notification: "Report Ready!"
echo.
echo YOU DO NOTHING! Just wake up to your report ready.
echo.

pause

echo.
echo [STEP 1] Creating Windows scheduled task...
echo.

schtasks /Create /TN "BeyondTrustDailyReport5AM" /TR "python \"Y:\Coding\Beyondtrust\daily_report_automation.py\"" /SC WEEKLY /D MON,TUE,WED,THU,FRI /ST 05:00 /RL HIGHEST /F

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================================
    echo [SUCCESS] Fully Automated Daily Report is SET UP!
    echo ============================================================
    echo.
    echo Starting next weekday at 5:00 AM (Mon-Fri), you will get:
    echo   - Automatic download from BeyondTrust
    echo   - Automatic HTML report generation
    echo   - Desktop notification when ready
    echo   - ZERO interaction needed!
    echo.
    echo The report will be in your Downloads folder:
    echo   Daily-Support-Performance-Report-[DATE].html
    echo.
    echo ============================================================
    echo Task Management Commands:
    echo ============================================================
    echo.
    echo Run now to test:
    echo   schtasks /Run /TN BeyondTrustDailyReport5AM
    echo.
    echo View in Task Scheduler:
    echo   - Open "Task Scheduler"
    echo   - Look for: BeyondTrustDailyReport5AM
    echo.
    echo Disable temporarily:
    echo   schtasks /Change /TN BeyondTrustDailyReport5AM /DISABLE
    echo.
    echo Enable again:
    echo   schtasks /Change /TN BeyondTrustDailyReport5AM /ENABLE
    echo.
    echo Delete task:
    echo   schtasks /Delete /TN BeyondTrustDailyReport5AM /F
    echo.
    echo ============================================================
    echo.
    echo [TIP] Want to test it now? Run this command:
    echo   schtasks /Run /TN BeyondTrustDailyReport5AM
    echo.
) else (
    echo.
    echo ============================================================
    echo [ERROR] Failed to create scheduled task
    echo ============================================================
    echo.
    echo You may need Administrator privileges.
    echo.
    echo Try this:
    echo   1. Right-click this file
    echo   2. Select "Run as administrator"
    echo.
)

pause
