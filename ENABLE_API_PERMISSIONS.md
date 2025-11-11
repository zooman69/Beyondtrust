# Enable BeyondTrust API Permissions

## Issue
The API client "Manager reporting" does not have permission to use the Command API.

## Solution
Enable Command API permissions for your API client in BeyondTrust.

## Steps

1. **Log into BeyondTrust Admin Console**
   - Go to: https://zengarinst.beyondtrustcloud.com
   - Log in with admin credentials

2. **Navigate to API Clients**
   - Go to: **Management** > **API Clients** (or **Users & Security** > **API Configuration**)
   - Find the API client named "Manager reporting"
   - Client ID: `b06f24f5909730b2d3ddf9c0f8594b1f854507bd`

3. **Enable Command API Permission**
   - Click on the API client to edit
   - Look for **Permissions** or **API Access** section
   - Enable: **Command API** (or **Allow Command API Access**)
   - Save changes

4. **Verify Permissions**
   After enabling, the API client should have these permissions:
   - ✓ OAuth Authentication
   - ✓ Command API Access
   - ✓ Read Session Data (or Reporting Access)

5. **Test the API**
   Run this command to verify:
   ```bash
   python Y:\Coding\Beyondtrust\discover_api_endpoints.py
   ```

   You should see a successful response instead of the permission error.

## Alternative: Create New API Client

If you can't modify the existing client, create a new one:

1. Go to **Management** > **API Clients**
2. Click **Create API Client** or **Add**
3. Name it: **Reporting Automation**
4. Enable permissions:
   - ✓ Command API
   - ✓ OAuth 2.0
   - ✓ Reporting Access
5. Save and copy the **Client ID** and **Client Secret**
6. Update `Y:\Coding\Beyondtrust\beyondtrust_api.py` with the new credentials

## Once Permissions Are Enabled

Your daily and monthly report buttons will work automatically:
- [DAILY_REPORT.bat](Y:\Coding\Beyondtrust\DAILY_REPORT.bat) - One click for yesterday's report
- [MONTHLY_REPORT.bat](Y:\Coding\Beyondtrust\MONTHLY_REPORT.bat) - One click for all previous month reports

Both will use the API with no browser automation required!
