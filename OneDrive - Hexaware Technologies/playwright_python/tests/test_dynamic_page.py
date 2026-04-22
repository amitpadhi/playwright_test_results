import pytest
from utils.config import BASE_URL
from tests.conftest import page, context

@pytest.mark.asyncio
async def test_dynamic_page_shows_content(page):
    await page.goto(BASE_URL + 'dynamic-content')
    assert page.url == 'https://play-qa.com/dynamic-content'
    
    # Wait for the dynamic content to load and be visible
    #await page.locator('button:has-text("Show Element")').click()
    
    #dynamic_element = page.locator('#dynamic-element')
    #await dynamic_element.wait_for(state="visible", timeout=5000)
    #assert dynamic_element.is_visible()
    #dynamic_text = page.locator('text=This element appeared dynamically!')
    #assert dynamic_text.is_visible()
    
    await page.locator('button:has-text("Open New Window")').click()
    
    


    
    #await dynamic_element.wait_for(state="visible", timeout=5000)


