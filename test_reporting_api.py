"""
Test BeyondTrust Reporting API endpoints
"""

from beyondtrust_api import BeyondTrustAPI


def test_reporting_endpoints(api):
    """Test various Reporting API endpoint patterns"""

    test_date = "2025-11-07"

    # Potential Reporting API endpoints
    endpoints_to_test = [
        ("/api/reporting/v1/support-session", {"start_date": test_date, "end_date": test_date}),
        ("/api/reporting/v1/support-sessions", {"start_date": test_date, "end_date": test_date}),
        ("/api/reporting/v1/session", {"start_date": test_date, "end_date": test_date}),
        ("/api/reporting/v1/sessions", {"start_date": test_date, "end_date": test_date}),
        ("/api/reporting/support-session", {"start_date": test_date, "end_date": test_date}),
        ("/api/reporting/support-sessions", {"start_date": test_date, "end_date": test_date}),

        # Try without date parameters to see structure
        ("/api/reporting/v1/support-session", None),
        ("/api/reporting/v1", None),
    ]

    print("=" * 80)
    print("TESTING REPORTING API ENDPOINTS")
    print("=" * 80)
    print()

    working_endpoints = []

    for endpoint, params in endpoints_to_test:
        param_str = f" (params: {params})" if params else ""
        print(f"Testing: {endpoint}{param_str}")

        try:
            response = api._make_request("GET", endpoint, params=params)

            if response.status_code == 200:
                print(f"  [SUCCESS] Status: 200")
                content_type = response.headers.get("Content-Type", "")
                print(f"  Content-Type: {content_type}")

                # Try to parse response
                try:
                    data = response.json()
                    print(f"  Response type: {type(data)}")

                    if isinstance(data, list):
                        print(f"  Number of items: {len(data)}")
                        if data:
                            print(f"  Sample item keys: {list(data[0].keys())[:10]}")
                    elif isinstance(data, dict):
                        print(f"  Response keys: {list(data.keys())[:10]}")

                    working_endpoints.append((endpoint, params, data))

                except:
                    print(f"  Response preview: {response.text[:200]}")

            else:
                print(f"  [FAILED] Status: {response.status_code}")

        except Exception as e:
            error_msg = str(e)[:150]
            print(f"  [ERROR] {error_msg}")

        print()

    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()

    if working_endpoints:
        print(f"Found {len(working_endpoints)} working endpoint(s)!")
        print()
        for endpoint, params, data in working_endpoints:
            print(f"Endpoint: {endpoint}")
            if params:
                print(f"Parameters: {params}")
            if isinstance(data, list):
                print(f"Returns: List with {len(data)} items")
            else:
                print(f"Returns: {type(data).__name__}")
            print()
    else:
        print("No working Reporting API endpoints found.")
        print()
        print("The Reporting API permission is enabled, but we may need")
        print("different endpoint paths or authentication method.")

    return working_endpoints


if __name__ == "__main__":
    api = BeyondTrustAPI()
    working = test_reporting_endpoints(api)
