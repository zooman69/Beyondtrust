"""
Automatic Support Session Report Generator
==========================================
This script automatically:
1. Cleans CSV files by removing specified columns (A, B, H, I, J, L, N, O, S, T, U, V)
2. Generates a formatted HTML report with statistics and charts
3. Opens the report in your browser

Usage:
    python auto_generate_report.py <path_to_csv_file>

Example:
    python auto_generate_report.py "C:\\Users\\YourName\\Downloads\\Support-sessions.csv"
"""

import csv
import sys
import os
from datetime import datetime
from collections import defaultdict
from pathlib import Path

def clean_csv(input_file):
    """Remove specified columns from CSV file"""
    print(f"Step 1: Cleaning CSV file...")

    # Columns to remove (0-indexed): A=0, B=1, H=7, I=8, J=9, L=11, N=13, O=14, S=18, T=19, U=20, V=21
    columns_to_remove = {0, 1, 7, 8, 9, 11, 13, 14, 18, 19, 20, 21}

    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        rows = list(reader)

    # Filter out the specified columns
    filtered_rows = []
    for row in rows:
        filtered_row = [col for idx, col in enumerate(row) if idx not in columns_to_remove]
        filtered_rows.append(filtered_row)

    # Create cleaned filename
    input_path = Path(input_file)
    cleaned_file = input_path.parent / f"{input_path.stem}_cleaned.csv"

    # Write cleaned CSV
    with open(cleaned_file, 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(filtered_rows)

    print(f"   [OK] Removed columns A, B, H, I, J, L, N, O, S, T, U, V")
    print(f"   [OK] Created: {cleaned_file}")

    return str(cleaned_file)

def generate_report(csv_file):
    """Generate HTML report from cleaned CSV file"""
    print(f"\nStep 2: Analyzing data and generating report...")

    # Read CSV data
    sessions = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('Started'):
                sessions.append(row)

    if not sessions:
        print("   [ERROR] No valid session data found in CSV")
        return None

    total_sessions = len(sessions)
    print(f"   [OK] Found {total_sessions} sessions")

    # Representative stats
    rep_counts = defaultdict(int)
    rep_time = defaultdict(int)
    for session in sessions:
        rep_name = session.get("Representative's Name", "Unknown")
        rep_counts[rep_name] += 1
        time_str = session.get("Representative's Time Involved", "")
        if time_str:
            parts = time_str.split(':')
            if len(parts) == 2:
                hours = int(parts[0])
                mins = int(parts[1])
                rep_time[rep_name] += hours * 60 + mins

    top_reps = sorted(rep_counts.items(), key=lambda x: x[1], reverse=True)[:5]

    # Hourly distribution
    hourly_counts = defaultdict(int)
    for session in sessions:
        started = session.get('Started', '')
        if started:
            dt = datetime.strptime(started.rsplit(' ', 1)[0], '%Y-%m-%d %H:%M:%S')
            hourly_counts[dt.hour] += 1

    # Extract date from first session
    first_session_date = datetime.strptime(sessions[0]['Started'].rsplit(' ', 1)[0], '%Y-%m-%d %H:%M:%S')
    report_date = first_session_date.strftime('%B %d, %Y')
    report_date_filename = first_session_date.strftime('%b-%d-%Y')  # Format: Nov-07-2025

    # Time block aggregation for staffing table
    time_blocks = {
        '07:00-08:00': hourly_counts[7],
        '08:00-09:00': hourly_counts[8],
        '09:00-10:00': hourly_counts[9],
        '10:00-11:00': hourly_counts[10],
        '11:00-12:00': hourly_counts[11],
        '12:00-13:00': hourly_counts[12],
        '13:00-14:00': hourly_counts[13],
        '14:00-15:00': hourly_counts[14],
        '15:00-17:00': hourly_counts[15] + hourly_counts[16],
        '17:00-19:00': hourly_counts[17] + hourly_counts[18]
    }

    # Find busiest hour
    if hourly_counts:
        busiest_hour = max(hourly_counts.items(), key=lambda x: x[1])
        busiest_hour_str = f'{busiest_hour[0]:02d}:00-{busiest_hour[0]+1:02d}:00'
    else:
        busiest_hour = (0, 0)
        busiest_hour_str = "N/A"

    # Classify time blocks
    counts = [c for c in time_blocks.values() if c > 0]
    counts.sort()
    if len(counts) >= 3:
        q33 = counts[len(counts) // 3]
        q67 = counts[2 * len(counts) // 3]
    else:
        q33 = 1
        q67 = 3

    peak_blocks = []
    moderate_blocks = []
    quiet_blocks = []

    for block, count in time_blocks.items():
        if count == 0:
            continue
        elif count > q67:
            peak_blocks.append(block)
        elif count > q33:
            moderate_blocks.append(block)
        else:
            quiet_blocks.append(block)

    # Find HTML template
    template_file = Path(r'c:\Users\Zengar User\OneDrive - Zengar Institute Inc\Documents\Work\Templates\Daily-Support-Performance-Report-[DATE].html')

    if not os.path.exists(template_file):
        print(f"   [ERROR] Template file not found at {template_file}")
        return None

    # Read HTML template
    with open(template_file, 'r', encoding='utf-8') as f:
        html = f.read()

    # Replace placeholders
    html = html.replace('[DATE]', report_date)
    html = html.replace('Daily-Support-Performance-Report-[DATE].html', f'Daily-Support-Performance-Report-{report_date_filename}.html')

    # Total Sessions
    html = html.replace('<div><span class="k">Total Sessions:</span> —</div>',
                       f'<div><span class="k">Total Sessions:</span> {total_sessions}</div>')

    # Top representatives
    top_reps_text = ', '.join([f'{rep} ({count})' for rep, count in top_reps[:3]])
    html = html.replace('<div style="margin-top:6px"><span class="k">Most Active Representatives:</span> —</div>',
                       f'<div style="margin-top:6px"><span class="k">Most Active Representatives:</span> {top_reps_text}</div>')

    # Busiest hour
    html = html.replace('<div style="margin-top:6px"><span class="k">Busiest Hour:</span> —</div>',
                       f'<div style="margin-top:6px"><span class="k">Busiest Hour:</span> {busiest_hour_str} ({busiest_hour[1]} sessions)</div>')

    # Time block recommendations
    if peak_blocks:
        peak_text = ', '.join(peak_blocks)
        html = html.replace('<span class="time-block peak">—</span>',
                           f'<span class="time-block peak">{peak_text}</span>')
    if moderate_blocks:
        moderate_text = ', '.join(moderate_blocks)
        html = html.replace('<span class="time-block moderate">—</span>',
                           f'<span class="time-block moderate">{moderate_text}</span>')
    if quiet_blocks:
        quiet_text = ', '.join(quiet_blocks)
        html = html.replace('<span class="time-block quiet">—</span>',
                           f'<span class="time-block quiet">{quiet_text}</span>')

    # Update staffing table rows
    for block, count in time_blocks.items():
        if count > 0:
            if count > q67:
                badge = 'Peak'
                badge_class = 'peak'
                staff = '4-5 agents' if count >= 5 else '3-4 agents'
                note = 'High volume period'
            elif count > q33:
                badge = 'Moderate'
                badge_class = 'moderate'
                staff = '2-3 agents'
                note = 'Baseline coverage'
            else:
                badge = 'Quiet'
                badge_class = 'quiet'
                staff = '1-2 agents'
                note = 'Good for breaks/training'

            old_row = f'<tr data-time="{block}">\n            <td>{block}</td>\n            <td class="session-count">—</td>\n            <td><span class="badge volume-badge">—</span></td>\n            <td class="staff-rec">—</td>\n            <td class="notes-cell">Awaiting data</td>'
            new_row = f'<tr data-time="{block}">\n            <td>{block}</td>\n            <td class="session-count">{count}</td>\n            <td><span class="badge {badge_class}">{badge}</span></td>\n            <td class="staff-rec">{staff}</td>\n            <td class="notes-cell">{note}</td>'
            html = html.replace(old_row, new_row)

    # Representative performance section
    rep_bars_html = ''
    max_sessions = max([count for _, count in top_reps]) if top_reps else 1
    for rep, count in top_reps:
        hours = rep_time[rep] // 60
        mins = rep_time[rep] % 60
        percent = (count / max_sessions) * 100
        color = '#ef4444' if count == max_sessions else '#2563eb'
        rep_bars_html += f'''
          <div class="row">
            <div style="font-weight:600">{rep}</div>
            <div class="bar"><span style="width:{percent}%;background:{color}"></span></div>
            <div style="text-align:right">{count}</div>
          </div>
          <div class="small" style="margin-bottom:8px">Time involved: {hours}h {mins}m</div>'''

    html = html.replace('<div class="empty">No representative session data provided.</div>', rep_bars_html)

    # Chart data - create SVG bars
    chart_svg = ''
    max_hourly = max(hourly_counts.values()) if hourly_counts else 1
    x_positions = [82, 122, 162, 202, 242, 282, 322, 362, 402, 442, 482, 508]
    hours = [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]

    for i, hour in enumerate(hours):
        count = hourly_counts[hour]
        if hour == 18:
            count += hourly_counts[19]
        if count > 0:
            height = (count / max_hourly) * 180
            y = 220 - height

            if count > q67:
                color = '#ef4444'
            elif count > q33:
                color = '#94a3b8'
            else:
                color = '#2563eb'

            chart_svg += f'<rect x="{x_positions[i]-15}" y="{y}" width="28" height="{height}" fill="{color}" rx="3"/>'

    html = html.replace('<text x="294" y="150" text-anchor="middle" class="empty">No hourly volume data</text>', chart_svg)

    # Update daily summary
    if len(top_reps) >= 3:
        summary_text = f'The support team completed <span class="k">{total_sessions} sessions</span> in total. Top performers were {top_reps[0][0]} with {top_reps[0][1]} sessions, {top_reps[1][0]} with {top_reps[1][1]} sessions, and {top_reps[2][0]} with {top_reps[2][1]} sessions.'
    else:
        summary_text = f'The support team completed <span class="k">{total_sessions} sessions</span> in total.'
    html = html.replace('The support team completed <span class="k">—</span> sessions in total. Top performers and busiest hours will appear once data is available.', summary_text)

    # Inject session data for filtering
    import json
    session_data = []
    for session in sessions:
        started = session.get('Started', '')
        if started:
            dt = datetime.strptime(started.rsplit(' ', 1)[0], '%Y-%m-%d %H:%M:%S')
            session_data.append({
                'rep': session.get("Representative's Name", "Unknown"),
                'hour': dt.hour,
                'started': started
            })

    # Inject data and populate dropdown
    reps_list = sorted(list(set([s['rep'] for s in session_data])))
    reps_options = '\n'.join([f'          <option value="{rep}">{rep}</option>' for rep in reps_list])

    html = html.replace('          <!-- Representative options will be populated by JavaScript -->',
                       reps_options)

    session_data_json = json.dumps(session_data)
    html = html.replace('let allSessionData = []; // Will be populated by the Python script',
                       f'let allSessionData = {session_data_json};')

    # Write output to Downloads folder
    csv_path = Path(csv_file)
    output_file = csv_path.parent / f'Daily-Support-Performance-Report-{report_date_filename}.html'

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"   [OK] Report generated successfully!")
    print(f"   [OK] Saved to: {output_file}")

    return str(output_file)

def main():
    print("=" * 60)
    print("Support Session Report Auto-Generator")
    print("=" * 60)

    if len(sys.argv) < 2:
        print("\nUsage: python auto_generate_report.py <csv_file>")
        print("\nExample:")
        print('  python auto_generate_report.py "C:\\Users\\...\\Support-sessions.csv"')
        sys.exit(1)

    input_file = sys.argv[1]

    if not os.path.exists(input_file):
        print(f"\n[ERROR] File not found: {input_file}")
        sys.exit(1)

    print(f"\nProcessing: {os.path.basename(input_file)}\n")

    try:
        # Step 1: Clean CSV
        cleaned_file = clean_csv(input_file)

        # Step 2: Generate Report
        report_file = generate_report(cleaned_file)

        if report_file:
            print("\n" + "=" * 60)
            print("[SUCCESS] Report generated and ready to view!")
            print("=" * 60)
            print(f"\nReport: {report_file}")

            # Ask if user wants to open
            print("\nOpening report in browser...")
            import webbrowser
            webbrowser.open(f'file:///{report_file}')
        else:
            print("\n[ERROR] Failed to generate report")
            sys.exit(1)

    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
