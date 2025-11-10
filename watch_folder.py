"""
Automatic Folder Watcher for Support Session Reports
====================================================
This script monitors a folder for new CSV files and automatically:
1. Cleans the CSV by removing unnecessary columns
2. Generates a formatted HTML report
3. Opens the report in your browser

Usage:
    python watch_folder.py [folder_path]

If no folder path is provided, it watches the Downloads folder by default.

To stop: Press Ctrl+C
"""

import os
import sys
import time
from pathlib import Path
from datetime import datetime
import subprocess

# Force output flushing for real-time display
sys.stdout.reconfigure(line_buffering=True)

# Import the report generation function
from auto_generate_report import clean_csv, generate_report

class FolderWatcher:
    def __init__(self, watch_folder):
        self.watch_folder = Path(watch_folder)
        self.processed_files = set()
        self.last_check_time = datetime.now()

        if not self.watch_folder.exists():
            raise ValueError(f"Folder does not exist: {watch_folder}")

        print(f"[WATCHING] Folder: {self.watch_folder}")
        print(f"[STARTED] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"\nWaiting for new CSV files...")
        print(f"(Press Ctrl+C to stop)\n")

        # Load existing files to avoid processing them
        self._load_existing_files()

    def _load_existing_files(self):
        """Mark all existing CSV files as already processed"""
        for file in self.watch_folder.glob("*.csv"):
            if not file.name.endswith("_cleaned.csv"):
                self.processed_files.add(str(file))

        if self.processed_files:
            print(f"[INFO] Ignoring {len(self.processed_files)} existing CSV files")
            print(f"       Only NEW files will be processed\n")

    def _is_support_session_file(self, file_path):
        """Check if file looks like a support session CSV"""
        # You can customize this logic
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

    def _process_file(self, file_path):
        """Process a CSV file and generate report"""
        try:
            print(f"\n{'='*60}")
            print(f"[NEW FILE] {file_path.name}")
            print(f"{'='*60}")

            # Give the file a moment to finish writing
            time.sleep(1)

            # Check if file is complete (not being written to)
            initial_size = file_path.stat().st_size
            time.sleep(0.5)
            final_size = file_path.stat().st_size

            if initial_size != final_size:
                print(f"[WAITING] File still being written...")
                time.sleep(2)

            # Run the report generation
            print(f"\n[PROCESSING] Cleaning and generating report...")

            # Clean CSV
            cleaned_file = clean_csv(str(file_path))
            print(f"   [OK] CSV cleaned")

            # Generate report
            report_file = generate_report(cleaned_file)

            if report_file:
                print(f"\n[SUCCESS] Report generated!")
                print(f"[FILE] {report_file}")
                print(f"\n[BROWSER] Opening report...")

                # Open in browser
                import webbrowser
                webbrowser.open(f'file:///{report_file}')

                print(f"\n{'='*60}")
                print(f"[COMPLETE] Processing finished!")
                print(f"{'='*60}\n")
                print(f"Waiting for next file...\n")
            else:
                print(f"\n[ERROR] Failed to generate report")

        except Exception as e:
            print(f"\n[ERROR] Error processing {file_path.name}: {e}")
            import traceback
            traceback.print_exc()

    def watch(self):
        """Main watch loop"""
        try:
            while True:
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

                        # Process the file
                        self._process_file(file)

                # Sleep for a bit before checking again
                time.sleep(2)

        except KeyboardInterrupt:
            print(f"\n\n{'='*60}")
            print(f"[STOPPED] Folder watcher stopped")
            print(f"[STATS] Processed {len([f for f in self.processed_files if not f.endswith('_cleaned.csv')])} files in this session")
            print(f"{'='*60}\n")
            sys.exit(0)

def main():
    print("=" * 60)
    print("Support Session Report - Automatic Folder Watcher")
    print("=" * 60)
    print()

    # Determine watch folder
    if len(sys.argv) > 1:
        watch_folder = sys.argv[1]
    else:
        # Default to Downloads folder
        watch_folder = str(Path.home() / "Downloads")

    try:
        watcher = FolderWatcher(watch_folder)
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
