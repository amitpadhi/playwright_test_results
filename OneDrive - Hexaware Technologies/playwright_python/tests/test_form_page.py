import pytest

from utils.config import BASE_URL
 

@pytest.mark.asyncio
async def test_form_page_shows_form(page):
    await page.goto(BASE_URL)
    await page.locator(":text-is('Forms & Validation')").click()
    assert page.url == 'https://play-qa.com/forms'
    assert page.locator("text=Forms & Validation").is_visible()
    
    #goto loginform 
    input_password = 'test12'
    email = page.locator("#login-email")
    password = page.locator("#login-password")
    
    await email.fill("test12@gmail.com")
    await password.fill(input_password)
    
    print("email:",email)
    print("password:",password)
    
    
    if len(input_password) < 6:
        assert page.locator("text=Password must be at least 6 characters").is_visible()
    else:
        await page.locator("#login-submit").click()
        assert page.locator("text=Login successful").is_visible()
        #screenshot after login
        await page.screenshot(path="login_success.png")
        