import test, { expect } from '@playwright/test';
import { HomePage } from '../pages/homePage';
import { ElementsPage } from '../pages/elementsPage';
import { assert } from 'node:console';

test('Elements page loads and navigates to Text Box page', async ({ page }) => {
    const homePage = new HomePage(page);
    const elementsPage = new ElementsPage(page);    

    await elementsPage.navigate();
    await page.waitForLoadState('load');
    //console.log('Current URL:', page.url());
    await expect(page).toHaveURL('https://demoqa.com/elements');

    await elementsPage.clickButtonsCard();
    await expect(page).toHaveURL(/buttons/);

    await page.locator('#doubleClickBtn').dblclick();
    const doubleClickMessage = page.locator('#doubleClickMessage');

    // Assert it is visible
    //assert(doubleClickMessage, 'Double click message element not found');

    await expect(doubleClickMessage).toBeVisible();

    //await expect(page.locator('#doubleClickMessage')).toBeVisible();
    await homePage.navigate();
    //await elementsPage.navigate();

    //console.log('Current URL:', page.url());

    //await elementsPage.clickLinksCard();
    //await expect(page).toHaveURL(/links/);

    //console.log('Current URL:', page.url());
    
    await homePage.clickWidgetsCard();
    //console.log('Current URL:', page.url());
    await page.locator('span').filter({ hasText: 'Accordian' }).click();
    await expect(page).toHaveURL(/accordian/);
    const accordionHeaders = page.locator('.accordion-header');

    const count = await accordionHeaders.count();
    console.log('Number of accordion headers:', count);

    const searchText = 'Lorem Ipsum is simply dummy text of the printing a';

    for (let i = 0; i < count; i++) {
        const header = await accordionHeaders.nth(i)
        const headerText = await header.textContent();
        console.log(`Header ${i + 1} text:`, headerText?.trim());

        const xpath = `(//p[contains(text(), '\${searchText}')])[\${i + 1}]`;

        // Use the fully formed XPath string in locator

        const panelParagraph = page.locator(xpath);

        console.log("Evaluating XPath:", xpath);

        //if (await panelParagraph.count() > 0) {
            //console.log(`Paragraph with search text found near header \${i + 1}`);
        //} else {
            //console.log(`Paragraph with search text NOT found near header \${i + 1}`);
        //}
    }
    //console.log('Current URL:', page.url());
    

    // check if the Text Box card is visible
    //await elementsPage.clickTextBoxCard();
    //console.log('Current URL:', page.url());

    //await page.waitForLoadState('networkidle');

    //await elementsPage.clickTextBoxCard();
    //await expect(page).toHaveURL('https://demoqa.com/text-box');

    //await expect(page).toHaveURL(/\/text-box\$/);

    //await elementsPage.navigate();

    //await elementsPage.clickCheckBoxCard();
    //await expect(page).toHaveURL(/check-box/);

    //await elementsPage.navigate();

    //await elementsPage.clickRadioButtonCard();
    //await expect(page).toHaveURL(/radio-button/);

    //await elementsPage.navigate();

    //await elementsPage.clickWebTablesCard();
    //await expect(page).toHaveURL(/webtables/);

    //await elementsPage.navigate();

   

    //await elementsPage.navigate();

    //await elementsPage.clickLinksCard();
    //await expect(page).toHaveURL(/links/);
});

    