"""
BeyondTrust Remote Support API Client
======================================
Handles OAuth authentication and API requests to BeyondTrust Remote Support.

Usage:
    from beyondtrust_api import BeyondTrustAPI

    api = BeyondTrustAPI()
    sessions = api.get_support_sessions()
"""

import requests
import base64
import json
from datetime import datetime, timedelta


class BeyondTrustAPI:
    """BeyondTrust Remote Support API Client"""

    def __init__(self):
        # API Configuration
        self.base_url = "https://zengarinst.beyondtrustcloud.com"
        self.client_id = "b06f24f5909730b2d3ddf9c0f8594b1f854507bd"
        self.client_secret = "Gv+IHrC3VJz0EaSxwVOoKkRlfUEeJUEnGG8TQQeYA2s="

        # Token storage
        self.access_token = None
        self.token_expires_at = None

    def _get_auth_header(self):
        """Generate Basic Auth header for OAuth token request"""
        credentials = f"{self.client_id}:{self.client_secret}"
        encoded = base64.b64encode(credentials.encode()).decode()
        return f"Basic {encoded}"

    def _get_access_token(self):
        """Get or refresh OAuth access token"""
        # Check if we have a valid token
        if self.access_token and self.token_expires_at:
            if datetime.now() < self.token_expires_at:
                return self.access_token

        # Request new token
        print("[API] Requesting new access token...")

        url = f"{self.base_url}/oauth2/token"
        headers = {
            "Authorization": self._get_auth_header(),
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = "grant_type=client_credentials"

        try:
            response = requests.post(url, headers=headers, data=data)
            response.raise_for_status()

            token_data = response.json()
            self.access_token = token_data["access_token"]
            expires_in = token_data.get("expires_in", 3600)

            # Set expiration time (with 5 minute buffer)
            self.token_expires_at = datetime.now() + timedelta(seconds=expires_in - 300)

            print(f"[API] Token acquired (expires in {expires_in}s)")
            return self.access_token

        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Failed to get access token: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"[ERROR] Response: {e.response.text}")
            raise

    def _make_request(self, method, endpoint, **kwargs):
        """Make authenticated API request"""
        token = self._get_access_token()

        url = f"{self.base_url}{endpoint}"
        headers = kwargs.get("headers", {})
        headers["Authorization"] = f"Bearer {token}"
        kwargs["headers"] = headers

        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] API request failed: {method} {endpoint}")
            print(f"[ERROR] {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"[ERROR] Response: {e.response.text}")
            raise

    def explore_api(self):
        """Explore available API endpoints"""
        print("\n" + "="*60)
        print("Exploring BeyondTrust API")
        print("="*60 + "\n")

        # Test authentication
        try:
            token = self._get_access_token()
            print(f"[OK] Authentication successful")
            print(f"[OK] Token: {token[:20]}...")
        except Exception as e:
            print(f"[FAILED] Authentication failed")
            return

        # Try common endpoints
        test_endpoints = [
            "/api/config/v1",
            "/api/config/v1/sessions",
            "/api/config/v1/reports",
            "/api/config/v1/representatives",
            "/api/config/v1/customers",
            "/api/reporting/v1",
            "/api/reporting/v1/sessions",
        ]

        print("\n[TESTING] Trying common endpoints...\n")

        available_endpoints = []
        for endpoint in test_endpoints:
            try:
                response = self._make_request("GET", endpoint)
                print(f"[OK] {endpoint}")
                print(f"     Status: {response.status_code}")

                # Try to parse JSON
                try:
                    data = response.json()
                    print(f"     Response type: {type(data)}")
                    if isinstance(data, dict):
                        print(f"     Keys: {list(data.keys())[:5]}")
                    elif isinstance(data, list):
                        print(f"     Items: {len(data)}")
                except:
                    print(f"     Response: {response.text[:100]}")

                available_endpoints.append(endpoint)
                print()

            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 404:
                    print(f"[404] {endpoint} - Not found")
                elif e.response.status_code == 403:
                    print(f"[403] {endpoint} - Forbidden")
                else:
                    print(f"[{e.response.status_code}] {endpoint} - {e}")
            except Exception as e:
                print(f"[ERROR] {endpoint} - {e}")

        print("\n" + "="*60)
        print(f"Available endpoints: {len(available_endpoints)}")
        print("="*60 + "\n")

        return available_endpoints

    def get_support_sessions(self, start_date=None, end_date=None):
        """
        Get support session data

        Args:
            start_date: Start date (datetime or string)
            end_date: End date (datetime or string)

        Returns:
            List of session data
        """
        # This endpoint will be determined after exploring the API
        endpoint = "/api/config/v1/sessions"  # Placeholder

        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date

        response = self._make_request("GET", endpoint, params=params)
        return response.json()


def main():
    """Test the API client"""
    api = BeyondTrustAPI()

    # Explore available endpoints
    api.explore_api()


if __name__ == "__main__":
    main()
