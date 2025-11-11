@echo off
REM ============================================
REM ONE-CLICK MONTHLY REPORT
REM ============================================
REM Automatically runs reports for all weekdays
REM in the previous month
REM ============================================

echo.
echo ====================================
echo   BEYONDTRUST MONTHLY REPORT
echo ====================================
echo.

REM Run the monthly report script (simple version - process downloaded CSVs)
python "%~dp0run_monthly_report_simple.py"

REM Pause to show results
echo.
echo.
pause
