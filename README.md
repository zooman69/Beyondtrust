# Support Session Report Auto-Generator

Automatically clean CSV files and generate formatted HTML reports for daily support performance.

## Quick Start

### Method 1: Drag and Drop (Easiest)

1. **Drag your CSV file** onto `process_support_report.bat`
2. The script will automatically:
   - Remove unnecessary columns (A, B, H, I, J, L, N, O, S, T, U, V)
   - Generate a formatted HTML report
   - Open the report in your browser
3. Done! Your report is ready.

### Method 2: Command Line

```bash
python auto_generate_report.py "path\to\your\Support-sessions.csv"
```

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

- `auto_generate_report.py` - Main Python script
- `process_support_report.bat` - Drag-and-drop batch file for Windows
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

- The script automatically detects the date from the CSV data
- Reports are color-coded: Red (Peak), Gray (Moderate), Blue (Quiet)
- Use the "Print PDF" button in the report to save as PDF
- Use the "Download HTML" button to save a standalone copy

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
