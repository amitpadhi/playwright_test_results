import pytest

from utils.config import BASE_URL

@pytest.mark.asyncio
async def test_form_page_shows_form(page):
    await page.goto(BASE_URL)
    await page.locator(":text-is('Forms & Validation')").click()
    assert page.url == 'https://play-qa.com/forms'
    text_input = page.locator("#field-text")
    await text_input.fill("Test11111")
    email_input = page.locator("#field-email")
    await email_input.fill("test1@hh.com")
    await page.locator("#country-code:visible").click()
    
    
    # Use a text-based locator that avoids relying on the emoji. Wait until
    # the button with the country text is visible, then click it.
    await page.get_by_role('option', name="India +91").click()
    
    
    
    
    