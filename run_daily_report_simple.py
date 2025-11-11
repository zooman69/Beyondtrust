"""
One-Click Daily Report Runner (Simple Version)
===============================================
Processes the most recent Support-sessions CSV from your Downloads folder
for the previous business day.

No browser automation - assumes you've already downloaded the CSV or will
remind you to download it if not found.
"""

import sys
from datetime import datetime, timedelta
from pathlib import Path
import subprocess
import time


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


def find_recent_csv(downloads_dir, target_date):
    """Find the most recent Support-sessions CSV file"""
    # Look for Support-sessions CSV files
    csv_pattern = "Support-sessions*.csv"
    csv_files = list(downloads_dir.glob(csv_pattern))

    # Filter out _cleaned files
    csv_files = [f for f in csv_files if not f.name.endswith("_cleaned.csv")]

    if not csv_files:
        return None

    # Get the most recent file (by modification time)
    recent_csv = max(csv_files, key=lambda x: x.stat().st_mtime)

    # Check if it was modified today (within last 24 hours)
    file_age = time.time() - recent_csv.stat().st_mtime
    if file_age > 86400:  # More than 24 hours old
        return None

    return recent_csv


def main():
    print("=" * 70)
    print("ONE-CLICK DAILY REPORT (SIMPLE MODE)")
    print("=" * 70)
    print()

    # Get previous business day
    target_date = get_previous_business_day()
    date_str = target_date.strftime("%Y-%m-%d")
    day_name = target_date.strftime("%A, %B %d, %Y")

    print(f"Report date: {day_name}")
    print(f"Date: {date_str}")
    print()

    downloads_dir = Path.home() / "Downloads"

    # Look for recent CSV file
    print(f"Looking for CSV file in: {downloads_dir}")
    csv_file = find_recent_csv(downloads_dir, target_date)

    if not csv_file:
        print()
        print("⚠️  NO RECENT CSV FILE FOUND")
        print("=" * 70)
        print()
        print("Please download the report manually:")
        print()
        print("1. Go to: https://zengarinst.beyondtrustcloud.com")
        print("2. Navigate to Reports > Support Sessions")
        print(f"3. Select date: {date_str}")
        print("4. Download the CSV to your Downloads folder")
        print("5. Run this script again")
        print()
        input("Press Enter to exit...")
        sys.exit(1)

    print(f"✓ Found CSV: {csv_file.name}")
    print(f"  Modified: {datetime.fromtimestamp(csv_file.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Generate the report
    print("=" * 70)
    print("GENERATING REPORT")
    print("=" * 70)
    print()

    script_dir = Path(__file__).parent
    report_script = script_dir / "auto_generate_report.py"

    result = subprocess.run(
        [sys.executable, str(report_script), str(csv_file)],
        cwd=str(script_dir)
    )

    if result.returncode == 0:
        print()
        print("=" * 70)
        print("✓ SUCCESS - Report generated!")
        print("=" * 70)
    else:
        print()
        print("=" * 70)
        print("✗ FAILED - Could not generate report")
        print("=" * 70)
        sys.exit(1)


if __name__ == "__main__":
    main()
