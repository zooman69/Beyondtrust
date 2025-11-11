"""
One-Click Monthly Report Runner (Simple Version)
=================================================
Processes CSV files for all business days in the previous month.

Assumes you will download the CSVs manually for each day, or processes
existing CSVs if they're already in your Downloads folder.
"""

import sys
from datetime import datetime, timedelta
from pathlib import Path
import subprocess
import time


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
    print("ONE-CLICK MONTHLY REPORT (SIMPLE MODE)")
    print("=" * 70)
    print()

    # Get previous month's weekdays
    weekdays, month_start, month_end = get_previous_month_weekdays()

    month_name = month_start.strftime("%B %Y")

    print(f"Report month: {month_name}")
    print(f"Date range: {month_start.strftime('%Y-%m-%d')} to {month_end.strftime('%Y-%m-%d')}")
    print(f"Business days: {len(weekdays)}")
    print()

    print("⚠️  MANUAL DOWNLOAD REQUIRED")
    print("=" * 70)
    print()
    print(f"This tool requires you to manually download CSV files for each day.")
    print(f"You will need to download {len(weekdays)} CSV files from BeyondTrust.")
    print()
    print("Instructions:")
    print("1. Go to: https://zengarinst.beyondtrustcloud.com")
    print("2. Navigate to Reports > Support Sessions")
    print("3. For each date below, download the CSV to Downloads folder:")
    print()

    for i, day in enumerate(weekdays, 1):
        print(f"   {i:2d}. {day.strftime('%A, %B %d, %Y')} ({day.strftime('%Y-%m-%d')})")

    print()
    print("4. After downloading all files, re-run this script to process them")
    print()
    print("=" * 70)
    print()

    response = input("Have you downloaded all CSV files? (y/n): ")
    if response.lower() != 'y':
        print("Cancelled. Download the files and run again.")
        sys.exit(0)

    print()
    print("=" * 70)
    print("PROCESSING REPORTS")
    print("=" * 70)
    print()

    downloads_dir = Path.home() / "Downloads"
    script_dir = Path(__file__).parent
    report_script = script_dir / "auto_generate_report.py"

    successful = 0
    failed = 0
    skipped = 0

    # Look for all CSV files
    csv_files = list(downloads_dir.glob("Support-sessions*.csv"))
    csv_files = [f for f in csv_files if not f.name.endswith("_cleaned.csv")]

    if not csv_files:
        print("✗ No CSV files found in Downloads folder!")
        print(f"  Location: {downloads_dir}")
        sys.exit(1)

    print(f"Found {len(csv_files)} CSV file(s) in Downloads folder")
    print()

    for csv_file in csv_files:
        print(f"Processing: {csv_file.name}")
        print("-" * 70)

        result = subprocess.run(
            [sys.executable, str(report_script), str(csv_file)],
            cwd=str(script_dir),
            capture_output=True
        )

        if result.returncode == 0:
            successful += 1
            print(f"✓ Success")
        else:
            failed += 1
            print(f"✗ Failed")

        print()

    # Summary
    print("=" * 70)
    print("MONTHLY REPORT SUMMARY")
    print("=" * 70)
    print(f"Month: {month_name}")
    print(f"CSV files processed: {len(csv_files)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print()

    if failed > 0:
        print("⚠️  Some reports failed to generate. Check the errors above.")
        sys.exit(1)
    else:
        print("✓ All reports completed successfully!")
        print(f"  Reports saved to: {downloads_dir}")
        sys.exit(0)


if __name__ == "__main__":
    main()
