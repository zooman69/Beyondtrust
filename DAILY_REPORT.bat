@echo off
REM ============================================
REM ONE-CLICK DAILY REPORT
REM ============================================
REM Automatically runs yesterday's report
REM (or Friday's report if today is Monday)
REM ============================================

echo.
echo ====================================
echo   BEYONDTRUST DAILY REPORT
echo ====================================
echo.

REM Run the daily report script (simple version - process downloaded CSV)
python "%~dp0run_daily_report_simple.py"

REM Pause to show results
echo.
echo.
pause
