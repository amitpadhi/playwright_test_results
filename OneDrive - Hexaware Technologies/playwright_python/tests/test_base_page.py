"""Simple smoke test: navigate to BASE_URL and assert presence of text.

This test assumes the Playwright fixtures in `tests/conftest.py` are available.
"""

import pytest

from utils.config import BASE_URL


@pytest.mark.asyncio
async def test_base_page_shows_master_qa_automation(page):
    """Open the base URL and assert 'Master QA Automation' is visible."""
    await page.goto(BASE_URL)

    # Use a text locator which matches visible text content
    locator = page.locator("text=Master QA Automation")

    # Wait briefly for the element/text to appear (timeout in ms)
    await locator.wait_for(timeout=5000)

    assert await locator.is_visible(), "Expected 'Master QA Automation' to be visible on the page"
    