"""
Systematically explore ALL enabled BeyondTrust APIs to see what data we can actually get.

Enabled APIs:
- Command API (Full Access)
- Reporting API (Support Session Reports access)
- Configuration API (Allow Access)
"""

from beyondtrust_api import BeyondTrustAPI
import json


def test_configuration_api(api):
    """Test Configuration API endpoints from the OpenAPI spec"""
    print("\n" + "=" * 80)
    print("CONFIGURATION API")
    print("=" * 80)

    # From the OpenAPI spec we saw these endpoints exist
    endpoints = [
        "/api/config/v1/user",
        "/api/config/v1/team",
        "/api/config/v1/session-policy",
        "/api/config/v1/jump-client",
        "/api/config/v1/rep-status",
    ]

    working = []

    for endpoint in endpoints:
        print(f"\nTesting: {endpoint}")
        try:
            response = api._make_request("GET", endpoint)
            if response.status_code == 200:
                data = response.json()
                print(f"  [SUCCESS] Status: 200")
                print(f"  Data type: {type(data)}")
                if isinstance(data, list):
                    print(f"  Items: {len(data)}")
                    if data:
                        print(f"  Sample keys: {list(data[0].keys())[:10]}")
                elif isinstance(data, dict):
                    print(f"  Keys: {list(data.keys())[:10]}")
                working.append((endpoint, data))
            else:
                print(f"  [FAILED] Status: {response.status_code}")
        except Exception as e:
            print(f"  [ERROR] {str(e)[:100]}")

    return working


def test_command_api_actions(api):
    """Test different Command API actions based on BeyondTrust docs"""
    print("\n" + "=" * 80)
    print("COMMAND API - Testing Common Actions")
    print("=" * 80)

    # Common BeyondTrust Command API actions from documentation
    actions = [
        # User/Representative management
        "get_representative_list",
        "get_rep_list",
        "list_representatives",
        "get_users",

        # Team management
        "get_team_list",
        "list_teams",
        "get_teams",

        # Session management
        "get_session_summary",
        "session_summary",
        "get_active_sessions",
        "list_active_sessions",

        # General
        "get_api_version",
        "version",
        "get_system_info",
    ]

    working = []

    for action in actions:
        print(f"\nTesting action: {action}")
        try:
            response = api._make_request("GET", "/api/command", params={"action": action})
            if response.status_code == 200:
                text = response.text

                # Check if it's an error
                if "<error" in text:
                    import xml.etree.ElementTree as ET
                    root = ET.fromstring(text)
                    error_msg = root.text
                    print(f"  [ERROR IN XML] {error_msg}")
                else:
                    print(f"  [SUCCESS] Got response!")
                    print(f"  Response preview: {text[:300]}")
                    working.append((action, text))
            else:
                print(f"  [FAILED] Status: {response.status_code}")
        except Exception as e:
            print(f"  [ERROR] {str(e)[:100]}")

    return working


def test_openapi_endpoints(api):
    """Check if there's an OpenAPI/Swagger doc for other APIs"""
    print("\n" + "=" * 80)
    print("LOOKING FOR API DOCUMENTATION ENDPOINTS")
    print("=" * 80)

    doc_endpoints = [
        "/api/config/v1/openapi.yaml",
        "/api/reporting/v1/openapi.yaml",
        "/api/openapi.yaml",
        "/openapi.yaml",
        "/api/docs",
        "/api/swagger.json",
        "/api/config/v1/openapi.json",
    ]

    for endpoint in doc_endpoints:
        print(f"\nTesting: {endpoint}")
        try:
            response = api._make_request("GET", endpoint)
            if response.status_code == 200:
                print(f"  [FOUND] Status: 200")
                content_type = response.headers.get("Content-Type", "")
                print(f"  Content-Type: {content_type}")
                print(f"  Size: {len(response.text)} bytes")

                # Save it if it's YAML/JSON
                if "yaml" in content_type or "json" in content_type:
                    filename = f"Y:\\Coding\\Beyondtrust\\api_docs_{endpoint.replace('/', '_')}"
                    with open(filename, 'w') as f:
                        f.write(response.text)
                    print(f"  [SAVED] {filename}")
        except Exception as e:
            print(f"  [FAILED] {str(e)[:100]}")


def main():
    print("=" * 80)
    print("BEYONDTRUST API COMPREHENSIVE EXPLORATION")
    print("=" * 80)
    print("\nThis will test all enabled APIs to find what data is actually available.\n")

    api = BeyondTrustAPI()

    # Test each API
    config_working = test_configuration_api(api)
    command_working = test_command_api_actions(api)
    test_openapi_endpoints(api)

    # Final summary
    print("\n" + "=" * 80)
    print("FINAL SUMMARY - WHAT WE CAN ACCESS")
    print("=" * 80)

    if config_working:
        print(f"\n[Configuration API] {len(config_working)} working endpoint(s):")
        for endpoint, data in config_working:
            print(f"  - {endpoint}")

    if command_working:
        print(f"\n[Command API] {len(command_working)} working action(s):")
        for action, data in command_working:
            print(f"  - action={action}")

    if not config_working and not command_working:
        print("\n[NO DATA AVAILABLE]")
        print("None of the enabled APIs returned usable data.")
        print("\nThis suggests the API credentials may need additional configuration")
        print("or the session reporting data is only available through the web UI.")

    print()


if __name__ == "__main__":
    main()
