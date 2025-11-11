"""
Enhanced Automatic Folder Watcher for Support Session Reports
==============================================================
This script monitors a folder for new CSV files and automatically:
1. Cleans the CSV by removing unnecessary columns
2. Generates a formatted HTML report
3. Opens the report in your browser
4. Logs all activities
5. Sends desktop notifications

Features:
- Robust file detection with retry logic
- Comprehensive logging
- Desktop notifications
- Processing history tracking
- Better error handling

Usage:
    python enhanced_watch_folder.py [folder_path]

If no folder path is provided, it watches the Downloads folder by default.

To stop: Press Ctrl+C
"""

import os
import sys
import time
import logging
from pathlib import Path
from datetime import datetime
import subprocess
import json
from collections import defaultdict

# Force output flushing for real-time display
sys.stdout.reconfigure(line_buffering=True)

# Import the report generation function
from auto_generate_report import clean_csv, generate_report


class EnhancedFolderWatcher:
    def __init__(self, watch_folder, log_file=None):
        self.watch_folder = Path(watch_folder)
        self.processed_files = set()
        self.last_check_time = datetime.now()
        self.processing_history = []

        # Setup logging
        if log_file is None:
            log_file = self.watch_folder / "report_processing.log"

        self.log_file = Path(log_file)
        self._setup_logging()

        if not self.watch_folder.exists():
            raise ValueError(f"Folder does not exist: {watch_folder}")

        self.logger.info("="*60)
        self.logger.info("Enhanced Folder Watcher Started")
        self.logger.info("="*60)
        self.logger.info(f"Watching: {self.watch_folder}")
        self.logger.info(f"Log file: {self.log_file}")

        print(f"[WATCHING] Folder: {self.watch_folder}")
        print(f"[STARTED] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"[LOG FILE] {self.log_file}")
        print(f"\nWaiting for new CSV files...")
        print(f"(Press Ctrl+C to stop)\n")

        # Load existing files to avoid processing them
        self._load_existing_files()

        # Load processing history
        self._load_history()

    def _setup_logging(self):
        """Setup logging configuration"""
        self.logger = logging.getLogger('ReportWatcher')
        self.logger.setLevel(logging.INFO)

        # File handler
        fh = logging.FileHandler(self.log_file)
        fh.setLevel(logging.INFO)

        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def _load_history(self):
        """Load processing history from JSON file"""
        history_file = self.watch_folder / "processing_history.json"
        if history_file.exists():
            try:
                with open(history_file, 'r') as f:
                    self.processing_history = json.load(f)
                self.logger.info(f"Loaded {len(self.processing_history)} historical records")
            except Exception as e:
                self.logger.warning(f"Could not load history: {e}")
                self.processing_history = []
        else:
            self.processing_history = []

    def _save_history(self):
        """Save processing history to JSON file"""
        history_file = self.watch_folder / "processing_history.json"
        try:
            with open(history_file, 'w') as f:
                json.dump(self.processing_history, f, indent=2)
        except Exception as e:
            self.logger.error(f"Could not save history: {e}")

    def _load_existing_files(self):
        """Mark all existing CSV files as already processed"""
        for file in self.watch_folder.glob("*.csv"):
            if not file.name.endswith("_cleaned.csv"):
                self.processed_files.add(str(file))

        if self.processed_files:
            self.logger.info(f"Ignoring {len(self.processed_files)} existing CSV files")
            print(f"[INFO] Ignoring {len(self.processed_files)} existing CSV files")
            print(f"       Only NEW files will be processed\n")

    def _is_support_session_file(self, file_path):
        """Check if file looks like a support session CSV"""
        filename = file_path.name.lower()

        # Skip already cleaned files
        if filename.endswith("_cleaned.csv"):
            return False

        # Look for support session patterns
        if "support" in filename and "session" in filename:
            return True

        # Check if it starts with "Support-sessions-"
        if filename.startswith("support-sessions-"):
            return True

        return False

    def _send_notification(self, title, message, success=True):
        """Send desktop notification (Windows)"""
        try:
            # Windows notification using PowerShell
            if sys.platform == 'win32':
                # Escape quotes in message
                message = message.replace('"', '`"')
                title = title.replace('"', '`"')

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
                [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("BeyondTrust Report Processor").Show($toast)
                '''

                subprocess.run(['powershell', '-Command', ps_script],
                             capture_output=True, timeout=5)
        except Exception as e:
            self.logger.debug(f"Notification failed: {e}")

    def _wait_for_file_complete(self, file_path, max_wait=30):
        """Wait for file to finish writing"""
        self.logger.info(f"Waiting for file to complete: {file_path.name}")

        for i in range(max_wait):
            try:
                initial_size = file_path.stat().st_size
                time.sleep(0.5)
                final_size = file_path.stat().st_size

                if initial_size == final_size and final_size > 0:
                    self.logger.info(f"File complete ({final_size} bytes)")
                    return True

                if i % 4 == 0:  # Every 2 seconds
                    self.logger.debug(f"Still waiting... ({initial_size} -> {final_size} bytes)")

            except Exception as e:
                self.logger.warning(f"Error checking file: {e}")
                time.sleep(0.5)

        self.logger.warning(f"File may still be writing after {max_wait/2}s")
        return False

    def _process_file(self, file_path):
        """Process a CSV file and generate report"""
        start_time = datetime.now()
        record = {
            'file': str(file_path),
            'filename': file_path.name,
            'start_time': start_time.isoformat(),
            'status': 'failed',
            'error': None,
            'report_file': None
        }

        try:
            self.logger.info("="*60)
            self.logger.info(f"NEW FILE DETECTED: {file_path.name}")
            self.logger.info("="*60)

            print(f"\n{'='*60}")
            print(f"[NEW FILE] {file_path.name}")
            print(f"{'='*60}")

            # Wait for file to finish writing
            if not self._wait_for_file_complete(file_path):
                self.logger.warning("Proceeding anyway...")

            # Run the report generation
            self.logger.info("Starting report generation...")
            print(f"\n[PROCESSING] Cleaning and generating report...")

            # Clean CSV
            self.logger.info("Step 1: Cleaning CSV...")
            cleaned_file = clean_csv(str(file_path))
            self.logger.info(f"CSV cleaned: {cleaned_file}")
            print(f"   [OK] CSV cleaned")

            # Generate report
            self.logger.info("Step 2: Generating HTML report...")
            report_file = generate_report(cleaned_file)

            if report_file:
                record['status'] = 'success'
                record['report_file'] = report_file
                record['end_time'] = datetime.now().isoformat()
                record['duration_seconds'] = (datetime.now() - start_time).total_seconds()

                self.logger.info(f"SUCCESS: Report generated at {report_file}")
                print(f"\n[SUCCESS] Report generated!")
                print(f"[FILE] {report_file}")
                print(f"\n[BROWSER] Opening report...")

                # Open in browser
                import webbrowser
                webbrowser.open(f'file:///{report_file}')

                # Send notification
                self._send_notification(
                    "Report Generated Successfully",
                    f"Generated: {Path(report_file).name}",
                    success=True
                )

                print(f"\n{'='*60}")
                print(f"[COMPLETE] Processing finished in {record['duration_seconds']:.1f}s")
                print(f"{'='*60}\n")
                print(f"Waiting for next file...\n")
            else:
                record['error'] = "Failed to generate report"
                self.logger.error("Failed to generate report")
                print(f"\n[ERROR] Failed to generate report")

                self._send_notification(
                    "Report Generation Failed",
                    f"Failed to process {file_path.name}",
                    success=False
                )

        except Exception as e:
            record['status'] = 'error'
            record['error'] = str(e)
            record['end_time'] = datetime.now().isoformat()

            self.logger.error(f"Error processing {file_path.name}: {e}", exc_info=True)
            print(f"\n[ERROR] Error processing {file_path.name}: {e}")

            self._send_notification(
                "Report Processing Error",
                f"Error: {str(e)[:100]}",
                success=False
            )

        finally:
            # Save to history
            self.processing_history.append(record)
            self._save_history()

    def get_statistics(self):
        """Get processing statistics"""
        if not self.processing_history:
            return None

        total = len(self.processing_history)
        successful = sum(1 for r in self.processing_history if r['status'] == 'success')
        failed = total - successful

        return {
            'total_processed': total,
            'successful': successful,
            'failed': failed,
            'success_rate': (successful / total * 100) if total > 0 else 0
        }

    def watch(self):
        """Main watch loop"""
        try:
            check_count = 0
            while True:
                check_count += 1

                # Check for new CSV files
                for file in self.watch_folder.glob("*.csv"):
                    file_str = str(file)

                    # Skip if already processed
                    if file_str in self.processed_files:
                        continue

                    # Skip if it's a cleaned file
                    if file.name.endswith("_cleaned.csv"):
                        continue

                    # Check if it's a support session file
                    if self._is_support_session_file(file):
                        # Mark as processed immediately to avoid double-processing
                        self.processed_files.add(file_str)
                        self.logger.info(f"Adding to processing queue: {file.name}")

                        # Process the file
                        self._process_file(file)

                # Log heartbeat every 5 minutes
                if check_count % 150 == 0:  # 150 * 2 seconds = 5 minutes
                    self.logger.debug(f"Heartbeat - Still watching ({check_count} checks)")

                # Sleep for a bit before checking again
                time.sleep(2)

        except KeyboardInterrupt:
            self._shutdown()

    def _shutdown(self):
        """Graceful shutdown"""
        self.logger.info("="*60)
        self.logger.info("Folder Watcher Stopping...")
        self.logger.info("="*60)

        stats = self.get_statistics()
        if stats:
            self.logger.info(f"Session Statistics:")
            self.logger.info(f"  Total Processed: {stats['total_processed']}")
            self.logger.info(f"  Successful: {stats['successful']}")
            self.logger.info(f"  Failed: {stats['failed']}")
            self.logger.info(f"  Success Rate: {stats['success_rate']:.1f}%")

        self.logger.info("Shutdown complete")

        print(f"\n\n{'='*60}")
        print(f"[STOPPED] Folder watcher stopped")
        if stats:
            print(f"[STATS] Processed {stats['total_processed']} files ({stats['successful']} successful)")
        print(f"{'='*60}\n")
        sys.exit(0)


def main():
    print("=" * 60)
    print("Enhanced Support Session Report - Automatic Folder Watcher")
    print("=" * 60)
    print()

    # Determine watch folder
    if len(sys.argv) > 1:
        watch_folder = sys.argv[1]
    else:
        # Default to Downloads folder
        watch_folder = str(Path.home() / "Downloads")

    try:
        watcher = EnhancedFolderWatcher(watch_folder)
        watcher.watch()
    except ValueError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
