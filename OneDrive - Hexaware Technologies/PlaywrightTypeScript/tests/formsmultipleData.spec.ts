import {test,expect} from '@playwright/test';
import { HomePage } from '../pages/homePage';
import { ElementsPage } from '../pages/elementsPage'; 
import { formsData } from './data/formsData';

formsData.forEach((data, index) => {
    test(`Practice Form submission dataset #${index + 1}`, async ({ page }) => {
    test.setTimeout(60000);

    const homePage = new HomePage(page);
    const elementsPage = new ElementsPage(page);

    await homePage.navigate();
    await page.waitForLoadState('networkidle');
    await homePage.clickFormsCard();
    await expect(page).toHaveURL(/forms/);

    await page.locator('span').filter({ hasText: 'Practice Form' }).click();
    await expect(page).toHaveURL(/automation-practice-form/);
    await expect(page.locator('h5')).toHaveText('Student Registration Form');

    await elementsPage.fillPracticeForm(data);
    await elementsPage.submitPracticeForm();

    await expect(elementsPage.getSubmissionResult()).toBeVisible();
    });
});

