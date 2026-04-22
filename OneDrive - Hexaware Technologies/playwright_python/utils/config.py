"""Simple configuration constants for tests."""

# Base URL for the application under test
BASE_URL = "https://play-qa.com/"

# Whether to run the browser in headless mode (False will show the browser window)
HEADLESS = True

# Which browser to use with Playwright: 'chromium', 'firefox', or 'webkit'
# Keep lowercase since conftest uses getattr(playwright, BROWSER)
BROWSER = "chromium"
