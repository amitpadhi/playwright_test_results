import { test, expect } from '@playwright/test';
import { HomePage } from '../pages/homePage';

test('Home page loads and navigates to Forms page', async ({ page }) => {
    const homePage = new HomePage(page);

    await homePage.navigate();
    await page.waitForLoadState('networkidle');

    //const bannerVisible = await homePage.bannerImage.isVisible();
    await homePage.clickFormsCard();

    await expect(page).toHaveURL(/forms/);

    await homePage.navigate();

    await homePage.clickElementsCard();
    await expect(page).toHaveURL(/elements/);

    await homePage.navigate(); 

    await homePage.clickWidgetsCard();
    await expect(page).toHaveURL(/widgets/);

    await homePage.navigate();

    await homePage.clickInteractionsCard();
    await expect(page).toHaveURL(/interaction/);

});
