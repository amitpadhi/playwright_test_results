import { Page, Locator } from '@playwright/test';
import { expect } from '@playwright/test';

export class ElementsPage {
    readonly page: Page;    
    readonly textBoxCard: Locator;
    readonly checkBoxCard: Locator;
    readonly radioButtonCard: Locator
    readonly webTablesCard: Locator;
    readonly buttonsCard: Locator;
    readonly linksCard: Locator;

    constructor(page: Page) {
        this.page = page;
        this.textBoxCard = page.locator('.element-list').filter({ hasText: 'Text Box' });
        this.checkBoxCard = page.locator('.element-list').filter({ hasText: 'Check Box' });
        this.radioButtonCard = page.locator('.element-list').filter({ hasText: 'Radio Button' });
        this.webTablesCard = page.locator('.element-list').filter({ hasText: 'Web Tables' });
        this.buttonsCard = page.locator('.element-list').filter({ hasText: 'Buttons' });
        this.linksCard = page.locator('.element-list').filter({ hasText: 'Links' });
    }
    
    async navigate() {
        await this.page.goto('https://demoqa.com/elements');
    } 
    
    async clickTextBoxCard() {
        await this.textBoxCard.click();
    }

    async clickCheckBoxCard() {
        await this.checkBoxCard.click();
    }

    async clickRadioButtonCard() {
        await this.radioButtonCard.click();
    }

    async clickWebTablesCard() {
        await this.webTablesCard.click();
    }

    async clickButtonsCard() {
        await this.buttonsCard.click();
    }

    async clickLinksCard() {
        await this.linksCard.click();
    }

    // -------------------------------
    // Practice Form Methods
    // -------------------------------
    async navigateToPracticeForm() {
        await this.page.goto('https://demoqa.com/automation-practice-form',{ timeout: 60000 });
        await expect(this.page.locator('h1')).toContainText('Practice Form');
    }

    async fillPracticeForm(data: {
        firstName: string;
        lastName: string;
        email: string;
        gender: string;
        mobile: string;
        dateOfBirth: string;
        subjects: string[];
        hobbies: string[];
        State: string;
        City: string;
    }) {
        await this.page.locator('#firstName').fill(data.firstName);
        console.log('Filling first name');
        await this.page.locator('#lastName').fill(data.lastName);
        console.log('Filling last name');
        await this.page.locator('#userEmail').fill(data.email);
        console.log('Filling email');
        await this.page.locator(`label[for="gender-radio-${data.gender === 'Male' ? 1 : data.gender === 'Female' ? 2 : 3}"]`).click();
        await this.page.fill('#userNumber', data.mobile);
        console.log('Filling mobile number');
        await this.page.click('#dateOfBirthInput'); 
        await this.page.fill('#dateOfBirthInput', data.dateOfBirth);
        await this.page.press('#dateOfBirthInput', 'Enter');
        console.log('Filling date of Birth');

        //subjects
        for (const subject of data.subjects) {
            await this.page.locator('#subjectsInput').pressSequentially(subject);
            await this.page.keyboard.press('Enter');
        }
        console.log('Filling subjects');

        //hobbies

        for (const hobby of data.hobbies) {
            await this.page.locator(`label[for="hobbies-checkbox-${hobby === 'Sports' ? 1 : hobby === 'Reading' ? 2 : 3}"]`).click();
        }

        console.log('Filling hobbies');

        //State and City
        
        await this.page.locator('#state').click();
        await this.page.locator('#react-select-3-input').pressSequentially(data.State);
        await this.page.keyboard.press('Enter');
        
        await this.page.locator('#city').click();
        await this.page.locator('#react-select-4-input').press('Enter')
        //await this.page.keyboard.press('Enter');
        console.log('Selecting city');
    }

    async submitPracticeForm() {
        await this.page.waitForSelector('#submit', { state: 'visible' });
        await this.page.locator('#submit').scrollIntoViewIfNeeded();
        await this.page.locator('#submit').click();
    }

    

    getSubmissionResult() {
        return this.page.locator('.modal-content');
    }


}