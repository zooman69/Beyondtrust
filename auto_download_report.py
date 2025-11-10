"""
BeyondTrust Automated Report Downloader
========================================
Automatically logs into BeyondTrust, navigates to reports, and downloads session data.

Usage:
    python auto_download_report.py [date]

Examples:
    python auto_download_report.py 2025-11-05
    python auto_download_report.py "November 5, 2025"
    python auto_download_report.py  # Downloads today's report

Requirements:
    - Selenium and Chrome browser
    - BeyondTrust credentials stored in .env file or passed as arguments
"""

import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import getpass

# Load environment variables from .env file
load_dotenv()


class BeyondTrustDownloader:
    """Automated BeyondTrust report downloader"""

    def __init__(self, username=None, password=None, headless=False):
        self.base_url = "https://zengarinst.beyondtrustcloud.com"
        self.username = username
        self.password = password
        self.headless = headless
        self.driver = None
        self.download_dir = str(Path.home() / "Downloads")

    def setup_driver(self):
        """Setup Chrome WebDriver with download preferences"""
        print("[SETUP] Initializing Chrome WebDriver...")

        chrome_options = Options()

        # Set download directory
        prefs = {
            "download.default_directory": self.download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        chrome_options.add_experimental_option("prefs", prefs)

        # Headless mode
        if self.headless:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")

        # Other options for stability
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")

        # Initialize driver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.implicitly_wait(10)

        print(f"[SETUP] Download directory: {self.download_dir}")
        print("[SETUP] WebDriver ready")

    def login(self):
        """Login to BeyondTrust"""
        print(f"\n[LOGIN] Navigating to {self.base_url}...")
        self.driver.get(f"{self.base_url}/login")

        try:
            # Wait for login form
            wait = WebDriverWait(self.driver, 15)

            # Find username field (may vary - we'll try common selectors)
            print("[LOGIN] Waiting for login form...")

            # Try to find username field
            username_selectors = [
                (By.ID, "username"),
                (By.ID, "user"),
                (By.NAME, "username"),
                (By.NAME, "user"),
                (By.CSS_SELECTOR, "input[type='text']"),
                (By.CSS_SELECTOR, "input[type='email']")
            ]

            username_field = None
            for selector_type, selector_value in username_selectors:
                try:
                    username_field = wait.until(
                        EC.presence_of_element_located((selector_type, selector_value))
                    )
                    print(f"[LOGIN] Found username field using {selector_type}: {selector_value}")
                    break
                except:
                    continue

            if not username_field:
                print("[ERROR] Could not find username field")
                print("[INFO] Page source preview:")
                print(self.driver.page_source[:500])
                return False

            # Enter username
            print(f"[LOGIN] Entering username: {self.username}")
            username_field.clear()
            username_field.send_keys(self.username)

            # Find password field
            password_selectors = [
                (By.ID, "password"),
                (By.ID, "pass"),
                (By.NAME, "password"),
                (By.NAME, "pass"),
                (By.CSS_SELECTOR, "input[type='password']")
            ]

            password_field = None
            for selector_type, selector_value in password_selectors:
                try:
                    password_field = self.driver.find_element(selector_type, selector_value)
                    print(f"[LOGIN] Found password field using {selector_type}: {selector_value}")
                    break
                except:
                    continue

            if not password_field:
                print("[ERROR] Could not find password field")
                return False

            # Enter password
            print("[LOGIN] Entering password...")
            password_field.clear()
            password_field.send_keys(self.password)

            # Find and click login button
            login_button_selectors = [
                (By.ID, "login"),
                (By.ID, "submit"),
                (By.NAME, "login"),
                (By.CSS_SELECTOR, "button[type='submit']"),
                (By.CSS_SELECTOR, "input[type='submit']"),
                (By.XPATH, "//button[contains(text(), 'Log') or contains(text(), 'Sign')]")
            ]

            login_button = None
            for selector_type, selector_value in login_button_selectors:
                try:
                    login_button = self.driver.find_element(selector_type, selector_value)
                    print(f"[LOGIN] Found login button using {selector_type}: {selector_value}")
                    break
                except:
                    continue

            if not login_button:
                print("[ERROR] Could not find login button")
                return False

            print("[LOGIN] Clicking login button...")
            login_button.click()

            # Wait for login to complete
            time.sleep(3)

            # Check if we're logged in
            current_url = self.driver.current_url
            print(f"[LOGIN] Current URL: {current_url}")

            # Check for session report page (zooman with reports access!)
            if "/login/session_report" in current_url:
                print("[LOGIN] SUCCESS: Redirected to session report page!")
                print("[LOGIN] This means the account has reports access - perfect!")
                return True

            # Check for console download page (for zooman/automation accounts)
            elif "/login/downloads/console" in current_url or "/console" in current_url:
                print("[LOGIN] Logged in to console page - this is a console account")
                print("[LOGIN] Console accounts can still access reports if permissions are set")
                # Don't return yet - we'll navigate to reports next
                return True

            # Check for MFA app page (for zooman account with MFA)
            elif "/login/mfa_app" in current_url:
                print("[LOGIN] WARNING: Multi-factor authentication detected!")
                print("[LOGIN] Please complete the MFA challenge in the browser...")
                print("[WAIT] Waiting 120 seconds (2 minutes) for you to complete MFA...")

                # Wait for user to complete MFA
                for i in range(120):
                    time.sleep(1)
                    current_url = self.driver.current_url
                    if "/login" not in current_url:
                        print(f"[LOGIN] SUCCESS: MFA completed! Now at: {current_url}")
                        return True

                # Check final URL
                current_url = self.driver.current_url
                if "/login" not in current_url:
                    print("[LOGIN] SUCCESS: Login successful!")
                    return True
                else:
                    print("[ERROR] MFA not completed in time")
                    return False

            # Check for challenge/2FA page
            elif "/login/challenge" in current_url:
                print("[LOGIN] WARNING: Two-factor authentication or security challenge detected!")
                print("[LOGIN] Please complete the security challenge in the browser...")
                print("[WAIT] Waiting 120 seconds (2 minutes) for you to complete the challenge...")

                # Wait for user to complete challenge
                for i in range(120):
                    time.sleep(1)
                    current_url = self.driver.current_url
                    if "/login" not in current_url:
                        print(f"[LOGIN] SUCCESS: Challenge completed! Now at: {current_url}")
                        return True

                # Check final URL
                current_url = self.driver.current_url
                if "/login" not in current_url:
                    print("[LOGIN] SUCCESS: Login successful!")
                    return True
                else:
                    print("[ERROR] Challenge not completed in time")
                    return False

            elif "/login" not in current_url or "dashboard" in current_url.lower():
                print("[LOGIN] SUCCESS: Login successful!")
                return True
            else:
                print("[ERROR] Login may have failed - still on login page")
                print(f"[DEBUG] Current URL: {current_url}")
                return False

        except Exception as e:
            print(f"[ERROR] Login failed: {e}")
            import traceback
            traceback.print_exc()
            return False

    def navigate_to_reports(self, target_date):
        """Navigate to reports section and select date"""
        print(f"\n[REPORTS] Navigating to reports for {target_date}...")

        try:
            # Check if we're already on a reports-related page
            current_url = self.driver.current_url
            if "/session_report" in current_url:
                print("[REPORTS] Already on session report page - staying here!")
                time.sleep(2)
            else:
                # Direct URL to support reports
                reports_url = f"{self.base_url}/appliance/reports.ns?controller=support_sessions"
                print(f"[REPORTS] Going to: {reports_url}")
                self.driver.get(reports_url)

                # Give it more time to load
                print("[REPORTS] Waiting for page to load...")
                time.sleep(5)

            wait = WebDriverWait(self.driver, 15)

            # Check current URL after navigation
            current_url = self.driver.current_url
            print(f"[REPORTS] Current URL after navigation: {current_url}")

            # Check page title
            page_title = self.driver.title
            print(f"[REPORTS] Page title: {page_title}")

            # Save screenshot for debugging
            screenshot_path = Path(self.download_dir) / "beyondtrust_reports_page.png"
            self.driver.save_screenshot(str(screenshot_path))
            print(f"[DEBUG] Screenshot saved: {screenshot_path}")

            # Check if we got "Document Not Found" error
            page_source = self.driver.page_source
            if "Document Not Found" in page_source:
                print("[ERROR] Got 'Document Not Found' error on reports page")
                print("[ERROR] The zooman account may not have proper web UI access")
                return False

            print("[REPORTS] Page loaded successfully!")
            return True

        except Exception as e:
            print(f"[ERROR] Failed to navigate to reports: {e}")
            import traceback
            traceback.print_exc()
            return False

    def download_report(self, target_date):
        """Download the session report for the specified date"""
        print(f"\n[DOWNLOAD] Attempting to download report for {target_date}...")

        try:
            wait = WebDriverWait(self.driver, 15)

            # Format date for input (MM/DD/YYYY format)
            date_str = target_date.strftime("%m/%d/%Y")
            print(f"[DOWNLOAD] Target date: {date_str}")

            # First, we need to enable the Date Range filter by clicking its checkbox
            print("[DOWNLOAD] Looking for Date Range checkbox...")

            # Scroll down a bit to make sure the Date Range section is visible
            self.driver.execute_script("window.scrollBy(0, 200);")
            time.sleep(0.5)

            # Try to find the Date Range checkbox by text
            date_range_checkbox_selectors = [
                # Try finding by the label text and then the associated checkbox
                (By.XPATH, "//label[contains(text(), 'Find all sessions within a specific date range')]/..//input[@type='checkbox']"),
                (By.XPATH, "//label[contains(text(), 'within a specific date range')]/..//input[@type='checkbox']"),
                # Try finding the checkbox near "Date Range" heading
                (By.XPATH, "//h3[contains(text(), 'Date Range')]/following-sibling::div//input[@type='checkbox']"),
                # Try all checkboxes and find the one near "date range" text
                (By.XPATH, "//input[@type='checkbox' and following-sibling::label[contains(., 'date range')]]"),
                # Broader search - find checkbox that comes before the date range text
                (By.XPATH, "//div[contains(@class, 'filter') or contains(@class, 'field')]//input[@type='checkbox'][following::text()[contains(., 'date range')]]"),
            ]

            date_checkbox = None
            for selector_type, selector_value in date_range_checkbox_selectors:
                try:
                    date_checkbox = self.driver.find_element(selector_type, selector_value)
                    print(f"[DOWNLOAD] Found Date Range checkbox using {selector_type}")
                    break
                except Exception as e:
                    continue

            if not date_checkbox:
                print("[ERROR] Could not find Date Range checkbox with specific selectors")
                print("[DEBUG] Trying to find all checkboxes on the page...")

                # Find all checkboxes and print their context
                all_checkboxes = self.driver.find_elements(By.XPATH, "//input[@type='checkbox']")
                print(f"[DEBUG] Found {len(all_checkboxes)} checkboxes on the page")

                # Try to find the one related to date range by looking at nearby text
                for i, checkbox in enumerate(all_checkboxes):
                    try:
                        # Get the parent element and its text
                        parent = checkbox.find_element(By.XPATH, "..")
                        parent_text = parent.text
                        if "date" in parent_text.lower() or "range" in parent_text.lower():
                            print(f"[DEBUG] Checkbox {i} has date/range related text: {parent_text[:50]}")
                            date_checkbox = checkbox
                            print(f"[DOWNLOAD] Using checkbox {i} for Date Range")
                            break
                    except:
                        continue

                if not date_checkbox:
                    print("[ERROR] Still could not find Date Range checkbox")
                    screenshot_path = Path(self.download_dir) / "beyondtrust_no_checkbox.png"
                    self.driver.save_screenshot(str(screenshot_path))
                    print(f"[DEBUG] Screenshot saved: {screenshot_path}")

                    # Save page source for debugging
                    page_source_path = Path(self.download_dir) / "beyondtrust_page_source.html"
                    with open(page_source_path, 'w', encoding='utf-8') as f:
                        f.write(self.driver.page_source)
                    print(f"[DEBUG] Page source saved: {page_source_path}")
                    return False

            # Check if the checkbox is already checked
            if not date_checkbox.is_selected():
                print("[DOWNLOAD] Clicking Date Range checkbox to enable date fields...")
                try:
                    date_checkbox.click()
                except:
                    # If regular click fails, try JavaScript click
                    print("[DOWNLOAD] Regular click failed, trying JavaScript click...")
                    self.driver.execute_script("arguments[0].click();", date_checkbox)
                time.sleep(1)
            else:
                print("[DOWNLOAD] Date Range checkbox already checked - date fields should be visible")

            # Now find and fill the date fields
            print("[DOWNLOAD] Looking for date input fields...")

            # Scroll down to make sure date fields are visible
            self.driver.execute_script("arguments[0].scrollIntoView(true);", date_checkbox)
            time.sleep(0.5)

            # This interface uses "End Date" radio button and a single date field
            print("[DOWNLOAD] Looking for 'End Date' radio button...")

            # First, click the "End Date" radio button to enable the date picker
            end_date_radio_selectors = [
                (By.XPATH, "//input[@type='radio' and following-sibling::text()[contains(., 'End Date')]]"),
                (By.XPATH, "//label[contains(text(), 'End Date')]/preceding-sibling::input[@type='radio']"),
                (By.XPATH, "//input[@type='radio'][following::text()[normalize-space()='End Date']]"),
            ]

            end_date_radio = None
            for selector_type, selector_value in end_date_radio_selectors:
                try:
                    end_date_radio = self.driver.find_element(selector_type, selector_value)
                    print(f"[DOWNLOAD] Found End Date radio button using {selector_type}")
                    break
                except:
                    continue

            if end_date_radio and not end_date_radio.is_selected():
                print("[DOWNLOAD] Clicking 'End Date' radio button...")
                end_date_radio.click()
                time.sleep(0.5)
            else:
                print("[DOWNLOAD] End Date radio button already selected or not found")

            # Now find the date input field (should be visible after clicking End Date radio)
            print("[DOWNLOAD] Looking for date input field...")

            # Wait a bit for the field to appear/become enabled
            time.sleep(1)

            date_field_selectors = [
                (By.XPATH, "//input[@type='text' and contains(@value, '/')]"),  # Date fields usually show MM/DD/YYYY
                (By.XPATH, "//input[@type='text'][following-sibling::*[contains(@class, 'calendar') or contains(@class, 'date')]]"),
                (By.XPATH, "//input[@type='text'][preceding-sibling::*[contains(text(), 'End Date')]]"),
                (By.CSS_SELECTOR, "input[type='text'].date"),
                (By.CSS_SELECTOR, "input[type='text'][class*='date']"),
            ]

            date_field = None
            for selector_type, selector_value in date_field_selectors:
                try:
                    date_field = self.driver.find_element(selector_type, selector_value)
                    print(f"[DOWNLOAD] Found date field using {selector_type}")
                    break
                except:
                    continue

            if not date_field:
                print("[ERROR] Could not find date input field")
                screenshot_path = Path(self.download_dir) / "beyondtrust_no_date_field.png"
                self.driver.save_screenshot(str(screenshot_path))
                print(f"[DEBUG] Screenshot saved: {screenshot_path}")
                return False

            # Clear and set the date
            print(f"[DOWNLOAD] Setting date to: {date_str}")
            date_field.clear()
            time.sleep(0.3)
            date_field.send_keys(date_str)
            time.sleep(0.5)
            print(f"[DOWNLOAD] Date set to: {date_str}")

            # Scroll down to find the submit/generate button
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

            # Look for the "Download Report" button
            print("[DOWNLOAD] Looking for 'Download Report' button...")
            download_button_selectors = [
                (By.XPATH, "//button[contains(text(), 'Download Report')]"),
                (By.XPATH, "//input[@value='Download Report']"),
                (By.XPATH, "//a[contains(text(), 'Download Report')]"),
                (By.CSS_SELECTOR, "button[class*='download']"),
                (By.PARTIAL_LINK_TEXT, "Download"),
            ]

            download_button = None
            for selector_type, selector_value in download_button_selectors:
                try:
                    download_button = self.driver.find_element(selector_type, selector_value)
                    print(f"[DOWNLOAD] Found Download Report button using {selector_type}")
                    break
                except:
                    continue

            if not download_button:
                print("[ERROR] Could not find 'Download Report' button")
                screenshot_path = Path(self.download_dir) / "beyondtrust_no_download_button.png"
                self.driver.save_screenshot(str(screenshot_path))
                print(f"[DEBUG] Screenshot saved: {screenshot_path}")
                return False

            print("[DOWNLOAD] Clicking 'Download Report' button...")
            download_button.click()

            print("[DOWNLOAD] Waiting for download to complete...")
            time.sleep(8)

            print("[SUCCESS] Report download should be complete!")
            return True

        except Exception as e:
            print(f"[ERROR] Download failed: {e}")
            import traceback
            traceback.print_exc()

            # Save screenshot for debugging
            try:
                screenshot_path = Path(self.download_dir) / "beyondtrust_error.png"
                self.driver.save_screenshot(str(screenshot_path))
                print(f"[DEBUG] Error screenshot: {screenshot_path}")
            except:
                pass

            return False

    def close(self):
        """Close the browser"""
        if self.driver:
            print("\n[CLEANUP] Closing browser...")
            self.driver.quit()


def parse_date(date_str):
    """Parse date string to datetime object"""
    if not date_str:
        return datetime.now().date()

    # Try common formats
    formats = [
        "%Y-%m-%d",
        "%m/%d/%Y",
        "%d/%m/%Y",
        "%B %d, %Y",
        "%b %d, %Y"
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except:
            continue

    print(f"[ERROR] Could not parse date: {date_str}")
    return None


def main():
    print("=" * 60)
    print("BeyondTrust Automated Report Downloader")
    print("=" * 60)
    print()

    # Get target date
    if len(sys.argv) > 1:
        target_date = parse_date(sys.argv[1])
    else:
        target_date = datetime.now().date()

    if not target_date:
        print("[ERROR] Invalid date provided")
        sys.exit(1)

    print(f"Target date: {target_date}")
    print()

    # Get credentials - try automation credentials first (no 2FA), then fall back to regular
    username = os.getenv("BEYONDTRUST_AUTO_USERNAME") or os.getenv("BEYONDTRUST_USERNAME")
    password = os.getenv("BEYONDTRUST_AUTO_PASSWORD") or os.getenv("BEYONDTRUST_PASSWORD")

    if not username:
        username = input("BeyondTrust Username: ")
    if not password:
        password = getpass.getpass("BeyondTrust Password: ")

    print()

    # Initialize downloader
    downloader = BeyondTrustDownloader(username, password, headless=False)

    try:
        # Setup driver
        downloader.setup_driver()

        # Login
        if not downloader.login():
            print("\n[FAILED] Could not login to BeyondTrust")
            sys.exit(1)

        # Navigate to reports
        if not downloader.navigate_to_reports(target_date):
            print("\n[FAILED] Could not navigate to reports")
            sys.exit(1)

        # Download report
        if not downloader.download_report(target_date):
            print("\n[FAILED] Could not download report")
            print("\n[NEXT STEPS]:")
            print("1. Check the screenshots saved in Downloads folder")
            print("2. Share them with me so I can see the BeyondTrust reports page")
            print("3. I'll update the script to automate the download")
            sys.exit(1)

        print("\n[SUCCESS] Report download initiated!")

    except KeyboardInterrupt:
        print("\n\n[STOPPED] Interrupted by user")
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        downloader.close()


if __name__ == "__main__":
    main()
