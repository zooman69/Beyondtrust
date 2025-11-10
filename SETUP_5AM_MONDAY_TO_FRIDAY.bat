@echo off
REM ===========================================================
REM BeyondTrust Daily Report - 5 AM Setup (Monday-Friday)
REM ===========================================================
REM
REM RIGHT-CLICK THIS FILE AND SELECT "RUN AS ADMINISTRATOR"
REM
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

python "Y:\Coding\Beyondtrust\setup_5am_task.py"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================================
    echo [SUCCESS] Setup Complete!
    echo ============================================================
    echo.
) else (
    echo.
    echo ============================================================
    echo [ERROR] Setup Failed
    echo ============================================================
    echo.
    echo Please right-click this file and select "Run as administrator"
    echo.
)

pause
