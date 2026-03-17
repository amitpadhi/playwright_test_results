import { Page, Locator } from '@playwright/test';

export class HomePage {
    readonly page: Page;
    readonly bannerImage: Locator;
    readonly formscard: Locator;
    readonly elementsCard: Locator;
    readonly widgetsCard: Locator;
    readonly interactionsCard: Locator; 

    
    constructor(page: Page) {
        this.page = page;
        this.bannerImage = page.locator('.banner-image');
        this.formscard = page.locator('.card').filter({ hasText: 'Forms' });
        this.elementsCard = page.locator('.card').filter({ hasText: 'Elements' });
        this.widgetsCard = page.locator('.card').filter({ hasText: 'Widgets' });
        this.interactionsCard = page.locator('.card').filter({ hasText: 'Interactions' });
    }   

    async navigate() {
    await this.page.goto('https://demoqa.com/');
    }

    async isLoaded(): Promise<boolean> {
        return await this.bannerImage.isVisible();
    }

    async clickFormsCard() {
        await this.formscard.click();
    }

    async clickElementsCard() {
        await this.elementsCard.click();
    }

    async clickWidgetsCard() {
        await this.widgetsCard.click();
    }

    async clickInteractionsCard() {
        await this.interactionsCard.click();
    }
}