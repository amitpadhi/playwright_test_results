import pytest
from utils.config import BASE_URL

@pytest.mark.asyncio
async def test_complex_scenario(page):
    await page.goto(BASE_URL + 'complex-scenarios')
    await page.locator('#redirect-home').click()
    assert page.url == BASE_URL + 'complex-scenarios'
    
    
    # Fill out the form
    
    