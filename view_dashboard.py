"""
BeyondTrust Report Processing Dashboard
========================================
View processing history, statistics, and manage reports.

Usage:
    python view_dashboard.py [downloads_folder]
"""

import sys
import json
from pathlib import Path
from datetime import datetime
import webbrowser
import os


def load_history(folder):
    """Load processing history"""
    history_file = Path(folder) / "processing_history.json"
    if history_file.exists():
        with open(history_file, 'r') as f:
            return json.load(f)
    return []


def generate_dashboard_html(history, folder):
    """Generate HTML dashboard"""

    # Calculate statistics
    total = len(history)
    successful = sum(1 for r in history if r['status'] == 'success')
    failed = total - successful
    success_rate = (successful / total * 100) if total > 0 else 0

    # Get recent reports
    recent = sorted(history, key=lambda x: x.get('start_time', ''), reverse=True)[:10]

    # Generate HTML
    html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>BeyondTrust Report Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f7fa;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        h1 {{
            color: #1e293b;
            margin-bottom: 10px;
        }}
        .subtitle {{
            color: #64748b;
            margin-bottom: 30px;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        .stat-label {{
            color: #64748b;
            font-size: 14px;
            margin-bottom: 5px;
        }}
        .stat-value {{
            font-size: 32px;
            font-weight: 700;
            color: #1e293b;
        }}
        .stat-value.success {{
            color: #10b981;
        }}
        .stat-value.error {{
            color: #ef4444;
        }}
        .stat-value.rate {{
            color: #3b82f6;
        }}
        .section {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        h2 {{
            color: #1e293b;
            margin-bottom: 15px;
            font-size: 18px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th {{
            text-align: left;
            padding: 12px;
            background: #f8fafc;
            color: #475569;
            font-weight: 600;
            font-size: 14px;
        }}
        td {{
            padding: 12px;
            border-top: 1px solid #e2e8f0;
            font-size: 14px;
        }}
        .badge {{
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 600;
        }}
        .badge.success {{
            background: #d1fae5;
            color: #065f46;
        }}
        .badge.error {{
            background: #fee2e2;
            color: #991b1b;
        }}
        .btn {{
            display: inline-block;
            padding: 8px 16px;
            background: #3b82f6;
            color: white;
            text-decoration: none;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 500;
            transition: background 0.2s;
        }}
        .btn:hover {{
            background: #2563eb;
        }}
        .btn-small {{
            padding: 4px 8px;
            font-size: 12px;
        }}
        .empty {{
            text-align: center;
            padding: 40px;
            color: #94a3b8;
        }}
        .timestamp {{
            color: #64748b;
            font-size: 13px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>BeyondTrust Report Dashboard</h1>
        <div class="subtitle">Processing History & Statistics</div>

        <div class="stats">
            <div class="stat-card">
                <div class="stat-label">Total Reports Processed</div>
                <div class="stat-value">{total}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Successful</div>
                <div class="stat-value success">{successful}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Failed</div>
                <div class="stat-value error">{failed}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Success Rate</div>
                <div class="stat-value rate">{success_rate:.1f}%</div>
            </div>
        </div>

        <div class="section">
            <h2>Recent Reports</h2>
'''

    if recent:
        html += '''
            <table>
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>File</th>
                        <th>Status</th>
                        <th>Duration</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
'''
        for record in recent:
            start_time = datetime.fromisoformat(record['start_time'])
            duration = record.get('duration_seconds', 0)
            status_class = 'success' if record['status'] == 'success' else 'error'
            status_text = record['status'].upper()

            report_link = ''
            if record.get('report_file') and Path(record['report_file']).exists():
                report_file_path = Path(record['report_file'])
                report_link = f'<a href="file:///{record["report_file"]}" class="btn btn-small">View Report</a>'

            html += f'''
                    <tr>
                        <td class="timestamp">{start_time.strftime('%Y-%m-%d %H:%M:%S')}</td>
                        <td>{record['filename']}</td>
                        <td><span class="badge {status_class}">{status_text}</span></td>
                        <td>{duration:.1f}s</td>
                        <td>{report_link}</td>
                    </tr>
'''

        html += '''
                </tbody>
            </table>
'''
    else:
        html += '''
            <div class="empty">No reports processed yet</div>
'''

    html += f'''
        </div>

        <div class="section">
            <h2>Quick Actions</h2>
            <a href="file:///{folder}" class="btn">Open Downloads Folder</a>
        </div>

        <div class="section" style="font-size:13px;color:#64748b;">
            <strong>Watching folder:</strong> {folder}<br>
            <strong>Last updated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>
    </div>
</body>
</html>
'''

    return html


def main():
    print("=" * 60)
    print("BeyondTrust Report Dashboard")
    print("=" * 60)
    print()

    # Determine folder
    if len(sys.argv) > 1:
        folder = sys.argv[1]
    else:
        folder = str(Path.home() / "Downloads")

    folder = Path(folder)

    if not folder.exists():
        print(f"[ERROR] Folder not found: {folder}")
        sys.exit(1)

    print(f"Loading history from: {folder}")

    # Load history
    history = load_history(folder)
    print(f"Found {len(history)} records")

    # Generate dashboard
    print("Generating dashboard...")
    html = generate_dashboard_html(history, folder)

    # Save dashboard
    dashboard_file = folder / "report_dashboard.html"
    with open(dashboard_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Dashboard saved to: {dashboard_file}")
    print("\nOpening in browser...")

    # Open in browser
    webbrowser.open(f'file:///{dashboard_file}')

    print("[SUCCESS] Dashboard opened!")


if __name__ == "__main__":
    main()
