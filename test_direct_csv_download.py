"""
Test if we can download CSV reports directly via authenticated HTTP request
instead of using browser automation or Command API.
"""

from beyondtrust_api import BeyondTrustAPI
import requests


def test_csv_download_urls(api):
    """Test various CSV download URL patterns"""

    test_date = "2025-11-07"

    # Potential CSV download URLs based on typical BeyondTrust patterns
    test_urls = [
        f"/appliance/reports.ns?controller=support_sessions&action=download&start_date={test_date}&end_date={test_date}&format=csv",
        f"/appliance/reports.ns?controller=support_sessions&action=export&start_date={test_date}&end_date={test_date}",
        f"/reporting/sessions/export?start_date={test_date}&end_date={test_date}&format=csv",
        f"/reporting/sessions/download?start_date={test_date}&end_date={test_date}",
        f"/reports/support-sessions/export?start_date={test_date}&end_date={test_date}",
        f"/api/reporting/sessions/export?start_date={test_date}&end_date={test_date}&format=csv",
    ]

    print("=" * 80)
    print("TESTING DIRECT CSV DOWNLOAD URLS")
    print("=" * 80)
    print()

    working_urls = []

    for url in test_urls:
        print(f"Testing: {url}")

        try:
            response = api._make_request("GET", url)

            if response.status_code == 200:
                content_type = response.headers.get("Content-Type", "")
                content_preview = response.text[:200]

                print(f"  [SUCCESS] Status: 200")
                print(f"  Content-Type: {content_type}")
                print(f"  Content preview: {content_preview}")

                # Check if it's actually CSV
                if "csv" in content_type.lower() or content_preview.startswith("Session"):
                    print(f"  [CONFIRMED] This looks like CSV data!")
                    working_urls.append(url)
                else:
                    print(f"  [WARNING] Response doesn't look like CSV")

            else:
                print(f"  [FAILED] Status: {response.status_code}")

        except Exception as e:
            print(f"  [ERROR] {str(e)[:100]}")

        print()

    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)

    if working_urls:
        print(f"\nFound {len(working_urls)} working CSV download URL(s)!")
        for url in working_urls:
            print(f"  - {url}")
    else:
        print("\nNo working CSV download URLs found.")
        print("\nThe BeyondTrust web interface may use session-based authentication")
        print("or require specific cookie/token values that aren't available via OAuth.")

    print()


if __name__ == "__main__":
    api = BeyondTrustAPI()
    test_csv_download_urls(api)
