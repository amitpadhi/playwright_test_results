import pytest
from utils.config import BASE_URL

@pytest.mark.asyncio
async def test_store_page_shows_store(page):
    await page.goto(BASE_URL+ 'store')
    #await page.locator(":text-is('Store')").click()
    assert page.url == 'https://play-qa.com/store'
    assert page.locator("text=Advance Store Challenge").is_visible()
    await page.locator("#sort-dropdown").click()
    await page.locator("span:text('Most Popular')").click()

    #await page.get_by_role("option", name="Highest Rated").click()
    await page.locator("label").filter(has_text="Furniture").click()
    rows_count = await page.locator("div.grid.grid-cols-1.md\\:grid-cols-2.xl\\:grid-cols-3.gap-3.md\\:gap-6> div:visible").count()
    # "Expected at least one product to be visible after filtering by Furniture and sorting by Highest Rated"
    assert rows_count == 3 


    # check highest rated product
    #highest_rated = page.locator('#sort-dropdown option[value="highest-rated"]')
    #await highest_rated.wait_for(state="visible", timeout=5000)
    #await highest_rated.click()
    
