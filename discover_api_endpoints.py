"""
BeyondTrust API Endpoint Discovery
===================================
Systematically tests common BeyondTrust API endpoints to find the session reporting endpoint.
"""

from beyondtrust_api import BeyondTrustAPI
import requests


def test_endpoint(api, method, endpoint, params=None):
    """Test a single endpoint and return results"""
    try:
        response = api._make_request(method, endpoint, params=params)
        return {
            "success": True,
            "status": response.status_code,
            "content_type": response.headers.get("Content-Type", ""),
            "response_preview": str(response.text)[:200]
        }
    except requests.exceptions.HTTPError as e:
        return {
            "success": False,
            "status": e.response.status_code if e.response else None,
            "error": str(e)[:100]
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)[:100]
        }


def main():
    print("=" * 80)
    print("BEYONDTRUST API ENDPOINT DISCOVERY")
    print("=" * 80)
    print()

    api = BeyondTrustAPI()

    # Test date for queries
    test_date = "2025-11-07"

    # Comprehensive list of potential endpoints based on BeyondTrust API patterns
    endpoints_to_test = [
        # Reporting API patterns
        ("/api/reporting/v1/sessions", {"start_date": test_date, "end_date": test_date}),
        ("/api/reporting/sessions", {"start_date": test_date, "end_date": test_date}),
        ("/api/v1/reporting/sessions", {"start_date": test_date, "end_date": test_date}),
        ("/api/v2/reporting/sessions", {"start_date": test_date, "end_date": test_date}),

        # Command API patterns (some BeyondTrust APIs use this)
        ("/api/command", {"action": "list_sessions", "start_date": test_date}),
        ("/appliance/api.ns", {"action": "list_sessions", "start_date": test_date}),
        ("/api/ns", {"action": "list_sessions", "start_date": test_date}),

        # Direct session endpoints
        ("/api/sessions", {"start_date": test_date}),
        ("/api/v1/sessions", {"start_date": test_date}),
        ("/api/support/sessions", {"start_date": test_date}),

        # Report endpoints
        ("/api/reports/sessions", {"start_date": test_date}),
        ("/api/v1/reports/sessions", {"start_date": test_date}),

        # Query endpoints
        ("/api/query/sessions", {"start_date": test_date}),
        ("/reporting/api/sessions", {"start_date": test_date}),

        # Without parameters to see base endpoints
        ("/api/reporting/v1/sessions", None),
        ("/api/sessions", None),
        ("/api/reports", None),
    ]

    print("Testing endpoints...")
    print()

    working_endpoints = []

    for endpoint, params in endpoints_to_test:
        param_str = f" (params: {params})" if params else ""
        print(f"Testing: {endpoint}{param_str}")

        result = test_endpoint(api, "GET", endpoint, params)

        if result["success"]:
            print(f"  [SUCCESS] Status: {result['status']}")
            print(f"  Content-Type: {result['content_type']}")
            print(f"  Response preview: {result['response_preview']}")
            working_endpoints.append((endpoint, params, result))
        else:
            status = result.get('status', 'N/A')
            error = result.get('error', 'Unknown error')
            print(f"  [FAILED] Status: {status} - {error}")

        print()

    # Summary
    print("=" * 80)
    print("DISCOVERY SUMMARY")
    print("=" * 80)
    print()

    if working_endpoints:
        print(f"Found {len(working_endpoints)} working endpoint(s):")
        print()
        for endpoint, params, result in working_endpoints:
            print(f"  Endpoint: {endpoint}")
            if params:
                print(f"  Parameters: {params}")
            print(f"  Status: {result['status']}")
            print()
    else:
        print("No working endpoints found.")
        print()
        print("Possible issues:")
        print("1. API credentials may not have reporting permissions")
        print("2. BeyondTrust version may use different API structure")
        print("3. Reporting API may require different authentication")
        print()
        print("Recommended next steps:")
        print("1. Check BeyondTrust admin console for API documentation")
        print("2. Contact BeyondTrust support for API endpoint documentation")
        print("3. Check if your API client has 'Reporting' permissions enabled")

    print()


if __name__ == "__main__":
    main()
