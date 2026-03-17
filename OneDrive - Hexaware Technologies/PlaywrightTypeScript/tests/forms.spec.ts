import {test,expect} from '@playwright/test';
import { HomePage } from '../pages/homePage';
import { ElementsPage } from '../pages/elementsPage'; 

test('Forms page loads and navigates to Practice Form page', async ({ page }) => {
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
    await elementsPage.fillPracticeForm({
        firstName: 'John',
        lastName: 'Doe',
        email: 'john.doe@example.com',
        gender: 'Male',
        mobile: '1234567890',
        dateOfBirth: '01 Jan 1990',
        subjects: ['Maths', 'Physics'],
        hobbies: ['Sports', 'Reading'],
        State: 'NCR',
        City: 'Delhi'
    })
    
        await elementsPage.submitPracticeForm();
        await expect(elementsPage.getSubmissionResult()).toBeVisible();
    
});
 