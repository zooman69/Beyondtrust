"""
One-Click Monthly Report Runner (API Version)
==============================================
Uses BeyondTrust API to download all weekday session data for the previous month.
100% automated - no browser, no manual downloads.
"""

import sys
from datetime import datetime, timedelta
from pathlib import Path
import subprocess


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
    print("ONE-CLICK MONTHLY REPORT (API VERSION)")
    print("=" * 70)
    print()

    # Get previous month's weekdays
    weekdays, month_start, month_end = get_previous_month_weekdays()

    month_name = month_start.strftime("%B %Y")

    print(f"Report month: {month_name}")
    print(f"Date range: {month_start.strftime('%Y-%m-%d')} to {month_end.strftime('%Y-%m-%d')}")
    print(f"Business days: {len(weekdays)}")
    print()

    # Confirm with user
    response = input(f"Download and process {len(weekdays)} reports via API? (y/n): ")
    if response.lower() != 'y':
        print("Cancelled.")
        sys.exit(0)

    print()
    print("=" * 70)
    print()

    script_dir = Path(__file__).parent
    api_script = script_dir / "api_download_sessions.py"
    report_script = script_dir / "auto_generate_report.py"
    downloads_dir = Path.home() / "Downloads"

    successful = 0
    failed = 0

    # Process each weekday
    for i, day in enumerate(weekdays, 1):
        date_str = day.strftime("%Y-%m-%d")
        day_name = day.strftime("%A, %B %d")

        print(f"[{i}/{len(weekdays)}] Processing {day_name} ({date_str})...")
        print("-" * 70)

        # Download via API
        result = subprocess.run(
            [sys.executable, str(api_script), date_str],
            cwd=str(script_dir),
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print(f"✗ API Download Failed: {day_name}")
            print(result.stderr)
            failed += 1
            print()
            continue

        # Find the CSV file
        date_str_compact = date_str.replace("-", "")
        csv_file = downloads_dir / f"Support-sessions-{date_str_compact}-{date_str_compact}.csv"

        if not csv_file.exists():
            print(f"✗ CSV Not Found: {day_name}")
            failed += 1
            print()
            continue

        # Generate report
        result = subprocess.run(
            [sys.executable, str(report_script), str(csv_file)],
            cwd=str(script_dir),
            capture_output=True
        )

        if result.returncode == 0:
            successful += 1
            print(f"✓ Success: {day_name}")
        else:
            failed += 1
            print(f"✗ Report Failed: {day_name}")

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
        print("✓ All reports completed successfully!")
        sys.exit(0)


if __name__ == "__main__":
    main()
