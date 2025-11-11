"""
Test different Command API action names to find the correct one for listing sessions
"""

from beyondtrust_api import BeyondTrustAPI


def test_action(api, action_name, params=None):
    """Test a single action"""
    endpoint = "/api/command"

    test_params = {"action": action_name}
    if params:
        test_params.update(params)

    try:
        print(f"\nTesting action: {action_name}")
        print(f"  Params: {test_params}")

        response = api._make_request("GET", endpoint, params=test_params)

        if response.status_code == 200:
            content = response.text[:500]

            if "<error" in content:
                # Extract error message
                import xml.etree.ElementTree as ET
                root = ET.fromstring(response.text)
                error_msg = root.text
                print(f"  [ERROR] {error_msg}")
                return False
            else:
                print(f"  [SUCCESS] Response received!")
                print(f"  Response preview: {content}")
                return True
        else:
            print(f"  [FAILED] Status: {response.status_code}")
            return False

    except Exception as e:
        print(f"  [EXCEPTION] {str(e)[:100]}")
        return False


def main():
    print("=" * 80)
    print("BEYONDTRUST COMMAND API ACTION DISCOVERY")
    print("=" * 80)

    api = BeyondTrustAPI()

    # Common BeyondTrust Command API action names
    actions_to_test = [
        # Session-related actions
        ("get_sessions", {"start_date": "2025-11-07", "end_date": "2025-11-07"}),
        ("get_session_list", {"start_date": "2025-11-07"}),
        ("session_list", {"start_date": "2025-11-07"}),
        ("sessions", {"start_date": "2025-11-07"}),
        ("get_support_sessions", {"start_date": "2025-11-07"}),
        ("list_support_sessions", {"start_date": "2025-11-07"}),
        ("report_sessions", {"start_date": "2025-11-07"}),
        ("session_report", {"start_date": "2025-11-07"}),
        ("get_session_report", {"start_date": "2025-11-07"}),

        # Report-related actions
        ("get_report", {"report_type": "sessions", "start_date": "2025-11-07"}),
        ("generate_report", {"type": "sessions", "start_date": "2025-11-07"}),
        ("report", {"type": "sessions", "start_date": "2025-11-07"}),

        # Query actions
        ("query_sessions", {"start_date": "2025-11-07"}),
        ("search_sessions", {"start_date": "2025-11-07"}),

        # Generic list actions
        ("list", {"object": "sessions", "start_date": "2025-11-07"}),
        ("get", {"object": "sessions", "start_date": "2025-11-07"}),

        # Check available actions
        ("help", None),
        ("get_help", None),
        ("list_actions", None),
        ("available_actions", None),
    ]

    working_actions = []

    for action, params in actions_to_test:
        if test_action(api, action, params):
            working_actions.append((action, params))

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    if working_actions:
        print(f"\nFound {len(working_actions)} working action(s):")
        for action, params in working_actions:
            print(f"\n  Action: {action}")
            print(f"  Params: {params}")
    else:
        print("\nNo working actions found.")
        print("\nThe Command API may require different action names or parameters.")
        print("Check the BeyondTrust API documentation for your version.")

    print()


if __name__ == "__main__":
    main()
