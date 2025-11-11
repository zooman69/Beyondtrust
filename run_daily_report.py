"""
One-Click Daily Report Runner
==============================
Runs the BeyondTrust report for the previous business day (skips weekends).

If today is Monday, it runs Friday's report.
Otherwise, it runs yesterday's report.
"""

import sys
from datetime import datetime, timedelta
from pathlib import Path
import subprocess


def get_previous_business_day():
    """Get the previous business day (skip weekends)"""
    today = datetime.now()

    # If today is Monday (0), go back 3 days to Friday
    if today.weekday() == 0:
        previous_day = today - timedelta(days=3)
    # If today is Sunday (6), go back 2 days to Friday
    elif today.weekday() == 6:
        previous_day = today - timedelta(days=2)
    # Otherwise, just go back 1 day
    else:
        previous_day = today - timedelta(days=1)

    return previous_day


def main():
    print("=" * 70)
    print("ONE-CLICK DAILY REPORT")
    print("=" * 70)
    print()

    # Get previous business day
    target_date = get_previous_business_day()
    date_str = target_date.strftime("%Y-%m-%d")
    day_name = target_date.strftime("%A, %B %d, %Y")

    print(f"Running report for: {day_name}")
    print(f"Date: {date_str}")
    print()

    # Run the daily automation script
    script_dir = Path(__file__).parent
    automation_script = script_dir / "daily_report_automation.py"

    result = subprocess.run(
        [sys.executable, str(automation_script), date_str],
        cwd=str(script_dir)
    )

    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
