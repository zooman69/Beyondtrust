"""
Daily BeyondTrust Report Automation
===================================
Automatically downloads yesterday's report from BeyondTrust and generates HTML report.

This script is designed to run on a schedule (e.g., daily at 5 AM) to automatically:
1. Download yesterday's support session report from BeyondTrust (no 2FA required)
2. Clean the CSV data
3. Generate the HTML report
4. Send desktop notification

Requirements:
- Non-2FA credentials stored in .env file as BEYONDTRUST_AUTO_USERNAME and BEYONDTRUST_AUTO_PASSWORD

Usage:
    python daily_report_automation.py [date]

    If no date provided, downloads yesterday's report.

Examples:
    python daily_report_automation.py                # Yesterday's report
    python daily_report_automation.py 2025-11-05    # Specific date
"""

import os
import sys
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def send_notification(title, message):
    """Send Windows desktop notification"""
    try:
        ps_script = f'''
        [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
        [Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null

        $template = @"
        <toast>
            <visual>
                <binding template="ToastText02">
                    <text id="1">{title}</text>
                    <text id="2">{message}</text>
                </binding>
            </visual>
        </toast>
"@

        $xml = New-Object Windows.Data.Xml.Dom.XmlDocument
        $xml.LoadXml($template)
        $toast = [Windows.UI.Notifications.ToastNotification]::new($xml)
        [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("BeyondTrust Daily Report").Show($toast)
        '''

        subprocess.run(['powershell', '-Command', ps_script],
                      capture_output=True, timeout=5)
    except:
        pass


def main():
    print("=" * 60)
    print("BeyondTrust Daily Report Automation")
    print("=" * 60)
    print()

    # Determine target date
    if len(sys.argv) > 1:
        date_str = sys.argv[1]
    else:
        # Default to yesterday (previous day's report)
        yesterday = datetime.now() - timedelta(days=1)
        date_str = yesterday.strftime("%Y-%m-%d")

    print(f"Target date: {date_str}")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    script_dir = Path(__file__).parent
    downloads_dir = Path.home() / "Downloads"

    # Step 1: Download report from BeyondTrust
    print("[STEP 1] Downloading report from BeyondTrust...")
    print("-" * 60)

    download_script = script_dir / "auto_download_report.py"
    result = subprocess.run(
        [sys.executable, str(download_script), date_str],
        capture_output=False  # Show output in real-time
    )

    if result.returncode != 0:
        print("\n[FAILED] Could not download report from BeyondTrust")
        send_notification(
            "BeyondTrust Report Failed",
            f"Failed to download report for {date_str}"
        )
        sys.exit(1)

    print("\n[SUCCESS] Report downloaded!")
    print()

    # Step 2: Find the downloaded CSV
    print("[STEP 2] Looking for downloaded CSV file...")
    print("-" * 60)

    # Look for recently downloaded CSV files
    csv_pattern = f"Support-sessions-*.csv"
    csv_files = list(downloads_dir.glob(csv_pattern))

    # Filter to only files modified in the last 5 minutes
    recent_csv = None
    cutoff_time = time.time() - 300  # 5 minutes ago

    for csv_file in csv_files:
        if csv_file.name.endswith("_cleaned.csv"):
            continue
        if csv_file.stat().st_mtime > cutoff_time:
            recent_csv = csv_file
            break

    if not recent_csv:
        print("[ERROR] Could not find recently downloaded CSV file")
        send_notification(
            "BeyondTrust Report Failed",
            "Downloaded CSV file not found"
        )
        sys.exit(1)

    print(f"[FOUND] {recent_csv.name}")
    print()

    # Step 3: Generate HTML report
    print("[STEP 3] Generating HTML report...")
    print("-" * 60)

    report_script = script_dir / "auto_generate_report.py"
    result = subprocess.run(
        [sys.executable, str(report_script), str(recent_csv)],
        capture_output=False
    )

    if result.returncode != 0:
        print("\n[FAILED] Could not generate HTML report")
        send_notification(
            "BeyondTrust Report Failed",
            f"Failed to generate report for {date_str}"
        )
        sys.exit(1)

    print("\n[SUCCESS] HTML report generated!")
    print()

    # Find the generated HTML report
    html_files = list(downloads_dir.glob("Daily-Support-Performance-Report-*.html"))
    if html_files:
        # Get most recent
        latest_html = max(html_files, key=lambda x: x.stat().st_mtime)

        print("=" * 60)
        print("[COMPLETE] Daily report automation finished!")
        print("=" * 60)
        print(f"\nReport: {latest_html}")
        print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Send success notification
        send_notification(
            "BeyondTrust Report Ready",
            f"Report for {date_str} is ready to view"
        )
    else:
        print("[WARNING] HTML report file not found")

    print()


if __name__ == "__main__":
    main()
