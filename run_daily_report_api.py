"""
One-Click Daily Report Runner (API Version)
============================================
Uses BeyondTrust API to download session data and generate reports.
100% automated - no browser, no manual downloads.
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
    print("ONE-CLICK DAILY REPORT (API VERSION)")
    print("=" * 70)
    print()

    # Get previous business day
    target_date = get_previous_business_day()
    date_str = target_date.strftime("%Y-%m-%d")
    day_name = target_date.strftime("%A, %B %d, %Y")

    print(f"Report date: {day_name}")
    print(f"Date: {date_str}")
    print()

    script_dir = Path(__file__).parent

    # Step 1: Download via API
    print("=" * 70)
    print("STEP 1: DOWNLOADING VIA API")
    print("=" * 70)
    print()

    api_script = script_dir / "api_download_sessions.py"
    result = subprocess.run(
        [sys.executable, str(api_script), date_str],
        cwd=str(script_dir),
        capture_output=True,
        text=True
    )

    print(result.stdout)

    if result.returncode != 0:
        print(result.stderr)
        print()
        print("=" * 70)
        print("✗ FAILED - Could not download via API")
        print("=" * 70)
        input("Press Enter to exit...")
        sys.exit(1)

    # Find the downloaded CSV
    downloads_dir = Path.home() / "Downloads"
    date_str_compact = date_str.replace("-", "")
    csv_file = downloads_dir / f"Support-sessions-{date_str_compact}-{date_str_compact}.csv"

    if not csv_file.exists():
        print(f"✗ Could not find downloaded CSV: {csv_file}")
        input("Press Enter to exit...")
        sys.exit(1)

    # Step 2: Generate report
    print()
    print("=" * 70)
    print("STEP 2: GENERATING HTML REPORT")
    print("=" * 70)
    print()

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
