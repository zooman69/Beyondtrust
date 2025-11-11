"""
One-Click Monthly Report Runner
================================
Runs BeyondTrust reports for the entire previous month (weekdays only).

Automatically calculates the previous month's date range and runs reports
for each business day (Monday-Friday).
"""

import sys
from datetime import datetime, timedelta
from pathlib import Path
import subprocess
import calendar


def get_previous_month_weekdays():
    """Get all weekdays from the previous month"""
    today = datetime.now()

    # Get first day of current month
    first_of_current_month = today.replace(day=1)

    # Get last day of previous month
    last_of_previous_month = first_of_current_month - timedelta(days=1)

    # Get first day of previous month
    first_of_previous_month = last_of_previous_month.replace(day=1)

    # Get all weekdays in the previous month
    weekdays = []
    current_day = first_of_previous_month

    while current_day <= last_of_previous_month:
        # Monday=0, Sunday=6
        if current_day.weekday() < 5:  # Monday through Friday
            weekdays.append(current_day)
        current_day += timedelta(days=1)

    return weekdays, first_of_previous_month, last_of_previous_month


def main():
    print("=" * 70)
    print("ONE-CLICK MONTHLY REPORT")
    print("=" * 70)
    print()

    # Get previous month's weekdays
    weekdays, month_start, month_end = get_previous_month_weekdays()

    month_name = month_start.strftime("%B %Y")

    print(f"Running reports for: {month_name}")
    print(f"Date range: {month_start.strftime('%Y-%m-%d')} to {month_end.strftime('%Y-%m-%d')}")
    print(f"Business days: {len(weekdays)}")
    print()

    # Confirm with user
    response = input(f"This will download and process {len(weekdays)} daily reports. Continue? (y/n): ")
    if response.lower() != 'y':
        print("Cancelled.")
        sys.exit(0)

    print()
    print("=" * 70)
    print()

    script_dir = Path(__file__).parent
    automation_script = script_dir / "daily_report_automation.py"

    successful = 0
    failed = 0

    # Process each weekday
    for i, day in enumerate(weekdays, 1):
        date_str = day.strftime("%Y-%m-%d")
        day_name = day.strftime("%A, %B %d")

        print(f"[{i}/{len(weekdays)}] Processing {day_name} ({date_str})...")
        print("-" * 70)

        result = subprocess.run(
            [sys.executable, str(automation_script), date_str],
            cwd=str(script_dir)
        )

        if result.returncode == 0:
            successful += 1
            print(f"✓ Success: {day_name}")
        else:
            failed += 1
            print(f"✗ Failed: {day_name}")

        print()

    # Summary
    print("=" * 70)
    print("MONTHLY REPORT SUMMARY")
    print("=" * 70)
    print(f"Month: {month_name}")
    print(f"Total business days: {len(weekdays)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print()

    if failed > 0:
        sys.exit(1)
    else:
        print("All reports completed successfully!")
        sys.exit(0)


if __name__ == "__main__":
    main()
