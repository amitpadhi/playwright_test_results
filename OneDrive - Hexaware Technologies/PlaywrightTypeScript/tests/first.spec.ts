import { test, expect } from '@playwright/test';

test('should have the correct title', async ({ page }) => {
    await page.goto('https://playwright.dev/');

  // Navigate to Docs
    await page.getByRole('link', { name: 'Docs' }).click();

  // Locate the heading link
    const heading = page.getByRole('link', { name: 'Direct link to Introduction' });

  // Assert that the heading is visible
    await expect(heading).toBeVisible();
})