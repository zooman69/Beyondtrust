# Support Session Report Auto-Generator

Automatically clean CSV files and generate formatted HTML reports for daily support performance.

## Quick Start

### Method 1: Automatic Folder Watcher (Best for Regular Use)

**Set it and forget it!** The folder watcher automatically processes new CSV files as they appear.

1. **Double-click** `start_folder_watcher.bat`
2. The watcher starts monitoring your Downloads folder
3. When you download a new support session CSV, it will automatically:
   - Detect the new file
   - Clean the CSV (remove unnecessary columns)
   - Generate the HTML report
   - Open the report in your browser
4. Leave it running all day - it will process files as they arrive
5. Press **Ctrl+C** to stop the watcher

**Perfect for:** Processing multiple reports throughout the day without manual intervention.

### Method 2: Drag and Drop (Quick One-Time Processing)

1. **Drag your CSV file** onto `process_support_report.bat`
2. The script will automatically:
   - Remove unnecessary columns (A, B, H, I, J, L, N, O, S, T, U, V)
   - Generate a formatted HTML report
   - Open the report in your browser
3. Done! Your report is ready.

**Perfect for:** Quick processing of a single report file.

### Method 3: Command Line

```bash
python auto_generate_report.py "path\to\your\Support-sessions.csv"
```

**Perfect for:** Automation scripts or custom workflows.

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

## Files

- `auto_generate_report.py` - Main Python script for processing CSV and generating reports
- `watch_folder.py` - Automatic folder monitoring script
- `start_folder_watcher.bat` - Launches the folder watcher (double-click to start)
- `process_support_report.bat` - Drag-and-drop batch file for one-time processing
- `README.md` - This file

## Requirements

- Python 3.x
- HTML template at: `c:\Users\Zengar User\OneDrive - Zengar Institute Inc\Documents\Work\Templates\Daily-Support-Performance-Report-[DATE].html`

## Output Files

The script creates two files in the same folder as your input CSV:

1. `Support-sessions-YYYYMMDD-YYYYMMDD_cleaned.csv` - Cleaned CSV with columns removed
2. `Daily-Support-Performance-Report-YYYY-MM-DD.html` - Formatted HTML report

## Example

```bash
# Input file
Support-sessions-20251107-20251108.csv

# Output files
Support-sessions-20251107-20251108_cleaned.csv
Daily-Support-Performance-Report-2025-11-07.html
```

## Tips

- **Folder Watcher**: The folder watcher only processes NEW files that arrive after it starts. Existing CSV files in the folder are ignored.
- **File Detection**: The watcher looks for files with "support" and "session" in the filename, or files starting with "Support-sessions-"
- **Auto-Open**: Reports automatically open in your default browser when generated
- The script automatically detects the date from the CSV data
- Reports are color-coded: Red (Peak), Gray (Moderate), Blue (Quiet)
- Use the "Print PDF" button in the report to save as PDF
- Use the "Download HTML" button to save a standalone copy
- **Representative Filter**: Use the dropdown menu in the report to filter by specific tech or view all representatives

## Troubleshooting

**Error: Template file not found**
- Make sure the HTML template exists at the path specified above
- Check that the template filename is exactly: `Daily-Support-Performance-Report-[DATE].html`

**Error: No valid session data found**
- Ensure your CSV has the correct column headers
- Check that the "Started" column contains valid dates

**Script doesn't run**
- Make sure Python is installed and in your PATH
- Try running from command line to see detailed error messages
