# conftest.py
import pytest
import pytest_asyncio
from playwright.async_api import async_playwright
from utils.config import HEADLESS, BROWSER

@pytest_asyncio.fixture
async def page():
    async with async_playwright() as p:
        browser = await getattr(p, BROWSER).launch(headless=HEADLESS)
        context = await browser.new_context()
        page = await context.new_page()
        yield page
        await context.close()
        await browser.close()
        