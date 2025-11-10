# BeyondTrust Report Automation System

Automatically process BeyondTrust support session CSV reports and generate formatted HTML reports with logging, notifications, and history tracking.

## Features

- **Automatic Folder Watching**: Monitors Downloads folder for new CSV files
- **Smart Processing**: Cleans CSV data and generates beautiful HTML reports
- **Desktop Notifications**: Get notified when reports are ready
- **Comprehensive Logging**: Track all processing activities
- **Processing History**: View dashboard with statistics and past reports
- **Auto-Start**: Set up to run automatically at Windows startup
- **Error Recovery**: Robust error handling and retry logic
- **BeyondTrust API Client**: Ready for future direct API integration

## Quick Start

### Method 1: Enhanced Folder Watcher (Recommended)

**Most robust option with logging, notifications, and history tracking!**

```bash
python enhanced_watch_folder.py
```

Or watch a specific folder:
```bash
python enhanced_watch_folder.py "C:\path\to\folder"
```

The enhanced watcher will:
- Monitor for new CSV files
- Process them automatically
- Send desktop notifications
- Log all activities
- Track processing history
- Handle errors gracefully

### Method 2: Basic Folder Watcher

**Simple option without extra features:**

1. **Double-click** `start_folder_watcher.bat`
2. Or run: `python watch_folder.py`

### Method 3: Drag and Drop (Quick One-Time Processing)

1. **Drag your CSV file** onto `process_support_report.bat`
2. Or run: `python auto_generate_report.py "path\to\Support-sessions.csv"`

**Perfect for:** Quick processing of a single report file.

## What It Does

### Step 1: CSV Cleanup
Removes these columns automatically:
- A: Session ID
- B: Session Sequence Number
- H: Jumpoint
- I: Jump Group
- J: External Key
- L: Customer's Private IP
- N: Representative's Public IP
- O: Representative's Private IP
- S: Additional Representatives
- T: # Files Transferred
- U: # Files Renamed
- V: # Files Deleted

### Step 2: Report Generation
Creates a professional HTML report with:
- **Summary Statistics**: Total sessions, top representatives, busiest hours
- **Staffing Recommendations**: Peak/Moderate/Quiet time blocks with agent recommendations
- **Hourly Chart**: Visual bar chart showing session distribution
- **Representative Performance**: Bar charts showing session counts and time involved
- **Detailed Staffing Table**: Time-by-time breakdown with volume badges

## Setup Automatic Startup

To have the folder watcher start automatically when Windows boots:

```bash
python setup_scheduler.py startup
```

This creates a Windows scheduled task that runs in the background.

### Manage the Scheduled Task

**Start the watcher now:**
```bash
schtasks /Run /TN BeyondTrustReportWatcher
```

**Stop the watcher:**
```bash
schtasks /End /TN BeyondTrustReportWatcher
```

**Remove scheduled task:**
```bash
python setup_scheduler.py remove
```

## View Processing Dashboard

See your processing history and statistics:

```bash
python view_dashboard.py
```

This creates an interactive HTML dashboard showing:
- Total reports processed
- Success/failure statistics
- Recent report history
- Quick links to view past reports

## Files

- `auto_generate_report.py` - Core report generation logic
- `enhanced_watch_folder.py` - **Enhanced folder watcher** with logging, notifications, and history
- `watch_folder.py` - Basic folder monitoring script (legacy)
- `setup_scheduler.py` - Set up automatic startup via Windows Task Scheduler
- `view_dashboard.py` - View processing history and statistics dashboard
- `beyondtrust_api.py` - BeyondTrust API client (OAuth authentication ready)
- `start_folder_watcher.bat` - Launches basic folder watcher
- `process_support_report.bat` - Drag-and-drop batch file
- `README.md` - This file

## Requirements

- Python 3.7+
- Windows (for scheduled tasks and notifications)
- HTML template at: `c:\Users\Zengar User\OneDrive - Zengar Institute Inc\Documents\Work\Templates\Daily-Support-Performance-Report-[DATE].html`

**Install Python dependencies:**
```bash
pip install requests
```

## Output Files

The enhanced system creates several files:

**Per CSV Report:**
1. `Support-sessions-YYYYMMDD-YYYYMMDD_cleaned.csv` - Cleaned CSV with columns removed
2. `Daily-Support-Performance-Report-YYYY-MM-DD.html` - Formatted HTML report

**System Files (in Downloads folder):**
3. `report_processing.log` - Detailed processing log
4. `processing_history.json` - JSON history of all processed reports
5. `report_dashboard.html` - Interactive statistics dashboard

## Example

```bash
# Input file
Support-sessions-20251107-20251108.csv

# Output files
Support-sessions-20251107-20251108_cleaned.csv
Daily-Support-Performance-Report-2025-11-07.html
```

## Notifications

Desktop notifications are sent when:
- ✅ Report generated successfully
- ❌ Report generation failed
- ⚠️ Processing error occurred

## Logs and History

All activity is logged to:
- `Downloads/report_processing.log` - Detailed processing log with timestamps
- `Downloads/processing_history.json` - JSON history of all processed reports
- View dashboard: `python view_dashboard.py`

## Tips

- **Folder Watcher**: Only processes NEW files that arrive after it starts. Existing CSV files are ignored.
- **File Detection**: Looks for files with "support" and "session" in the filename, or starting with "Support-sessions-"
- **Auto-Open**: Reports automatically open in your default browser when generated
- **Date Detection**: Script automatically detects the date from the CSV data
- **Color Coding**: Reports use Red (Peak), Gray (Moderate), Blue (Quiet)
- **PDF Export**: Use the "Print PDF" button in the report to save as PDF
- **Representative Filter**: Use the dropdown menu in the report to filter by specific tech
- **Background Running**: Enhanced watcher can run in the background via Task Scheduler
- **Error Recovery**: Enhanced watcher automatically retries on transient errors

## Troubleshooting

### Watcher not detecting files

1. Check if the file matches the pattern (contains "support" and "session" in filename)
2. Verify the folder path is correct
3. Check the log file: `Downloads/report_processing.log`

### Report not opening

1. Check if the HTML file was created in Downloads folder
2. Try opening manually from the Downloads folder
3. Check the log for errors: `Downloads/report_processing.log`

### Scheduled task not running

1. Open Task Scheduler (search in Windows)
2. Look for "BeyondTrustReportWatcher"
3. Check the "History" tab for errors
4. Try running manually: `schtasks /Run /TN BeyondTrustReportWatcher`

### Template file not found

- Make sure the HTML template exists at: `c:\Users\Zengar User\OneDrive - Zengar Institute Inc\Documents\Work\Templates\Daily-Support-Performance-Report-[DATE].html`
- Check that the template filename is exactly: `Daily-Support-Performance-Report-[DATE].html`

### No valid session data found

- Ensure your CSV has the correct column headers
- Check that the "Started" column contains valid dates

## Future Enhancements

- Direct API integration with BeyondTrust Reporting API (when available)
- Email notifications
- Report comparison (day-over-day trends)
- Custom report templates
- Multi-format export (PDF, Excel)
- Real-time analytics dashboard
