"""
BeyondTrust API Session Downloader
===================================
Downloads support session data via BeyondTrust API and saves as CSV.

This replaces browser automation with direct API calls.
"""

import csv
import sys
from datetime import datetime, timedelta
from pathlib import Path
from beyondtrust_api import BeyondTrustAPI
import xml.etree.ElementTree as ET


def parse_xml_sessions(xml_data):
    """Parse BeyondTrust XML session data"""
    print("[XML] Parsing session data from XML response...")

    try:
        root = ET.fromstring(xml_data)
        sessions = []

        # BeyondTrust typically uses <session> or <item> tags
        # We'll search for common patterns
        session_elements = root.findall('.//session') or root.findall('.//item') or root.findall('.//record')

        if not session_elements:
            # Try to find any repeating elements
            print("[XML] No standard session tags found, analyzing structure...")
            print(f"[XML] Root tag: {root.tag}")
            print(f"[XML] Children: {[child.tag for child in root][:10]}")

            # Return all direct children as potential sessions
            session_elements = list(root)

        print(f"[XML] Found {len(session_elements)} session elements")

        for session_elem in session_elements:
            session = {}

            # Extract all attributes and child elements
            for key, value in session_elem.attrib.items():
                session[key] = value

            for child in session_elem:
                session[child.tag] = child.text or ""

            sessions.append(session)

        print(f"[XML] Parsed {len(sessions)} sessions")

        if sessions:
            print(f"[XML] Sample session keys: {list(sessions[0].keys())[:10]}")

        return sessions

    except Exception as e:
        print(f"[XML] Parse error: {e}")
        import traceback
        traceback.print_exc()
        print(f"[XML] Raw data preview: {xml_data[:500]}")
        return None


def format_date_for_api(date_obj):
    """Format date for API request"""
    return date_obj.strftime("%Y-%m-%d")


def download_sessions_for_date(api, target_date):
    """Download session data for a specific date via API"""
    print(f"[API] Fetching sessions for {target_date}...")

    # BeyondTrust Command API endpoint for listing sessions
    endpoint = "/api/command"
    params = {
        "action": "list_sessions",
        "start_date": target_date,
        "end_date": target_date
    }

    try:
        print(f"[API] Using Command API endpoint: {endpoint}")
        print(f"[API] Parameters: {params}")
        response = api._make_request("GET", endpoint, params=params)

        if response.status_code == 200:
            print(f"[API] SUCCESS! Data received")

            # BeyondTrust Command API returns XML, need to parse it
            content_type = response.headers.get("Content-Type", "")

            if "xml" in content_type.lower():
                print(f"[API] Response format: XML")
                # Parse XML response
                import xml.etree.ElementTree as ET
                xml_data = response.text

                # Check for error in XML
                if "<error" in xml_data:
                    print("[API] Error in API response:")
                    print(xml_data[:500])
                    return None, None

                # Parse sessions from XML
                sessions = parse_xml_sessions(xml_data)
                return sessions, endpoint
            else:
                # Try JSON
                print(f"[API] Response format: JSON")
                data = response.json()
                return data, endpoint

    except Exception as e:
        print(f"[API] Failed: {str(e)[:200]}")
        import traceback
        traceback.print_exc()
        return None, None


def sessions_to_csv(sessions_data, output_file):
    """Convert session data to CSV format"""
    print(f"[CSV] Converting {len(sessions_data)} sessions to CSV...")

    # Define expected CSV columns based on your existing template
    # These are the columns BEFORE removal (we'll remove them later)
    columns = [
        "Session ID",
        "Session Sequence Number",
        "Started",
        "Ended",
        "Representative's Name",
        "Representative's Time Involved",
        "Session Key",
        "Jumpoint",
        "Jump Group",
        "External Key",
        "Customer's Name",
        "Customer's Private IP",
        "Customer's Public IP",
        "Representative's Public IP",
        "Representative's Private IP",
        "Session Type",
        "Chat Transcript",
        "Notes",
        "Additional Representatives",
        "# Files Transferred",
        "# Files Renamed",
        "# Files Deleted",
    ]

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction='ignore')
        writer.writeheader()

        for session in sessions_data:
            # Map API response fields to CSV columns
            # This mapping will need to be adjusted based on actual API response
            row = {
                "Session ID": session.get("id", ""),
                "Session Sequence Number": session.get("sequence", ""),
                "Started": session.get("start_time", session.get("started", "")),
                "Ended": session.get("end_time", session.get("ended", "")),
                "Representative's Name": session.get("representative_name", session.get("rep_name", "")),
                "Representative's Time Involved": session.get("rep_time", ""),
                "Session Key": session.get("session_key", ""),
                "Customer's Name": session.get("customer_name", ""),
                "Customer's Public IP": session.get("customer_ip", ""),
                "Session Type": session.get("session_type", ""),
                "Chat Transcript": session.get("chat", ""),
                "Notes": session.get("notes", ""),
            }
            writer.writerow(row)

    print(f"[CSV] Saved to: {output_file}")
    return output_file


def main():
    if len(sys.argv) < 2:
        print("Usage: python api_download_sessions.py YYYY-MM-DD")
        sys.exit(1)

    target_date = sys.argv[1]

    print("=" * 70)
    print("BEYONDTRUST API SESSION DOWNLOADER")
    print("=" * 70)
    print()
    print(f"Target date: {target_date}")
    print()

    # Initialize API client
    api = BeyondTrustAPI()

    # Download session data
    sessions_data, endpoint = download_sessions_for_date(api, target_date)

    if not sessions_data:
        print()
        print("=" * 70)
        print("FAILED - Could not download session data via API")
        print("=" * 70)
        print()
        print("The API endpoint for session reports may not be available or")
        print("the API credentials may not have the necessary permissions.")
        print()
        print("Possible solutions:")
        print("1. Check BeyondTrust API documentation for the correct endpoint")
        print("2. Verify API credentials have 'reporting' permissions")
        print("3. Contact BeyondTrust support for API access")
        print()
        sys.exit(1)

    # Determine output path
    downloads_dir = Path.home() / "Downloads"
    date_str = target_date.replace("-", "")
    output_file = downloads_dir / f"Support-sessions-{date_str}-{date_str}.csv"

    # Convert to CSV
    csv_file = sessions_to_csv(sessions_data, output_file)

    print()
    print("=" * 70)
    print("SUCCESS - Session data downloaded via API")
    print("=" * 70)
    print(f"CSV file: {csv_file}")
    print(f"Endpoint used: {endpoint}")
    print()

    return str(csv_file)


if __name__ == "__main__":
    main()
