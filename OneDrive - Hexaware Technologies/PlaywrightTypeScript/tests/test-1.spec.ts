import { test, expect } from '@playwright/test';

test('has title', async ({ page }) => {
    test.setTimeout(60000);
    await page.goto('https://sauce-demo.myshopify.com/');
  // Expect a title "to contain" a substring.
    await page.getByRole('link', { name: 'Catalog' }).click();
    await expect(page).toHaveURL('https://sauce-demo.myshopify.com/collections/all');
    await expect(page.getByAltText('Black heels')).toBeVisible
    await page.getByRole('heading', { name: 'Black heels' }).click();
    await expect(page).toHaveURL('https://sauce-demo.myshopify.com/products/flower-print-jeans');
    await page.selectOption('#product-select-option-0', 'M');
    await page.selectOption('#product-select-option-1', 'Red');
    await page.locator("#add").click();

    const cartLink = await page.locator('a').filter({ hasText: 'My Cart (1)' }).first()
    await expect(cartLink).toBeVisible();

    const CheckOut = await page.getByRole('link', { name: /Check Out/i })
    await expect(CheckOut).toBeVisible();
    await CheckOut.click();
    //await expect(page).toHaveURL("https://sauce-demo.myshopify.com/cart");






    // check the cart value 
    await page.locator('#minicart').locator('a').nth(0)

        

    //await page.locator('a').filter({ hasText: 'My Cart (1)' }).first().click();

    // Wait for cart page or drawer to show and then click checkout button
    //await page.locator('a').filter({ hasText: 'Checkout' }).first().click();

    //await page.locator('a:has-text("Check Out")').click();
    // Then click or assert the cart selector:
    // await expect(page).toHaveURL("https://sauce-demo.myshopify.com/cart");
    

 // Click the get started link.    
 //   await page.goBack();

 // Expects the url to be named as blog
 //   await page.getByRole('link', { name: 'Blog' }).click();
 //   await expect(page).toHaveURL('https://sauce-demo.myshopify.com/blogs/news');

 // Click the get started link.    
 //   await page.goBack();  
});